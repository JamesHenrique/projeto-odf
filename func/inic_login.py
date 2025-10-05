import subprocess
import psutil
from time import sleep as sp

PATH_EXECUTAVEL = r"\\SERVIDORDELL\FCerta\fcerta.exe"
def closed_fcerta():
    # Itera sobre todos os processos em execução
    for processo in psutil.process_iter(['pid', 'name']):
        # Verifica se o processo com o nome "fcerta.exe" está em execução
        if processo.info['name'] == "fcerta.exe":
            # Encerra o processo encontrado
            processo.terminate()
            print("Fórmula Certa foi fechado.")
            return True
    return False



def verifica_fcerta():
    # Itera sobre todos os processos em execução
    for processo in psutil.process_iter(['pid', 'name']):
        # Verifica se o processo com o nome "fcerta.exe" está em execução
        if processo.info['name'] == "fcerta.exe":

            return True
    return False



def login_fcerta():
    path_executavel = PATH_EXECUTAVEL

    # Inicia o processo de forma assíncrona e retorna o objeto do processo
    processo = subprocess.Popen(path_executavel)
    print("INICIANDO ODF.")
    
    return True


def reiniciar_fcerta():
    print('REINICIANDO ODF.')
    if not closed_fcerta():
        print("Fórmula Certa não estava em execução.")
        return False
    sp(10)
    login_fcerta()
    print("Reiniciado com sucesso.")
    return True


