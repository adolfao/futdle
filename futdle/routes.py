from flask import render_template, Blueprint, request, session, jsonify
from futdle.models import Time, normalizar_nome
from futdle.classico import classico_mode
from futdle.escudo import escudo_mode

# Blueprint principal para organizar as rotas
main = Blueprint('main', __name__)

# === ROTAS PRINCIPAIS DO JOGO ===

@main.route('/')
def home():
    """Página inicial com seleção dos modos de jogo."""
    return render_template('home.html')

@main.route('/classico', methods=["GET", "POST"])
def classico():
    """Modo clássico - delega lógica para o módulo classico.py."""
    return classico_mode()

@main.route('/escudo', methods=["GET", "POST"])
def escudo():
    """Modo escudo - ainda em desenvolvimento."""
    return escudo_mode()

# === API ENDPOINTS ===

@main.route('/api/sugestoes', methods=["GET"])
def sugestoes():
    """API para autocomplete de nomes de times."""
    query = request.args.get('q', '').strip()
    tentativas_nomes = session.get("tentativas", [])
    
    # Usa o método otimizado da classe Time
    sugestoes_list = Time.buscar_sugestoes(
        query=query,
        times_ja_tentados=tentativas_nomes
    )
    
    return jsonify(sugestoes_list)

@main.route('/api/time_info', methods=["GET"])
def time_info():
    """API para buscar informações detalhadas de um time."""
    from futdle.classico import comparar_cores
    
    nome = request.args.get('nome')
    if not nome:
        return jsonify({"error": "Nome do time não fornecido"}), 400
        
    time = Time.buscar_por_nome_normalizado(nome)
    if not time:
        return jsonify({"error": "Time não encontrado"}), 404
    
    # Verifica se existe um jogo ativo
    if "time_secreto_id" not in session:
        return jsonify({"error": "Nenhum jogo ativo"}), 400
        
    time_secreto = Time.get_by_id(session["time_secreto_id"])
    
    # Determina as classes CSS baseadas na comparação
    cores_status = ""
    if comparar_cores(time.cores, time_secreto.cores) == "exato":
        cores_status = "cores-exato"
    elif comparar_cores(time.cores, time_secreto.cores) == "parcial":
        cores_status = "cores-parcial"
    else:
        cores_status = "cores-diferente"
    
    estado_status = "estado-correto" if time.estado == time_secreto.estado else "estado-incorreto"
    ano_status = "ano-correto" if time.ano_fundacao == time_secreto.ano_fundacao else "ano-incorreto"
    
    return jsonify({
        'nome': time.nome,
        'escudo': time.escudo,
        'cores': time.cores,
        'estado': time.estado,
        'ano_fundacao': time.ano_fundacao,
        'cores_status': cores_status,
        'estado_status': estado_status,
        'ano_status': ano_status
    })

@main.route('/reiniciar-jogo', methods=["POST"])
def reiniciar_jogo():
    """Limpa todos os dados do jogo atual da sessão."""
    session.pop("time_secreto_id", None)
    session.pop("tentativas", None)
    session.pop("tentativas_erradas", None)
    session.pop("jogo_finalizado", None)
    return jsonify({"success": True})

# === ROTAS DO RODAPÉ ===
@main.route('/sobre')
def sobre():
    return render_template('sobre.html')

@main.route('/como-jogar')
def como_jogar():
    return render_template('como_jogar.html')

@main.route('/politica-privacidade')
def politica_privacidade():
    return render_template('politica_privacidade.html')

@main.route('/contato')
def contato():
    return render_template('contato.html')

@main.route('/atualizacoes')
def atualizacoes():
    return render_template('atualizacoes.html')
