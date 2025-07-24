from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()
load_dotenv()

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///futdle.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.secret_key = os.getenv("SECRET_KEY") 

  db.init_app(app)

  from futdle.routes import main
  app.register_blueprint(main)

  with app.app_context():
      from futdle.models import Time
      db.create_all()

  return app