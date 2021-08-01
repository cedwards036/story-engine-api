import pytest

from flask import json
from story_engine_api import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_get_decks(client):
    result = client.get('/decks')
    assert [] == json.loads(result.data)
