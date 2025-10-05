from func.actions_btn import alerta_Prodembalagens, alerta_Retirada, alerta_acrescimo, alerta_impressao, alerta_maisformulas, click_btn_fecharLogo, alerta_sem_cadastro, alerta_qntzerada, click_btn_okModal, click_campo_data,click_btn_ok,click_btn_sim,click_btn_nao,alerta_dadoscorretos,alerta_controlados, click_novo_orcamento
import pyautogui as py  
from time import sleep as sp
import re
from datetime import datetime

from func.integrador_chatwoot_sheets import atualizar_tags_chatwoot, enviar_chatwoot_nota, obter_dados_base_receita, atualizar_status_receita
from logger_config import get_logger

# Configura o logger para este módulo
logger = get_logger('interection_receita')




def gerar_orcamento():
    
        # # Captura todas as receitas do JSON
        dados_receitas = obter_dados_base_receita()
        total_receitas = len(dados_receitas["data"])

        logger.info(f"Total de receitas para processar: {total_receitas}")

        if total_receitas == 0: 
            logger.warning("Nenhuma receita com status 'consultado' encontrada para processar")
            logger.info("Verifique se existem receitas com status 'consultado' na planilha")
            logger.info("Receitas com status 'orçamento feito' são ignoradas automaticamente")
            return 'sem receitas'
        
        # Processa cada receita individualmente
        for indice_receita, receita in enumerate(dados_receitas["data"]):
            logger.info(f"PROCESSANDO RECEITA {indice_receita + 1} DE {total_receitas}")
            
            qsp = False
            id_conversa = receita["conversation_id"]
            id_receita = receita["id"]  # ID único da receita para atualização de status


            texto_variacoes = receita["medicamentos_com_variacoes"]

            # Divide por vírgulas principais (mas preserva o conteúdo dentro dos colchetes)
            partes = re.split(r',(?![^\[]*\])', texto_variacoes)
            partes = [p.strip() for p in partes if p.strip()]

            variacoes_dict = {}

            for parte in partes:
                if ":" in parte:
                    nome, conteudo = parte.split(":", 1)
                    nome = nome.strip()
                    # Extrai tudo que está dentro dos colchetes
                    itens = re.findall(r'\[([^\]]+)\]', conteudo)
                    if itens:
                        lista_itens = [v.strip() for v in itens[0].split(",") if v.strip()]
                        variacoes_dict[nome] = lista_itens
                    else:
                        variacoes_dict[nome] = []
                else:
                    variacoes_dict[parte] = []

            logger.debug("Dicionário de medicamentos e variações criado")
            for k, v in variacoes_dict.items():
                logger.debug(f" - {k}: {v}")

            # Lista principal de medicamentos
            medicamentos = list(variacoes_dict.keys())
            dosagens = [d.strip() for d in receita["dosagem"].split(",")]
            quantidade = str(receita["quantidade"])
            quantidade_limpa = re.search(r'\d+(?:[.,]\d+)?', quantidade)
            quantidade_limpa = quantidade_limpa.group().replace(',', '.') if quantidade_limpa else ''

            tipo = str(receita["tipo"])
            medico = str(receita["medico"])
            possologia = str(receita["possologia"])
            data_precisao = str(receita["data_receita"])

            if data_precisao == '' or data_precisao is None:
                data_precisao = datetime.now().strftime("%d/%m/%Y")
                data_precisao = str(data_precisao)
                
            tipo_embalagem = ''
            qnt_embalagem = 0

            # # # --- CAMPOS INICIAIS ---
            sp(3)
            resultado_campo = click_campo_data()
            if resultado_campo == 'não':
                print("NÃO LOCALIZOU O ICONE CAMPO DATA")

            py.press('tab')
            py.write(data_precisao)
            py.press('tab')
            py.write("WHATSAPP") # CANAL
            py.press('tab')
            py.write("1") # YASNA
            sp(3)
            py.press('ENTER', presses=2, interval=2)

            # --- CAMPO MÉDICO ---
            sp(3)
            py.press('tab', presses=3) # CAMPO MÉDICO
            print("Medico - > ",medico)
            py.write(medico,interval=0.05)
            py.press('tab')
            sp(3)
            alerta_encontrado = alerta_sem_cadastro()
            if alerta_encontrado == 'sim':
                print("⚠️ ALERTA DE MÉDICO SEM CADASTRO")
                py.press('enter')
                py.press('esc')
                sp(3)
                py.write('YASNA BAEZA')  # fallback padrão
            sp(3)
            py.press('ENTER')
            sp(3)
            click_btn_fecharLogo()
            print("✅ CAMPOS MÉDICO PREENCHIDOS")



            # # # --- CAMPO FORMA FARMACÊUTICA ---
            print("PRÓXIMO CAMPO - FORMA FARMACÊUTICA")
            py.press('tab')
            sp(2)
            py.hotkey('shift', 'a')
            sp(2)

            if tipo.lower() in ['capsula', 'cápsula']:
                tipo = '1'
                tipo_formula = 'CAP'
                qnt_embalagem = 1
            elif tipo.lower() == 'creme':
                qsp = True
                tipo = '2'
                if int(quantidade_limpa) == 30 or int(quantidade_limpa) == 60:
                    qnt_embalagem = int(quantidade_limpa) / 30
                    tipo_embalagem = '30 ML'
                    tipo_formula = 'G'
                    if qnt_embalagem == 1:
                        qnt_embalagem = 1
                    elif qnt_embalagem == 2:
                        qnt_embalagem = 2
                elif int(quantidade_limpa) == 50 or int(quantidade_limpa) == 100:
                    qnt_embalagem = int(quantidade_limpa) / 50
                    tipo_embalagem = '50 ML'
                    tipo_formula = 'G'
                    if qnt_embalagem == 1:
                        qnt_embalagem = 1
                    elif qnt_embalagem == 2:
                        qnt_embalagem = 2
                else:
                    tipo_embalagem = ''
                    qnt_embalagem = 1
                    tipo_formula = 'G'

            elif tipo.lower() == 'loção':
                tipo = '3'
                tipo_formula = 'ML'
                qnt_embalagem = 1

            print("Tipo -> ",tipo)
            py.write(tipo)
            py.press('tab')

            print('quantidade -> ',quantidade_limpa)
            py.write(str(quantidade_limpa))
            py.press('tab')
            print("Tipo de formula -> ",tipo_formula)
            py.write(str(tipo_formula))  # Tipo de fórmula
            py.press('tab', presses=2)

            sp(2)
            if tipo != '2':
                py.hotkey('shift', 'tab')
            else:
                for _ in range(2):
                    py.hotkey('shift', 'tab')

            py.write(possologia,interval=0.05)  # prescrição
            py.press('tab')
            print("Quantidade de potes -> ",qnt_embalagem)
            print("Tipo do pote -> ",tipo_embalagem)
            py.write(str(qnt_embalagem))  # Quantidade de potes

            # # ** ETAPA INSERINDO OS INSUMOS **

            # Garante que há pelo menos um item em 'data'
            py.press('tab', presses=9,interval=0.5)  # Vai para o primeiro campo de insumo antes 6
            for i, medicamento in enumerate(medicamentos):
                sp(2)
                py.write(medicamento, interval=0.05)
                py.press("tab")
                sp(2)

                if alerta_sem_cadastro() == "sim":
                    print(f"⚠️ {medicamento} não cadastrado — tentando variações...")
                    py.press("enter")
                    py.press("backspace", presses=len(medicamento))
                    sp(1)

                    variacoes = variacoes_dict.get(medicamento, [])
                    if not variacoes:
                        print(f"❌ Nenhuma variação disponível para {medicamento}, pulando...")
                        continue

                    encontrado = False
                    for v in variacoes:
                        py.write(v, interval=0.05)
                        py.press("tab")
                        sp(1)
                        if alerta_sem_cadastro() == "nao":
                            print(f"✅ {v} encontrado!")
                            encontrado = True
                            break
                        else:
                            py.press("enter")
                            py.press("backspace", presses=len(v))

                    if not encontrado:
                        print(f"❌ Nenhuma variação válida para {medicamento}, pulando...")
                        continue

                py.press("enter")

                # Insere a dosagem correspondente
                if i < len(dosagens):
                    dose = dosagens[i]
                    sp(1)
                    py.write(dose)
                    print(f"💊 {medicamento} → dose: {dose}")
                    py.press("tab")

                    unidade = re.findall(r"[A-Za-z]+", dose)
                    if unidade:
                        unidade = unidade[0].upper()
                        if unidade == "CC":
                            unidade = "G"
                            print(f"Convertendo {dose} para {unidade}")
                        py.write(unidade)
                    else:
                        py.write("")

                py.press("enter")
                alerta_qntzerada()


            # # -- ETAPA FINALIZA O PEDIDO
            click_btn_ok()

            if qsp:
                print('QSP selecionado')
                click_btn_sim()
            else:
                print('QSP não selecionado')
                click_btn_nao()
            sp(3)
            #-- Clica no botão  'ok' para confirmar a quantidade
            if click_btn_okModal() == 'sim': 
                print("Quantidade confirmada")
                

            # Aviso de remedios controlados 
            if alerta_controlados() == 'sim':
                print("⚠️ ALERTA DE REMEDIOS CONTROLADOS")
                click_btn_sim()

            if alerta_dadoscorretos() == 'sim':
                print("⚠️ ALERTA DE DADOS CORRETOS")
                click_btn_sim()

            sp(2)
            if tipo == '2':
                ('inserindo o nome da embalagem ',tipo_embalagem)
                py.write(f'UNI CONTROL {tipo_embalagem}')
                sp(2)
                py.press('tab')
            else:
                py.press('enter',presses=2,interval=1)

            if alerta_Prodembalagens() == 'sim': 
                print("Embalagem confirmada")
                sp(2)
                py.press('enter')
                sp(2)
                py.press('enter')

            if alerta_acrescimo() == 'sim': 
                print("Alerta de acréscimo localizado")
                py.press('TAB',presses=5)
                py.press('ENTER')


            if alerta_Retirada() == 'sim': 
                print("Alerta de retirada localizado")
                click_btn_okModal()


            # # --Existem mais formulas
            num_orçamento = alerta_maisformulas()
            if num_orçamento != 'nao': 
                print("Alerta de mais fórmulas localizado")
                click_btn_nao()

            #--Impressão da receita
            if alerta_impressao() == 'sim': 
                print("Alerta de impressão localizado")
                sp(2)
                py.press('esc')
                
            # # Envia os dados do número do orçamento para Chatwoot
            enviar_chatwoot_nota(id_conversa, num_orçamento)
            # # Remove a tag orçamento e adiciona tag orçamento-realizado
            atualizar_tags_chatwoot(id_conversa)
            # # Atualiza o status da receita no Google Sheets usando ID único
            atualizar_status_receita(id_receita, "orçamento feito")

            # Verifica se há mais receitas para processar
            if indice_receita < total_receitas - 1:
                print(f"\n🔄 Iniciando próxima receita ({indice_receita + 2}/{total_receitas})...")
                sp(5)
                py.press('f2') #gerran um novo orçamento 
                sp(3)
                py.press('enter')
                sp(2)
            else:
                print(f"\n✅ TODAS AS {total_receitas} RECEITAS FORAM PROCESSADAS!")
                print("Processo finalizado com sucesso!")
                sp(5)
                py.press('f2') #gerran um novo orçamento 
                sp(3)
                py.press('enter')
                sp(2)
                return True

       



