import pyautogui as py
from time import sleep as sp
import re
import os


# sp(3)
# screenshot = py.screenshot(r'C:\Users\Servidor\Documents\Project ODF\assets\btn_OrcamentoDisable.png',region=(234,404,250,30))#x,y,largura,altura


def input_username():
    sp(1)
    tentativas = 0
    while tentativas != 5:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\username.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('username localizado')

              
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - username')
            tentativas += 1
        sp(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'

def icon_username():
    sp(1)
    tentativas = 0
    while tentativas != 5:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\icon_username.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('username localizado')

                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - username')
            tentativas += 1
        sp(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def click_receita():
    sp(1)
    tentativas = 0
    while tentativas != 5:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\icon_receita.png", confidence=0.7) #alterar o confidence sempre que não achar
            if button_location:
                print('receita localizado')
                py.click(button_location)
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - receita')
            tentativas += 1
        sp(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def click_orcamento():
    sp(1)
    tentativas = 0
    while tentativas != 5:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\icon_orcamento.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('orcamento localizado')
                py.click(button_location)
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - orcamento')
            tentativas += 1
        sp(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'

def click_novo_orcamento():
    sp(1)
    tentativas = 0
    while tentativas != 5:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\novo_orcamento.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('novo_orcamento localizado')
                py.click(button_location)
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - novo_orcamento')
            tentativas += 1
        sp(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def click_btn_ok():
    sp(1)
    tentativas = 0
    while tentativas != 5:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\btn_OKv2.png", confidence=0.7) #alterar o confidence sempre que não achar
            if button_location:
                print('btn_ok localizado')
                py.click(button_location)
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - btn_ok')
            tentativas += 1
        sp(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'

def click_btn_okModal():
    sp(1)
    tentativas = 0
    while tentativas != 5:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\btn_okModal.png", confidence=0.6) #alterar o confidence sempre que não achar
            if button_location:
                print('btn_ok Modal localizado')
                py.click(button_location)
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - btn_ok Modal')
            tentativas += 1
        sp(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'





def click_campo_data():
    sp(1)
    tentativas = 0
    while tentativas != 5:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\campo_data.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('campo_data localizado')
                # Extrai as coordenadas do box
                x, y, w, h = button_location

                # Calcula o centro do elemento
                centro_x = x + w / 2
                centro_y = y + h / 2

                # # Move 20px para a direita
                # py.click(centro_x + 5, centro_y)

                # py.write("01/02/2025")

                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - campo_data')
            tentativas += 1
        sp(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def click_campo_tipo():
    sp(1)
    tentativas = 0
    while tentativas != 5:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\campo_tipo.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('campo_tipo localizado')
                # Extrai as coordenadas do box
                x, y, w, h = button_location

                # Calcula o centro do elemento
                centro_x = x + w / 2
                centro_y = y + h / 2

                # Move 20px para a direita
                py.click(centro_x + 4, centro_y)

                # py.write('5')
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - campo_tipo')
            tentativas += 1
        sp(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'




def alerta_sem_cadastro():
    sp(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\alerta_semcadastro.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('alerta_sem_cadastro localizado')
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - alerta_sem_cadastro')
            tentativas += 1
        sp(3)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def alerta_qntzerada():
    sp(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\alerta_qntzerada.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('alerta_qntzerada localizado')
                sp(2)
                py.press('tab')
                py.press('enter')

                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - alerta_qntzerada')
            tentativas += 1
        sp(3)  # Espera 1 segundo antes de tentar novamente
    return 'nao'

def alerta_semestoque():
    sp(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\alerta_semestoque.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('alerta_semestoque localizado')
                sp(2)
                py.press('enter')

                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - alerta_semestoque')
            tentativas += 1
        sp(3)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def alerta_qsp():
    sp(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\alerta_qsp.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('alerta_qsp localizado')
                sp(2)
          

                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - alerta_qsp')
            tentativas += 1
        sp(3)  # Espera 1 segundo antes de tentar novamente
    return 'nao'

def alerta_controlados():
    sp(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\alerta_controlados.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('alerta_controlados localizado')
                sp(2)
             

                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - alerta_controlados')
            tentativas += 1
        sp(3)  # Espera 1 segundo antes de tentar novamente
    return 'nao'

def alerta_dadoscorretos():
    sp(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\alerta_dadoscorretos.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('alerta_dadoscorretos localizado')
                sp(2)
              
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - alerta_dadoscorretos')
            tentativas += 1
        sp(3)  # Espera 1 segundo antes de tentar novamente
    return 'nao'

def click_btn_sim():
    sp(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\btn_sim.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('btn_sim localizado')
                sp(2)
                py.click(button_location)
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - btn_sim')
            tentativas += 1
        sp(3)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def click_btn_nao():
    sp(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\btn_nao.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('btn_nao localizado')
                sp(2)
                py.click(button_location)
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - btn_nao')
            tentativas += 1
        sp(3)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def click_btn_cancelar():
    sp(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\btn_cancelar.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('btn_cancelar localizado')
                sp(2)
                py.click(button_location)
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - btn_cancelar')
            tentativas += 1
        sp(3)  # Espera 1 segundo antes de tentar novamente
    return 'nao'

def click_btn_fecharLogo():
    sp(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\btn_fecharLogo.png", confidence=0.7) #alterar o confidence sempre que não achar
            if button_location:
                print('btn_fecharLogo localizado')
                sp(2)
                py.click(button_location)
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - btn_fecharLogo')
            tentativas += 1
        sp(3)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def alerta_acrescimo():
    sp(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\alerta_acrescimo.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('alerta_acrescimo localizado')
                sp(2)
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - alerta_acrescimo')
            tentativas += 1
        sp(3)  # Espera 1 segundo antes de tentar novamente
    return 'nao'





from google.cloud import vision
import io

def extrair_texto_google(caminho_imagem):
    """
    Extrai texto de uma imagem usando Google Cloud Vision OCR.
    """
    client = vision.ImageAnnotatorClient()

    with io.open(caminho_imagem, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        print(f"❌ Erro Google OCR: {response.error.message}")
        return ""

    if texts:
        return texts[0].description.strip()
    else:
        return ""



def alerta_maisformulas():
    sp(1)
    tentativas = 0
    pasta_orcamentos = r"C:\Users\Servidor\Documents\Project ODF\orcamentos"
    caminho_imagem = os.path.join(pasta_orcamentos, "temp_alerta.png")

    while tentativas < 3:
        try:
            button_location = py.locateOnScreen(
                r"C:\Users\Servidor\Documents\Project ODF\assets\alerta_maisformulas.png",
                confidence=0.9
            )

            if button_location:
                print('✅ alerta_maisformulas localizado')

                # Extrai coordenadas do botão
                x, y, w, h = map(int, button_location)

                # Captura área acima do botão
        
                top = max(y - 25, 0)
                left = int(x)
                width = int(w)
                height = int(h + 10)

                region = (left, top, width, height)

          
                # Captura screenshot
                screenshot = py.screenshot(region=region)
                screenshot.save(caminho_imagem)
                print(f"🖼️ Screenshot salvo em: {caminho_imagem}")

                # 🔹 Extrai texto via Google Cloud Vision
                texto_extraido = extrair_texto_google(caminho_imagem)
                print("📄 Texto extraído (Google OCR):", texto_extraido)

               # Busca número de orçamento
                match = re.search(r'\b\d{4,}\b', texto_extraido)
                if match:
                    numero_orcamento = match.group(0)
                    novo_nome = f"{numero_orcamento}.png"
                    novo_caminho = os.path.join(pasta_orcamentos, novo_nome)

                    # Se o arquivo já existir, remove antes de renomear
                    if os.path.exists(novo_caminho):
                        os.remove(novo_caminho)

                    os.rename(caminho_imagem, novo_caminho)
                    print(f"✅ Imagem renomeada para: {novo_nome}")

                    # Sai do loop imediatamente após renomear
                    return numero_orcamento
                else:
                    print("⚠️ Nenhum número de orçamento encontrado no texto.")
                    # Também podemos sair do loop se quiser
                    return 'nao'



        except Exception as e:
            print(f"tentando localizar - alerta_maisformulas ({tentativas + 1}/3) | Erro: {e}")

        tentativas += 1
        sp(2)

    return 'nao'









def alerta_impressao():
    sp(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\alerta_impressao.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('alerta_impressao localizado')
                sp(2)
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - alerta_impressao')
            tentativas += 1
        sp(3)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def alerta_Prodembalagens():
        sp(1)
        tentativas = 0
        while tentativas != 3:
            try:
                button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\alerta_Prodembalagens.png", confidence=0.9) #alterar o confidence sempre que não achar
                if button_location:
                    print('alerta_Prodembalagens localizado')
                    sp(2)
                    return 'sim'
            except:
                # py.press('esc',presses=2)
                print('tentando localizar - alerta_Prodembalagens')
                tentativas += 1
            sp(3)  # Espera 1 segundo antes de tentar novamente
        return 'nao'

def alerta_Retirada():
        sp(1)
        tentativas = 0
        while tentativas != 3:
            try:
                button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\alerta_Retirada.png", confidence=0.9) #alterar o confidence sempre que não achar
                if button_location:
                    print('alerta_Retirada localizado')
                    sp(2)
                    return 'sim'
            except:
                # py.press('esc',presses=2)
                print('tentando localizar - alerta_Retirada')
                tentativas += 1
            sp(3)  # Espera 1 segundo antes de tentar novamente
        return 'nao'



def aba_orcamento():
        sp(1)
        tentativas = 0
        while tentativas != 5:
            try:
                button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\aba_orcamento.png", confidence=0.9) #alterar o confidence sempre que não achar
                if button_location:
                    print('aba_orcamento localizado')
                    sp(2)
                    return 'sim'
            except:
                # py.press('esc',presses=2)
                print('tentando localizar - aba_orcamento')
                tentativas += 1
            sp(3)  # Espera 1 segundo antes de tentar novamente
        return 'nao'


def btn_OrcamentoDisable():
        sp(1)
        tentativas = 0
        while tentativas != 5:
            try:
                button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\btn_OrcamentoDisable.png", confidence=0.95) #alterar o confidence sempre que não achar
                if button_location:
                    print('btn_OrcamentoDisable localizado')

                    py.press('esc')
                    click_btn_sim()
                    sp(2)
                    py.press('f2')
                    py.press('enter')
                    return 'sim'
            except:
                # py.press('esc',presses=2)
                print('tentando localizar - btn_OrcamentoDisable')
                tentativas += 1
            sp(3)  # Espera 1 segundo antes de tentar novamente
        return 'nao'



def bnt_OKDISABLE():
    sp(1)
    tentativas = 0
    while tentativas != 5:
        try:
            button_location = py.locateOnScreen(r"C:\Users\Servidor\Documents\Project ODF\assets\btn_OKDisable.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('btn_OKDisable localizado')

                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - btn_OKDisable')
            tentativas += 1
        sp(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'
