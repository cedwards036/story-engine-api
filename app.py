import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
# Heroku's DATABASE_URL uses the outdated "postgres://" prefix which SQLAlchemy doesn't accept anymore
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Deck

@app.route('/')
def hello():
    return 'My key: ' + os.environ["SECRET_KEY"]

@app.route('/<deck>')
def hello_name(deck):
    return f'This deck is {deck}'

if __name__ == '__main__':
    app.run()