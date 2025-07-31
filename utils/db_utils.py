"""utilitários para operações de banco de dados do futdle"""
import sqlite3
import os
from futdle.config import DB_PATH

def verificar_integridade_banco():
    """verifica se banco tem estrutura e dados corretos"""
    if not os.path.exists(DB_PATH):
        return False, "banco de dados não encontrado"
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # verifica se tabela times existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='times'")
        if not cursor.fetchone():
            conn.close()
            return False, "tabela times não encontrada"
        
        # verifica colunas
        cursor.execute("PRAGMA table_info(times)")
        colunas = [col[1] for col in cursor.fetchall()]
        colunas_esperadas = ['id', 'nome', 'cores', 'estado', 'ano_fundacao', 'serie', 'mascote']
        
        for col in colunas_esperadas:
            if col not in colunas:
                conn.close()
                return False, f"coluna {col} não encontrada"
        
        # verifica se tem dados
        cursor.execute("SELECT COUNT(*) FROM times")
        count = cursor.fetchone()[0]
        
        conn.close()
        
        if count == 0:
            return False, "banco vazio - sem times cadastrados"
        
        return True, f"banco integro com {count} times"
        
    except Exception as e:
        return False, f"erro ao verificar banco: {e}"

def backup_banco(destino=None):
    """cria backup do banco de dados"""
    if not destino:
        destino = DB_PATH + '.backup'
    
    try:
        import shutil
        shutil.copy2(DB_PATH, destino)
        return True, f"backup criado em {destino}"
    except Exception as e:
        return False, f"erro ao criar backup: {e}"

def estatisticas_banco():
    """retorna estatisticas do banco"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # times por serie
        cursor.execute("SELECT serie, COUNT(*) FROM times GROUP BY serie ORDER BY serie")
        series = {serie: count for serie, count in cursor.fetchall()}
        
        # total
        cursor.execute("SELECT COUNT(*) FROM times")
        total = cursor.fetchone()[0]
        
        # anos
        cursor.execute("SELECT MIN(ano_fundacao), MAX(ano_fundacao) FROM times")
        ano_min, ano_max = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_times': total,
            'times_por_serie': series,
            'ano_mais_antigo': ano_min,
            'ano_mais_recente': ano_max
        }
        
    except Exception as e:
        return {'erro': str(e)}

if __name__ == "__main__":
    # testa integridade
    ok, msg = verificar_integridade_banco()
    print(f"integridade do banco: {msg}")
    
    if ok:
        stats = estatisticas_banco()
        print("\nestatísticas:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
