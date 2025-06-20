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
        clients = Client.query.all()
        return jsonify([client.to_dict() for client in clients])
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
