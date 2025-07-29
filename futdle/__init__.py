from flask import Flask
import os

def create_app():
    """
    Factory function para criar instância da aplicação Flask.
    Configura banco de dados, chave secreta, popula dados e registra blueprints.
    
    Returns:
        Flask: Instância configurada da aplicação
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///futdle.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configura chave secreta do Flask
    _configure_secret_key(app)
    
    # Inicializa banco de dados
    _initialize_database()
    
    # Registra funções auxiliares no Jinja
    _register_jinja_functions(app)
    
    # Registra blueprints
    from futdle.routes import main
    app.register_blueprint(main)
    
    return app

def _configure_secret_key(app):
    """Configura chave secreta com fallback para desenvolvimento."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        app.secret_key = os.getenv('SECRET_KEY', 'chave-secreta-temporaria-para-desenvolvimento')
    except ImportError:
        app.secret_key = "chave-secreta-temporaria-para-desenvolvimento"

def _initialize_database():
    """Popula banco de dados com times brasileiros."""
    try:
        from popular_db import popular_times
        popular_times()
    except Exception as e:
        print(f"⚠️  Erro ao popular banco: {e}")
        print("ℹ️  Execute 'python popular_db.py' manualmente para popular o banco")

def _register_jinja_functions(app):
    """Registra funções auxiliares no contexto global do Jinja."""
    
    def comparar_cores_jinja(cores1, cores2):
        """
        Compara cores dos times para feedback visual.
        
        Args:
            cores1, cores2 (str): Strings com cores separadas por vírgula
            
        Returns:
            str: 'exato', 'parcial' ou 'diferente'
        """
        if cores1 == cores2:
            return "exato"
        
        # Normaliza as cores separando e ordenando alfabeticamente
        cores1_list = sorted([c.strip().lower() for c in cores1.replace(' e ', ',').split(',')])
        cores2_list = sorted([c.strip().lower() for c in cores2.replace(' e ', ',').split(',')])
        
        # Se os conjuntos ordenados são iguais, é exato
        if cores1_list == cores2_list:
            return "exato"
        
        # Verifica se há alguma cor em comum
        for cor1 in cores1_list:
            for cor2 in cores2_list:
                if cor1 == cor2:
                    return "parcial"
        
        return "diferente"

    def comparar_anos_jinja(ano_chute, ano_secreto):
        """
        Compara anos de fundação e retorna direção da seta.
        
        Args:
            ano_chute, ano_secreto (int): Anos a serem comparados
            
        Returns:
            str: 'correto', 'seta_cima' ou 'seta_baixo'
        """
        if ano_chute == ano_secreto:
            return "correto"
        elif ano_chute < ano_secreto:
            return "seta_cima"
        else:
            return "seta_baixo"

    # Registra funções no contexto global do Jinja
    app.jinja_env.globals.update(comparar_cores=comparar_cores_jinja)
    app.jinja_env.globals.update(comparar_anos=comparar_anos_jinja)
