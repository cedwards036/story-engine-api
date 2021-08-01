import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)

@app.route('/')
def hello():
    return os.environ["SECRET_KEY"]


if __name__ == '__main__':
    app.run()