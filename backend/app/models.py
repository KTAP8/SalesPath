from . import db
from sqlalchemy.sql import func
from datetime import datetime


class SalesMan(db.Model):
    __bind_key__ = "chaluck"
    __tablename__ = "vsalesperson"

    SalesId = db.Column(
        db.BigInteger, primary_key=True, name="saleperson_id")
    SalesName = db.Column(db.Text, name='name')
    SalesLogin = db.Column(db.Text, name='saleperson_login')  # ✅ fixed here

    def to_dict(self):
        return {"SalesId": self.SalesId, "SalesName": self.SalesName}


class Client(db.Model):
    __bind_key__ = "chaluck"
    __tablename__ = "vcustomer"
    __table_args__ = {"extend_existing": True}  # safety for views

    id = db.Column(db.BigInteger, primary_key=True)
    ClientId = db.Column(db.Text, name="customernumber")
    ClientReg = db.Column(db.String(100), name="addr4")
    ClientSubReg = db.Column(db.String(100), name="shiptoaddr3")
    SalesLogin = db.Column(db.Text, name="salepersonlogin")
    SalesId = db.Column(db.BigInteger, name="saleperson_id")
    ClientType = db.Column(db.Text, name="f4")

    def to_dict(self):
        return {
            "id": self.id,
            "ClientId": self.ClientId,
            "ClientReg": self.ClientReg,
            "ClientSubReg": self.ClientSubReg,
            "SalesLogin": self.SalesLogin,
            "SalesId": self.SalesId,
            "ClientType": self.ClientType,
        }


class Visit(db.Model):
    __bind_key__ = "touchdb"
    __tablename__ = "Visit"

    VisitId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # , db.ForeignKey('SalesMan.SalesName'))
    SalesName = db.Column(db.String(255))
    ClientId = db.Column(db.String(255))  # , db.ForeignKey('Client.ClientId'))
    VisitDateTime = db.Column(db.DateTime, default=func.now())
    Activity = db.Column(db.String(255))
    Notes = db.Column(db.String(10000))
    ProblemNotes = db.Column(db.String(10000))
    Sales = db.Column(db.JSON)
    # TINYINT maps to Boolean in SQLAlchemy
    Resolved = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "VisitId": self.VisitId,
            "SalesName": self.SalesName,
            "ClientId": self.ClientId,
            "VisitDateTime": (
                self.VisitDateTime.isoformat() if self.VisitDateTime else None
            ),
            "Activity": self.Activity,
            "Notes": self.Notes,
            "ProblemNotes": self.ProblemNotes,
            "Sales": self.Sales,
            "Resolved": self.Resolved
        }

    def __init__(self, SalesName, ClientId, Activity, Notes=None, ProblemNotes=None, Sales=None, Resolved=None, VisitDateTime=None):
        self.SalesName = SalesName
        self.ClientId = ClientId
        self.Activity = Activity
        self.Notes = Notes
        self.ProblemNotes = ProblemNotes if Activity.lower() == "problem" else None
        self.Sales = Sales if Activity.lower() == 'sale' else None
        self.VisitDateTime = VisitDateTime if VisitDateTime else func.now()

        # Default Resolved: False if "Problem", otherwise True
        if Resolved is not None:
            self.Resolved = Resolved
        else:
            self.Resolved = False if Activity.lower() == "problem" else True


class Invoice(db.Model):
    __bind_key__ = "chaluck"
    __tablename__ = "vlistinv"
    __table_args__ = {"extend_existing": True}

    InvoiceId = db.Column(db.BigInteger, primary_key=True, name="id")
    TaxId = db.Column(db.Text, name="invnumber")
    TransactionDate = db.Column(db.Date, name="transdate")
    # hidden from to_dict
    _customerId = db.Column(db.BigInteger, name="customer_id")
    ClientId = db.Column(db.Text, name="customernumber")
    Amount = db.Column(db.Numeric, name="amount")

    def to_dict(self):
        return {
            "InvoiceId": self.InvoiceId,
            "TaxId": self.TaxId,
            "TransactionDate": (
                self.TransactionDate.isoformat() if self.TransactionDate else None
            ),
            "ClientId": self.ClientId,
            "Amount": float(self.Amount) if self.Amount is not None else None,
        }


class Prospect(db.Model):
    __bind_key__ = "touchdb"
    __tablename__ = "Prospect"

    ProspectNum = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProspectId = db.Column(db.String(255))  # your external ID
    ProspectReg = db.Column(db.String(255))
    ProspectSubReg = db.Column(db.String(255))
    SalesName = db.Column(db.String(255))
    Phone = db.Column(db.String(255))
    ProspectDateTime= db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {
            "ProspectNum": self.ProspectNum,
            "ProspectId": self.ProspectId,
            "ProspectReg": self.ProspectReg,
            "ProspectSubReg": self.ProspectSubReg,
            "SalesName": self.SalesName,
            "Phone": self.Phone,
            "ProspectDateTime": self.ProspectDateTime.isoformat() if self.ProspectDateTime else None
        }


class Auth_Users(db.Model):
    __bind_key__ = "touchdb"
    __tablename__ = "auth_users"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # handy serializer for JSON responses
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
