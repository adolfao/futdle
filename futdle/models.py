import sqlite3
import unicodedata
import os

#remove acentos e normaliza nomes para comparacao
def normalizar_nome(nome):
    nome_normalizado = unicodedata.normalize('NFKD', nome)
    nome_normalizado = ''.join([c for c in nome_normalizado if not unicodedata.combining(c)])
    nome_normalizado = nome_normalizado.lower().replace('ç', 'c').strip()
    return nome_normalizado

class Time:
    def __init__(self, id=None, nome=None, cores=None, estado=None, ano_fundacao=None, serie=None, mascote=None):
        self.id = id
        self.nome = nome
        self.cores = cores
        self.estado = estado
        self.ano_fundacao = ano_fundacao
        self.serie = serie
        self.mascote = mascote

    #gera nome do arquivo de escudo sem espacos e caracteres especiais
    def nome_arquivo(self):
        return normalizar_nome(self.nome).replace(' ', '')

    def __repr__(self):
        return f'<Time {self.nome}>'

    @staticmethod
    def get_db_connection():
        db_path = os.path.join('futdle', 'futdle.db')
        return sqlite3.connect(db_path)

    #colunas padrao para todas as consultas sql
    COLUNAS_SQL = "id, nome, cores, estado, ano_fundacao, serie, mascote"

    #cria objeto time a partir de linha do banco de dados
    @staticmethod
    def _criar_time_de_row(row):
        return Time(
            id=row[0],
            nome=row[1],
            cores=row[2],
            estado=row[3],
            ano_fundacao=row[4],
            serie=row[5],
            mascote=row[6]
        )

    #executa query no banco e fecha conexao automaticamente
    @classmethod
    def _executar_query(cls, query, params=None, fetch_all=False):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        resultado = cursor.fetchall() if fetch_all else cursor.fetchone()
        conn.close()
        return resultado

    @classmethod
    def query_all(cls):
        rows = cls._executar_query(f"SELECT {cls.COLUNAS_SQL} FROM times", fetch_all=True)
        return [cls._criar_time_de_row(row) for row in rows]

    @classmethod
    def get_by_id(cls, time_id):
        row = cls._executar_query(f"SELECT {cls.COLUNAS_SQL} FROM times WHERE id = ?", (time_id,))
        return cls._criar_time_de_row(row) if row else None

    @classmethod
    def get_by_nome(cls, nome):
        row = cls._executar_query(f"SELECT {cls.COLUNAS_SQL} FROM times WHERE nome = ?", (nome,))
        return cls._criar_time_de_row(row) if row else None
    
    #busca time comparando nome normalizado para evitar problemas com acentos
    @classmethod
    def buscar_por_nome_normalizado(cls, nome_busca):
        nome_normalizado = normalizar_nome(nome_busca)
        times = cls.query_all()
        
        for time in times:
            if nome_normalizado == normalizar_nome(time.nome):
                return time
        return None
