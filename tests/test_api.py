import pytest

from flask import json
from story_engine_api import create_app, db
from story_engine_api.models import Deck

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

def load_test_data(db):
    db.session.add(Deck('The Story Engine'))
    db.session.add(Deck('Deck of Worlds'))
    db.session.commit()