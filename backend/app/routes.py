from .models import Prospect
from flask import request
from datetime import datetime
from . import db
from .models import Visit
from flask import Blueprint, jsonify, request
from sqlalchemy import text, and_, func
from . import db  # import from __init__.py
from .models import SalesMan, Client, Visit, Invoice, Prospect

main = Blueprint("main", __name__)

# testing the db connection


@main.route('/')
def test_connection():
    try:
        db.session.execute(text('SELECT 1'))
        return '✅ Connected to MySQL successfully!'
    except Exception as e:
        return f'❌ Failed to connect to MySQL: {str(e)}'

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
def get_filtered_visits():
    try:
        from_date = request.args.get('from')
        to_date = request.args.get('to')
        sales_name = request.args.get('sales')
        client_region = request.args.get('region')
        activity = request.args.get('activity')
        resolved = request.args.get('resolved')  # 0 or 1

        # Base query: Visit JOIN Client
        query = db.session.query(
            Visit,
            Client.ClientReg,
            Client.ClientType,
            Invoice.Amount.label("InvoiceAmount")
        ).join(
            Client, Visit.ClientId == Client.ClientId
        ).outerjoin(
            Invoice,
            and_(
                Visit.ClientId == Invoice.ClientId,
                func.date(Visit.VisitDateTime) == Invoice.TransactionDate
            )
        )

        filters = []
        if from_date:
            filters.append(Visit.VisitDateTime >= from_date)
        if to_date:
            filters.append(Visit.VisitDateTime <= to_date)
        if sales_name:
            filters.append(Visit.SalesName == sales_name)
        if client_region:
            filters.append(Client.ClientReg == client_region)
        if activity:
            filters.append(Visit.Activity == activity)
        if resolved is not None:
            try:
                filters.append(Visit.Resolved == int(resolved))
            except ValueError:
                return jsonify({"error": "Resolved must be 0 or 1"}), 400

        if filters:
            query = query.filter(and_(*filters))

        results = query.all()

        # ✅ Format output
        response = []
        for visit, client_reg, client_type, amount in results:
            visit_data = visit.to_dict()
            visit_data["ClientReg"] = client_reg
            visit_data["ClientType"] = client_type
            visit_data["InvoiceAmount"] = float(amount) if amount else None
            response.append(visit_data)

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

        db.session.add(new_visit)
        db.session.commit()

        return jsonify({"message": "Visit created successfully", "visit": new_visit.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Update the Resolved status (0 or 1) for a specific visit


@main.route('/api/visit/<int:visit_id>/resolve', methods=['PUT'])
def update_resolved_status(visit_id):
    try:
        data = request.get_json()
        resolved = data.get("Resolved")

        # Validate the resolved field
        if resolved not in [0, 1, "0", "1"]:
            return jsonify({"error": "Resolved must be 0 or 1"}), 400

        # Fetch the visit
        visit = Visit.query.get(visit_id)
        if not visit:
            return jsonify({"error": f"Visit ID {visit_id} not found"}), 404

        # Update and save
        visit.Resolved = int(resolved)
        db.session.commit()

        return jsonify({
            "message": f"Visit ID {visit_id} resolved status updated to {resolved}",
            "VisitId": visit.VisitId,
            "Resolved": visit.Resolved
        })

    except Exception as e:
        db.session.rollback()
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
