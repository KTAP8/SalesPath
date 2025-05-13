from . import db
from sqlalchemy.sql import func


class SalesMan(db.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'SalesMan'

    SalesName = db.Column(db.String(100), primary_key=True)

    def to_dict(self):
        return {
            "SalesName": self.SalesName
        }


class Client(db.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'Client'

    ClientId = db.Column(db.String(255), primary_key=True)
    ClientReg = db.Column(db.String(255))
    ClientSubReg = db.Column(db.String(255))
    ClientType = db.Column(db.String(255))
    SalesName = db.Column(db.String(255), db.ForeignKey('SalesMan.SalesName'))

    def to_dict(self):
        return {
            "ClientId": self.ClientId,
            "ClientReg": self.ClientReg,
            "ClientSubReg": self.ClientSubReg,
            "ClientType": self.ClientType,
            "SalesName": self.SalesName
        }


class Visit(db.Model):
    __bind_key__ = 'postgres'
    __tablename__ = 'Visit'

    VisitId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # , db.ForeignKey('SalesMan.SalesName'))
    SalesName = db.Column(db.String(255))
    ClientId = db.Column(db.String(255))  # , db.ForeignKey('Client.ClientId'))
    VisitDateTime = db.Column(db.DateTime, default=func.now())
    Activity = db.Column(db.String(255))
    Notes = db.Column(db.String(10000))
    ProblemNotes = db.Column(db.String(10000))
    # TINYINT maps to Boolean in SQLAlchemy
    Resolved = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "VisitId": self.VisitId,
            "SalesName": self.SalesName,
            "ClientId": self.ClientId,
            "VisitDateTime": self.VisitDateTime.isoformat() if self.VisitDateTime else None,
            "Activity": self.Activity,
            "Notes": self.Notes,
            "ProblemNotes": self.ProblemNotes,
            "Resolved": self.Resolved
        }

    def __init__(self, SalesName, ClientId, Activity, Notes=None, ProblemNotes=None, Resolved=None, VisitDateTime=None):
        self.SalesName = SalesName
        self.ClientId = ClientId
        self.Activity = Activity
        self.Notes = Notes
        self.ProblemNotes = ProblemNotes if Activity.lower() == "problem" else None
        self.VisitDateTime = VisitDateTime if VisitDateTime else func.now()

        # Default Resolved: False if "Problem", otherwise True
        if Resolved is not None:
            self.Resolved = Resolved
        else:
            self.Resolved = False if Activity.lower() == "problem" else True


class Invoice(db.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'Invoice'

    InvoiceId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TaxId = db.Column(db.String(255))
    TransactionDate = db.Column(db.Date)
    ClientId = db.Column(db.String(255), db.ForeignKey('Client.ClientId'))
    Amount = db.Column(db.Numeric(precision=12, scale=2))

    def to_dict(self):
        return {
            "InvoiceId": self.InvoiceId,
            "TaxId": self.TaxId,
            "TransactionDate": self.TransactionDate.isoformat() if self.TransactionDate else None,
            "ClientId": self.ClientId,
            "Amount": float(self.Amount)
        }


class Prospect(db.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'Prospect'

    ProspectId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProspectReg = db.Column(db.String(255))
    ProspectSubReg = db.Column(db.String(255))
    SalesName = db.Column(db.String(255), db.ForeignKey('SalesMan.SalesName'))

    def to_dict(self):
        return {
            "ProspectId": self.ProspectId,
            "ProspectReg": self.ProspectReg,
            "ProspectSubReg": self.ProspectSubReg,
            "SalesName": self.SalesName
        }
