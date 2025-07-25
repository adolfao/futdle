from flask import render_template, Blueprint, request, session
import random
from futdle.models import Time

main = Blueprint('main', __name__)

@main.route('/')
def home():
  return render_template('home.html')

@main.route('/classico', methods=["GET", "POST"])
def classico():
  if "time_secreto_id" not in session:
    times = Time.query.all()
    time_secreto = random.choice(times)
    session["time_secreto_id"] = time_secreto.id
  else:
    time_secreto = Time.query.get(session["time_secreto_id"])

  resultado = None

  if request.method == "POST":
      chute = request.form.get("chute", "").strip()
      if chute.lower() == time_secreto.nome.lower():
        resultado = "Acertou!"
        session.pop("time_secreto_id", None)
      else:
        resultado = "Errou!"

  return render_template("classico.html", resultado=resultado)