from flask import render_template, request, session
from futdle.models import Time
import random
import unicodedata

def normalizar_nome(nome):
  nome_normalizado = unicodedata.normalize('NFKD', nome)
  nome_normalizado = ''.join([c for c in nome_normalizado if not unicodedata.combining(c)])
  nome_normalizado = nome_normalizado.lower().replace('ç', 'c').strip()
  return nome_normalizado

def comparar_cores(cores1, cores2):
  if cores1 == cores2:
    return "exato"
  
  # Converte para minúsculo e separa por vírgula ou "e"
  cores1_list = [c.strip().lower() for c in cores1.replace(' e ', ',').split(',')]
  cores2_list = [c.strip().lower() for c in cores2.replace(' e ', ',').split(',')]
  
  # Verifica se há alguma cor em comum
  for cor1 in cores1_list:
    for cor2 in cores2_list:
      if cor1 == cor2:
        return "parcial"
  
  return "diferente"

def buscar_time_por_nome(chute):
  chute_normalizado = normalizar_nome(chute)
  times = Time.query.all()
  
  for time in times:
    nome_time_normalizado = normalizar_nome(time.nome)
    if chute_normalizado == nome_time_normalizado:
      return time
  return None

def classico_mode():
  if "time_secreto_id" not in session:
    times = Time.query.all()
    time_secreto = random.choice(times)
    session["time_secreto_id"] = time_secreto.id
    session["tentativas"] = []
  else:
    time_secreto = Time.query.get(session["time_secreto_id"])

  resultado = None
  tentativas_nomes = session.get("tentativas", [])
  
  tentativas_objetos = []
  for nome in tentativas_nomes:
    time_obj = Time.query.filter_by(nome=nome).first()
    if time_obj:
      tentativas_objetos.append(time_obj)

  if request.method == "POST":
    chute = request.form.get("chute", "").strip()
    time_chutado = buscar_time_por_nome(chute)

    if not time_chutado:
      resultado = "Time não encontrado!"
    elif time_chutado.nome in tentativas_nomes:
      resultado = "Você já digitou esse time!"
    elif time_chutado.id == time_secreto.id:
      resultado = "Acertou!"
      session.pop("time_secreto_id", None)
      session["tentativas"] = []
      tentativas_nomes = []
      tentativas_objetos = []
    else:
      resultado = "Errou!"
      tentativas_nomes.append(time_chutado.nome)
      session["tentativas"] = tentativas_nomes
      tentativas_objetos.append(time_chutado)

  return render_template("classico.html", resultado=resultado, tentativas=tentativas_objetos, time_secreto=time_secreto)
