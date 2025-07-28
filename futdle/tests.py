from futdle import create_app, db
from futdle.models import Time
#python -m futdle.tests

app = create_app()

with app.app_context():
    times_dados = [
        {"nome": "Cruzeiro", "cores": "Azul e Branco", "estado": "MG", "ano_fundacao": 1921},
        {"nome": "Santos", "cores": "Branco e Preto", "estado": "SP", "ano_fundacao": 1912},
        {"nome": "Palmeiras", "cores": "Verde e Branco", "estado": "SP", "ano_fundacao": 1914},
        {"nome": "Corinthians", "cores": "Preto e Branco", "estado": "SP", "ano_fundacao": 1910},
        {"nome": "Flamengo", "cores": "Vermelho e Preto", "estado": "RJ", "ano_fundacao": 1895},
    ]

    adicionados = 0
    for dado in times_dados:
        existente = Time.query.filter_by(nome=dado["nome"]).first()
        if not existente:
            novo_time = Time(**dado) 
            db.session.add(novo_time)
            adicionados += 1

    db.session.commit()
    print(f"{adicionados} times adicionados com sucesso!")
    print(Time.query.all())
