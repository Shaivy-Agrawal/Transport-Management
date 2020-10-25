from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.secret_key = "gumnaam"

from app import views, rest

app.config.from_object('config')