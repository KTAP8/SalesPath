from .models import Visit, Client, Invoice
from flask import request, jsonify
from sqlalchemy import and_, func
from .models import Prospect
from flask import request
from datetime import datetime
from . import db
from .models import Visit
from flask import Blueprint, jsonify, request
from sqlalchemy import text, and_, func
from . import db  # import from __init__.py
from .models import SalesMan, Client, Visit, Invoice, Prospect
from sqlalchemy.orm import Session
from flask import current_app

main = Blueprint("main", __name__)

# testing the db connection


@main.route('/')
def test_connection():
    try:
        # Get the bound engine directly
        engine = db.get_engine(app=None, bind='postgres')  # or 'mysql'
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))

        return '✅ Connected to PostgreSQL successfully!'
    except Exception as e:
        return f'❌ Failed to connect to db: {str(e)}'

# get all salesman


@main.route('/api/salesmen', methods=['GET'])
def get_all_salesmen():
    try:
        salesmen = SalesMan.query.all()
        return jsonify([s.to_dict() for s in salesmen])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# get all clients


@main.route('/api/clients', methods=['GET'])
def get_all_clients():
    try:
        clients = Client.query.all()
        return jsonify([client.to_dict() for client in clients])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# get all visits + revenue: filter by SalesName, Region, date range, Activity, Resolved


@main.route('/api/visits', methods=['GET'])
def get_filtered_visits_cross_db():
    try:
        from flask import current_app
        from sqlalchemy.orm import Session

        # Step 1: Get filters from query params
        from_date = request.args.get('from')
        to_date = request.args.get('to')
        sales_name = request.args.get('sales')
        client_region = request.args.get('region')
        activity = request.args.get('activity')
        resolved = request.args.get('resolved')  # 0 or 1

        # Step 2: Create bind-specific sessions
        pg_session = Session(db.get_engine(current_app, bind='postgres'))
        mysql_session = Session(db.get_engine(current_app, bind='mysql'))

        # Step 3: Query Visit table (Postgres)
        visit_query = pg_session.query(Visit)
        if from_date:
            visit_query = visit_query.filter(Visit.VisitDateTime >= from_date)
        if to_date:
            visit_query = visit_query.filter(Visit.VisitDateTime <= to_date)
        if sales_name:
            visit_query = visit_query.filter(Visit.SalesName == sales_name)
        if activity:
            visit_query = visit_query.filter(Visit.Activity == activity)
        if resolved is not None:
            try:
                visit_query = visit_query.filter(
                    Visit.Resolved == bool(int(resolved)))
            except ValueError:
                return jsonify({"error": "Resolved must be 0 or 1"}), 400

        visits = visit_query.all()

        # Step 4: Query Client and Invoice tables (MySQL)
        clients = mysql_session.query(Client).all()
        invoices = mysql_session.query(Invoice).all()

        client_map = {c.ClientId: c for c in clients}
        invoice_map = {(i.ClientId, i.TransactionDate): i for i in invoices}

        # Step 5: Combine data in memory
        response = []
        for v in visits:
            c = client_map.get(v.ClientId)
            invoice = invoice_map.get(
                (v.ClientId, v.VisitDateTime.date() if v.VisitDateTime else None))

            visit_data = v.to_dict()
            visit_data["ClientReg"] = c.ClientReg if c else None
            visit_data["ClientType"] = c.ClientType if c else None
            visit_data["InvoiceAmount"] = float(
                invoice.Amount) if invoice else None

            # Region filter after join
            if client_region and visit_data["ClientReg"] != client_region:
                continue

            response.append(visit_data)

        # Cleanup
        pg_session.close()
        mysql_session.close()

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST new visit to database
@main.route('/api/visits', methods=['POST'])
def create_visit():
    try:
        data = request.get_json()

        SalesName = data.get("SalesName")
        ClientId = data.get("ClientId")
        Activity = data.get("Activity")
        Notes = data.get("Notes")
        ProblemNotes = data.get("ProblemNotes")
        Resolved = data.get("Resolved")

        # Validation: required fields
        if not all([SalesName, ClientId, Activity, Notes]):
            return jsonify({"error": "Missing required fields"}), 400

        # Optional: VisitDateTime override
        visit_datetime_str = data.get("VisitDateTime")
        if visit_datetime_str:
            VisitDateTime = datetime.fromisoformat(visit_datetime_str)
        else:
            VisitDateTime = datetime.now()

        # Create Visit object
        new_visit = Visit(
            SalesName=SalesName,
            ClientId=ClientId,
            Activity=Activity,
            Notes=Notes,
            ProblemNotes=ProblemNotes,
            Resolved=Resolved,
            VisitDateTime=VisitDateTime
        )

        pg_session = Session(db.get_engine(current_app, bind='postgres'))
        pg_session.add(new_visit)
        pg_session.commit()
        response = new_visit.to_dict()
        pg_session.close()

        return jsonify({"message": "Visit created successfully", "visit": response}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Update the Resolved status (0 or 1) for a specific visit


@main.route('/api/visit/<int:visit_id>/resolve', methods=['PUT'])
def update_resolved_status(visit_id):
    try:
        from sqlalchemy.orm import Session
        from flask import current_app, request

        # print("➡️ Received PUT /api/visit with ID:", visit_id)
        data = request.get_json(force=True, silent=True)
        # print("📦 Payload:", data)

        if not data or "Resolved" not in data:
            return jsonify({"error": "Missing 'Resolved' in request body"}), 400

        resolved = int(data["Resolved"])
        # print("✅ Parsed resolved value:", resolved)

        pg_session = Session(db.get_engine(current_app, bind='postgres'))
        visit = pg_session.get(Visit, visit_id)
        if not visit:
            pg_session.close()
            return jsonify({"error": f"Visit ID {visit_id} not found"}), 404

        visit.Resolved = resolved
        pg_session.commit()

        # ✅ Access before closing session
        response = {
            "message": f"Visit ID {visit_id} resolved status updated.",
            "VisitId": visit.VisitId,
            "Resolved": visit.Resolved
        }

        pg_session.close()
        return jsonify(response)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# get prospect filter by SalesName, Prospect Region


@main.route('/api/prospects', methods=['GET'])
def get_prospects():
    try:
        sales_name = request.args.get('sales')
        region = request.args.get('region')

        query = Prospect.query

        if sales_name:
            query = query.filter(Prospect.SalesName == sales_name)

        if region:
            query = query.filter(Prospect.ProspectReg == region)

        prospects = query.all()
        return jsonify([p.to_dict() for p in prospects])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST prospect


@main.route('/api/prospects', methods=['POST'])
def create_prospect():
    try:
        data = request.get_json()

        ProspectId = data.get("ProspectId")
        ProspectReg = data.get("ProspectReg")
        ProspectSubReg = data.get("ProspectSubReg")
        SalesName = data.get("SalesName")

        # Validate required fields
        if not all([ProspectReg, ProspectSubReg, SalesName]):
            return jsonify({"error": "Missing required fields"}), 400

        # Optional: check if SalesName exists in SalesMan table
        if not SalesMan.query.filter_by(SalesName=SalesName).first():
            return jsonify({"error": f"SalesName '{SalesName}' does not exist"}), 404

        new_prospect = Prospect(
            ProspectId=ProspectId,
            ProspectReg=ProspectReg,
            ProspectSubReg=ProspectSubReg,
            SalesName=SalesName
        )

        db.session.add(new_prospect)
        db.session.commit()

        return jsonify({
            "message": "Prospect created successfully",
            "prospect": new_prospect.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# get invoice data filter by time section
@main.route("/api/invoices", methods=["GET"])
def get_invoices():
    try:
        from_date = request.args.get("from")  # e.g., 2024-04-01
        to_date = request.args.get("to")      # e.g., 2024-04-30

        query = Invoice.query

        # Apply optional date filters
        if from_date:
            query = query.filter(Invoice.TransactionDate >= from_date)
        if to_date:
            query = query.filter(Invoice.TransactionDate <= to_date)

        invoices = query.all()

        return jsonify([invoice.to_dict() for invoice in invoices])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# getting the revenue generated by each salesman in a specific time


@main.route("/api/revenue", methods=["GET"])
def get_salesman_revenue():
    try:
        from_date = request.args.get("from")
        to_date = request.args.get("to")
        region = request.args.get("region")  # 🌍 Optional region filter

        # Base query: Join Visit, Invoice, and Client
        query = db.session.query(
            Visit.SalesName,
            func.sum(Invoice.Amount).label("TotalRevenue"),
            func.count(func.distinct(Visit.ClientId)).label(
                "ClientSoldCount")  # ✅ new line
        ).join(
            Invoice,
            and_(
                Visit.ClientId == Invoice.ClientId,
                func.date(Visit.VisitDateTime) == Invoice.TransactionDate
            )
        ).join(
            Client, Visit.ClientId == Client.ClientId
        ).filter(
            Visit.Activity == "Sale"
        )

        # Optional filters
        if from_date:
            query = query.filter(Visit.VisitDateTime >= from_date)
        if to_date:
            query = query.filter(Visit.VisitDateTime <= to_date)
        if region:
            query = query.filter(Client.ClientReg == region)

        query = query.group_by(Visit.SalesName).order_by(
            func.sum(Invoice.Amount).desc())

        results = query.all()

        return jsonify([
            {
                "SalesName": name,
                "TotalRevenue": float(revenue),
                "ClientSoldCount": client_count
            }
            for name, revenue, client_count in results
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# to get the #of client each salesman have visited and also the total number of client


@main.route("/api/clients-per-salesman", methods=["GET"])
def get_client_counts():
    try:
        from_date = request.args.get("from")
        to_date = request.args.get("to")

        # Step 1: Subquery to count distinct visited clients within time range
        visit_subquery = db.session.query(
            Visit.SalesName,
            func.count(func.distinct(Visit.ClientId)).label("VisitedClients")
        )

        if from_date:
            visit_subquery = visit_subquery.filter(
                Visit.VisitDateTime >= from_date)
        if to_date:
            visit_subquery = visit_subquery.filter(
                Visit.VisitDateTime <= to_date)

        visit_subquery = visit_subquery.group_by(Visit.SalesName).subquery()

        # Step 2: Query all salesmen with total clients and join visited count
        query = db.session.query(
            SalesMan.SalesName,
            func.count(Client.ClientId).label("TotalClients"),
            func.coalesce(visit_subquery.c.VisitedClients,
                          0).label("VisitedClients")
        ).outerjoin(
            Client, Client.SalesName == SalesMan.SalesName
        ).outerjoin(
            visit_subquery, visit_subquery.c.SalesName == SalesMan.SalesName
        ).group_by(SalesMan.SalesName)

        results = query.all()

        return jsonify([
            {
                "SalesName": name,
                "TotalClients": total,
                "VisitedClients": visited
            }
            for name, total, visited in results
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @main.route('/api/visit-columns')
# def get_visit_columns():
#     inspector = db.inspect(db.engine)
#     columns = inspector.get_columns('Visit')
#     return jsonify([{"name": c["name"], "type": str(c["type"])} for c in columns])
