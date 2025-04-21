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


# get all visits + revenue: filter by SalesName, Region, date range

@main.route('/api/visits', methods=['GET'])
def get_filtered_visits():
    try:
        from_date = request.args.get('from')
        to_date = request.args.get('to')
        sales_name = request.args.get('sales')
        client_region = request.args.get('region')

        # Base query: Visit joined with Client
        query = db.session.query(
            Visit,
            Invoice.Amount.label("InvoiceAmount")
        ).join(Client, Visit.ClientId == Client.ClientId
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

        if filters:
            query = query.filter(and_(*filters))

        results = query.all()

        # Format output
        response = []
        for visit, amount in results:
            visit_data = visit.to_dict()
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

# @main.route('/api/visit-columns')
# def get_visit_columns():
#     inspector = db.inspect(db.engine)
#     columns = inspector.get_columns('Visit')
#     return jsonify([{"name": c["name"], "type": str(c["type"])} for c in columns])
