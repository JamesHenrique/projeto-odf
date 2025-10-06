
import pyautogui as py
from dotenv import load_dotenv
import os
import sys
import traceback
from time import sleep as sp

from func.actions_btn import aba_orcamento, bnt_OKDISABLE, btn_OrcamentoDisable, click_btn_fecharLogo, click_btn_ok, click_btn_sim, click_novo_orcamento, click_orcamento,click_receita,icon_username
from func.inic_login import reiniciar_fcerta,login_fcerta,closed_fcerta, verifica_fcerta
from func.interection_receita import gerar_orcamento
from func.logger_config import get_logger
from func.integrador_chatwoot_sheets import obter_dados_json, buscar_conversas_chatwoot, enviar_erro_para_sheets, registrar_erro_automatico

# Configura o logger para o módulo main
logger = get_logger('main')


def handler_global_exceptions(exc_type, exc_value, exc_traceback):
    """
    Handler global para capturar exceções não tratadas e enviá-las para o Google Sheets.
    """
    if issubclass(exc_type, KeyboardInterrupt):
        # Permite que Ctrl+C funcione normalmente
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    # Extrai informações da exceção
    tipo_erro = exc_type.__name__
    mensagem_erro = str(exc_value)
    
    # Extrai informações do traceback
    tb_linhas = traceback.format_exception(exc_type, exc_value, exc_traceback)
    traceback_completo = ''.join(tb_linhas)
    
    # Pega o último frame do traceback para informações específicas
    if exc_traceback:
        ultimo_frame = exc_traceback
        while ultimo_frame.tb_next:
            ultimo_frame = ultimo_frame.tb_next
        
        arquivo = ultimo_frame.tb_frame.f_code.co_filename
        linha = ultimo_frame.tb_lineno
        funcao = ultimo_frame.tb_frame.f_code.co_name
        
        contexto = f"Exceção não tratada em {funcao}()"
        modulo_origem = os.path.basename(arquivo)
        linha_erro = str(linha)
    else:
        contexto = "Exceção não tratada (sem traceback)"
        modulo_origem = "desconhecido"
        linha_erro = ""
    
    # Registra o erro no sistema de log local
    logger.critical(f"EXCEÇÃO NÃO TRATADA: {tipo_erro} - {mensagem_erro}")
    logger.critical(f"Arquivo: {modulo_origem}, Linha: {linha_erro}")
    logger.critical(f"Traceback completo:\n{traceback_completo}")
    
    # Tenta enviar para o Google Sheets
    try:
        enviar_erro_para_sheets(
            tipo_erro=f"CRÍTICO: {tipo_erro}",
            mensagem_erro=f"{mensagem_erro}\n\nTraceback:\n{traceback_completo[:1000]}",  # Limita o traceback
            contexto=contexto,
            modulo=modulo_origem,
            linha_erro=linha_erro
        )
        logger.info("Exceção não tratada registrada no Google Sheets")
    except Exception as e:
        logger.error(f"Falha ao registrar exceção não tratada no Sheets: {str(e)}")
    
    # Chama o handler padrão do sistema
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


# Configura o handler global de exceções
sys.excepthook = handler_global_exceptions







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
        erro_msg = f"Erro ao verificar conversas no Chatwoot: {str(e)}"
        logger.error(erro_msg)
        # Registra erro no Google Sheets
        registrar_erro_automatico(e, "verificar_conversas_pendentes", "main.py")
        return False


def inic_process():
    logger.info("Iniciando processo de verificação do Fórmula Certa")
    
    try:
        is_open = verifica_fcerta()

        if is_open:
            logger.info("Fórmula Certa já está em execução")
        
            if aba_orcamento() == 'nao':
                logger.warning("NÃO LOCALIZOU A ABA ORÇAMENTO")
                clicou_receita = click_receita()
                if clicou_receita == 'nao':
                    erro_msg = "NÃO LOCALIZOU O ICONE RECEITA"
                    logger.error(erro_msg)
                    enviar_erro_para_sheets(
                        tipo_erro="UIElementNotFound",
                        mensagem_erro=erro_msg,
                        contexto="inic_process - buscar icone receita",
                        modulo="main.py"
                    )

                if aba_orcamento() == 'sim':
                    logger.info("LOCALIZOU A ABA ORÇAMENTO")
                    if bnt_OKDISABLE() == 'nao':
                        erro_msg = "NÃO LOCALIZOU O ICONE OK DISABLED"
                        logger.error(erro_msg)
                        enviar_erro_para_sheets(
                            tipo_erro="UIElementNotFound",
                            mensagem_erro=erro_msg,
                            contexto="inic_process - buscar botão OK disabled",
                            modulo="main.py"
                        )
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
                    erro_msg = "NÃO LOCALIZOU O ICONE ORÇAMENTO"
                    logger.error(erro_msg)
                    enviar_erro_para_sheets(
                        tipo_erro="UIElementNotFound",
                        mensagem_erro=erro_msg,
                        contexto="inic_process - buscar icone orçamento",
                        modulo="main.py"
                    )
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
                erro_msg = "Falha ao iniciar o ODF. Encerrando o programa"
                logger.error(erro_msg)
                enviar_erro_para_sheets(
                    tipo_erro="ApplicationStartupError",
                    mensagem_erro=erro_msg,
                    contexto="inic_process - login Fórmula Certa",
                    modulo="main.py"
                )
                return False

            resultado_icon = icon_username()
        if resultado_icon == 'nao':
            erro_msg = "NÃO LOCALIZOU O ICONE USERNAME"
            logger.error(erro_msg)
            logger.info("Reiniciando o ODF")
            enviar_erro_para_sheets(
                tipo_erro="UIElementNotFound",
                mensagem_erro=erro_msg,
                contexto="inic_process - buscar icone username",
                modulo="main.py"
            )
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
            erro_msg = "NÃO LOCALIZOU O ICONE FECHAR LOGO"
            logger.error(erro_msg)
            enviar_erro_para_sheets(
                tipo_erro="UIElementNotFound",
                mensagem_erro=erro_msg,
                contexto="inic_process - buscar botão fechar logo",
                modulo="main.py"
            )
            return False
            
        clicou_receita = click_receita()
        if clicou_receita == 'não':
            erro_msg = "NÃO LOCALIZOU O ICONE RECEITA"
            logger.error(erro_msg)
            enviar_erro_para_sheets(
                tipo_erro="UIElementNotFound",
                mensagem_erro=erro_msg,
                contexto="inic_process - buscar icone receita (pós-login)",
                modulo="main.py"
            )
            return False
            
        clicou_orcamento = click_orcamento()
        if clicou_orcamento == 'não':
            erro_msg = "NÃO LOCALIZOU O ICONE ORÇAMENTO"
            logger.error(erro_msg)
            enviar_erro_para_sheets(
                tipo_erro="UIElementNotFound",
                mensagem_erro=erro_msg,
                contexto="inic_process - buscar icone orçamento (pós-login)",
                modulo="main.py"
            )
            return False
            
        clicou_novo_orcamento = click_novo_orcamento()
        if clicou_novo_orcamento == 'não':
            erro_msg = "NÃO LOCALIZOU O ICONE NOVO ORÇAMENTO"
            logger.error(erro_msg)
            enviar_erro_para_sheets(
                tipo_erro="UIElementNotFound",
                mensagem_erro=erro_msg,
                contexto="inic_process - buscar icone novo orçamento",
                modulo="main.py"
            )
            return False
            
        clicou_ok = click_btn_ok()
        if clicou_ok == 'não':
            erro_msg = "NÃO LOCALIZOU O ICONE OK"
            logger.error(erro_msg)
            enviar_erro_para_sheets(
                tipo_erro="UIElementNotFound",
                mensagem_erro=erro_msg,
                contexto="inic_process - buscar botão OK final",
                modulo="main.py"
            )
            return False
            
        sp(2)
        py.press('enter')
        logger.info("Login e configuração inicial concluídos com sucesso")
        return True
    
    except Exception as e:
        erro_msg = f"Erro crítico durante inicialização do processo: {str(e)}"
        logger.error(erro_msg)
        registrar_erro_automatico(e, "inic_process - erro geral", "main.py")
        return False


max_tentativas = 3

try:
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
        
        try:
            resultado = inic_process()
            
            if not resultado:
                logger.error("FALHA AO INICIAR O PROCESSO")
                logger.info("Reiniciando o Fórmula Certa")
                
                if not reiniciar_fcerta():
                    erro_msg = "Falha ao reiniciar o Fórmula Certa"
                    logger.critical(erro_msg)
                    logger.error("Enviando EMail notificando de erro no sistema")
                    enviar_erro_para_sheets(
                        tipo_erro="SystemRestartFailure",
                        mensagem_erro=erro_msg,
                        contexto=f"Loop principal - tentativa {tentativa}",
                        modulo="main.py"
                    )
                    break
            else:
                logger.info("Processo iniciado com sucesso!")
                
                try:
                    if gerar_orcamento():
                        logger.info("Geração de orçamentos concluída com sucesso")
                        break
                    else:
                        for _ in range(2):
                            py.hotkey('alt', 'f4')
                            sp(2)
                            click_btn_sim()
                        logger.info("Tentando reiniciar o processo de geração de orçamentos")
                        resultado = inic_process()
                            
                            
                except Exception as e:
                    erro_msg = f"Erro durante geração de orçamentos: {str(e)}"
                    logger.error(erro_msg)
                    registrar_erro_automatico(e, f"gerar_orcamento - tentativa {tentativa}", "main.py")
                    continue
                    
        except Exception as e:
            erro_msg = f"Erro na tentativa {tentativa} do loop principal: {str(e)}"
            logger.error(erro_msg)
            registrar_erro_automatico(e, f"loop_principal - tentativa {tentativa}", "main.py")
            continue

    logger.info("Finalizando execução do sistema")

except Exception as e:
    erro_msg = f"Erro crítico no sistema principal: {str(e)}"
    logger.critical(erro_msg)
    registrar_erro_automatico(e, "sistema_principal_critico", "main.py")
    logger.critical("Sistema será encerrado devido a erro crítico")
    sys.exit(1)
  