from flask import render_template, request, session
from futdle.models import Time
import random

def classico_mode():
  if "time_secreto_id" not in session:
    times = Time.query.all()
    time_secreto = random.choice(times)
    session["time_secreto_id"] = time_secreto.id
    session["tentativas"] = []
  else:
    time_secreto = Time.query.get(session["time_secreto_id"])

  resultado = None
  tentativas = session.get("tentativas", [])

  if request.method == "POST":
    chute = request.form.get("chute", "").strip()

    if chute.lower() == time_secreto.nome.lower():
        resultado = "Acertou!"
        session.pop("time_secreto_id", None)
        session["tentativas"] = []
        tentativas = []
    else:
      resultado = "Errou!"
      chute_formatado = chute.lower().split(" ")[0]
      if chute_formatado not in tentativas:
        tentativas.append(chute)
        session["tentativas"] = tentativas

  return render_template("classico.html", resultado=resultado, tentativas=tentativas)
