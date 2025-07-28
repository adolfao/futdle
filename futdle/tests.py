from futdle import create_app, db
from futdle.models import Time

#py -m futdle.tests
app = create_app()

with app.app_context():
  times_dados = [
    {"nome": "Atlético Mineiro", "cores": "Preto e Branco", "estado": "MG", "ano_fundacao": 1908},
    {"nome": "Bahia", "cores": "Azul, Vermelho e Branco", "estado": "BA", "ano_fundacao": 1931},
    {"nome": "Botafogo", "cores": "Preto e Branco", "estado": "RJ", "ano_fundacao": 1904},
    {"nome": "Bragantino", "cores": "Branco e Vermelho", "estado": "SP", "ano_fundacao": 1928},
    {"nome": "Ceará", "cores": "Preto e Branco", "estado": "CE", "ano_fundacao": 1914},
    {"nome": "Corinthians", "cores": "Preto e Branco", "estado": "SP", "ano_fundacao": 1910},
    {"nome": "Cruzeiro", "cores": "Azul e Branco", "estado": "MG", "ano_fundacao": 1921},
    {"nome": "Flamengo", "cores": "Vermelho e Preto", "estado": "RJ", "ano_fundacao": 1895},
    {"nome": "Fluminense", "cores": "Verde, Grená e Branco", "estado": "RJ", "ano_fundacao": 1902},
    {"nome": "Fortaleza", "cores": "Azul, Vermelho e Branco", "estado": "CE", "ano_fundacao": 1918},
    {"nome": "Grêmio", "cores": "Azul, Preto e Branco", "estado": "RS", "ano_fundacao": 1903},
    {"nome": "Internacional", "cores": "Vermelho e Branco", "estado": "RS", "ano_fundacao": 1909},
    {"nome": "Juventude", "cores": "Verde e Branco", "estado": "RS", "ano_fundacao": 1913},
    {"nome": "Mirassol", "cores": "Amarelo e Verde", "estado": "SP", "ano_fundacao": 1925},
    {"nome": "Palmeiras", "cores": "Verde e Branco", "estado": "SP", "ano_fundacao": 1914},
    {"nome": "Santos", "cores": "Branco e Preto", "estado": "SP", "ano_fundacao": 1912},
    {"nome": "São Paulo", "cores": "Branco, Vermelho e Preto", "estado": "SP", "ano_fundacao": 1930},
    {"nome": "Sport", "cores": "Vermelho e Preto", "estado": "PE", "ano_fundacao": 1905},
    {"nome": "Vasco da Gama", "cores": "Preto e Branco", "estado": "RJ", "ano_fundacao": 1898},
    {"nome": "Vitória", "cores": "Vermelho e Preto", "estado": "BA", "ano_fundacao": 1899},
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
