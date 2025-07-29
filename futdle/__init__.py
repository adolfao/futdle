from flask import Flask
import os
import sqlite3

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///futdle.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "chave-secreta-temporaria-para-desenvolvimento"

    #funcao auxiliar para comparar cores no template jinja
    def comparar_cores_jinja(cores1, cores2):
        if cores1 == cores2:
            return "exato"
        
        cores1_list = [c.strip().lower() for c in cores1.replace(' e ', ',').split(',')]
        cores2_list = [c.strip().lower() for c in cores2.replace(' e ', ',').split(',')]
        
        for cor1 in cores1_list:
            for cor2 in cores2_list:
                if cor1 == cor2:
                    return "parcial"
        
        return "diferente"

    #funcao auxiliar para comparar anos e mostrar setas no template
    def comparar_anos_jinja(ano_chute, ano_secreto):
        if ano_chute == ano_secreto:
            return "correto"
        elif ano_chute < ano_secreto:
            return "seta_cima"
        else:
            return "seta_baixo"

    #registra funcoes no contexto global do jinja
    app.jinja_env.globals.update(comparar_cores=comparar_cores_jinja)
    app.jinja_env.globals.update(comparar_anos=comparar_anos_jinja)

    from futdle.routes import main
    app.register_blueprint(main)

    return app
