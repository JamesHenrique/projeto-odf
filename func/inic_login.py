import subprocess
import psutil
from time import sleep as sp
from pywinauto import Application
import time

PATH_EXECUTAVEL = r"\\SERVIDORDELL\FCerta\fcerta.exe"

def fechar_janelas_fc_receitas():
    """
    Fecha todas as janelas abertas do FCReceitas antes de encerrar o processo.
    Evita que abas abertas causem problemas no próximo login.
    """
    pid = obter_pid_fc_receitas()
    if not pid:
        print("ℹ️ FCReceitas não está em execução.")
        return True
    
    try:
        print("🔍 Verificando janelas abertas do FCReceitas...")
        app = Application(backend="uia").connect(process=pid, timeout=5)
        janelas = app.windows()
        
        janelas_fechadas = 0
        for janela in janelas:
            try:
                titulo = janela.window_text()
                if "fórmulacerta" in titulo.lower():
                    print(f"🗑️ Fechando janela: {titulo}")
                    janela.close()
                    janelas_fechadas += 1
                    sp(0.5)
            except Exception as e:
                print(f"⚠️ Erro ao fechar janela: {e}")
                continue
        
        if janelas_fechadas > 0:
            print(f"✅ {janelas_fechadas} janela(s) do FCReceitas fechada(s)")
            sp(1)  # Aguarda confirmação do fechamento
        
        return True
        
    except Exception as e:
        print(f"⚠️ Erro ao manipular janelas FCReceitas: {e}")
        return True  # Continua mesmo com erro

def closed_fcerta():
    """
    Fecha completamente o Fórmula Certa e FCReceitas.
    Garante que todas as janelas e processos sejam encerrados.
    """
    print("🔄 Iniciando fechamento do Fórmula Certa...")
    
    # Primeiro fecha as janelas abertas do FCReceitas
    fechar_janelas_fc_receitas()
    sp(1)
    
    processos_fechados = 0
    
    # Fecha FCReceitas.exe
    for processo in psutil.process_iter(['pid', 'name']):
        try:
            nome = processo.info['name']
            if nome and nome.lower() in ['fcreceitas.exe', 'fcreceitas']:
                print(f"🗑️ Encerrando processo: {nome}")
                processo.terminate()
                processo.wait(timeout=3)
                processos_fechados += 1
                print("✅ FCReceitas foi fechado.")
        except (psutil.NoSuchProcess, psutil.TimeoutExpired, psutil.AccessDenied) as e:
            print(f"⚠️ Erro ao fechar FCReceitas: {e}")
            continue
    
    sp(1)
    
    # Fecha fcerta.exe
    for processo in psutil.process_iter(['pid', 'name']):
        try:
            nome = processo.info['name']
            if nome and nome.lower() in ['fcerta.exe', 'fcerta']:
                print(f"🗑️ Encerrando processo: {nome}")
                processo.terminate()
                processo.wait(timeout=3)
                processos_fechados += 1
                print("✅ Fórmula Certa foi fechado.")
        except (psutil.NoSuchProcess, psutil.TimeoutExpired, psutil.AccessDenied) as e:
            print(f"⚠️ Erro ao fechar Fórmula Certa: {e}")
            continue
    
    if processos_fechados > 0:
        print(f"✅ Total: {processos_fechados} processo(s) encerrado(s)")
        return True
    else:
        print("ℹ️ Nenhum processo do Fórmula Certa estava em execução.")
        return False

def verifica_fcerta():
    """
    Verifica se o processo fcerta.exe está em execução.
    """
    for processo in psutil.process_iter(['pid', 'name']):
        try:
            nome = processo.info['name']
            if nome and nome.lower() in ['fcerta.exe', 'fcerta']:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def obter_pid_fc_receitas():
    """
    Retorna o PID do processo FCReceitas.exe, se estiver em execução.
    """
    for p in psutil.process_iter(['pid', 'name']):
        try:
            nome = p.info['name']
            if nome and nome.lower() in ['fcreceitas.exe', 'fcreceitas']:
                return p.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None


def verificar_aba_orcamento_disponivel():
    """
    Verifica se a aba de Orçamento está disponível no FCReceitas.
    Retorna True se encontrada e focada, False caso contrário.
    """
    pid = obter_pid_fc_receitas()
    if not pid:
        print("ℹ️ FCReceitas não está em execução.")
        return False
    
    try:
        print("🔍 Verificando abas do FCReceitas...")
        app = Application(backend="uia").connect(process=pid, timeout=5)
        janelas = app.windows()
        
        for janela in janelas:
            try:
                titulo = janela.window_text()
                if "fórmulacerta" in titulo.lower():
                    print(f"🪟 Encontrada janela: {titulo}")
                    
                    # Prioriza aba de Orçamentos
                    if "orçamento" in titulo.lower():
                        print(f"✅ Aba de Orçamento encontrada: {titulo}")
                        janela.restore()
                        janela.set_focus()
                        sp(0.5)
                        return True
                    
                    # Aceita também Receitas como alternativa
                    elif "receita" in titulo.lower():
                        print(f"ℹ️ Aba de Receitas encontrada: {titulo}")
                        janela.restore()
                        janela.set_focus()
                        sp(0.5)
                        return True
            except Exception as e:
                print(f"⚠️ Erro ao verificar janela: {e}")
                continue
        
        print("❌ Nenhuma aba de Orçamento ou Receitas encontrada")
        return False
        
    except Exception as e:
        print(f"⚠️ Erro ao conectar ao FCReceitas: {e}")
        return False


def manipular_janelas_fc_receitas():
    """
    Manipula janelas do FCReceitas, priorizando a aba de Orçamentos.
    """
    pid = obter_pid_fc_receitas()
    if not pid:
        print("⚠️ FCReceitas não está aberto.")
        return False

    try:
        app = Application(backend="uia").connect(process=pid, timeout=5)
        janelas = app.windows()

        # Primeira passagem: procura por Orçamentos
        for janela in janelas:
            try:
                titulo = janela.window_text()
                if "fórmulacerta" in titulo.lower() and "orçamento" in titulo.lower():
                    print(f"✅ Aba de Orçamentos encontrada: {titulo}")
                    janela.restore()
                    janela.set_focus()
                    sp(0.5)
                    return True
            except Exception as e:
                print(f"⚠️ Erro ao manipular janela: {e}")
                continue

        # Segunda passagem: procura por Receitas
        for janela in janelas:
            try:
                titulo = janela.window_text()
                if "fórmulacerta" in titulo.lower() and "receita" in titulo.lower():
                    print(f"ℹ️ Aba de Receitas encontrada: {titulo}")
                    janela.restore()
                    janela.set_focus()
                    sp(0.5)
                    return True
            except Exception as e:
                continue

        print("❌ Nenhuma janela de Orçamentos ou Receitas encontrada.")
        return False

    except Exception as e:
        print(f"❌ Erro ao manipular janelas: {e}")
        return False


def login_fcerta():
    """
    Inicia o processo do Fórmula Certa.
    """
    path_executavel = PATH_EXECUTAVEL

    try:
        processo = subprocess.Popen(path_executavel)
        print("✅ INICIANDO Fórmula Certa...")
        return True
    except Exception as e:
        print(f"❌ Erro ao iniciar Fórmula Certa: {e}")
        return False


def reiniciar_fcerta():
    """
    Reinicia o Fórmula Certa completamente.
    Garante que todos os processos e janelas sejam fechados antes de reiniciar.
    Previne loops infinitos verificando o estado após cada etapa.
    """
    print('🔄 REINICIANDO Fórmula Certa...')
    
    # Etapa 1: Fechar tudo
    if not closed_fcerta():
        print("ℹ️ Fórmula Certa não estava em execução.")
    
    # Etapa 2: Aguardar fechamento completo
    print("⏳ Aguardando 10 segundos para fechamento completo...")
    sp(10)
    
    # Etapa 3: Verificar se realmente fechou (proteção anti-loop)
    tentativas_verificacao = 0
    max_tentativas_verificacao = 3
    
    while verifica_fcerta() and tentativas_verificacao < max_tentativas_verificacao:
        tentativas_verificacao += 1
        print(f"⚠️ Fórmula Certa ainda está em execução. Tentativa {tentativas_verificacao}/{max_tentativas_verificacao}")
        
        # Força fechamento novamente
        closed_fcerta()
        sp(5)
    
    if verifica_fcerta():
        print("❌ ERRO: Não foi possível fechar o Fórmula Certa completamente.")
        return False
    
    # Etapa 4: Iniciar novamente
    print("🚀 Iniciando Fórmula Certa...")
    if not login_fcerta():
        print("❌ ERRO: Falha ao iniciar Fórmula Certa.")
        return False
    
    # Etapa 5: Aguardar inicialização
    print("⏳ Aguardando inicialização (5 segundos)...")
    sp(5)
    
    # Etapa 6: Verificar se iniciou corretamente (proteção anti-loop)
    if not verifica_fcerta():
        print("❌ ERRO: Fórmula Certa não iniciou corretamente.")
        return False
    
    print("✅ Fórmula Certa reiniciado com sucesso!")
    return True


