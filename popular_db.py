import sqlite3
import os
from futdle.config import DB_PATH

def popular_times():
    """Popula banco de dados com times brasileiros das séries A, B e C."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Cria tabela se não existir
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS times (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        cores TEXT NOT NULL,
        estado TEXT NOT NULL,
        ano_fundacao INTEGER NOT NULL,
        serie TEXT NOT NULL DEFAULT 'A',
        mascote TEXT
    )
    ''')

    # Dados dos times brasileiros organizados por série
    times_dados = [
        ("Atlético Mineiro", "Preto e Branco", "MG", 1908, "A", "Galo"),
        ("Bahia", "Azul, Vermelho e Branco", "BA", 1931, "A", "Super-Homem Tricolor"),
        ("Botafogo", "Preto e Branco", "RJ", 1904, "A", "Manequinho"),
        ("Bragantino", "Branco e Vermelho", "SP", 1928, "A", "Toro Loko"),
        ("Ceará", "Preto e Branco", "CE", 1914, "A", "Vozão"),
        ("Corinthians", "Preto e Branco", "SP", 1910, "A", "Mosqueteiro"),
        ("Cruzeiro", "Azul e Branco", "MG", 1921, "A", "Raposa"),
        ("Flamengo", "Vermelho e Preto", "RJ", 1895, "A", "Urubu"),
        ("Fluminense", "Verde, Vermelho e Branco", "RJ", 1902, "A", "Guerreiro Tricolor"),
        ("Fortaleza", "Azul, Vermelho e Branco", "CE", 1918, "A", "Leão"),
        ("Grêmio", "Azul, Preto e Branco", "RS", 1903, "A", "Mosqueteiro"),
        ("Internacional", "Vermelho e Branco", "RS", 1909, "A", "Saci"),
        ("Juventude", "Verde e Branco", "RS", 1913, "A", "Juju"),
        ("Mirassol", "Amarelo e Verde", "SP", 1925, "A", "Leão"),
        ("Palmeiras", "Verde e Branco", "SP", 1914, "A", "Porco Gobbato"),
        ("Santos", "Branco e Preto", "SP", 1912, "A", "Baleia"),
        ("São Paulo", "Branco, Vermelho e Preto", "SP", 1930, "A", "Santo Paulo"),
        ("Sport", "Vermelho e Preto", "PE", 1905, "A", "Leão"),
        ("Vasco da Gama", "Preto e Branco", "RJ", 1898, "A", "Almirante"),
        ("Vitória", "Vermelho e Preto", "BA", 1899, "A", "Leão"),
        ("Goiás", "Verde e Branco", "GO", 1943, "B", "Periquito"),
        ("Coritiba", "Verde e Branco", "PR", 1909, "B", "Vovô Coxa"),
        ("Novorizontino", "Amarelo e Preto", "SP", 2010, "B", "Tigre"),
        ("Chapecoense", "Verde e Branco", "SC", 1973, "B", "Índio Condá"),
        ("Remo", "Azul e Branco", "PA", 1905, "B", "Leão Azul"),
        ("Cuiabá", "Verde e Amarelo", "MT", 2001, "B", "Periquito"),
        ("Avaí", "Azul e Branco", "SC", 1923, "B", "Leão da Ilha"),
        ("Vila Nova", "Vermelho e Branco", "GO", 1943, "B", "Tigre"),
        ("Criciúma", "Amarelo, Preto e Branco", "SC", 1947, "B", "Tigrão"),
        ("CRB", "Vermelho e Branco", "AL", 1912, "B", "Galo de Campina"),
        ("Athletico-PR", "Vermelho e Preto", "PR", 1924, "B", "Furacão"),
        ("Operário", "Preto e Branco", "PR", 1912, "B", "Fantasma"),
        ("Atlético-GO", "Vermelho e Preto", "GO", 1937, "B", "Dragão"),
        ("Athletic", "Preto e Branco", "MG", 1909, "B", "Elefante"),
        ("América-MG", "Verde e Branco", "MG", 1912, "B", "Coelho"),
        ("Volta Redonda", "Amarelo e Preto", "RJ", 1976, "B", "Volty"),
        ("Ferroviária", "Vermelho e Branco", "SP", 1950, "B", "Locomotiva"),
        ("Paysandu", "Azul e Branco", "PA", 1914, "B", "Papão da Curuzu"),
        ("Amazonas", "Amarelo e Preto", "AM", 2019, "B", "Onça-Pintada"),
        ("Botafogo-SP", "Vermelho, Preto e Branco", "SP", 1918, "B", "Pantera"),
        ("Caxias", "Vermelho e Branco", "RS", 1935, "C", "Grená"),
        ("Ponte Preta", "Preto e Branco", "SP", 1900, "C", "Macaca"),
        ("Londrina", "Azul e Branco", "PR", 1956, "C", "Tubarão"),
        ("Náutico", "Vermelho e Branco", "PE", 1901, "C", "Timbu"),
        ("São Bernardo", "Amarelo e Preto", "SP", 2004, "C", "Cachorrão"),
        ("Ypiranga", "Verde e Amarelo", "RS", 1924, "C", "Canarinho"),
        ("Floresta", "Verde e Branco", "CE", 1954, "C", "Lobo"),
        ("Botafogo-PB", "Preto, Vermelho e Branco", "PB", 1931, "C", "Belo"),
        ("Brusque", "Amarelo, Verde e Vermelho", "SC", 1987, "C", "Quadricolor"),
        ("CSA", "Azul e Branco", "AL", 1913, "C", "Azulão"),
        ("Ituano", "Preto e Vermelho", "SP", 1947, "C", "Galo de Itu"),
        ("Guarani", "Verde e Branco", "SP", 1911, "C", "Bugre"),
        ("Maringá", "Preto e Branco", "PR", 2010, "C", "Dogão"),
        ("Anápolis", "Vermelho e Branco", "GO", 1946, "C", "Galo da Comarca"),
        ("ABC", "Preto e Branco", "RN", 1915, "C", "Elefante"),
        ("Figueirense", "Preto e Branco", "SC", 1921, "C", "Figueira"),
        ("Itabaiana", "Vermelho, Azul e Branco", "SE", 1938, "C", "Tremendão"),
        ("Confiança", "Azul e Branco", "SE", 1936, "C", "Dragão do Bairro Industrial"),
        ("Retrô", "Azul e Dourado", "PE", 2016, "C", "Águia Dourada"),
        ("Tombense", "Vermelho e Branco", "MG", 1914, "C", "Gavião-Carcará")
    ]

    cursor.execute("SELECT COUNT(*) FROM times")
    count = cursor.fetchone()[0]

    # Só insere se banco estiver vazio
    if count == 0:
        print("📊 Inserindo times no banco de dados...")
        cursor.executemany(
            "INSERT INTO times (nome, cores, estado, ano_fundacao, serie, mascote) VALUES (?, ?, ?, ?, ?, ?)",
            times_dados
        )
        conn.commit()
        print(f"✅ {len(times_dados)} times inseridos com sucesso!")
    else:
        print(f"ℹ️  Banco já possui {count} times. Nenhum time foi inserido.")

    # Mostra primeiros times para verificação
    print("\n📋 Primeiros 5 times no banco:")
    cursor.execute("SELECT nome, cores, estado, ano_fundacao, serie, mascote FROM times LIMIT 5")
    for row in cursor.fetchall():
        nome, cores, estado, ano, serie, mascote = row
        print(f"   • {nome} ({estado}) - {cores} - {ano} - Série {serie} - Mascote: {mascote}")

    # Estatísticas por série
    cursor.execute("SELECT serie, COUNT(*) FROM times GROUP BY serie ORDER BY serie")
    print("\n📈 Times por série:")
    for serie, count in cursor.fetchall():
        print(f"   • Série {serie}: {count} times")

    conn.close()
    print("\n🎉 Banco de dados populado com sucesso!")

if __name__ == "__main__":
    popular_times()
