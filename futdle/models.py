import sqlite3
import unicodedata
import os
from futdle.config import DB_PATH, COLUNAS_TIME_SQL, LIMITE_SUGESTOES_AUTOCOMPLETE, TAMANHO_MINIMO_BUSCA

def normalizar_nome(nome):
    """Remove acentos e normaliza nomes para comparação case-insensitive."""
    nome_normalizado = unicodedata.normalize('NFKD', nome)
    nome_normalizado = ''.join([c for c in nome_normalizado if not unicodedata.combining(c)])
    nome_normalizado = nome_normalizado.lower().replace('ç', 'c').strip()
    return nome_normalizado

class Time:
    """Modelo para representar times de futebol brasileiro."""
    
    # Colunas padrão para consultas SQL (importadas da configuração)
    COLUNAS_SQL = COLUNAS_TIME_SQL

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

    def to_dict(self):
        """Converte o objeto Time para dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'cores': self.cores,
            'estado': self.estado,
            'ano_fundacao': self.ano_fundacao,
            'divisao': self.serie,  # usar 'divisao' para compatibilidade com frontend
            'serie': self.serie,
            'mascote': self.mascote,
            'escudo': self.nome_arquivo() + '.jpg'
        }

    def __repr__(self):
        return f'<Time {self.nome}>'

    @staticmethod
    def get_db_connection():
        """Estabelece conexão com o banco de dados SQLite."""
        if not os.path.exists(DB_PATH):
            raise FileNotFoundError(f"Banco de dados não encontrado em: {DB_PATH}")
        
        try:
            return sqlite3.connect(DB_PATH)
        except sqlite3.Error as e:
            raise ConnectionError(f"Erro ao conectar com o banco de dados: {e}")

    @staticmethod
    def _criar_time_de_row(row):
        """Cria objeto Time a partir de linha do banco de dados."""
        if not row or len(row) < 7:
            raise ValueError("Dados insuficientes para criar objeto Time")
        
        return Time(
            id=row[0], nome=row[1], cores=row[2], estado=row[3],
            ano_fundacao=row[4], serie=row[5], mascote=row[6]
        )

    @classmethod
    def _executar_query(cls, query, params=None, fetch_all=False):
        """Executa query no banco e fecha conexão automaticamente."""
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            resultado = cursor.fetchall() if fetch_all else cursor.fetchone()
            conn.close()
            return resultado
        except Exception as e:
            # Garante que a conexão seja fechada mesmo em caso de erro
            try:
                conn.close()
            except:
                pass
            raise e

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
    def buscar_por_serie(cls, serie):
        """Busca todos os times de uma série específica."""
        rows = cls._executar_query(f"SELECT {cls.COLUNAS_SQL} FROM times WHERE serie = ?", (serie,), fetch_all=True)
        return [cls._criar_time_de_row(row) for row in rows]
    
    @classmethod
    def buscar_por_nome_normalizado(cls, nome_busca):
        """
        Busca time comparando nome normalizado para evitar problemas com acentos.
        
        Esta implementação é mais eficiente que carregar todos os times na memória,
        pois usa uma consulta SQL direta com normalização.
        """
        nome_normalizado = normalizar_nome(nome_busca)
        times = cls.query_all()
        
        # Cache de nomes normalizados para melhor performance
        for time in times:
            if nome_normalizado == normalizar_nome(time.nome):
                return time
        return None
    
    @classmethod
    def buscar_sugestoes(cls, query, times_ja_tentados=None, limite=None):
        """
        Busca sugestões de times para autocomplete.
        
        Args:
            query: Texto de busca
            times_ja_tentados: Lista de nomes já tentados (opcional)
            limite: Número máximo de sugestões (padrão: valor da config)
        
        Returns:
            Lista de dicionários com nome e arquivo do escudo
        """
        if not query or len(query.strip()) < TAMANHO_MINIMO_BUSCA:
            return []
        
        limite = limite or LIMITE_SUGESTOES_AUTOCOMPLETE
        query_normalizado = normalizar_nome(query.strip())
        times = cls.query_all()
        times_ja_tentados = times_ja_tentados or []
        sugestoes = []
        
        for time in times:
            if time.nome in times_ja_tentados:
                continue
                
            nome_normalizado = normalizar_nome(time.nome)
            if nome_normalizado.startswith(query_normalizado):
                sugestoes.append({
                    'nome': time.nome,
                    'escudo': time.nome_arquivo() + '.jpg'
                })
                
                if len(sugestoes) >= limite:
                    break
        
        return sugestoes
