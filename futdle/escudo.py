from flask import render_template, request, session, jsonify
from futdle.models import Time
import random
import os

def escudo_mode():
    """
    Modo escudo - jogador deve adivinhar o time baseado apenas no escudo.
    """
    # Busca todos os times da Série A do banco de dados
    times_serie_a = Time.buscar_por_serie('A')
    
    # Converte os nomes dos times para o formato usado nos arquivos (sem espaços, minúsculo)
    times_com_escudo = []
    for time in times_serie_a:
        nome_arquivo = time.nome_arquivo()
        times_com_escudo.append(nome_arquivo)
    
    # Verifica quais arquivos de escudo realmente existem na pasta times_escudo
    pasta_escudos = os.path.join('futdle', 'static', 'times_escudo')
    times_disponveis = []
    
    for time_nome in times_com_escudo:
        arquivo_escudo = f"{time_nome}_escudo.png"
        caminho_completo = os.path.join(pasta_escudos, arquivo_escudo)
        if os.path.exists(caminho_completo):
            times_disponveis.append(time_nome)
    
    # Se nenhum arquivo foi encontrado, usa apenas vascodagama como fallback
    if not times_disponveis:
        times_disponveis = ["vascodagama"]
    
    # Inicializa o jogo se não existir na sessão
    if 'escudo_game' not in session:
        time_secreto_nome = random.choice(times_disponveis)
        session['escudo_game'] = {
            'time_secreto': time_secreto_nome,
            'tentativas_erradas': 0,
            'jogo_finalizado': False,
            'tentativas': []
        }
    
    game_data = session['escudo_game']
    
    # Se for GET e o jogo estiver finalizado, inicia uma nova rodada
    if request.method == 'GET' and game_data.get('jogo_finalizado', False):
        time_secreto_nome = random.choice(times_disponveis)
        session['escudo_game'] = {
            'time_secreto': time_secreto_nome,
            'tentativas_erradas': 0,
            'jogo_finalizado': False,
            'tentativas': []
        }
        game_data = session['escudo_game']
    
    # Se for POST, processa o chute
    if request.method == 'POST':
        try:
            chute = request.form.get('chute', '').strip()
            
            if not chute:
                return jsonify({'sucesso': False, 'mensagem': 'Digite o nome de um time!'})
            
            # Busca o time no banco de dados
            time_chutado = Time.buscar_por_nome_normalizado(chute)
            
            if not time_chutado:
                return jsonify({'sucesso': False, 'mensagem': 'Time não encontrado!'})
            
            # Verifica se o time já foi tentado
            times_ja_tentados = [t['nome'] for t in game_data['tentativas']]
            if time_chutado.nome in times_ja_tentados:
                return jsonify({'sucesso': False, 'mensagem': f'{time_chutado.nome} já foi tentado!'})
            
            # Verifica se acertou - busca o time secreto pelo nome do arquivo
            time_secreto_nome_arquivo = game_data['time_secreto']
            
            # Encontra o time secreto no banco usando o nome do arquivo
            time_secreto_obj = None
            for time in Time.buscar_por_serie('A'):
                if time.nome_arquivo() == time_secreto_nome_arquivo:
                    time_secreto_obj = time
                    break
            
            if time_secreto_obj:
                # Compara os nomes normalizados (sem acentos)
                from futdle.models import normalizar_nome
                time_secreto_normalizado = normalizar_nome(time_secreto_obj.nome)
                time_chutado_normalizado = normalizar_nome(time_chutado.nome)
                
                if time_secreto_normalizado == time_chutado_normalizado:
                    game_data['jogo_finalizado'] = True
                    session['escudo_game'] = game_data
                    return jsonify({'sucesso': True, 'mensagem': 'Parabéns! Você acertou!'})
            
            # Se não acertou, adiciona tentativa errada
                game_data['tentativas_erradas'] += 1
                game_data['tentativas'].append({
                    'nome': time_chutado.nome,
                    'escudo': time_chutado.nome_arquivo() + '.jpg'
                })
                
                session['escudo_game'] = game_data
                return jsonify({
                    'sucesso': False, 
                    'mensagem': f'Não é {time_chutado.nome}. Tente novamente!',
                    'tentativas_erradas': game_data['tentativas_erradas'],
                    'time_chutado': {
                        'nome': time_chutado.nome,
                        'escudo': time_chutado.nome_arquivo() + '.jpg'
                    }
                })
                
        except Exception as e:
            return jsonify({'sucesso': False, 'mensagem': f'Erro interno: {str(e)}'})
    
    # Renderiza o template do modo escudo
    return render_template('escudo.html', 
                         jogo_finalizado=game_data['jogo_finalizado'],
                         time_secreto_nome=game_data['time_secreto'],
                         tentativas_erradas=game_data['tentativas_erradas'],
                         tentativas=game_data['tentativas'])
