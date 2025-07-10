import os
import sys

# Adiciona a pasta BOT/ ao sys.path para permitir importações absolutas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.database import get_connection  # ajuste conforme seu nome do método

def test_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        cursor.close()
        conn.close()
        print("✅ Conexão bem-sucedida. Tabelas:", [t[0] for t in tables])
    except Exception as e:
        print("❌ Erro ao conectar:", e)

if __name__ == "__main__":
    test_connection()
