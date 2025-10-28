
import pyautogui as py
from dotenv import load_dotenv
import os
import sys
import traceback
import signal
from time import sleep as sp

from func.actions_btn import aba_orcamento, bnt_OKDISABLE, btn_OrcamentoDisable, click_btn_fecharLogo, click_btn_ok, click_btn_sim, click_novo_orcamento, click_orcamento,click_receita,icon_username
from func.inic_login import reiniciar_fcerta,login_fcerta,closed_fcerta, verifica_fcerta, verificar_aba_orcamento_disponivel
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


class TimeoutError(Exception):
    """Exceção customizada para timeout."""
    pass


def timeout_handler(signum, frame):
    """Handler para timeout."""
    raise TimeoutError("Operação excedeu o tempo limite")


def executar_com_timeout(funcao, timeout_segundos=60):
    """
    Executa uma função com timeout.
    
    Args:
        funcao: Função a ser executada
        timeout_segundos: Tempo máximo de execução em segundos
    
    Returns:
        Resultado da função ou None em caso de timeout
    """
    # Windows não suporta signal.alarm, então usamos uma abordagem diferente
    import threading
    
    resultado = [None]
    excecao = [None]
    
    def wrapper():
        try:
            resultado[0] = funcao()
        except Exception as e:
            excecao[0] = e
    
    thread = threading.Thread(target=wrapper)
    thread.daemon = True
    thread.start()
    thread.join(timeout=timeout_segundos)
    
    if thread.is_alive():
        logger.error(f"Função {funcao.__name__} excedeu timeout de {timeout_segundos}s")
        enviar_erro_para_sheets(
            tipo_erro="TimeoutError",
            mensagem_erro=f"Função {funcao.__name__} travou por mais de {timeout_segundos} segundos",
            contexto="executar_com_timeout",
            modulo="main.py"
        )
        return None
    
    if excecao[0]:
        raise excecao[0]
    
    return resultado[0]








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
            
            # Verifica se a aba de orçamento está disponível no FCReceitas
            logger.info("Verificando disponibilidade da aba de Orçamento...")
            aba_disponivel = verificar_aba_orcamento_disponivel()
            
            if not aba_disponivel:
                logger.warning("ABA DE ORÇAMENTO NÃO DISPONÍVEL - Sistema precisa ser reiniciado completamente")
                logger.info("Fechando Fórmula Certa para reiniciar com login completo...")
                
                # Fecha o Fórmula Certa completamente (incluindo FCReceitas)
                try:
                    closed_fcerta()
                    sp(5)
                    logger.info("Fórmula Certa e FCReceitas fechados com sucesso")
                except Exception as e:
                    logger.error(f"Erro ao fechar Fórmula Certa: {str(e)}")
                    enviar_erro_para_sheets(
                        tipo_erro="SystemCloseError",
                        mensagem_erro=f"Erro ao fechar sistema: {str(e)}",
                        contexto="inic_process - fechar para reiniciar",
                        modulo="main.py"
                    )
                
                # Define como fechado para entrar no fluxo de login completo
                is_open = False
                logger.info("Sistema será reiniciado com processo de login completo")
            
            # Se a aba está disponível, verifica os botões
            if is_open and aba_disponivel:
                logger.info("Aba de Orçamento disponível - verificando estado dos botões")
                
                if aba_orcamento() == 'nao':
                    logger.warning("Aba de orçamento não está ativa na interface")
                    # Tenta ativar manualmente
                    logger.info("Tentando ativar aba de orçamento...")
                    clicou_receita = click_receita()
                    sp(2)
                    clicou_orcamento = click_orcamento()
                    sp(2)
                    
                    if aba_orcamento() == 'nao':
                        logger.error("Não foi possível ativar aba de orçamento")
                        return False
                
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
        
        
        # Se chegou aqui, sistema não estava aberto ou foi fechado
        if not is_open:
            logger.info("Iniciando processo completo de login...")
            
            # Tenta fazer login no sistema
            resultado_login = login_fcerta()
            
            if not resultado_login:
                erro_msg = "Falha ao iniciar o Fórmula Certa"
                logger.error(erro_msg)
                enviar_erro_para_sheets(
                    tipo_erro="ApplicationStartupError",
                    mensagem_erro=erro_msg,
                    contexto="inic_process - login Fórmula Certa",
                    modulo="main.py"
                )
                return False
            
            logger.info("Aplicação Fórmula Certa iniciada, aguardando carregamento...")
            sp(3)  # Aguarda 3 segundos para a aplicação carregar
            
            # Verifica se o ícone de username apareceu
            tentativas_username = 0
            max_tentativas_username = 5
            resultado_icon = 'nao'
            
            while tentativas_username < max_tentativas_username and resultado_icon == 'nao':
                logger.info(f"Tentativa {tentativas_username + 1}/{max_tentativas_username} de localizar ícone username")
                resultado_icon = icon_username()
                
                if resultado_icon == 'nao':
                    tentativas_username += 1
                    if tentativas_username < max_tentativas_username:
                        logger.warning(f"Ícone username não encontrado, aguardando 2 segundos...")
                        sp(2)
            
            if resultado_icon == 'nao':
                erro_msg = "NÃO LOCALIZOU O ICONE USERNAME após múltiplas tentativas"
                logger.error(erro_msg)
                enviar_erro_para_sheets(
                    tipo_erro="UIElementNotFound",
                    mensagem_erro=erro_msg,
                    contexto="inic_process - buscar icone username",
                    modulo="main.py"
                )
                return False
           
        # Inserindo dados para o login
        logger.info("Realizando login no sistema")
        sp(1)  # Pequena pausa antes de começar
        py.press('ENTER')
        sp(0.5)
        py.write(USERNAME)
        sp(0.5)
        py.press('ENTER')
        sp(0.5)
        py.write(SENHA)
        sp(0.5)
        py.press('ENTER')
        logger.info("Credenciais inseridas com sucesso")
        logger.info("Aguardando sistema processar login...")
        sp(5)
        
        # Tenta fechar logo com múltiplas tentativas
        logger.info("Buscando botão fechar logo...")
        tentativas_fechar = 0
        max_tentativas_fechar = 3
        clicou_fecharLogo = 'não'
        
        while tentativas_fechar < max_tentativas_fechar and clicou_fecharLogo == 'não':
            clicou_fecharLogo = click_btn_fecharLogo()
            if clicou_fecharLogo == 'não':
                tentativas_fechar += 1
                if tentativas_fechar < max_tentativas_fechar:
                    logger.warning(f"Botão fechar logo não encontrado, tentativa {tentativas_fechar}/{max_tentativas_fechar}")
                    sp(2)
        
        if clicou_fecharLogo == 'não':
            erro_msg = "NÃO LOCALIZOU O ICONE FECHAR LOGO após múltiplas tentativas"
            logger.error(erro_msg)
            enviar_erro_para_sheets(
                tipo_erro="UIElementNotFound",
                mensagem_erro=erro_msg,
                contexto="inic_process - buscar botão fechar logo",
                modulo="main.py"
            )
            return False
        
        logger.info("Botão fechar logo clicado com sucesso")
        sp(1)
            
        # Tenta clicar no ícone receita com múltiplas tentativas
        logger.info("Buscando ícone receita...")
        tentativas_receita = 0
        max_tentativas_receita = 3
        clicou_receita = 'não'
        
        while tentativas_receita < max_tentativas_receita and clicou_receita == 'não':
            clicou_receita = click_receita()
            if clicou_receita == 'não':
                tentativas_receita += 1
                if tentativas_receita < max_tentativas_receita:
                    logger.warning(f"Ícone receita não encontrado, tentativa {tentativas_receita}/{max_tentativas_receita}")
                    sp(2)
        
        if clicou_receita == 'não':
            erro_msg = "NÃO LOCALIZOU O ICONE RECEITA após múltiplas tentativas"
            logger.error(erro_msg)
            enviar_erro_para_sheets(
                tipo_erro="UIElementNotFound",
                mensagem_erro=erro_msg,
                contexto="inic_process - buscar icone receita (pós-login)",
                modulo="main.py"
            )
            return False
        
        logger.info("Ícone receita clicado com sucesso")
        sp(1)
        
        # Tenta clicar no ícone orçamento com múltiplas tentativas
        logger.info("Buscando ícone orçamento...")
        tentativas_orcamento = 0
        max_tentativas_orcamento = 3
        clicou_orcamento = 'não'
        
        while tentativas_orcamento < max_tentativas_orcamento and clicou_orcamento == 'não':
            clicou_orcamento = click_orcamento()
            if clicou_orcamento == 'não':
                tentativas_orcamento += 1
                if tentativas_orcamento < max_tentativas_orcamento:
                    logger.warning(f"Ícone orçamento não encontrado, tentativa {tentativas_orcamento}/{max_tentativas_orcamento}")
                    sp(2)
        
        if clicou_orcamento == 'não':
            erro_msg = "NÃO LOCALIZOU O ICONE ORÇAMENTO após múltiplas tentativas"
            logger.error(erro_msg)
            enviar_erro_para_sheets(
                tipo_erro="UIElementNotFound",
                mensagem_erro=erro_msg,
                contexto="inic_process - buscar icone orçamento (pós-login)",
                modulo="main.py"
            )
            return False
        
        logger.info("Ícone orçamento clicado com sucesso")
        sp(1)
            
        # Tenta clicar no novo orçamento com múltiplas tentativas
        logger.info("Buscando ícone novo orçamento...")
        tentativas_novo = 0
        max_tentativas_novo = 3
        clicou_novo_orcamento = 'não'
        
        while tentativas_novo < max_tentativas_novo and clicou_novo_orcamento == 'não':
            clicou_novo_orcamento = click_novo_orcamento()
            if clicou_novo_orcamento == 'não':
                tentativas_novo += 1
                if tentativas_novo < max_tentativas_novo:
                    logger.warning(f"Ícone novo orçamento não encontrado, tentativa {tentativas_novo}/{max_tentativas_novo}")
                    sp(2)
        
        if clicou_novo_orcamento == 'não':
            erro_msg = "NÃO LOCALIZOU O ICONE NOVO ORÇAMENTO após múltiplas tentativas"
            logger.error(erro_msg)
            enviar_erro_para_sheets(
                tipo_erro="UIElementNotFound",
                mensagem_erro=erro_msg,
                contexto="inic_process - buscar icone novo orçamento",
                modulo="main.py"
            )
            return False
        
        logger.info("Ícone novo orçamento clicado com sucesso")
        sp(1)
            
        # Tenta clicar no botão OK com múltiplas tentativas
        logger.info("Buscando botão OK...")
        tentativas_ok = 0
        max_tentativas_ok = 3
        clicou_ok = 'não'
        
        while tentativas_ok < max_tentativas_ok and clicou_ok == 'não':
            clicou_ok = click_btn_ok()
            if clicou_ok == 'não':
                tentativas_ok += 1
                if tentativas_ok < max_tentativas_ok:
                    logger.warning(f"Botão OK não encontrado, tentativa {tentativas_ok}/{max_tentativas_ok}")
                    sp(2)
        
        if clicou_ok == 'não':
            erro_msg = "NÃO LOCALIZOU O ICONE OK após múltiplas tentativas"
            logger.error(erro_msg)
            enviar_erro_para_sheets(
                tipo_erro="UIElementNotFound",
                mensagem_erro=erro_msg,
                contexto="inic_process - buscar botão OK final",
                modulo="main.py"
            )
            return False
        
        logger.info("Botão OK clicado com sucesso")
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
            # Executa inic_process com timeout de 120 segundos (2 minutos)
            logger.info("Iniciando processo com timeout de 120 segundos...")
            resultado = executar_com_timeout(inic_process, timeout_segundos=120)
            
            if resultado is None:
                # Timeout ocorreu
                erro_msg = f"Processo de inicialização travou na tentativa {tentativa}"
                logger.error(erro_msg)
                logger.warning("Tentando reiniciar o Fórmula Certa...")
                
                # Tenta forçar fechamento
                try:
                    closed_fcerta()
                    sp(3)
                except Exception as e:
                    logger.error(f"Erro ao fechar Fórmula Certa: {str(e)}")
                
                # Se não é a última tentativa, tenta reiniciar
                if tentativa < max_tentativas:
                    logger.info(f"Aguardando 5 segundos antes da próxima tentativa...")
                    sp(5)
                    continue
                else:
                    logger.critical("Todas as tentativas falharam devido a timeout")
                    enviar_erro_para_sheets(
                        tipo_erro="CRÍTICO: TimeoutFailure",
                        mensagem_erro=f"Sistema travou em todas as {max_tentativas} tentativas",
                        contexto="loop_principal - timeout múltiplo",
                        modulo="main.py"
                    )
                    break
            
            if not resultado:
                logger.error("FALHA AO INICIAR O PROCESSO")
                
                # Se não é a última tentativa, tenta reiniciar
                if tentativa < max_tentativas:
                    logger.info("Reiniciando o Fórmula Certa...")
                    
                    if not reiniciar_fcerta():
                        logger.error("Falha ao reiniciar Fórmula Certa, aguardando antes de nova tentativa")
                        sp(5)
                    else:
                        logger.info("Fórmula Certa reiniciado com sucesso")
                        sp(3)
                    continue
                else:
                    erro_msg = "Falha ao iniciar processo após todas as tentativas"
                    logger.critical(erro_msg)
                    enviar_erro_para_sheets(
                        tipo_erro="SystemRestartFailure",
                        mensagem_erro=erro_msg,
                        contexto=f"Loop principal - tentativa final {tentativa}",
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
  