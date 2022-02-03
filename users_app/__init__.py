# python3 -m venv env/myenv
# source env/myenv/bin/activate
from flask import Flask

app = Flask(__name__)
app.secret_key = 'asldfkjeoivn;akn'