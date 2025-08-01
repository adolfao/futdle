from flask import Flask
import os
from futdle.config import SECRET_KEY_DEFAULT, MENSAGENS
from futdle.sitemap import sitemap_bp


def create_app():
    """Factory function para criar instância da aplicação Flask."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///futdle.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
    # Configura chave secreta do Flask
    _configure_secret_key(app)
    
    app.register_blueprint(sitemap_bp)
    
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
        app.secret_key = os.getenv('SECRET_KEY', SECRET_KEY_DEFAULT)
    except ImportError:
        app.secret_key = SECRET_KEY_DEFAULT

def _initialize_database():
    """Popula banco de dados com times brasileiros."""
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
        from populate_db import popular_banco
        popular_banco()
    except Exception as e:
        print(MENSAGENS['banco_erro'].format(error=e))
        print(MENSAGENS['banco_instrucao'])

def _register_jinja_functions(app):
    """Registra funções auxiliares no contexto global do Jinja."""
    
    def comparar_cores_jinja(cores1, cores2):
        """Compara cores dos times para feedback visual."""
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
        """Compara anos de fundação e retorna direção da seta."""
        if ano_chute == ano_secreto:
            return "correto"
        elif ano_chute < ano_secreto:
            return "seta_cima"
        else:
            return "seta_baixo"

    # Registra funções no contexto global do Jinja
    app.jinja_env.globals.update(comparar_cores=comparar_cores_jinja)
    app.jinja_env.globals.update(comparar_anos=comparar_anos_jinja)
