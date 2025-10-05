
import pyautogui as py
from dotenv import load_dotenv
import os
from time import sleep as sp

from func.actions_btn import aba_orcamento, bnt_OKDISABLE, btn_OrcamentoDisable, click_btn_fecharLogo, click_btn_ok, click_btn_sim, click_novo_orcamento, click_orcamento,click_receita,icon_username
from func.inic_login import reiniciar_fcerta,login_fcerta,closed_fcerta, verifica_fcerta
from func.interection_receita import gerar_orcamento
from func.logger_config import get_logger
from func.integrador_chatwoot_sheets import buscar_conversas_chatwoot

# Configura o logger para o módulo main
logger = get_logger('main')







load_dotenv()
USERNAME = os.getenv("LOGIN_ODF")
SENHA = os.getenv("SENHA_ODF")

def verificar_conversas_pendentes():
    """
    Verifica se existem conversas com tag 'orçamento' no Chatwoot.
    
    Returns:
        bool: True se existem conversas pendentes, False caso contrário
    """
    logger.info("Verificando conversas pendentes no Chatwoot...")
    
    try:
        ids_conversas = buscar_conversas_chatwoot("orçamento")
        
        if ids_conversas:
            logger.info(f"Encontradas {len(ids_conversas)} conversas com tag 'orçamento'")
            logger.debug(f"IDs das conversas: {ids_conversas}")
            return True
        else:
            logger.info("Nenhuma conversa com tag 'orçamento' encontrada")
            return False
            
    except Exception as e:
        logger.error(f"Erro ao verificar conversas no Chatwoot: {str(e)}")
        return False


def inic_process():
    logger.info("Iniciando processo de verificação do Fórmula Certa")
    
    is_open = verifica_fcerta()

    if is_open:
        logger.info("Fórmula Certa já está em execução")
    
        if aba_orcamento() == 'nao':
            logger.warning("NÃO LOCALIZOU A ABA ORÇAMENTO")
            clicou_receita = click_receita()
            if clicou_receita == 'nao':
                logger.error("NÃO LOCALIZOU O ICONE RECEITA")

            if aba_orcamento() == 'sim':
                logger.info("LOCALIZOU A ABA ORÇAMENTO")
                if bnt_OKDISABLE() == 'nao':
                    logger.error("NÃO LOCALIZOU O ICONE OK DISABLED")
                    return False
                    
                if btn_OrcamentoDisable() == 'nao':
                    logger.warning("NÃO LOCALIZOU O ICONE ORÇAMENTO DISABLED")
                    py.press('f2')
                    sp(2)
                    py.press('enter')
                
                logger.info("Processo inicializado com sucesso - Orçamento disponível")
                return True
                    
            clicou_orcamento = click_orcamento()
            if clicou_orcamento == 'nao':
                logger.error("NÃO LOCALIZOU O ICONE ORÇAMENTO")
                return False 

            sp(2) 
            py.press('f2')
            sp(2)
            py.press('enter')
            logger.info("Orçamento ativado com sucesso")
            return True

        btn_OrcamentoDisable()
        logger.info("Sistema já configurado corretamente")
        return True
    else:
        logger.info("Fórmula Certa não está em execução, iniciando login")
        login_fcerta()
        if not login_fcerta():
            logger.error("Falha ao iniciar o ODF. Encerrando o programa")
            return False

        resultado_icon = icon_username()
        if resultado_icon == 'nao':
            logger.error("NÃO LOCALIZOU O ICONE USERNAME")
            logger.info("Reiniciando o ODF")
            return False
           
        # Inserindo dados para o login
        logger.info("Realizando login no sistema")
        py.press('ENTER')
        py.write(USERNAME)
        py.press('ENTER')
        py.write(SENHA)
        py.press('ENTER')
        logger.info("Credenciais inseridas com sucesso")
        sp(5)
        
        clicou_fecharLogo = click_btn_fecharLogo()
        if clicou_fecharLogo == 'não':
            logger.error("NÃO LOCALIZOU O ICONE FECHAR LOGO")
            return False
            
        clicou_receita = click_receita()
        if clicou_receita == 'não':
            logger.error("NÃO LOCALIZOU O ICONE RECEITA")
            return False
            
        clicou_orcamento = click_orcamento()
        if clicou_orcamento == 'não':
            logger.error("NÃO LOCALIZOU O ICONE ORÇAMENTO")
            return False
            
        clicou_novo_orcamento = click_novo_orcamento()
        if clicou_novo_orcamento == 'não':
            logger.error("NÃO LOCALIZOU O ICONE NOVO ORÇAMENTO")
            return False
            
        clicou_ok = click_btn_ok()
        if clicou_ok == 'não':
            logger.error("NÃO LOCALIZOU O ICONE OK")
            return False
            
        sp(2)
        py.press('enter')
        logger.info("Login e configuração inicial concluídos com sucesso")
        return True


max_tentativas = 3

logger.info(f"Iniciando sistema com máximo de {max_tentativas} tentativas")

# Verifica se existem conversas pendentes antes de iniciar
logger.info("=== VERIFICAÇÃO INICIAL ===")
if not verificar_conversas_pendentes():
    logger.warning("Nenhuma conversa com tag 'orçamento' encontrada no Chatwoot")
    logger.info("Sistema não será iniciado - aguardando novas conversas")
    logger.info("Execute novamente quando houver conversas pendentes")
    exit(0)

logger.info("Conversas pendentes encontradas - iniciando processo...")
logger.info("=== INICIANDO SISTEMA ===")

for tentativa in range(1, max_tentativas + 1):
    logger.info(f"Tentativa {tentativa} de {max_tentativas} para iniciar o processo")
    resultado = inic_process()
    
    if not resultado:
        logger.error("FALHA AO INICIAR O PROCESSO")
        logger.info("Reiniciando o Fórmula Certa")
        
        if not reiniciar_fcerta():
            logger.critical("Falha ao reiniciar o Fórmula Certa")
            logger.error("Enviando EMail notificando de erro no sistema")
            break
    else:
        logger.info("Processo iniciado com sucesso!")
        
        try:
            if gerar_orcamento():
                logger.info("Geração de orçamentos concluída com sucesso")
                break
        except Exception as e:
            logger.error(f"Erro durante geração de orçamentos: {str(e)}")
            continue

logger.info("Finalizando execução do sistema")
  