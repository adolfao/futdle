from futdle import create_app
from flask import render_template, Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def home():
  return render_template('home.html')

@main.route('/classico')
def classico():
  return render_template('classico.html')