from futdle import create_app
from futdle.config import HOST_DEFAULT, PORT_DEFAULT, DEBUG_DEFAULT, MENSAGENS

app = create_app()

# Ponto de entrada principal da aplicação
if __name__ == '__main__':
    print(MENSAGENS['servidor_iniciando'])
    print(MENSAGENS['servidor_url'].format(port=PORT_DEFAULT))
    print(MENSAGENS['servidor_classico'].format(port=PORT_DEFAULT))
    print(MENSAGENS['servidor_parar'])
    app.run(debug=DEBUG_DEFAULT, host=HOST_DEFAULT, port=PORT_DEFAULT)