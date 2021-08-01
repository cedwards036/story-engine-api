import pytest

from flask import json
from story_engine_api import create_app, db
from story_engine_api.models import Deck, Pack, Category, Card

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            load_test_data(db)
        yield client

def test_get_decks(client):
    result = client.get('/decks')
    assert [{'id': 1, 'name': 'The Story Engine'}, {'id': 2, 'name': 'Deck of Worlds'}] == json.loads(result.data)

def test_get_deck_packs(client):
    expected1 = [
        {'id': 1, 'name': 'Base'},
        {'id': 2, 'name': 'Cyberpunk'},
        {'id': 3, 'name': 'Fantasy'}
    ]
    result1 = client.get('/decks/1/packs')
    assert expected1 == json.loads(result1.data)

    expected2 = [
        {'id': 4, 'name': 'Base'},
        {'id': 5, 'name': 'Desert'}
    ]
    result2 = client.get('/decks/2/packs')
    assert expected2 == json.loads(result2.data)

def test_get_random_hand(client):
    result = json.loads(client.get('/decks/1/random/hand?pack=1&pack=3').data)
    assert 3 == len(result)
    assert ['Agent', 'Anchor', 'Conflict'] == sorted([row['category'] for row in result])
    for row in result:
        assert row['pack'] in ['Base', 'Fantasy']

def test_get_random_card_from_category(client):
    result = json.loads(client.get('/decks/1/random/card?category=3&pack=3').data)
    assert {'cue': 'But the dragon will be mad', 'category': 'Conflict', 'category_id': 3, 'pack': 'Fantasy'} == result

def test_upload_csv_for_insertion(client):
    with open('tests/test_upload.csv', 'rb') as file:
        result = json.loads(client.post('/upload/insert', data={'file': file}, content_type='multipart/form-data').data)
        assert result == {'message': '6 rows processed successfully!'}

        # assert that new data was inserted successfully
        assert db.session.query(Deck).filter(Deck.name=='The Story Engine II').first() is not None
        assert db.session.query(Pack).join(Deck).filter(Deck.name=='The Story Engine II', Pack.name=='Theatre').first() is not None
        assert db.session.query(Category).join(Deck).filter(Deck.name=='The Story Engine II', Category.name=='Detail').first() is not None
        assert db.session.query(Card).join(Pack).join(Category).filter(Pack.name=='Theatre', Category.name=='Detail', Card.cue=='The sky was green today').first() is not None
        assert db.session.query(Card).join(Pack).join(Category).filter(Pack.name=='Fantasy', Category.name=='Anchor', Card.cue=='The one ring').first() is not None

        # assert that no duplicate data was inserted (duplicates shown in expected values are due to multiple decks sharing values)
        assert ['The Story Engine', 'Deck of Worlds', 'The Story Engine II'] == [deck.name for deck in db.session.query(Deck).all()]
        assert ['Base', 'Cyberpunk', 'Fantasy', 'Base', 'Desert', 'Theatre'] == [pack.name for pack in db.session.query(Pack).all()]
        assert ['Agent', 'Anchor', 'Conflict', 'Conflict', 'Detail'] == [category.name for category in db.session.query(Category).all()]
        assert ['A wizard'] == [card.cue for card in db.session.query(Card).filter_by(cue='A wizard').all()]

def load_test_data(db):
    db.session.add(Deck('The Story Engine'))
    db.session.add(Deck('Deck of Worlds'))
    
    db.session.add(Pack(1, 'Base'))
    db.session.add(Pack(1, 'Cyberpunk'))
    db.session.add(Pack(1, 'Fantasy'))
    db.session.add(Pack(2, 'Base'))
    db.session.add(Pack(2, 'Desert'))

    db.session.add(Category(1, 'Agent'))
    db.session.add(Category(1, 'Anchor'))
    db.session.add(Category(1, 'Conflict'))

    db.session.add(Card(1, 1, 'A wizard'))
    db.session.add(Card(1, 1, 'A rogue'))
    db.session.add(Card(2, 1, 'Keanu Reeves'))
    db.session.add(Card(1, 2, 'A letter'))
    db.session.add(Card(1, 3, 'But it will hurt'))
    db.session.add(Card(3, 3, 'But the dragon will be mad'))

    db.session.commit()