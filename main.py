
import pyautogui as py
from dotenv import load_dotenv
import os
from time import sleep as sp


from func.actions_btn import aba_orcamento, bnt_OKDISABLE, btn_OrcamentoDisable, click_btn_fecharLogo, click_btn_ok, click_btn_sim, click_novo_orcamento, click_orcamento,click_receita,icon_username
from func.inic_login import reiniciar_fcerta,login_fcerta,closed_fcerta, verifica_fcerta
from func.interection_receita import gerar_orcamento







load_dotenv()
USERNAME = os.getenv("LOGIN_ODF")
SENHA = os.getenv("SENHA_ODF")


def inic_process():

    is_open = verifica_fcerta()

    if is_open:
        print("Fórmula Certa já está em execução.")
    
        if aba_orcamento() == 'nao':
            print("NÃO LOCALIZOU A ABA ORÇAMENTO")
            clicou_receita = click_receita()
            if clicou_receita == 'nao':
                print("NÃO LOCALIZOU O ICONE RECEITA")

            if aba_orcamento() == 'sim':
                print("LOCALIZOU A ABA ORÇAMENTO")
                if bnt_OKDISABLE() == 'nao':
                    print("NÃO LOCALIZOU O ICONE OK DISABLED")
                    return False
                    
                if btn_OrcamentoDisable() == 'nao':
                    print("NÃO LOCALIZOU O ICONE ORÇAMENTO DISABLED")
                    py.press('f2')
                    sp(2)
                    py.press('enter')
                
                return True
                    
            clicou_orcamento = click_orcamento()
            if clicou_orcamento == 'nao':
                print("NÃO LOCALIZOU O ICONE ORÇAMENTO")  
                return False 

            sp(2) 
            py.press('f2')
            sp(2)
            py.press('enter')
            return True

        btn_OrcamentoDisable()
        return True
    else:
        login_fcerta()
        if not login_fcerta():
            print("Falha ao iniciar o ODF. Encerrando o programa.")
            return False

        resultado_icon = icon_username()
        if resultado_icon == 'nao':
            print("NÃO LOCALIZOU O ICONE USERNAME")
            print('reiniciando o ODF')
            return False
           
        #inserindo dados para o login
        py.press('ENTER')
        py.write(USERNAME)
        py.press('ENTER')
        py.write(SENHA)
        py.press('ENTER')
        print('Login realizado com sucesso!')
        sp(5)
        clicou_fecharLogo = click_btn_fecharLogo()
        if clicou_fecharLogo == 'não':
            print("NÃO LOCALIZOU O ICONE FECHAR LOGO")
            return False
        clicou_receita = click_receita()
        if clicou_receita == 'não':
            print("NÃO LOCALIZOU O ICONE RECEITA")
            return False
        clicou_orcamento = click_orcamento()
        if clicou_orcamento == 'não':
            print("NÃO LOCALIZOU O ICONE ORÇAMENTO")
            return False
        clicou_novo_orcamento = click_novo_orcamento()
        if clicou_novo_orcamento == 'não':
            print("NÃO LOCALIZOU O ICONE NOVO ORÇAMENTO")
            return False
        clicou_ok = click_btn_ok()
        if clicou_ok == 'não':
            print("NÃO LOCALIZOU O ICONE OK")
            return False
        sp(2)
        py.press('enter')
        return True


max_tentativas = 3

for tentativa in range(1, max_tentativas + 1):
    print(f"Tentativa {tentativa} de {max_tentativas} para iniciar o processo.")
    resultado  = inic_process()
    if not resultado:
        print("FALHA AO INICIAR O PROCESSO.")
        print('Reiniciando o Formula Certa!')
        
        if not reiniciar_fcerta():
            print("Falha ao reiniciar o Formula Certa.")
            print('enviando EMail notificando de erro no sistema ')
            break
        
    
    else:
        print("Processo iniciado com sucesso!")

        if gerar_orcamento():
            break
  