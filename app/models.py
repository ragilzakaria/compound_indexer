from app import db


class UserPoints(db.Model):
    """Model to store user points."""
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(42), unique=True, nullable=False)  # Ethereum address
    points = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<UserPoints {self.address}: {self.points}>"
