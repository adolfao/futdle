"""
Configurações centralizadas do projeto Futdle.

Este arquivo contém todas as constantes e configurações utilizadas
em diferentes partes da aplicação, facilitando manutenção e modificações.
"""

import os

# === CONFIGURAÇÕES DO BANCO DE DADOS ===
DB_NAME = 'futdle.db'
DB_PATH = os.path.join('futdle', DB_NAME)

# === CONFIGURAÇÕES DO JOGO ===
# Número de tentativas erradas para mostrar dicas
TENTATIVAS_PARA_DICA_SERIE = 4
TENTATIVAS_PARA_DICA_MASCOTE = 7

# Limite de sugestões no autocomplete
LIMITE_SUGESTOES_AUTOCOMPLETE = 5

# === CONFIGURAÇÕES DA APLICAÇÃO ===
# Configuração padrão para desenvolvimento
SECRET_KEY_DEFAULT = "chave-secreta-temporaria-para-desenvolvimento"

# Configurações do servidor
HOST_DEFAULT = '0.0.0.0'
PORT_DEFAULT = 5000
DEBUG_DEFAULT = True

# === MENSAGENS DO SISTEMA ===
MENSAGENS = {
    'time_nao_encontrado': "Time não encontrado!",
    'time_ja_tentado': "Você já digitou esse time!",
    'acertou': "Acertou!",
    'errou': "Errou!",
    'banco_erro': "⚠️  Erro ao popular banco: {error}",
    'banco_instrucao': "ℹ️  Execute 'python popular_db.py' manualmente para popular o banco",
    'servidor_iniciando': "🚀 Iniciando servidor Futdle...",
    'servidor_url': "🌐 Acesse: http://localhost:{port}",
    'servidor_classico': "⚽ Modo Clássico: http://localhost:{port}/classico",
    'servidor_parar': "🛑 Para parar: Ctrl+C"
}

# === VALIDAÇÕES ===
# Tamanho mínimo para busca de sugestões
TAMANHO_MINIMO_BUSCA = 1

# === COLUNAS DO BANCO ===
COLUNAS_TIME_SQL = "id, nome, cores, estado, ano_fundacao, serie, mascote"
