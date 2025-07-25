from flask import render_template, Blueprint, request, session
from futdle.models import Time
from futdle.classico import classico_mode

main = Blueprint('main', __name__)

@main.route('/')
def home():
  return render_template('home.html')

@main.route('/classico', methods=["GET", "POST"])
def classico():
  return classico_mode()