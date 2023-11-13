from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine

# Todo
def create_app(test_config=None):
    app = Flask(__name__)
    return app