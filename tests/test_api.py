import pytest

from flask import json
from story_engine_api import create_app, db
from story_engine_api.models import Deck, Pack

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
        {'id': 3, 'name': 'Fantasy'},
        {'id': 2, 'name': 'Steampunk'}
    ]
    result1 = client.get('/decks/1/packs')
    assert expected1 == json.loads(result1.data)

    expected2 = [
        {'id': 4, 'name': 'Base'},
        {'id': 5, 'name': 'Desert'}
    ]
    result2 = client.get('/decks/2/packs')
    assert expected2 == json.loads(result2.data)

def load_test_data(db):
    db.session.add(Deck('The Story Engine'))
    db.session.add(Deck('Deck of Worlds'))
    db.session.add(Pack(1, 'Base'))
    db.session.add(Pack(1, 'Steampunk'))
    db.session.add(Pack(1, 'Fantasy'))
    db.session.add(Pack(2, 'Base'))
    db.session.add(Pack(2, 'Desert'))
    db.session.commit()