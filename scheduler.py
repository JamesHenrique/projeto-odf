import subprocess
import time
import os

# Caminho completo para o seu script principal
SCRIPT_PATH = r"C:\Users\Servidor\Documents\Project ODF\main.py"
VENV_PYTHON = r"C:\Users\Servidor\Documents\Project ODF\env\Scripts\python.exe"

while True:
    print("⏱️ Iniciando execução do BOT...")
    try:
        # Executa o main.py e aguarda ele terminar
        subprocess.run([VENV_PYTHON, SCRIPT_PATH], check=True)
        print("✅ Execução concluída com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro durante execução: {e}")
    except Exception as e:
        print(f"⚠️ Erro inesperado: {e}")
    
    # Espera 60 segundos antes de tentar de novo
    print("Aguardando 60 segundos antes da próxima execução...\n")
    time.sleep(60)
