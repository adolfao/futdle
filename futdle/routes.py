from flask import render_template, Blueprint, request, session, jsonify
from futdle.models import Time, normalizar_nome
from futdle.classico import classico_mode

main = Blueprint('main', __name__)

@main.route('/')
def home():
  return render_template('home.html')

@main.route('/classico', methods=["GET", "POST"])
def classico():
  return classico_mode()

#api para autocomplete do campo de busca
@main.route('/api/sugestoes', methods=["GET"])
def sugestoes():
  query = request.args.get('q', '').strip()
  if len(query) < 1:
    return jsonify([])
  
  query_normalizado = normalizar_nome(query)
  times = Time.query_all()
  tentativas_nomes = session.get("tentativas", [])
  sugestoes = []
  
  #filtra times que ja foram tentados
  for time in times:
    if time.nome in tentativas_nomes:
      continue
    nome_normalizado = normalizar_nome(time.nome)
    # Busca apenas no início do nome (não em qualquer parte)
    if nome_normalizado.startswith(query_normalizado):
      sugestoes.append({
        'nome': time.nome,
        'escudo': time.nome_arquivo() + '.jpg'
      })
  
  return jsonify(sugestoes[:5])

#reinicia jogo limpando sessao
@main.route('/reiniciar-jogo', methods=["POST"])
def reiniciar_jogo():
  session.pop("time_secreto_id", None)
  session.pop("tentativas", None)
  session.pop("tentativas_erradas", None)
  session.pop("jogo_finalizado", None)
  return jsonify({"success": True})