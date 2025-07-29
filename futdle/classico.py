from flask import render_template, request, session
from futdle.models import Time, normalizar_nome
import random

#compara cores dos times e retorna exato, parcial ou diferente
def comparar_cores(cores1, cores2):
  if cores1 == cores2:
    return "exato"
  
  #converte para listas normalizadas
  cores1_list = [c.strip().lower() for c in cores1.replace(' e ', ',').split(',')]
  cores2_list = [c.strip().lower() for c in cores2.replace(' e ', ',').split(',')]
  
  #verifica se ha alguma cor em comum
  if any(cor1 == cor2 for cor1 in cores1_list for cor2 in cores2_list):
    return "parcial"
  
  return "diferente"

def buscar_time_por_nome(chute):
  return Time.buscar_por_nome_normalizado(chute)

#inicializa novo jogo se nao existe ou retorna time secreto atual
def inicializar_jogo():
  if "time_secreto_id" not in session:
    times = Time.query_all()
    time_secreto = random.choice(times)
    session.update({
      "time_secreto_id": time_secreto.id,
      "tentativas": [],
      "tentativas_erradas": 0,
      "jogo_finalizado": False
    })
    return time_secreto
  return Time.get_by_id(session["time_secreto_id"])

#funcao principal do modo classico
def classico_mode():
  time_secreto = inicializar_jogo()
  jogo_finalizado = session.get("jogo_finalizado", False)
  tentativas_nomes = session.get("tentativas", [])
  tentativas_erradas = session.get("tentativas_erradas", 0)
  mostrar_dica_mascote = tentativas_erradas >= 7
  mostrar_dica_serie = tentativas_erradas >= 4
  
  #converte nomes das tentativas em objetos time
  tentativas_objetos = [Time.get_by_nome(nome) for nome in tentativas_nomes if Time.get_by_nome(nome)]

  resultado = None
  if request.method == "POST":
    resultado = processar_chute(tentativas_nomes, tentativas_objetos, time_secreto)
    tentativas_erradas = session.get("tentativas_erradas", 0)
    mostrar_dica_mascote = tentativas_erradas >= 7
    mostrar_dica_serie = tentativas_erradas >= 4

  return render_template("classico.html", 
                       resultado=resultado, 
                       tentativas=tentativas_objetos, 
                       time_secreto=time_secreto, 
                       jogo_finalizado=session.get("jogo_finalizado", False),
                       tentativas_erradas=tentativas_erradas,
                       mostrar_dica_mascote=mostrar_dica_mascote,
                       mostrar_dica_serie=mostrar_dica_serie,
                       comparar_cores=comparar_cores)

#processa tentativa do usuario e atualiza estado do jogo
def processar_chute(tentativas_nomes, tentativas_objetos, time_secreto):
  chute = request.form.get("chute", "").strip()
  time_chutado = buscar_time_por_nome(chute)

  if not time_chutado:
    return "Time não encontrado!"
  
  if time_chutado.nome in tentativas_nomes:
    return "Você já digitou esse time!"

  tentativas_nomes.append(time_chutado.nome)
  tentativas_objetos.append(time_chutado)
  session["tentativas"] = tentativas_nomes

  if time_chutado.id == time_secreto.id:
    session["jogo_finalizado"] = True
    return "Acertou!"
  else:
    tentativas_erradas = session.get("tentativas_erradas", 0) + 1
    session["tentativas_erradas"] = tentativas_erradas
    return "Errou!"
