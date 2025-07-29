#para rodar manualmente: py -m futdle.tests_db.tests

from futdle import create_app, db
from futdle.models import Time

def popular_times():
    times_dados = [
        {"nome": "Atlético Mineiro", "cores": "Preto e Branco", "estado": "MG", "ano_fundacao": 1908, "serie": "A"},
        {"nome": "Bahia", "cores": "Azul, Vermelho e Branco", "estado": "BA", "ano_fundacao": 1931, "serie": "A"},
        {"nome": "Botafogo", "cores": "Preto e Branco", "estado": "RJ", "ano_fundacao": 1904, "serie": "A"},
        {"nome": "Bragantino", "cores": "Branco e Vermelho", "estado": "SP", "ano_fundacao": 1928, "serie": "A"},
        {"nome": "Ceará", "cores": "Preto e Branco", "estado": "CE", "ano_fundacao": 1914, "serie": "A"},
        {"nome": "Corinthians", "cores": "Preto e Branco", "estado": "SP", "ano_fundacao": 1910, "serie": "A"},
        {"nome": "Cruzeiro", "cores": "Azul e Branco", "estado": "MG", "ano_fundacao": 1921, "serie": "A"},
        {"nome": "Flamengo", "cores": "Vermelho e Preto", "estado": "RJ", "ano_fundacao": 1895, "serie": "A"},
        {"nome": "Fluminense", "cores": "Verde, Vermelho e Branco", "estado": "RJ", "ano_fundacao": 1902, "serie": "A"},
        {"nome": "Fortaleza", "cores": "Azul, Vermelho e Branco", "estado": "CE", "ano_fundacao": 1918, "serie": "A"},
        {"nome": "Grêmio", "cores": "Azul, Preto e Branco", "estado": "RS", "ano_fundacao": 1903, "serie": "A"},
        {"nome": "Internacional", "cores": "Vermelho e Branco", "estado": "RS", "ano_fundacao": 1909, "serie": "A"},
        {"nome": "Juventude", "cores": "Verde e Branco", "estado": "RS", "ano_fundacao": 1913, "serie": "A"},
        {"nome": "Mirassol", "cores": "Amarelo e Verde", "estado": "SP", "ano_fundacao": 1925, "serie": "A"},
        {"nome": "Palmeiras", "cores": "Verde e Branco", "estado": "SP", "ano_fundacao": 1914, "serie": "A"},
        {"nome": "Santos", "cores": "Branco e Preto", "estado": "SP", "ano_fundacao": 1912, "serie": "A"},
        {"nome": "São Paulo", "cores": "Branco, Vermelho e Preto", "estado": "SP", "ano_fundacao": 1930, "serie": "A"},
        {"nome": "Sport", "cores": "Vermelho e Preto", "estado": "PE", "ano_fundacao": 1905, "serie": "A"},
        {"nome": "Vasco da Gama", "cores": "Preto e Branco", "estado": "RJ", "ano_fundacao": 1898, "serie": "A"},
        {"nome": "Vitória", "cores": "Vermelho e Preto", "estado": "BA", "ano_fundacao": 1899, "serie": "A"},
        {"nome": "Goiás", "cores": "Verde e Branco", "estado": "GO", "ano_fundacao": 1943, "serie": "B"},
    {"nome": "Coritiba", "cores": "Verde e Branco", "estado": "PR", "ano_fundacao": 1909, "serie": "B"},
    {"nome": "Novorizontino", "cores": "Amarelo e Preto", "estado": "SP", "ano_fundacao": 2010, "serie": "B"},
    {"nome": "Chapecoense", "cores": "Verde e Branco", "estado": "SC", "ano_fundacao": 1973, "serie": "B"},
    {"nome": "Remo", "cores": "Azul e Branco", "estado": "PA", "ano_fundacao": 1905, "serie": "B"},
    {"nome": "Cuiabá", "cores": "Verde e Amarelo", "estado": "MT", "ano_fundacao": 2001, "serie": "B"},
    {"nome": "Avaí", "cores": "Azul e Branco", "estado": "SC", "ano_fundacao": 1923, "serie": "B"},
    {"nome": "Vila Nova", "cores": "Vermelho e Branco", "estado": "GO", "ano_fundacao": 1943, "serie": "B"},
    {"nome": "Criciúma", "cores": "Amarelo, Preto e Branco", "estado": "SC", "ano_fundacao": 1947, "serie": "B"},
    {"nome": "CRB", "cores": "Vermelho e Branco", "estado": "AL", "ano_fundacao": 1912, "serie": "B"},
    {"nome": "Athletico-PR", "cores": "Vermelho e Preto", "estado": "PR", "ano_fundacao": 1924, "serie": "B"},
    {"nome": "Operário", "cores": "Preto e Branco", "estado": "PR", "ano_fundacao": 1912, "serie": "B"},
    {"nome": "Atlético-GO", "cores": "Vermelho e Preto", "estado": "GO", "ano_fundacao": 1937, "serie": "B"},
    {"nome": "Athletic", "cores": "Preto e Branco", "estado": "MG", "ano_fundacao": 1909, "serie": "B"},
    {"nome": "América-MG", "cores": "Verde e Branco", "estado": "MG", "ano_fundacao": 1912, "serie": "B"},
    {"nome": "Volta Redonda", "cores": "Amarelo e Preto", "estado": "RJ", "ano_fundacao": 1976, "serie": "B"},
    {"nome": "Ferroviária", "cores": "Grená e Branco", "estado": "SP", "ano_fundacao": 1950, "serie": "B"},
    {"nome": "Paysandu", "cores": "Azul e Branco", "estado": "PA", "ano_fundacao": 1914, "serie": "B"},
    {"nome": "Amazonas", "cores": "Amarelo e Preto", "estado": "AM", "ano_fundacao": 2019, "serie": "B"},
    {"nome": "Botafogo-SP", "cores": "Vermelho, Preto e Branco", "estado": "SP", "ano_fundacao": 1918, "serie": "B"},
    {"nome": "Caxias", "cores": "Grená e Branco", "estado": "RS", "ano_fundacao": 1935, "serie": "C"},
    {"nome": "Ponte Preta", "cores": "Preto e Branco", "estado": "SP", "ano_fundacao": 1900, "serie": "C"},
    {"nome": "Londrina", "cores": "Azul Celeste e Branco", "estado": "PR", "ano_fundacao": 1956, "serie": "C"},
    {"nome": "Náutico", "cores": "Vermelho e Branco", "estado": "PE", "ano_fundacao": 1901, "serie": "C"},
    {"nome": "São Bernardo", "cores": "Amarelo e Preto", "estado": "SP", "ano_fundacao": 2004, "serie": "C"},
    {"nome": "Ypiranga", "cores": "Verde e Amarelo", "estado": "RS", "ano_fundacao": 1924, "serie": "C"},
    {"nome": "Floresta", "cores": "Verde e Branco", "estado": "CE", "ano_fundacao": 1954, "serie": "C"},
    {"nome": "Botafogo-PB", "cores": "Preto, Vermelho e Branco", "estado": "PB", "ano_fundacao": 1931, "serie": "C"},
    {"nome": "Brusque", "cores": "Amarelo, Verde e Vermelho", "estado": "SC", "ano_fundacao": 1987, "serie": "C"},
    {"nome": "CSA", "cores": "Azul e Branco", "estado": "AL", "ano_fundacao": 1913, "serie": "C"},
    {"nome": "Ituano", "cores": "Preto e Vermelho", "estado": "SP", "ano_fundacao": 1947, "serie": "C"},
    {"nome": "Guarani", "cores": "Verde e Branco", "estado": "SP", "ano_fundacao": 1911, "serie": "C"},
    {"nome": "Maringá", "cores": "Preto e Branco", "estado": "PR", "ano_fundacao": 2010, "serie": "C"},
    {"nome": "Anápolis", "cores": "Vermelho e Branco", "estado": "GO", "ano_fundacao": 1946, "serie": "C"},
    {"nome": "ABC", "cores": "Preto e Branco", "estado": "RN", "ano_fundacao": 1915, "serie": "C"},
    {"nome": "Figueirense", "cores": "Preto e Branco", "estado": "SC", "ano_fundacao": 1921, "serie": "C"},
    {"nome": "Itabaiana", "cores": "Vermelho, Azul e Branco", "estado": "SE", "ano_fundacao": 1938, "serie": "C"},
    {"nome": "Confiança", "cores": "Azul e Branco", "estado": "SE", "ano_fundacao": 1936, "serie": "C"},
    {"nome": "Retrô", "cores": "Azul e Dourado", "estado": "PE", "ano_fundacao": 2016, "serie": "C"},
    {"nome": "Tombense", "cores": "Vermelho e Branco", "estado": "MG", "ano_fundacao": 1914, "serie": "C"}
    ]
    adicionados = 0
    for dado in times_dados:
        if not Time.query.filter_by(nome=dado["nome"]).first():
            db.session.add(Time(**dado))
            adicionados += 1
    db.session.commit()
    print(f"{adicionados} times adicionados com sucesso!")

def popular_se_vazio():
    if not Time.query.first():
        popular_times()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        popular_se_vazio()
