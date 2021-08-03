import os
import random
import io
import csv
from dotenv import load_dotenv
from flask import Flask, jsonify, request
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
    from story_engine_api.serializers import DeckSchema, PackSchema, CategorySchema

    @app.route('/decks', methods=['GET'])
    def get_decks():
        return DeckSchema(many=True).dumps(Deck.query.all())

    @app.route('/decks', methods=['POST'])
    def create_deck():
        deck_name = request.json['name']
        if Deck.query.filter_by(name=deck_name).first() is None:
            new_deck = Deck(deck_name)
            db.session.add(new_deck)
            db.session.commit()
            db.session.refresh(new_deck)
            return DeckSchema().dumps(new_deck)
        else:
            return jsonify({'Error': f'Deck "{deck_name}" already exists'}), 422
    
    @app.route('/decks/<deck_id>/packs', methods=['GET'])
    def get_deck_packs(deck_id):
        return PackSchema(many=True).dumps(Pack.query.filter(Pack.deck_id==deck_id).order_by(Pack.name).all())
    
    @app.route('/decks/<deck_id>/packs', methods=['POST'])
    def create_pack(deck_id):
        pack_name = request.json['name']
        if Pack.query.filter_by(name=pack_name, deck_id=deck_id).first() is None:
            new_pack = Pack(deck_id, pack_name)
            db.session.add(new_pack)
            db.session.commit()
            db.session.refresh(new_pack)
            return PackSchema().dumps(new_pack)
        else:
            return jsonify({'Error': f'Pack "{pack_name}" already exists'}), 422

    
    @app.route('/decks/<deck_id>/categories', methods=['POST'])
    def create_category(deck_id):
        category_name = request.json['name']
        category_order = request.json['order']
        if Category.query.filter_by(name=category_name, deck_id=deck_id).first() is None:
            new_category = Category(deck_id, category_name, category_order)
            db.session.add(new_category)
            db.session.commit()
            db.session.refresh(new_category)
            return CategorySchema().dumps(new_category)
        else:
            return jsonify({'Error': f'Category "{category_name}" already exists'}), 422

    @app.route('/decks/<deck_id>/random/hand', methods=['GET'])
    def get_random_hand(deck_id):
        categories = get_deck_categories(deck_id)
        packs = request.args.getlist('pack')
        return jsonify([get_random_card(category.id, packs) for category in categories])

    @app.route('/decks/<deck_id>/random/card', methods=['GET'])
    def get_random_card_from_category(deck_id):
        category_id = request.args.get('category')
        pack_ids = request.args.getlist('pack')
        return jsonify(get_random_card(category_id, pack_ids))
    
    @app.route('/upload/insert', methods=['POST'])
    def upload_csv_for_insertion():
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({'message': 'No file selected'}), 400
        else:
            file = request.files['file']
            stream = io.StringIO(file.stream.read().decode('UTF8'), newline=None)
            csv_input = [row for row in csv.DictReader(stream)]
            for row in csv_input:
                deck = Deck.query.filter_by(name=row['deck']).first()
                pack = Pack.query.join(Deck).filter(Deck.name==row['deck'], Pack.name==row['pack']).first()
                category = Category.query.join(Deck).filter(Deck.name==row['deck'], Category.name==row['category']).first()
                card = Card.query.join(Pack).join(Deck).join(Category).filter(Deck.name==row['deck'], Pack.name==row['pack'], Category.name==row['category'], Card.cue==row['cue']).first()
                if deck is None or pack is None or category is None:
                    return jsonify({'message': 'Invalid data'}), 400
                elif card is None:
                    card = Card(pack.id, category.id, row['cue'])
                    db.session.add(card)
            db.session.commit()
            return jsonify({'message': f'{len(csv_input)} rows processed successfully!'})



    def get_deck_categories(deck_id):
        return Category.query.filter(Category.deck_id==deck_id).order_by(Category.order).all()

    def get_random_card(category_id, pack_ids):
        query_results = Card.query.join(Card.category).join(Card.pack).filter(Card.category_id==category_id, Card.pack_id.in_(pack_ids)).all()
        chosen_card = random.choice(query_results)
        return {
            'cue': chosen_card.cue,
            'category': chosen_card.category.name,
            'category_id': chosen_card.category.id,
            'pack': chosen_card.pack.name
        }

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()