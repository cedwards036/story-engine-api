from app import db


class Deck(db.Model):
    __tablename__ = 'deck'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    packs = db.relationship('Pack', backref=db.backref('deck', lazy=True))
    categories = db.relationship('Category', backref=db.backref('deck', lazy=True))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Deck id: {self.id}, name: {self.name}>'


class Pack(db.Model):
    __tablename__ = 'pack'

    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    cards = db.relationship('Card', backref=db.backref('pack', lazy=True))
    db.UniqueConstraint(deck_id, name)

    def __init__(self, deck_id, name):
        self.deck_id = deck_id
        self.name = name

    def __repr__(self):
        return f'<Pack id: {self.id}, deck_id: {self.deck_id}, name: {self.name}>'


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    cards = db.relationship('Card', backref=db.backref('category', lazy=True))
    db.UniqueConstraint(deck_id, name)

    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name

    def __repr__(self):
        return f'<Category id: {self.id}, deck_id: {self.deck_id}, name: {self.name}>'


class Card(db.Model):
    __tablename__ = 'card'

    id = db.Column(db.Integer, primary_key=True)
    pack_id = db.Column(db.Integer, db.ForeignKey('pack.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    cue = db.Column(db.String(), nullable=False)
    db.UniqueConstraint(pack_id, category_id, cue)

    def __init__(self, pack_id, category_id, cue):
        self.pack_id = pack_id
        self.category_id = category_id
        self.cue = cue

    def __repr__(self):
        return f'<Card id: {self.id}, pack_id: {self.pack_id}, category_id: {self.category_id}, cue: {self.cue}>'
