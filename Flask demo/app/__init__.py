__author__ = 's1407459'
from flask import Flask

app = Flask(__name__, instance_relative_config=True)

# load config
app.config.from_object('config')