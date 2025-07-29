import sqlite3
import unicodedata
import os

def normalizar_nome(nome):
    """Remove acentos e normaliza nomes para comparação case-insensitive."""
    nome_normalizado = unicodedata.normalize('NFKD', nome)
    nome_normalizado = ''.join([c for c in nome_normalizado if not unicodedata.combining(c)])
    nome_normalizado = nome_normalizado.lower().replace('ç', 'c').strip()
    return nome_normalizado

class Time:
    """Modelo para representar times de futebol brasileiro."""
    
    # Colunas padrão para consultas SQL
    COLUNAS_SQL = "id, nome, cores, estado, ano_fundacao, serie, mascote"

    def __init__(self, id=None, nome=None, cores=None, estado=None, ano_fundacao=None, serie=None, mascote=None):
        self.id = id
        self.nome = nome
        self.cores = cores
        self.estado = estado
        self.ano_fundacao = ano_fundacao
        self.serie = serie
        self.mascote = mascote

    def nome_arquivo(self):
        """Gera nome do arquivo de escudo sem espaços e caracteres especiais."""
        return normalizar_nome(self.nome).replace(' ', '')

    def __repr__(self):
        return f'<Time {self.nome}>'

    @staticmethod
    def get_db_connection():
        """Estabelece conexão com o banco de dados SQLite."""
        db_path = os.path.join('futdle', 'futdle.db')
        return sqlite3.connect(db_path)

    @staticmethod
    def _criar_time_de_row(row):
        """Cria objeto Time a partir de linha do banco de dados."""
        return Time(
            id=row[0], nome=row[1], cores=row[2], estado=row[3],
            ano_fundacao=row[4], serie=row[5], mascote=row[6]
        )

    @classmethod
    def _executar_query(cls, query, params=None, fetch_all=False):
        """Executa query no banco e fecha conexão automaticamente."""
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        resultado = cursor.fetchall() if fetch_all else cursor.fetchone()
        conn.close()
        return resultado

    @classmethod
    def query_all(cls):
        """Retorna todos os times do banco de dados."""
        rows = cls._executar_query(f"SELECT {cls.COLUNAS_SQL} FROM times", fetch_all=True)
        return [cls._criar_time_de_row(row) for row in rows]

    @classmethod
    def get_by_id(cls, time_id):
        """Busca time por ID."""
        row = cls._executar_query(f"SELECT {cls.COLUNAS_SQL} FROM times WHERE id = ?", (time_id,))
        return cls._criar_time_de_row(row) if row else None

    @classmethod
    def get_by_nome(cls, nome):
        """Busca time por nome exato."""
        row = cls._executar_query(f"SELECT {cls.COLUNAS_SQL} FROM times WHERE nome = ?", (nome,))
        return cls._criar_time_de_row(row) if row else None
    
    @classmethod
    def buscar_por_nome_normalizado(cls, nome_busca):
        """Busca time comparando nome normalizado para evitar problemas com acentos."""
        nome_normalizado = normalizar_nome(nome_busca)
        times = cls.query_all()
        
        for time in times:
            if nome_normalizado == normalizar_nome(time.nome):
                return time
        return None
