from ..database import db


class BlockedJWT(db.Model):
    __tablename__ = "blocked_jwt"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), nullable=False, unique=True)

