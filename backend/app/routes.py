# from .models import Visit, Client, Invoice
# from flask import request, jsonify
# from sqlalchemy import and_, func
# from .models import Prospect
# from flask import request
# from datetime import datetime
# from . import db
# from .models import Visit
# from flask import Blueprint, jsonify, request
# from sqlalchemy import text, and_, func
# from . import db  # import from __init__.py
# from .models import SalesMan, Client, Visit, Invoice, Prospect
# from sqlalchemy.orm import Session
# from flask import current_app

# main = Blueprint("main", __name__)

# # testing the db connection


# @main.route('/')
# def test_connection():
#     try:
#         # Get the bound engine directly
#         engine = db.get_engine(app=None, bind='postgres')  # or 'mysql'
#         with engine.connect() as conn:
#             conn.execute(text('SELECT 1'))

#         return '✅ Connected to PostgreSQL successfully!'
#     except Exception as e:
#         return f'❌ Failed to connect to db: {str(e)}'

# # get all salesman


# @main.route('/api/salesmen', methods=['GET'])
# def get_all_salesmen():
#     try:
#         salesmen = SalesMan.query.all()
#         return jsonify([s.to_dict() for s in salesmen])
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # get all clients


# @main.route('/api/clients', methods=['GET'])
# def get_all_clients():
#     try:
#         clients = Client.query.all()
#         return jsonify([client.to_dict() for client in clients])
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # get all visits + revenue: filter by SalesName, Region, date range, Activity, Resolved


# @main.route('/api/visits', methods=['GET'])
# def get_filtered_visits_cross_db():
#     try:
#         from flask import current_app
#         from sqlalchemy.orm import Session

#         # Step 1: Get filters from query params
#         from_date = request.args.get('from')
#         to_date = request.args.get('to')
#         sales_name = request.args.get('sales')
#         client_region = request.args.get('region')
#         activity = request.args.get('activity')
#         resolved = request.args.get('resolved')  # 0 or 1

#         # Step 2: Create bind-specific sessions
#         pg_session = Session(db.get_engine(current_app, bind='postgres'))
#         mysql_session = Session(db.get_engine(current_app, bind='mysql'))

#         # Step 3: Query Visit table (Postgres)
#         visit_query = pg_session.query(Visit)
#         if from_date:
#             visit_query = visit_query.filter(Visit.VisitDateTime >= from_date)
#         if to_date:
#             visit_query = visit_query.filter(Visit.VisitDateTime <= to_date)
#         if sales_name:
#             visit_query = visit_query.filter(Visit.SalesName == sales_name)
#         if activity:
#             visit_query = visit_query.filter(Visit.Activity == activity)
#         if resolved is not None:
#             try:
#                 visit_query = visit_query.filter(
#                     Visit.Resolved == bool(int(resolved)))
#             except ValueError:
#                 return jsonify({"error": "Resolved must be 0 or 1"}), 400

#         visits = visit_query.all()

#         # Step 4: Query Client and Invoice tables (MySQL)
#         clients = mysql_session.query(Client).all()
#         invoices = mysql_session.query(Invoice).all()

#         client_map = {c.ClientId: c for c in clients}
#         invoice_map = {(i.ClientId, i.TransactionDate): i for i in invoices}

#         # Step 5: Combine data in memory
#         response = []
#         for v in visits:
#             c = client_map.get(v.ClientId)
#             invoice = invoice_map.get(
#                 (v.ClientId, v.VisitDateTime.date() if v.VisitDateTime else None))

#             visit_data = v.to_dict()
#             visit_data["ClientReg"] = c.ClientReg if c else None
#             visit_data["ClientType"] = c.ClientType if c else None
#             visit_data["InvoiceAmount"] = float(
#                 invoice.Amount) if invoice else None

#             # Region filter after join
#             if client_region and visit_data["ClientReg"] != client_region:
#                 continue

#             response.append(visit_data)

#         # Cleanup
#         pg_session.close()
#         mysql_session.close()

#         return jsonify(response)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # POST new visit to database
# @main.route('/api/visits', methods=['POST'])
# def create_visit():
#     try:
#         from sqlalchemy.orm import Session
#         from flask import current_app
#         import traceback

#         data = request.get_json()
#         print("📥 Received visit POST data:", data)

#         SalesName = data.get("SalesName")
#         ClientId = data.get("ClientId")
#         Activity = data.get("Activity")
#         Notes = data.get("Notes")
#         ProblemNotes = data.get("ProblemNotes")
#         Resolved = data.get("Resolved")
#         visit_datetime_str = data.get("VisitDateTime")

#         print(
#             f"🔍 Extracted: SalesName={SalesName}, ClientId={ClientId}, Activity={Activity}, Resolved={Resolved}")

#         # Validation
#         if not all([SalesName, ClientId, Activity, Notes]):
#             print("❌ Missing required fields")
#             return jsonify({"error": "Missing required fields"}), 400

#         # Handle date
#         if visit_datetime_str:
#             VisitDateTime = datetime.fromisoformat(visit_datetime_str)
#         else:
#             VisitDateTime = datetime.now()

#         print(f"🕓 Using VisitDateTime: {VisitDateTime}")

#         # Create object
#         new_visit = Visit(
#             SalesName=SalesName,
#             ClientId=ClientId,
#             Activity=Activity,
#             Notes=Notes,
#             ProblemNotes=ProblemNotes,
#             Resolved=Resolved,
#             VisitDateTime=VisitDateTime
#         )

#         # PostgreSQL session
#         pg_session = Session(db.get_engine(current_app, bind='postgres'))

#         print("💾 Adding visit to session...")
#         pg_session.add(new_visit)
#         pg_session.commit()
#         response = new_visit.to_dict()
#         print("✅ Commit successful")
#         pg_session.close()

#         return jsonify({"message": "Visit created successfully", "visit": response}), 201

#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({"error": str(e)}), 500

# # Update the Resolved status (0 or 1) for a specific visit


# @main.route('/api/visit/<int:visit_id>/resolve', methods=['PUT'])
# def update_resolved_status(visit_id):
#     try:
#         from sqlalchemy.orm import Session
#         from flask import current_app, request

#         # print("➡️ Received PUT /api/visit with ID:", visit_id)
#         data = request.get_json(force=True, silent=True)
#         # print("📦 Payload:", data)

#         if not data or "Resolved" not in data:
#             return jsonify({"error": "Missing 'Resolved' in request body"}), 400

#         resolved = int(data["Resolved"])
#         # print("✅ Parsed resolved value:", resolved)

#         pg_session = Session(db.get_engine(current_app, bind='postgres'))
#         visit = pg_session.get(Visit, visit_id)
#         if not visit:
#             pg_session.close()
#             return jsonify({"error": f"Visit ID {visit_id} not found"}), 404

#         visit.Resolved = resolved
#         pg_session.commit()

#         # ✅ Access before closing session
#         response = {
#             "message": f"Visit ID {visit_id} resolved status updated.",
#             "VisitId": visit.VisitId,
#             "Resolved": visit.Resolved
#         }

#         pg_session.close()
#         return jsonify(response)

#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return jsonify({"error": str(e)}), 500


# # get prospect filter by SalesName, Prospect Region


# @main.route('/api/prospects', methods=['GET'])
# def get_prospects_postgres():
#     try:
#         from sqlalchemy.orm import Session
#         from flask import current_app

#         sales_name = request.args.get('sales')
#         region = request.args.get('region')

#         # ✅ Use PostgreSQL-bound session
#         pg_session = Session(db.get_engine(current_app, bind='postgres'))

#         query = pg_session.query(Prospect)

#         if sales_name:
#             query = query.filter(Prospect.SalesName == sales_name)

#         if region:
#             query = query.filter(Prospect.ProspectReg == region)

#         prospects = query.all()
#         result = [p.to_dict() for p in prospects]

#         pg_session.close()
#         return jsonify(result)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # POST prospect


# @main.route('/api/prospects', methods=['POST'])
# def create_prospect_postgres():
#     try:
#         from sqlalchemy.orm import Session
#         from flask import current_app

#         data = request.get_json()
#         print("📥 Received data:", data)

#         ProspectId = data.get("ProspectId")
#         ProspectReg = data.get("ProspectReg")
#         ProspectSubReg = data.get("ProspectSubReg")
#         SalesName = data.get("SalesName")

#         if not all([ProspectReg, ProspectSubReg, SalesName]):
#             return jsonify({"error": "Missing required fields"}), 400

#         pg_session = Session(db.get_engine(current_app, bind='postgres'))

#         # if not pg_session.query(SalesMan).filter_by(SalesName=SalesName).first():
#         #     pg_session.close()
#         #     return jsonify({"error": f"SalesName '{SalesName}' does not exist"}), 404

#         new_prospect = Prospect(
#             ProspectId=ProspectId,
#             ProspectReg=ProspectReg,
#             ProspectSubReg=ProspectSubReg,
#             SalesName=SalesName
#         )

#         pg_session.add(new_prospect)
#         pg_session.commit()

#         response = {
#             "message": "Prospect created successfully",
#             "prospect": new_prospect.to_dict()
#         }
#         print("✅ Successfully inserted")
#         pg_session.close()
#         return jsonify(response), 201

#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return jsonify({"error": str(e)}), 500


# # get invoice data filter by time section
# @main.route("/api/invoices", methods=["GET"])
# def get_invoices():
#     try:
#         from_date = request.args.get("from")  # e.g., 2024-04-01
#         to_date = request.args.get("to")      # e.g., 2024-04-30

#         query = Invoice.query

#         # Apply optional date filters
#         if from_date:
#             query = query.filter(Invoice.TransactionDate >= from_date)
#         if to_date:
#             query = query.filter(Invoice.TransactionDate <= to_date)

#         invoices = query.all()

#         return jsonify([invoice.to_dict() for invoice in invoices])

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # getting the revenue generated by each salesman in a specific time


# @main.route("/api/revenue", methods=["GET"])
# def get_salesman_revenue():
#     try:
#         from_date = request.args.get("from")
#         to_date = request.args.get("to")
#         region = request.args.get("region")  # 🌍 Optional region filter

#         # Base query: Join Visit, Invoice, and Client
#         query = db.session.query(
#             Visit.SalesName,
#             func.sum(Invoice.Amount).label("TotalRevenue"),
#             func.count(func.distinct(Visit.ClientId)).label(
#                 "ClientSoldCount")  # ✅ new line
#         ).join(
#             Invoice,
#             and_(
#                 Visit.ClientId == Invoice.ClientId,
#                 func.date(Visit.VisitDateTime) == Invoice.TransactionDate
#             )
#         ).join(
#             Client, Visit.ClientId == Client.ClientId
#         ).filter(
#             Visit.Activity == "Sale"
#         )

#         # Optional filters
#         if from_date:
#             query = query.filter(Visit.VisitDateTime >= from_date)
#         if to_date:
#             query = query.filter(Visit.VisitDateTime <= to_date)
#         if region:
#             query = query.filter(Client.ClientReg == region)

#         query = query.group_by(Visit.SalesName).order_by(
#             func.sum(Invoice.Amount).desc())

#         results = query.all()

#         return jsonify([
#             {
#                 "SalesName": name,
#                 "TotalRevenue": float(revenue),
#                 "ClientSoldCount": client_count
#             }
#             for name, revenue, client_count in results
#         ])

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # to get the #of client each salesman have visited and also the total number of client


# @main.route("/api/clients-per-salesman", methods=["GET"])
# def get_client_counts():
#     try:
#         from_date = request.args.get("from")
#         to_date = request.args.get("to")

#         # Step 1: Subquery to count distinct visited clients within time range
#         visit_subquery = db.session.query(
#             Visit.SalesName,
#             func.count(func.distinct(Visit.ClientId)).label("VisitedClients")
#         )

#         if from_date:
#             visit_subquery = visit_subquery.filter(
#                 Visit.VisitDateTime >= from_date)
#         if to_date:
#             visit_subquery = visit_subquery.filter(
#                 Visit.VisitDateTime <= to_date)

#         visit_subquery = visit_subquery.group_by(Visit.SalesName).subquery()

#         # Step 2: Query all salesmen with total clients and join visited count
#         query = db.session.query(
#             SalesMan.SalesName,
#             func.count(Client.ClientId).label("TotalClients"),
#             func.coalesce(visit_subquery.c.VisitedClients,
#                           0).label("VisitedClients")
#         ).outerjoin(
#             Client, Client.SalesName == SalesMan.SalesName
#         ).outerjoin(
#             visit_subquery, visit_subquery.c.SalesName == SalesMan.SalesName
#         ).group_by(SalesMan.SalesName)

#         results = query.all()

#         return jsonify([
#             {
#                 "SalesName": name,
#                 "TotalClients": total,
#                 "VisitedClients": visited
#             }
#             for name, total, visited in results
#         ])

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from sqlalchemy import tuple_
from .models import Visit, Client, Invoice, Prospect, SalesMan
from flask import request, jsonify, Blueprint, current_app
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, text
from datetime import datetime
from . import db
from sqlalchemy.sql import exists
from sqlalchemy.exc import OperationalError

main = Blueprint("main", __name__)


@main.route('/')
def test_connection():
    try:
        engine = db.get_engine(app=None, bind='touchdb')
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        return '✅ Connected to PostgreSQL (touchdb) successfully!'
    except Exception as e:
        return f'❌ Failed to connect to db: {str(e)}'


@main.route('/api/salesmen', methods=['GET'])
def get_all_salesmen():
    try:
        salesmen = SalesMan.query.all()
        return jsonify([s.to_dict() for s in salesmen])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/api/clients', methods=['GET'])
def get_all_clients():
    try:
        sales_name = request.args.get('sales')
        session = Session(db.get_engine(current_app, bind='chaluck'))

        query = session.query(Client)

        if sales_name:
            # Step 1: Get SalesLogin from SalesMan using SalesName
            salesman = session.query(SalesMan).filter(
                SalesMan.SalesName == sales_name).first()
            if salesman:
                # Step 2: Filter clients using the SalesLogin
                query = query.filter(Client.SalesLogin == salesman.SalesLogin)
            else:
                # No matching salesperson found, return empty list
                return jsonify([])

        result = [p.to_dict() for p in query.all()]
        session.close()

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/api/visits', methods=['GET'])
def get_filtered_visits_cross_db():
    try:
        from_date = request.args.get('from')
        to_date = request.args.get('to')
        sales_name = request.args.get('sales')
        client_region = request.args.get('region')
        activity = request.args.get('activity')
        resolved = request.args.get('resolved')

        touchdb_session = Session(db.get_engine(current_app, bind='touchdb'))
        chaluck_session = Session(db.get_engine(current_app, bind='chaluck'))

        # Step 1: Filter Visit records from touchdb
        visit_query = touchdb_session.query(Visit)
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

        # Step 2: Get related clients
        clients = chaluck_session.query(Client).all()
        client_map = {c.ClientId: c for c in clients}

        # Step 3: Build (ClientId, Date) keys from visits
        invoice_keys = {
            (v.ClientId, v.VisitDateTime.date())
            for v in visits if v.VisitDateTime
        }

        # Step 4: Query only needed invoices from chaluck
        invoices = (
            chaluck_session.query(Invoice)
            .filter(tuple_(Invoice.ClientId, Invoice.TransactionDate).in_(invoice_keys))
            .all()
        )
        invoice_map = {(i.ClientId, i.TransactionDate): i for i in invoices}

        # Step 5: Combine into response
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

            if client_region and visit_data["ClientReg"] != client_region:
                continue

            response.append(visit_data)

        touchdb_session.close()
        chaluck_session.close()
        return jsonify(response)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


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
        visit_datetime_str = data.get("VisitDateTime")

        if not all([SalesName, ClientId, Activity, Notes]):
            return jsonify({"error": "Missing required fields"}), 400

        VisitDateTime = datetime.fromisoformat(
            visit_datetime_str) if visit_datetime_str else datetime.now()

        new_visit = Visit(
            SalesName=SalesName,
            ClientId=ClientId,
            Activity=Activity,
            Notes=Notes,
            ProblemNotes=ProblemNotes,
            Resolved=Resolved,
            VisitDateTime=VisitDateTime
        )

        session = Session(db.get_engine(current_app, bind='touchdb'))
        session.add(new_visit)
        session.commit()
        response = new_visit.to_dict()
        session.close()

        return jsonify({"message": "Visit created successfully", "visit": response}), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@main.route('/api/visit/<int:visit_id>/resolve', methods=['PUT'])
def update_resolved_status(visit_id):
    try:
        data = request.get_json(force=True, silent=True)
        if not data or "Resolved" not in data:
            return jsonify({"error": "Missing 'Resolved' in request body"}), 400

        resolved = int(data["Resolved"])

        session = Session(db.get_engine(current_app, bind='touchdb'))
        visit = session.get(Visit, visit_id)
        if not visit:
            session.close()
            return jsonify({"error": f"Visit ID {visit_id} not found"}), 404

        visit.Resolved = resolved
        session.commit()

        session.close()
        return jsonify({
            "message": f"Visit ID {visit_id} resolved status updated.",
            "VisitId": visit.VisitId,
            "Resolved": visit.Resolved
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/api/prospects', methods=['GET'])
def get_prospects():
    try:
        sales_name = request.args.get('sales')
        region = request.args.get('region')

        session = Session(db.get_engine(current_app, bind='touchdb'))
        query = session.query(Prospect)

        if sales_name:
            query = query.filter(Prospect.SalesName == sales_name)
        if region:
            query = query.filter(Prospect.ProspectReg == region)

        result = [p.to_dict() for p in query.all()]
        session.close()
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/api/prospects', methods=['POST'])
def create_prospect():
    try:
        data = request.get_json()
        ProspectId = data.get("ProspectId")
        ProspectReg = data.get("ProspectReg")
        ProspectSubReg = data.get("ProspectSubReg")
        SalesName = data.get("SalesName")

        if not all([ProspectReg, ProspectSubReg, SalesName]):
            return jsonify({"error": "Missing required fields"}), 400

        session = Session(db.get_engine(current_app, bind='touchdb'))
        new_prospect = Prospect(
            ProspectId=ProspectId,
            ProspectReg=ProspectReg,
            ProspectSubReg=ProspectSubReg,
            SalesName=SalesName
        )

        session.add(new_prospect)
        session.commit()
        response = new_prospect.to_dict()
        session.close()
        return jsonify({"message": "Prospect created successfully", "prospect": response}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/api/invoices", methods=["GET"])
def get_invoices():
    try:
        from_date = request.args.get("from")
        to_date = request.args.get("to")

        if not from_date and not to_date:
            return jsonify({"error": "Please provide a date range to avoid full-table scan"}), 400

        session = Session(db.get_engine(current_app, bind='chaluck'))
        query = session.query(Invoice)

        if from_date:
            query = query.filter(Invoice.TransactionDate >= from_date)
        if to_date:
            query = query.filter(Invoice.TransactionDate <= to_date)

        result = [inv.to_dict() for inv in query.all()]
        session.close()
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/api/revenue", methods=["GET"])
def get_salesman_revenue():
    try:
        region = request.args.get("region")

        # 🗓️ Default from = 1st day of previous month, to = today
        today = datetime.today()
        default_from = (today.replace(day=1) -
                        relativedelta(months=1)).strftime("%Y-%m-%d")
        default_to = today.strftime("%Y-%m-%d")

        from_date = request.args.get("from") or default_from
        to_date = request.args.get("to") or default_to

        session_touchdb = Session(db.get_engine(current_app, bind='touchdb'))
        session_chaluck = Session(db.get_engine(current_app, bind='chaluck'))

        # 🧾 Fetch visit data with date range
        visits = session_touchdb.query(Visit).filter(Visit.Activity == "Sale")
        visits = visits.filter(Visit.VisitDateTime >= from_date)
        visits = visits.filter(Visit.VisitDateTime <= to_date)
        visit_data = visits.all()

        # 📄 Fetch invoice and client data, filtered by date
        invoice_query = session_chaluck.query(Invoice)
        invoice_query = invoice_query.filter(
            Invoice.TransactionDate >= from_date)
        invoice_query = invoice_query.filter(
            Invoice.TransactionDate <= to_date)
        invoices = invoice_query.all()

        clients = session_chaluck.query(Client).all()

        client_map = {c.ClientId: c for c in clients}
        invoice_map = {(i.ClientId, i.TransactionDate): i for i in invoices}

        revenue_summary = {}

        for v in visit_data:
            client = client_map.get(v.ClientId)
            invoice = invoice_map.get(
                (v.ClientId, v.VisitDateTime.date())
            ) if v.VisitDateTime else None

            if region and (not client or client.ClientReg != region):
                continue

            name = v.SalesName
            if name not in revenue_summary:
                revenue_summary[name] = {"TotalRevenue": 0, "ClientIds": set()}

            if invoice:
                revenue_summary[name]["TotalRevenue"] += float(invoice.Amount)

            revenue_summary[name]["ClientIds"].add(v.ClientId)

        session_touchdb.close()
        session_chaluck.close()

        return jsonify([
            {
                "SalesName": name,
                "TotalRevenue": data["TotalRevenue"],
                "ClientSoldCount": len(data["ClientIds"])
            }
            for name, data in revenue_summary.items()
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/api/clients-per-salesman", methods=["GET"])
def get_client_counts():
    try:
        from datetime import date, timedelta

        from_date = request.args.get("from")
        to_date = request.args.get("to")

        if not to_date:
            to_date = date.today().isoformat()
        if not from_date:
            from_date = (date.today() - timedelta(days=30)).isoformat()

        session_touchdb = Session(db.get_engine(current_app, bind='touchdb'))
        session_chaluck = Session(db.get_engine(current_app, bind='chaluck'))

        # Step 1: Fetch visited clients from touchdb
        visit_data = session_touchdb.query(
            Visit.SalesName,
            func.count(func.distinct(Visit.ClientId)).label("VisitedClients")
        ).filter(
            Visit.VisitDateTime >= from_date,
            Visit.VisitDateTime <= to_date
        ).group_by(Visit.SalesName).all()

        visited_map = {row.SalesName: row.VisitedClients for row in visit_data}

        # Step 2: Fetch all salesmen and their total clients from chaluck
        query = session_chaluck.query(
            SalesMan.SalesName,
            func.count(Client.ClientId).label("TotalClients")
        ).outerjoin(
            Client, Client.SalesId == SalesMan.SalesId
        ).group_by(SalesMan.SalesName)

        result = []
        for row in query.all():
            visited = visited_map.get(row.SalesName, 0)
            result.append({
                "SalesName": row.SalesName,
                "TotalClients": row.TotalClients,
                "VisitedClients": visited
            })

        session_touchdb.close()
        session_chaluck.close()
        return jsonify(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@main.route('/api/webhook', methods=['POST'])
def dialogflow_webhook():
    try:
        req = request.get_json()
        intent = req.get('queryResult', {}).get(
            'intent', {}).get('displayName')
        output_contexts = req.get('queryResult', {}).get('outputContexts', [])
        print("💡 Detected intent:", intent)

        def get_param_from_contexts(name):
            for ctx in output_contexts:
                params = ctx.get('parameters', {})
                if name in params:
                    return params[name]
            return "-"
        if intent == "AskCustomerType":
            customer_type = req.get('queryResult', {}).get(
                'parameters', {}).get('customer_type')

            if customer_type == "ใหม่":
                return jsonify({
                    'fulfillmentText': "ขอทราบชื่อลูกค้าใหม่ของคุณครับ",
                    'outputContexts': [
                        {
                            "name": f"{req['session']}/contexts/awaiting_customer_name",
                            "lifespanCount": 5
                        }
                    ]
                })

            elif customer_type == "เดิม":
                return jsonify({
                    'fulfillmentText': "กรุณาระบุรหัสลูกค้าของคุณครับ",
                    'outputContexts': [
                        {
                            "name": f"{req['session']}/contexts/awaiting_client_id",
                            "lifespanCount": 5
                        }
                    ]
                })

            else:
                return jsonify({
                    'fulfillmentText': "กรุณาระบุว่าเป็นลูกค้าใหม่หรือเดิมครับ"
                })
        elif intent == "GetCustomerName":
            customer_name = req.get('queryResult', {}).get(
                'parameters', {}).get('customer_name')

            return jsonify({
                'fulfillmentText': f"รับทราบชื่อลูกค้า: {customer_name} ครับ\nกรุณาระบุจังหวัดของลูกค้า เช่น กรุงเทพ หรือ เชียงใหม่ ครับ",
                'outputContexts': [
                    {
                        "name": f"{req['session']}/contexts/awaiting_customer_city",
                        "lifespanCount": 5,
                        "parameters": {
                                "customer_name": customer_name
                        }
                    }
                ]
            })

        elif intent == "GetCustomerCity":
            city = req.get('queryResult', {}).get('parameters', {}).get('city')
            customer_name = get_param_from_contexts('customer_name')

            return jsonify({
                'fulfillmentText': f"ลูกค้า {customer_name} อยู่ที่ {city} ครับ กรุณาระบุเขต/อำเภอของลูกค้าด้วยครับ",
                'outputContexts': [
                    {
                        "name": f"{req['session']}/contexts/awaiting_customer_subregion",
                        "lifespanCount": 5,
                        "parameters": {
                            "city": city,
                            "customer_name": customer_name
                        }
                    }
                ]
            })

        elif intent == "GetCustomerSubregion":
            subregion = req.get('queryResult', {}).get(
                'parameters', {}).get('subregion')
            customer_name = get_param_from_contexts("customer_name")
            city = get_param_from_contexts("city")

            response_text = (
                f"คุณได้ระบุข้อมูลดังนี้:\n"
                f"👤 ชื่อลูกค้า: {customer_name}\n"
                f"📍 ภูมิภาค: {city}\n"
                f"🗺️ เขต/อำเภอ: {subregion}\n"
                "กรุณายืนยันข้อมูล: ใช่ หรือ ไม่ใช่?"
            )

            return jsonify({
                'fulfillmentText': response_text,
                'outputContexts': [
                    {
                        "name": f"{req['session']}/contexts/awaiting_confirmation_new_customer",
                        "lifespanCount": 5,
                        "parameters": {
                            "customer_name": customer_name,
                            "city": city,
                            "subregion": subregion
                        }
                    }
                ]
            })

        elif intent == "ConfirmNewCustomer":
            customer_name = get_param_from_contexts("customer_name")
            city = get_param_from_contexts("city")
            subregion = get_param_from_contexts("subregion")

            user_id = req.get('originalDetectIntentRequest', {}).get(
                'payload', {}).get('data', {}).get('source', {}).get('userId', '-')

            session = None
            try:
                engine = db.get_engine(current_app, bind='touchdb', connect_args={
                                       "connect_timeout": 3})
                session = Session(engine)

                new_prospect = Prospect(
                    ProspectId=customer_name,
                    ProspectReg=city,
                    ProspectSubReg=subregion,
                    SalesName=user_id
                )

                session.add(new_prospect)
                session.commit()
                session.close()

                return jsonify({
                    'fulfillmentText': "✅ บันทึกข้อมูลลูกค้าใหม่เรียบร้อยแล้ว\nกรุณาระบุประเภทลูกค้าใหม่อีกครั้ง (ใหม่ / เดิม) เพื่อจดครั้งต่อไป",
                    'outputContexts': [
                        {
                            "name": f"{req['session']}/contexts/awaiting_customer_type",
                            "lifespanCount": 5
                        }
                    ]
                })

            except OperationalError as e:
                print("❌ Database timeout or connection error:", e)
                return jsonify({
                    'fulfillmentText': "❌ ระบบตอบสนองช้า กรุณาลองใหม่ในอีกสักครู่ครับ"
                })
            except Exception as e:
                print("❌ General error:", e)
                return jsonify({
                    'fulfillmentText': "เกิดข้อผิดพลาดในการบันทึกข้อมูล กรุณาลองใหม่อีกครั้ง"
                })
            finally:
                if session:
                    session.close()

        elif intent == "GetClientId":
            clientId = req.get('queryResult', {}).get(
                'parameters', {}).get('clientId')
            print("🔍 Checking clientId:", clientId)

            try:
                session = Session(db.get_engine(current_app, bind='chaluck'))
                exists_query = session.query(
                    session.query(Client).filter_by(ClientId=clientId).exists()
                ).scalar()
                session.close()

                if exists_query:
                    return jsonify({
                        'fulfillmentText': f"พบลูกค้า {clientId} ในระบบ ✅\nกรุณาระบุกิจกรรมที่คุณทำ:\n🛍️ ขาย\n🤝 ความสัมพันธ์ลูกค้า\n🐞 แจ้งปัญหา (เท่านั้น)",
                        'outputContexts': [
                            {
                                "name": f"{req['session']}/contexts/awaiting_activity_type",
                                "lifespanCount": 5,
                                "parameters": {
                                    "clientId": clientId
                                }
                            }
                        ]
                    })
                else:
                    return jsonify({
                        'fulfillmentText': "ไม่พบรหัสลูกค้า กรุณาระบุใหม่อีกครั้งครับ"
                    })

            except Exception as e:
                print("❌ Error querying clientId:", e)
                return jsonify({
                    'fulfillmentText': "เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูลครับ"
                })

        elif intent == "AskActivityType":
            activity_type = req.get('queryResult', {}).get(
                'parameters', {}).get('activity_type')
            clientId = get_param_from_contexts("clientId")

            return jsonify({
                'fulfillmentText': f"กิจกรรม: {activity_type} ✅\nกรุณาระบุหมายเหตุ/ข้อมูลสำหรับกิจกรรมนี้ครับ",
                'outputContexts': [
                    {
                        "name": f"{req['session']}/contexts/awaiting_activity_note",
                        "lifespanCount": 5,
                        "parameters": {
                            "clientId": clientId,
                            "activityType": activity_type
                        }
                    }
                ]
            })

        elif intent == "ProvideActivityNote":
            activity_note = req.get('queryResult', {}).get(
                'parameters', {}).get('activity_note')
            clientId = get_param_from_contexts("clientId")
            activityType = get_param_from_contexts("activityType")

            print("📝 Note:", activity_note, "| Type:", activityType)

            if activityType == "แจ้งปัญหา":
                return jsonify({
                    'fulfillmentText': "กรุณาระบุรายละเอียดของปัญหาด้วยครับ",
                    'outputContexts': [
                        {
                            "name": f"{req['session']}/contexts/awaiting_problem_note",
                            "lifespanCount": 5,
                            "parameters": {
                                "clientId": clientId,
                                "activityType": activityType,
                                "activityNote": activity_note
                            }
                        }
                    ]
                })
            else:
                return jsonify({
                    'fulfillmentText': (
                        f"กรุณายืนยันข้อมูลนี้อีกครั้ง:\n"
                        f"📄 รหัสลูกค้า: {clientId}\n"
                        f"📌 กิจกรรม: {activityType}\n"
                        f"📝 หมายเหตุ: {activity_note}\n"
                        "ข้อมูลถูกต้องใช่หรือไม่? (ใช่ / ไม่ใช่)"
                    ),
                    'outputContexts': [
                        {
                            "name": f"{req['session']}/contexts/awaiting_confirmation_existing_customer",
                            "lifespanCount": 5,
                            "parameters": {
                                "clientId": clientId,
                                "activityType": activityType,
                                "activityNote": activity_note
                            }
                        }
                    ]
                })

        elif intent == "ProvideProblemNote":
            problem_note = req.get('queryResult', {}).get(
                'parameters', {}).get('problem_note')
            clientId = get_param_from_contexts("clientId")
            activityType = get_param_from_contexts("activityType")
            activityNote = get_param_from_contexts("activityNote")

            print("🐞 Problem note received:", problem_note)

            confirmation_text = (
                f"กรุณายืนยันข้อมูลนี้อีกครั้ง:\n"
                f"📄 รหัสลูกค้า: {clientId}\n"
                f"📌 กิจกรรม: {activityType}\n"
                f"📝 หมายเหตุ: {activityNote}\n"
                f"🐞 รายละเอียดปัญหา: {problem_note}\n"
                "ข้อมูลถูกต้องใช่หรือไม่? (ใช่ / ไม่ใช่)"
            )

            return jsonify({
                'fulfillmentText': confirmation_text,
                'outputContexts': [
                    {
                        "name": f"{req['session']}/contexts/awaiting_confirmation_existing_customer",
                        "lifespanCount": 5,
                        "parameters": {
                            "clientId": clientId,
                            "activityType": activityType,
                            "activityNote": activityNote,
                            "problemNote": problem_note
                        }
                    }
                ]
            })

        elif intent == "ConfirmExistingCustomerActivity - yes":
            clientId = get_param_from_contexts("clientId")
            activityType = get_param_from_contexts("activityType")
            activityNote = get_param_from_contexts("activityNote")
            problemNote = get_param_from_contexts("problemNote")
            visit_datetime = datetime.now()

            # Map Thai activity to internal codes
            activity_map = {
                "ขาย": "Sale",
                "ความสัมพันธ์ลูกค้า": "Relation",
                "แจ้งปัญหา": "Problem"
            }
            activity_code = activity_map.get(activityType, activityType)

            # Determine resolved status
            resolved = False if activity_code == "Problem" else True

            # Extract LINE user ID
            user_id = req.get('originalDetectIntentRequest', {}).get(
                'payload', {}).get('data', {}).get('source', {}).get('userId', '-')

            try:
                session = Session(db.get_engine(current_app, bind='touchdb'))

                new_visit = Visit(
                    SalesName=user_id,
                    ClientId=clientId,
                    Activity=activity_code,
                    Notes=activityNote,
                    ProblemNotes=problemNote,
                    Resolved=resolved,
                    VisitDateTime=visit_datetime
                )

                session.add(new_visit)
                session.commit()
                session.close()

                return jsonify({
                    'fulfillmentText': "✅ บันทึกข้อมูลเรียบร้อยแล้ว\nกรุณาระบุประเภทลูกค้าใหม่อีกครั้ง (ใหม่ / เดิม) เพื่อจดครั้งต่อไป",
                    'outputContexts': [
                        {
                            "name": f"{req['session']}/contexts/awaiting_customer_type",
                            "lifespanCount": 5
                        }
                    ]
                })

            except Exception as e:
                import traceback
                traceback.print_exc()
                return jsonify({
                    'fulfillmentText': "❌ ระบบเกิดข้อผิดพลาดในการบันทึกข้อมูล กรุณาลองใหม่อีกครั้ง"
                })

        elif intent == "ConfirmExistingCustomerActivity - no":
            return jsonify({
                'fulfillmentText': "โอเคครับ หากต้องการแก้ไข กรุณาระบุประเภทลูกค้าใหม่อีกครั้ง (ใหม่ / เดิม)",
                'outputContexts': [
                    {
                        "name": f"{req['session']}/contexts/awaiting_customer_type",
                        "lifespanCount": 5
                    }
                ]
            })

        elif intent == "RestartConversation":
            return jsonify({
                'fulfillmentText': "เริ่มต้นใหม่ครับ กรุณาระบุว่าคุณเป็นลูกค้าใหม่หรือลูกค้าเดิม",
                'outputContexts': [
                    {
                        "name": f"{req['session']}/contexts/_",
                        "lifespanCount": 0
                    },
                    {
                        "name": f"{req['session']}/contexts/awaiting_customer_type",
                        "lifespanCount": 5
                    }
                ]
            })

        return jsonify({'fulfillmentText': "ไม่พบ intent ที่ต้องการ"})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({'fulfillmentText': "ระบบเกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง"}), 200
