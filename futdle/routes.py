from flask import render_template, Blueprint, request, session, jsonify
from futdle.models import Time
from futdle.classico import classico_mode, normalizar_nome

main = Blueprint('main', __name__)

@main.route('/')
def home():
  return render_template('home.html')

@main.route('/classico', methods=["GET", "POST"])
def classico():
  return classico_mode()

@main.route('/api/sugestoes', methods=["GET"])
def sugestoes():
  query = request.args.get('q', '').strip()
  if len(query) < 1:
    return jsonify([])
  
  query_normalizado = normalizar_nome(query)
  times = Time.query.all()
  sugestoes = []
  
  for time in times:
    nome_normalizado = normalizar_nome(time.nome)
    if query_normalizado in nome_normalizado:
      sugestoes.append({
        'nome': time.nome,
        'escudo': time.nome_arquivo() + '.jpg'
      })
  
  # Limita a 5 sugestões
  return jsonify(sugestoes[:5])