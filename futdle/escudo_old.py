from flask import render_template, request, session, jsonify
from futdle.models import Time
import random
import os

def escudo_mode():
    """
    Modo escudo - jogador deve adivinhar o time baseado apenas no escudo.
    """
    # Lista de times disponíveis com escudos
    times_com_escudo = [
        "vascodagama",
        "flamengo", 
        "corinthians",
        "palmeiras",
        "saopaulo"
    ]
    
    # Inicializa o jogo se não existir na sessão
    if 'escudo_game' not in session:
        time_secreto_nome = random.choice(times_com_escudo)
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
            print(f"[DEBUG] Chute recebido: '{chute}'")
            
            if not chute:
                return jsonify({'sucesso': False, 'mensagem': 'Digite o nome de um time!'})
            
            # Busca o time no banco de dados
            time_chutado = Time.query.filter(Time.nome.ilike(f'%{chute}%')).first()
            print(f"[DEBUG] Time encontrado: {time_chutado.nome if time_chutado else 'Nenhum'}")
            
            if not time_chutado:
                return jsonify({'sucesso': False, 'mensagem': 'Time não encontrado!'})
            
            print(f"[DEBUG] Time secreto: {game_data['time_secreto']}")
            print(f"[DEBUG] Comparando: '{time_chutado.nome.lower().replace(' ', '')}' com '{game_data['time_secreto'].lower()}'")
            
            # Verifica se acertou (comparação mais flexível)
            time_secreto_normalizado = game_data['time_secreto'].lower()
            time_chutado_normalizado = time_chutado.nome.lower().replace(' ', '').replace('-', '')
            
            if (time_secreto_normalizado in time_chutado_normalizado or 
                time_chutado_normalizado in time_secreto_normalizado):
                game_data['jogo_finalizado'] = True
                session['escudo_game'] = game_data
                return jsonify({'sucesso': True, 'mensagem': 'Parabéns! Você acertou!'})
            else:
                # Adiciona tentativa errada
                game_data['tentativas_erradas'] += 1
                if time_chutado.nome not in [t['nome'] for t in game_data['tentativas']]:
                    game_data['tentativas'].append({
                        'nome': time_chutado.nome,
                        'escudo': time_chutado.escudo
                    })
                
                session['escudo_game'] = game_data
                return jsonify({
                    'sucesso': False, 
                    'mensagem': f'Não é {time_chutado.nome}. Tente novamente!',
                    'tentativas_erradas': game_data['tentativas_erradas'],
                    'time_chutado': {
                        'nome': time_chutado.nome,
                        'escudo': time_chutado.escudo
                    }
                })
                
        except Exception as e:
            print(f"[ERROR] Erro no processamento: {e}")
            return jsonify({'sucesso': False, 'mensagem': f'Erro interno: {str(e)}'})
    
    # Renderiza o template do modo escudo
    return render_template('escudo.html', 
                         jogo_finalizado=game_data['jogo_finalizado'],
                         time_secreto_nome=game_data['time_secreto'],
                         tentativas_erradas=game_data['tentativas_erradas'],
                         tentativas=game_data['tentativas'])