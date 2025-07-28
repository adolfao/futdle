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

  # Função personalizada para comparar cores
  def comparar_cores_jinja(cores1, cores2):
    if cores1 == cores2:
      return "exato"
    
    cores1_list = [c.strip().lower() for c in cores1.replace(' e ', ',').split(',')]
    cores2_list = [c.strip().lower() for c in cores2.replace(' e ', ',').split(',')]
    
    for cor1 in cores1_list:
      for cor2 in cores2_list:
        if cor1 == cor2:
          return "parcial"
    
    return "diferente"

  # Função personalizada para comparar anos
  def comparar_anos_jinja(ano_chute, ano_secreto):
    if ano_chute == ano_secreto:
      return "correto"
    elif ano_chute < ano_secreto:
      return "seta_cima"  # Precisa ir para cima (ano maior)
    else:
      return "seta_baixo"  # Precisa ir para baixo (ano menor)

  app.jinja_env.globals.update(comparar_cores=comparar_cores_jinja)
  app.jinja_env.globals.update(comparar_anos=comparar_anos_jinja)

  from futdle.routes import main
  app.register_blueprint(main)

  with app.app_context():
    from futdle.models import Time
    from tests_db.tests import popular_times

    db.create_all()
    popular_times()

  return app