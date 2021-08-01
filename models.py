from app import db


class Deck(db.Model):
    __tablename__ = 'deck'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<id {self.id}>'