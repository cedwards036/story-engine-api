import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
# Heroku's DATABASE_URL uses the outdated "postgres://" prefix which SQLAlchemy doesn't accept anymore
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Deck, Pack, Category, Card

@app.route('/decks')
def get_decks():
    return jsonify(Deck.query.all())

if __name__ == '__main__':
    app.run()
