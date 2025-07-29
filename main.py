from futdle import create_app

app = create_app()

#ponto de entrada principal da aplicacao
if __name__ == '__main__':
    print("Iniciando servidor Futdle...")
    print("Acesse: http://localhost:5000")
    print("Modo Classico: http://localhost:5000/classico")
    print("Para parar: Ctrl+C")
    app.run(debug=True, host='0.0.0.0', port=5000)