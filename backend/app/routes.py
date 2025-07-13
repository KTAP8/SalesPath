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
from .models import Visit, Client, Invoice, Prospect, SalesMan, Auth_Users
from flask import request, jsonify, Blueprint, current_app, make_response
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, text
from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from . import jwt  # ✅ pulls the shared jwt object
from sqlalchemy.sql import exists
from sqlalchemy.exc import OperationalError
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
import calendar

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import csv
from flask import Response

from decimal import Decimal
from io import StringIO

main = Blueprint("main", __name__)


# --- JWT Error Handlers ---
# This callback is called if an expired but otherwise valid access token
# attempts to access a protected endpoint.
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """
    Handles responses for expired JWT tokens.
    Returns a 401 Unauthorized response with a specific message.
    """
    return jsonify({
        "msg": "The access token has expired",
        "error": "token_expired"
    }), 401

# This callback is called if an invalid JWT token attempts to access
# a protected endpoint (e.g., tampered, malformed).
@jwt.invalid_token_loader
def invalid_token_callback(callback_error):
    """
    Handles responses for invalid JWT tokens.
    Returns a 401 Unauthorized response with a specific message.
    """
    return jsonify({
        "msg": "Signature verification failed or token is invalid",
        "error": "invalid_token"
    }), 401

# This callback is called if no JWT token is provided when required.
@jwt.unauthorized_loader
def unauthorized_callback(callback_error):
    """
    Handles responses when no JWT token is provided for a protected endpoint.
    Returns a 401 Unauthorized response with a specific message.
    """
    return jsonify({
        "msg": "Missing Authorization Header",
        "error": "authorization_required"
    }), 401

@main.route("/")
@jwt_required()
def test_connection():
    try:
        engine = db.get_engine(app=None, bind="touchdb")
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "✅ Connected to PostgreSQL (touchdb) successfully!"
    except Exception as e:
        return f"❌ Failed to connect to db: {str(e)}"


@main.route("/api/salesmen", methods=["GET"])
@jwt_required()
def get_all_salesmen():
    try:
        salesmen = SalesMan.query.all()
        return jsonify([s.to_dict() for s in salesmen])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/api/clients", methods=["GET"])
@jwt_required()
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


@main.route("/api/visits", methods=["GET"])
@jwt_required()
def get_filtered_visits_cross_db():
    try:
        from_date = request.args.get("from")
        to_date = request.args.get("to")
        sales_name = request.args.get("sales")
        client_region = request.args.get("region")
        activity = request.args.get("activity")
        resolved = request.args.get("resolved")

        touchdb_session = Session(db.get_engine(current_app, bind="touchdb"))
        chaluck_session = Session(db.get_engine(current_app, bind="chaluck"))

        # Filter Visit records from touchdb
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
                visit_query = visit_query.filter(Visit.Resolved == bool(int(resolved)))
            except ValueError:
                return jsonify({"error": "Resolved must be 0 or 1"}), 400

        visits = visit_query.all()

        # Get related clients
        clients = chaluck_session.query(Client).all()
        client_map = {c.ClientId: c for c in clients}

        # Combine into response
        response = []
        for v in visits:
            c = client_map.get(v.ClientId)

            visit_data = v.to_dict()
            visit_data["ClientReg"] = c.ClientReg if c else None
            visit_data["ClientType"] = c.ClientType if c else None
            visit_data["Sales"] = v.Sales  # Keep sales info

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


@main.route("/api/visits", methods=["POST"])
@jwt_required()
def create_visit():
    try:
        data = request.get_json()
        SalesName = data.get("SalesName")
        ClientId = data.get("ClientId")
        Activity = data.get("Activity")
        Notes = data.get("Notes")
        ProblemNotes = data.get("ProblemNotes")
        Resolved = data.get("Resolved")
        Sales = data.get("Sales") if Activity == "Sale" else None
        visit_datetime_str = data.get("VisitDateTime")

        if not all([SalesName, ClientId, Activity, Notes]):
            return jsonify({"error": "Missing required fields"}), 400

        VisitDateTime = (
            datetime.fromisoformat(visit_datetime_str)
            if visit_datetime_str
            else datetime.now()
        )

        new_visit = Visit(
            SalesName=SalesName,
            ClientId=ClientId,
            Activity=Activity,
            Notes=Notes,
            ProblemNotes=ProblemNotes,
            Resolved=Resolved,
            VisitDateTime=VisitDateTime,
            Sales=Sales
        )

        session = Session(db.get_engine(current_app, bind="touchdb"))
        session.add(new_visit)
        session.commit()
        response = new_visit.to_dict()
        session.close()

        return (
            jsonify({"message": "Visit created successfully", "visit": response}),
            201,
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@main.route("/api/visit/<int:visit_id>/resolve", methods=["PUT"])
@jwt_required()
def update_resolved_status(visit_id):
    try:
        data = request.get_json(force=True, silent=True)
        if not data or "Resolved" not in data:
            return jsonify({"error": "Missing 'Resolved' in request body"}), 400

        resolved = int(data["Resolved"])

        session = Session(db.get_engine(current_app, bind="touchdb"))
        visit = session.get(Visit, visit_id)
        if not visit:
            session.close()
            return jsonify({"error": f"Visit ID {visit_id} not found"}), 404

        visit.Resolved = resolved
        session.commit()

        session.close()
        return jsonify(
            {
                "message": f"Visit ID {visit_id} resolved status updated.",
                "VisitId": visit.VisitId,
                "Resolved": visit.Resolved,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/api/prospects", methods=["GET"])
@jwt_required()
def get_prospects():
    try:
        sales_name = request.args.get("sales")
        region = request.args.get("region")

        session = Session(db.get_engine(current_app, bind="touchdb"))
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


@main.route("/api/prospects", methods=["POST"])
@jwt_required()
def create_prospect():
    try:
        data = request.get_json()
        ProspectId = data.get("ProspectId")
        ProspectReg = data.get("ProspectReg")
        ProspectSubReg = data.get("ProspectSubReg")
        SalesName = data.get("SalesName")

        if not all([ProspectReg, ProspectSubReg, SalesName]):
            return jsonify({"error": "Missing required fields"}), 400

        session = Session(db.get_engine(current_app, bind="touchdb"))
        new_prospect = Prospect(
            ProspectId=ProspectId,
            ProspectReg=ProspectReg,
            ProspectSubReg=ProspectSubReg,
            SalesName=SalesName,
        )

        session.add(new_prospect)
        session.commit()
        response = new_prospect.to_dict()
        session.close()
        return (
            jsonify({"message": "Prospect created successfully", "prospect": response}),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/api/invoices", methods=["GET"])
@jwt_required()
def get_invoices():
    try:
        from_date = request.args.get("from")
        to_date = request.args.get("to")

        if not from_date and not to_date:
            return (
                jsonify(
                    {"error": "Please provide a date range to avoid full-table scan"}
                ),
                400,
            )

        session = Session(db.get_engine(current_app, bind="chaluck"))
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
@jwt_required()
def get_salesman_revenue():
    try:
        # 🗓️ Default date range: from first day of previous month to today
        today = datetime.today()
        default_from = (today.replace(day=1) - relativedelta(months=1)).strftime(
            "%Y-%m-%d"
        )
        default_to = today.strftime("%Y-%m-%d")

        from_date = request.args.get("from") or default_from
        to_date = request.args.get("to") or default_to

        session = Session(db.get_engine(current_app, bind='chaluck'))

        # Fetch all clients and invoices within date range
        clients = session.query(Client).all()
        invoices = session.query(Invoice).filter(
            Invoice.TransactionDate >= from_date,
            Invoice.TransactionDate <= to_date
        ).all()
        salesmen = session.query(SalesMan).all()

        # Create lookup maps
        client_map = {c.ClientId: c for c in clients}
        salesman_name_map = {s.SalesId: s.SalesName for s in salesmen}

        # Group revenue by SalesId
        revenue_summary = {}

        for invoice in invoices:
            client = client_map.get(invoice.ClientId)
            if not client:
                continue

            sales_id = client.SalesId
            if sales_id not in revenue_summary:
                revenue_summary[sales_id] = {
                    "SalesName": salesman_name_map.get(sales_id, "Unknown"),
                    "TotalRevenue": 0,
                    "ClientIds": set()
                }

            revenue_summary[sales_id]["TotalRevenue"] += float(
                invoice.Amount or 0)
            revenue_summary[sales_id]["ClientIds"].add(invoice.ClientId)

        session.close()

        # Return as list of dicts
        return jsonify([
            {
                "SalesId": sid,
                "SalesName": data["SalesName"],
                "TotalRevenue": data["TotalRevenue"],
                "ClientSoldCount": len(data["ClientIds"])
            }
            for sid, data in revenue_summary.items()
        ])

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@main.route("/api/clients-per-salesman", methods=["GET"])
@jwt_required()
def get_client_counts():
    try:
        from datetime import date, timedelta

        from_date = request.args.get("from")
        to_date = request.args.get("to")

        if not to_date:
            to_date = date.today().isoformat()
        if not from_date:
            from_date = (date.today() - timedelta(days=30)).isoformat()

        session_touchdb = Session(db.get_engine(current_app, bind="touchdb"))
        session_chaluck = Session(db.get_engine(current_app, bind="chaluck"))

        # Step 1: Fetch visited clients from touchdb
        visit_data = (
            session_touchdb.query(
                Visit.SalesName,
                func.count(func.distinct(Visit.ClientId)).label("VisitedClients"),
            )
            .filter(Visit.VisitDateTime >= from_date, Visit.VisitDateTime <= to_date)
            .group_by(Visit.SalesName)
            .all()
        )

        visited_map = {row.SalesName: row.VisitedClients for row in visit_data}

        # Step 2: Fetch all salesmen and their total clients from chaluck
        query = session_chaluck.query(
            SalesMan.SalesId,                      # <-- Added
            SalesMan.SalesName,
            func.count(Client.ClientId).label("TotalClients")
        ).outerjoin(
            Client, Client.SalesId == SalesMan.SalesId
        ).group_by(SalesMan.SalesId, SalesMan.SalesName)  # <-- Group by SalesId too

        result = []
        for row in query.all():
            visited = visited_map.get(row.SalesName, 0)
            result.append({
                "SalesId": row.SalesId,             # <-- Added
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


@main.route("/api/users", methods=["POST"])
def create_user():
    """
    POST /api/users
    Body JSON: { "email": "...", "password": "..." }

    1. Validate input
    2. Refuse duplicates
    3. Hash password
    4. INSERT new row
    5. Return the public data (never the hash)
    """
    data = request.get_json(silent=True)
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "email and password required"}), 400

    # step 2: duplicate check
    if Auth_Users.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "email already registered"}), 409

    # step 3: hash pw
    pw_hash = generate_password_hash(data["password"])

    # step 4: insert
    new_user = Auth_Users(email=data["email"], password_hash=pw_hash)
    db.session.add(new_user)
    db.session.commit()

    # step 5: reply (uses AuthUser.to_dict() from models.py)
    return jsonify(new_user.to_dict()), 201


@main.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or request.form.to_dict()
    email = data.get("email") if data else None
    password = data.get("password") if data else None

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    user = Auth_Users.query.filter_by(email=email).first()
    if user is None or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)

    return (
        jsonify(
            {
                "access_token": access_token,
                "user": user.to_dict(),  # safe public info only
            }
        ),
        200,
    )
font_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'static', 'fonts', 'THSarabunNew.ttf'
))
pdfmetrics.registerFont(TTFont('THSarabun', font_path))


@main.route('/api/sales-report', methods=['GET'])
def generate_sales_report():
    try:
        # Get parameters from query string
        salesman_id = request.args.get('salesman_id', type=int)
        month_str = request.args.get('month')  # Expected format: YYYY-MM

        if not salesman_id or not month_str:
            return jsonify({"error": "salesman_id and month (YYYY-MM) are required"}), 400

        try:
            year, month = map(int, month_str.split('-'))
            if not (1 <= month <= 12):
                raise ValueError
        except ValueError:
            return jsonify({"error": "Invalid month format. Use YYYY-MM"}), 400

        # Initialize sessions
        touchdb_session = Session(db.get_engine(current_app, bind='touchdb'))
        chaluck_session = Session(db.get_engine(current_app, bind='chaluck'))

        try:
            # Get the salesman
            salesman = chaluck_session.query(
                SalesMan).filter_by(SalesId=salesman_id).first()
            if not salesman:
                return jsonify({"error": "Salesman not found"}), 404

            # Calculate date range for the month
            _, last_day = calendar.monthrange(year, month)
            start_date = datetime(year, month, 1)
            end_date = datetime(year, month, last_day, 23, 59, 59)

            print(start_date, end_date)

            # Query 1: Total clients visited in the month
            visits = touchdb_session.query(Visit).filter(
                Visit.SalesName == salesman.SalesName,
                Visit.VisitDateTime >= start_date,
                Visit.VisitDateTime <= end_date
            ).all()
            client_ids_visited = {visit.ClientId for visit in visits}
            total_clients_visited = len(client_ids_visited)

            # Query 2: Visits with sales
            sales_visits = touchdb_session.query(Visit).filter(
                Visit.SalesName == salesman.SalesName,
                Visit.VisitDateTime >= start_date,
                Visit.VisitDateTime <= end_date,
                Visit.Activity.ilike('sale')
            ).count()

            # Query 3: Revenue from invoices
            revenue = chaluck_session.query(func.sum(Invoice.Amount)).join(
                Client, Invoice.ClientId == Client.ClientId
            ).filter(
                Client.SalesId == salesman_id,
                Invoice.TransactionDate >= start_date,
                Invoice.TransactionDate <= end_date
            ).scalar() or 0.0

            revenue = revenue / Decimal("1.07")

            # Query 4: Clients with no sales
            clients_no_sales = chaluck_session.query(Client).outerjoin(
                Invoice, Client.ClientId == Invoice.ClientId
            ).filter(
                Client.SalesId == salesman_id,
                Invoice.InvoiceId.is_(None)
            ).all()

            # Query 5: Clients not visited
            # Step 1: Get all visited client IDs for this salesman from touchdb
            visited_clients = touchdb_session.query(Visit.ClientId).filter(
                Visit.SalesName == salesman.SalesName
            ).distinct().all()
            visited_client_ids = {row[0] for row in visited_clients}

            # Step 2: Get all clients from chaluck for this salesman
            all_clients = chaluck_session.query(Client).filter(
                Client.SalesId == salesman_id
            ).all()

            # Step 3: Clients not visited = those whose ID is not in visited_client_ids
            clients_no_visits = [
                client for client in all_clients if client.ClientId not in visited_client_ids]

            # Generate PDF
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(
                name='ThaiTitle', fontName='THSarabun', fontSize=24, leading=28, alignment=1))
            styles.add(ParagraphStyle(name='ThaiHeading',
                       fontName='THSarabun', fontSize=18, leading=22))
            styles.add(ParagraphStyle(name='ThaiNormal',
                       fontName='THSarabun', fontSize=14, leading=18))
            elements = []

            # Title
            elements.append(Paragraph(
                f"รายงานยอดขาย {salesman.SalesName} - {year}-{month:02d}", styles['ThaiTitle']
            ))

            elements.append(Spacer(1, 12))
            elements.append(Paragraph("สรุปรายงาน", styles['ThaiHeading']))

            summary_data = [
                ["Metric", "Value"],
                ["Total Clients Visited", str(total_clients_visited)],
                ["Visits Resulting in Sales", str(sales_visits)],
                ["Total Revenue", f"${revenue:,.2f}"]
            ]
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                # ✅ Apply to all cells
                ('FONTNAME', (0, 0), (-1, -1), 'THSarabun'),
                ('FONTSIZE', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(summary_table)
            elements.append(Spacer(1, 12))

            # Clients with No Sales
            elements.append(
                Paragraph("ลูกค้าที่ไม่มียอดขาย", styles['ThaiHeading']))
            no_sales_data = [["Client ID", "จังหวัด", "เขต/ตำบล"]] + [
                [client.ClientId, client.ClientReg or "N/A",
                    client.ClientSubReg or "N/A"]
                for client in clients_no_sales
            ]
            if len(no_sales_data) == 1:
                no_sales_data.append(["-", "-", "-"])
            no_sales_table = Table(no_sales_data)
            no_sales_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                # ✅ Apply to all cells
                ('FONTNAME', (0, 0), (-1, -1), 'THSarabun'),
                ('FONTSIZE', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(no_sales_table)
            elements.append(Spacer(1, 12))

            # Clients Not Visited
            elements.append(
                Paragraph("ลูกค้าที่ไม่ได้ไปหา", styles['ThaiHeading']))
            no_visits_data = [["Client ID", "จังหวัด", "เขต/ตำบล"]] + [
                [client.ClientId, client.ClientReg or "N/A",
                    client.ClientSubReg or "N/A"]
                for client in clients_no_visits
            ]
            if len(no_visits_data) == 1:
                no_visits_data.append(["-", "-", "-"])
            no_visits_table = Table(no_visits_data)
            no_visits_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                # ✅ Apply to all cells
                ('FONTNAME', (0, 0), (-1, -1), 'THSarabun'),
                ('FONTSIZE', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(no_visits_table)

            # Clients Visited This Month
            elements.append(Spacer(1, 12))
            elements.append(
                Paragraph("ลูกค้าที่เข้าพบในเดือนนี้", styles['ThaiHeading']))

            visited_data = [["Client ID", "วันที่เข้าพบ", "กิจกรรม", "หมายเหตุ"]] + [
                [
                    visit.ClientId or "-",
                    visit.VisitDateTime.strftime("%Y-%m-%d"),
                    visit.Activity or "-",
                    visit.Notes or "-"
                ]
                for visit in visits
            ]
            if len(visited_data) == 1:
                visited_data.append(["-", "-", "-", "-"])

            visited_table = Table(visited_data, colWidths=[80, 80, 100, 250])
            visited_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'THSarabun'),
                ('FONTSIZE', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(visited_table)

            # Optional footer with page numbers
            def footer(canvas, doc):
                canvas.saveState()
                canvas.setFont('Helvetica', 9)
                canvas.drawString(30, 20, f"Page {doc.page}")
                canvas.restoreState()

            # Build PDF
            doc.build(elements, onFirstPage=footer, onLaterPages=footer)
            pdf = buffer.getvalue()
            buffer.close()

            # Create response
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers[
                'Content-Disposition'] = f'attachment; filename=sales_report_{salesman_id}_{year}_{month:02d}.pdf'
            return response

        finally:
            touchdb_session.close()
            chaluck_session.close()

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@main.route('/api/sales-report-csv', methods=['GET'])
def export_sales_report_csv():
    try:
        salesman_id = request.args.get('salesman_id', type=int)
        month_str = request.args.get('month')

        if not salesman_id or not month_str:
            return jsonify({"error": "salesman_id and month (YYYY-MM) are required"}), 400

        try:
            year, month = map(int, month_str.split('-'))
            if not (1 <= month <= 12):
                raise ValueError
        except ValueError:
            return jsonify({"error": "Invalid month format. Use YYYY-MM"}), 400

        touchdb_session = Session(db.get_engine(current_app, bind='touchdb'))
        chaluck_session = Session(db.get_engine(current_app, bind='chaluck'))

        try:
            salesman = chaluck_session.query(
                SalesMan).filter_by(SalesId=salesman_id).first()
            if not salesman:
                return jsonify({"error": "Salesman not found"}), 404

            _, last_day = calendar.monthrange(year, month)
            start_date = datetime(year, month, 1)
            end_date = datetime(year, month, last_day, 23, 59, 59)

            # Query 1: Total clients visited
            visits = touchdb_session.query(Visit).filter(
                Visit.SalesName == salesman.SalesName,
                Visit.VisitDateTime >= start_date,
                Visit.VisitDateTime <= end_date
            ).all()
            client_ids_visited = {visit.ClientId for visit in visits}
            total_clients_visited = len(client_ids_visited)

            # Query 2: Sales visits
            sales_visits = touchdb_session.query(Visit).filter(
                Visit.SalesName == salesman.SalesName,
                Visit.VisitDateTime >= start_date,
                Visit.VisitDateTime <= end_date,
                Visit.Activity.ilike('sale')
            ).count()

            # Query 3: Revenue
            revenue = chaluck_session.query(func.sum(Invoice.Amount)).join(
                Client, Invoice.ClientId == Client.ClientId
            ).filter(
                Client.SalesId == salesman_id,
                Invoice.TransactionDate >= start_date,
                Invoice.TransactionDate <= end_date
            ).scalar() or 0.0

            revenue = revenue / Decimal("1.07")

            # Query 4: Clients with no sales
            clients_no_sales = chaluck_session.query(Client).outerjoin(
                Invoice, Client.ClientId == Invoice.ClientId
            ).filter(
                Client.SalesId == salesman_id,
                Invoice.InvoiceId.is_(None)
            ).all()

            # Query 5: Clients not visited
            visited_client_ids = {row[0] for row in touchdb_session.query(
                Visit.ClientId).filter(
                    Visit.SalesName == salesman.SalesName).distinct().all()}

            all_clients = chaluck_session.query(Client).filter(
                Client.SalesId == salesman_id).all()

            clients_no_visits = [
                c for c in all_clients if c.ClientId not in visited_client_ids]

            # Build each table as list of rows
            summary_rows = [
                ["Metric", "Value"],
                ["Total Clients Visited", total_clients_visited],
                ["Visits Resulting in Sales", sales_visits],
                ["Total Revenue (excl. VAT)", f"{revenue:,.2f}"]
            ]

            no_sales_rows = [["Client ID", "จังหวัด", "เขต/ตำบล"]]
            for c in clients_no_sales:
                no_sales_rows.append(
                    [c.ClientId, c.ClientReg or "N/A", c.ClientSubReg or "N/A"])

            not_visited_rows = [["Client ID", "จังหวัด", "เขต/ตำบล"]]
            for c in clients_no_visits:
                not_visited_rows.append(
                    [c.ClientId, c.ClientReg or "N/A", c.ClientSubReg or "N/A"])

            visited_rows = [
                ["Client ID", "วันที่เข้าพบ", "กิจกรรม", "หมายเหตุ"]]
            for v in visits:
                visited_rows.append([
                    v.ClientId or "-",
                    v.VisitDateTime.strftime("%Y-%m-%d"),
                    v.Activity or "-",
                    v.Notes or "-"
                ])

            # Pad shorter tables so all have the same number of rows
            max_len = max(len(summary_rows), len(no_sales_rows),
                          len(not_visited_rows), len(visited_rows))

            def pad_rows(rows, width):
                while len(rows) < max_len:
                    rows.append([""] * width)
                return rows

            summary_rows = pad_rows(summary_rows, 2)
            no_sales_rows = pad_rows(no_sales_rows, 3)
            not_visited_rows = pad_rows(not_visited_rows, 3)
            visited_rows = pad_rows(visited_rows, 4)

            # Merge horizontally row by row
            final_rows = []
            for i in range(max_len):
                final_rows.append(
                    summary_rows[i] + [""] + no_sales_rows[i] + [""] +
                    not_visited_rows[i] + [""] + visited_rows[i]
                )

            # Add the two rows above
            title_row = [f"{year}-{month:02d}_{salesman_id}_report"]
            section_titles = (
                ["Summary", ""] + [""] +
                ["No Sales"] + [""] * 3 +
                ["Not Visited"] + [""] * 3 +
                ["Visited"]
            )
            final_rows.insert(0, section_titles)
            final_rows.insert(0, title_row)

            # Write to CSV
            output = StringIO()
            writer = csv.writer(output)
            for row in final_rows:
                writer.writerow(row)

            csv_data = output.getvalue()
            output.close()

            response = make_response(csv_data)
            response.headers[
                'Content-Disposition'] = f'attachment; filename=sales_report_{salesman_id}_{year}_{month:02d}.csv'
            # Important for Thai support in Excel
            response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
            return response

        finally:
            touchdb_session.close()
            chaluck_session.close()

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
                        'fulfillmentText': f"พบลูกค้า {clientId} ในระบบ ✅\nกรุณาระบุกิจกรรมที่คุณทำ:\n🛍️ ขาย\n🤝 ความสัมพันธ์ลูกค้า\n🐞 แจ้งปัญหา\n(เท่านั้น)",
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
            elif activityType == 'ขาย':
                return jsonify({
                    'fulfillmentText': "กรุณาระบุของที่คุณขายในรูปแบบนี้(เท่านั้น):\nสินค้าA:จำนวน, สินค้าB:จำนวน\nเช่น สินค้าA:10, สินค้าB:50",
                    'outputContexts': [
                        {
                            "name": f"{req['session']}/contexts/awaiting_sales_detail",
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

        elif intent == "ProvideSalesDetail":
            sales_detail = req.get('queryResult', {}).get(
                'parameters', {}).get('sales_detail')
            clientId = get_param_from_contexts("clientId")
            activityType = get_param_from_contexts("activityType")
            activityNote = get_param_from_contexts("activityNote")

            # Validate sales_detail format
            pattern = r'^(\s*\S+\s*:\s*\d+\s*)(,\s*\S+\s*:\s*\d+\s*)*$'
            if not sales_detail or not re.match(pattern, sales_detail):
                return jsonify({
                    'fulfillmentText': (
                        "❌ รูปแบบข้อมูลไม่ถูกต้องครับ\n"
                        "กรุณาระบุของที่คุณขายในรูปแบบนี้ (เท่านั้น):\nสินค้าA:จำนวน, สินค้าB:จำนวน\n"
                        "ตัวอย่างเช่น: สินค้าA:10, สินค้าB:50"
                    ),
                    'outputContexts': [
                        {
                            "name": f"{req['session']}/contexts/awaiting_sales_detail",
                            "lifespanCount": 5,
                            "parameters": {
                                "clientId": clientId,
                                "activityType": activityType,
                                "activityNote": activityNote
                            }
                        }
                    ]
                })

            # If valid, continue
            confirmation_text = (
                f"กรุณายืนยันข้อมูลนี้อีกครั้ง:\n"
                f"📄 รหัสลูกค้า: {clientId}\n"
                f"📌 กิจกรรม: {activityType}\n"
                f"📝 หมายเหตุ: {activityNote}\n"
                f"🛍️ รายการขาย: {sales_detail}\n"
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
                            "salesDetail": sales_detail
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
            raw_sales_detail = get_param_from_contexts("salesDetail")

            def parse_sales_detail(text):
                try:
                    sales_dict = {}
                    if not text:
                        return None
                    items = text.split(",")
                    for item in items:
                        name, amount = item.strip().split(":")
                        sales_dict[name.strip()] = int(amount.strip())
                    return sales_dict
                except Exception as e:
                    print("❌ Error parsing sales detail:", e)
                    return None

            sales_json = parse_sales_detail(raw_sales_detail)

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
                    VisitDateTime=visit_datetime,
                    Sales=sales_json
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
