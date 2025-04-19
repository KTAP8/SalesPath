from . import db


class SalesMan(db.Model):
    __tablename__ = 'SalesMan'

    SalesName = db.Column(db.String(100), primary_key=True)

    def to_dict(self):
        return {
            "SalesName": self.SalesName
        }
