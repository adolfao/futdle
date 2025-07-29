from flask import render_template, request, session
from futdle.models import Time, normalizar_nome
import random

def comparar_cores(cores1, cores2):
    """Compara cores dos times e retorna 'exato', 'parcial' ou 'diferente'."""
    if cores1 == cores2:
        return "exato"
    
    # Normaliza as cores separando e ordenando alfabeticamente
    cores1_list = sorted([c.strip().lower() for c in cores1.replace(' e ', ',').split(',')])
    cores2_list = sorted([c.strip().lower() for c in cores2.replace(' e ', ',').split(',')])
    
    # Se os conjuntos ordenados são iguais, é exato
    if cores1_list == cores2_list:
        return "exato"
    
    # Verifica se há alguma cor em comum
    if any(cor1 == cor2 for cor1 in cores1_list for cor2 in cores2_list):
        return "parcial"
    
    return "diferente"

def buscar_time_por_nome(chute):
    """Busca time usando normalização de nome."""
    return Time.buscar_por_nome_normalizado(chute)

def inicializar_jogo():
    """Inicializa novo jogo se não existe ou retorna time secreto atual."""
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

def classico_mode():
    """Função principal do modo clássico."""
    time_secreto = inicializar_jogo()
    jogo_finalizado = session.get("jogo_finalizado", False)
    tentativas_nomes = session.get("tentativas", [])
    tentativas_erradas = session.get("tentativas_erradas", 0)
    
    # Define quais dicas mostrar baseado no número de erros
    mostrar_dica_serie = tentativas_erradas >= 4
    mostrar_dica_mascote = tentativas_erradas >= 7
    
    # Converte nomes das tentativas em objetos Time
    tentativas_objetos = [Time.get_by_nome(nome) for nome in tentativas_nomes if Time.get_by_nome(nome)]

    resultado = None
    if request.method == "POST":
        resultado = processar_chute(tentativas_nomes, tentativas_objetos, time_secreto)
        # Atualiza contadores após processamento
        tentativas_erradas = session.get("tentativas_erradas", 0)
        mostrar_dica_serie = tentativas_erradas >= 4
        mostrar_dica_mascote = tentativas_erradas >= 7

    return render_template("classico.html", 
                         resultado=resultado, 
                         tentativas=tentativas_objetos, 
                         time_secreto=time_secreto, 
                         jogo_finalizado=jogo_finalizado,
                         tentativas_erradas=tentativas_erradas,
                         mostrar_dica_serie=mostrar_dica_serie,
                         mostrar_dica_mascote=mostrar_dica_mascote,
                         comparar_cores=comparar_cores)

def processar_chute(tentativas_nomes, tentativas_objetos, time_secreto):
    """Processa tentativa do usuário e atualiza estado do jogo."""
    chute = request.form.get("chute", "").strip()
    time_chutado = buscar_time_por_nome(chute)

    if not time_chutado:
        return "Time não encontrado!"
    
    if time_chutado.nome in tentativas_nomes:
        return "Você já digitou esse time!"

    # Adiciona tentativa às listas
    tentativas_nomes.append(time_chutado.nome)
    tentativas_objetos.append(time_chutado)
    session["tentativas"] = tentativas_nomes

    # Verifica se acertou
    if time_chutado.id == time_secreto.id:
        session["jogo_finalizado"] = True
        return "Acertou!"
    else:
        # Incrementa contador de erros
        tentativas_erradas = session.get("tentativas_erradas", 0) + 1
        session["tentativas_erradas"] = tentativas_erradas
        return "Errou!"
