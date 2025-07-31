"""script para popular banco de dados com times brasileiros"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
from futdle.config import DB_PATH

def criar_tabela(cursor):
    """cria tabela times se nao existir"""
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

def obter_dados_times():
    """retorna lista com dados dos times brasileiros"""
    return [
        ("Atletico Mineiro", "Preto e Branco", "MG", 1908, "A", "Galo"),
        ("Bahia", "Azul, Vermelho e Branco", "BA", 1931, "A", "Super-Homem Tricolor"),
        ("Botafogo", "Preto e Branco", "RJ", 1904, "A", "Manequinho"),
        ("Bragantino", "Branco e Vermelho", "SP", 1928, "A", "Toro Loko"),
        ("Ceara", "Preto e Branco", "CE", 1914, "A", "Vozao"),
        ("Corinthians", "Preto e Branco", "SP", 1910, "A", "Mosqueteiro"),
        ("Cruzeiro", "Azul e Branco", "MG", 1921, "A", "Raposa"),
        ("Flamengo", "Vermelho e Preto", "RJ", 1895, "A", "Urubu"),
        ("Fluminense", "Verde, Vermelho e Branco", "RJ", 1902, "A", "Guerreiro Tricolor"),
        ("Fortaleza", "Azul, Vermelho e Branco", "CE", 1918, "A", "Leao"),
        ("Gremio", "Azul, Preto e Branco", "RS", 1903, "A", "Mosqueteiro"),
        ("Internacional", "Vermelho e Branco", "RS", 1909, "A", "Saci"),
        ("Juventude", "Verde e Branco", "RS", 1913, "A", "Juju"),
        ("Mirassol", "Amarelo e Verde", "SP", 1925, "A", "Leao"),
        ("Palmeiras", "Verde e Branco", "SP", 1914, "A", "Porco Gobbato"),
        ("Santos", "Branco e Preto", "SP", 1912, "A", "Baleia"),
        ("Sao Paulo", "Branco, Vermelho e Preto", "SP", 1930, "A", "Santo Paulo"),
        ("Sport", "Vermelho e Preto", "PE", 1905, "A", "Leao"),
        ("Vasco da Gama", "Preto e Branco", "RJ", 1898, "A", "Almirante"),
        ("Vitoria", "Vermelho e Preto", "BA", 1899, "A", "Leao"),
        ("Goias", "Verde e Branco", "GO", 1943, "B", "Periquito"),
        ("Coritiba", "Verde e Branco", "PR", 1909, "B", "Vovo Coxa"),
        ("Novorizontino", "Amarelo e Preto", "SP", 2010, "B", "Tigre"),
        ("Chapecoense", "Verde e Branco", "SC", 1973, "B", "Indio Conda"),
        ("Remo", "Azul e Branco", "PA", 1905, "B", "Leao Azul"),
        ("Cuiaba", "Verde e Amarelo", "MT", 2001, "B", "Periquito"),
        ("Avai", "Azul e Branco", "SC", 1923, "B", "Leao da Ilha"),
        ("Vila Nova", "Vermelho e Branco", "GO", 1943, "B", "Tigre"),
        ("Criciuma", "Amarelo, Preto e Branco", "SC", 1947, "B", "Tigrao"),
        ("CRB", "Vermelho e Branco", "AL", 1912, "B", "Galo de Campina"),
        ("Athletico-PR", "Vermelho e Preto", "PR", 1924, "B", "Furacao"),
        ("Operario", "Preto e Branco", "PR", 1912, "B", "Fantasma"),
        ("Atletico-GO", "Vermelho e Preto", "GO", 1937, "B", "Dragao"),
        ("Athletic", "Preto e Branco", "MG", 1909, "B", "Elefante"),
        ("America-MG", "Verde e Branco", "MG", 1912, "B", "Coelho"),
        ("Volta Redonda", "Amarelo e Preto", "RJ", 1976, "B", "Volty"),
        ("Ferroviaria", "Vermelho e Branco", "SP", 1950, "B", "Locomotiva"),
        ("Paysandu", "Azul e Branco", "PA", 1914, "B", "Papao da Curuzu"),
        ("Amazonas", "Amarelo e Preto", "AM", 2019, "B", "Onca-Pintada"),
        ("Botafogo-SP", "Vermelho, Preto e Branco", "SP", 1918, "B", "Pantera"),
        ("Caxias", "Vermelho e Branco", "RS", 1935, "C", "Grena"),
        ("Ponte Preta", "Preto e Branco", "SP", 1900, "C", "Macaca"),
        ("Londrina", "Azul", "PR", 1956, "C", "Tubarao"),
        ("Nautico", "Vermelho e Branco", "PE", 1901, "C", "Timbu"),
        ("Sao Bernardo", "Amarelo e Preto", "SP", 2004, "C", "Cachorro"),
        ("Ypiranga", "Verde e Amarelo", "RS", 1924, "C", "Canarinho"),
        ("Floresta", "Verde e Branco", "CE", 1954, "C", "Lobo"),
        ("Botafogo-PB", "Preto, Vermelho e Branco", "PB", 1931, "C", "Belo"),
        ("Brusque", "Amarelo, Verde e Vermelho", "SC", 1987, "C", "Quadricolor"),
        ("CSA", "Azul e Branco", "AL", 1913, "C", "Azulao"),
        ("Ituano", "Preto e Vermelho", "SP", 1947, "C", "Galo de Itu"),
        ("Guarani", "Verde e Branco", "SP", 1911, "C", "Bugre"),
        ("Maringa", "Preto e Branco", "PR", 2010, "C", "Dogao"),
        ("Anapolis", "Vermelho e Branco", "GO", 1946, "C", "Galo da Comarca"),
        ("ABC", "Preto e Branco", "RN", 1915, "C", "Elefante"),
        ("Figueirense", "Preto e Branco", "SC", 1921, "C", "Figueira"),
        ("Itabaiana", "Vermelho, Azul e Branco", "SE", 1938, "C", "Tremendao"),
        ("Confianca", "Azul e Branco", "SE", 1936, "C", "Dragao do Bairro Industrial"),
        ("Retro", "Azul e Dourado", "PE", 2016, "C", "Aguia Dourada"),
        ("Tombense", "Vermelho e Branco", "MG", 1914, "C", "Gaviao-Carcara")
    ]

def popular_banco():
    """popula banco de dados com times brasileiros"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        criar_tabela(cursor)
        times_dados = obter_dados_times()
        
        cursor.execute("SELECT COUNT(*) FROM times")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("inserindo times no banco de dados...")
            cursor.executemany(
                "INSERT INTO times (nome, cores, estado, ano_fundacao, serie, mascote) VALUES (?, ?, ?, ?, ?, ?)",
                times_dados
            )
            conn.commit()
            print(f"{len(times_dados)} times inseridos com sucesso")
        else:
            print(f"banco ja possui {count} times")
        
        # mostra primeiros times
        print("\nprimeiros 5 times no banco:")
        cursor.execute("SELECT nome, cores, estado, ano_fundacao, serie, mascote FROM times LIMIT 5")
        for row in cursor.fetchall():
            nome, cores, estado, ano, serie, mascote = row
            print(f"  {nome} ({estado}) - {cores} - {ano} - Serie {serie} - Mascote: {mascote}")
        
        # estatisticas por serie
        cursor.execute("SELECT serie, COUNT(*) FROM times GROUP BY serie ORDER BY serie")
        print("\ntimes por serie:")
        for serie, count in cursor.fetchall():
            print(f"  Serie {serie}: {count} times")
            
    except Exception as e:
        print(f"erro ao popular banco: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    popular_banco()
