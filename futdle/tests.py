from . import create_app, db
from .models import Time

app = create_app()

with app.app_context():
    times = [
        Time(nome="Cruzeiro", cores="Azul e Branco", estado="MG", ano_fundacao=1921),
        Time(nome="Santos", cores="Branco e Preto", estado="SP", ano_fundacao=1912),
        Time(nome="Palmeiras", cores="Verde e Branco", estado="SP", ano_fundacao=1914),
        Time(nome="Corinthians", cores="Preto e Branco", estado="SP", ano_fundacao=1910),
        Time(nome="Flamengo", cores="Vermelho e Preto", estado="RJ", ano_fundacao=1895),
    ]

    adicionados = 0
    for dado in times:
        existente = Time.query.filter_by(nome=dado["nome"]).first()
        if not existente:
            novo_time = Time(**dado)
            db.session.add(novo_time)
            adicionados += 1
    
    db.session.commit()
    print("Times adicionados com sucesso!")
    print(Time.query.all())