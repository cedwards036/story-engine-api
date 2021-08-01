import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Heroku's DATABASE_URL uses the outdated "postgres://" prefix which SQLAlchemy doesn't accept anymore
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    from story_engine_api.models import Deck, Pack, Category, Card

    @app.route('/decks')
    def get_decks():
        return jsonify(Deck.query.all())
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()