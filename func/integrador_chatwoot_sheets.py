import requests
import gspread
from google.oauth2.service_account import Credentials
import os
import json
from dotenv import load_dotenv
from func.logger_config import get_logger

# Configura o logger para este módulo
logger = get_logger('integrador_chatwoot_sheets')

load_dotenv()

# CONFIGURACOES CHATWOOT
CHATWOOT_URL = os.getenv("CHATWOOT_URL")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
API_TOKEN = os.getenv("API_TOKEN")
TAG = "orçamento"

# CONFIGURACOES GOOGLE SHEETS
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credenciais.json")
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
SHEET_NAME = "medicamentos-farmacia"
WORKSHEET_NAME = "base_receita"

def buscar_conversas_chatwoot(label):
    """
    Busca conversas no Chatwoot com a label especificada.
    Retorna lista de IDs das conversas.
    """
    headers = {
        "Content-Type": "application/json",
        "api_access_token": API_TOKEN
    }
    
    url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/conversations/filter"
    
    payload = {
        "payload": [
            {
                "attribute_key": "labels",
                "filter_operator": "equal_to",
                "values": [label],
                "query_operator": None
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            logger.error(f"Erro Chatwoot {response.status_code}: {response.text}")
            return []
        
        data = response.json()
        conversas = data.get("payload") or data.get("data", {}).get("payload") or []
        
        # Extrai apenas os IDs das conversas
        ids_conversas = [conv.get('id') for conv in conversas if conv.get('id')]
        
        logger.info(f"Encontradas {len(ids_conversas)} conversas no Chatwoot com a tag '{label}'")
        logger.debug(f"IDs das conversas: {ids_conversas}")
        
        return ids_conversas
        
    except Exception as e:
        logger.error(f"Erro ao buscar conversas no Chatwoot: {str(e)}")
        return []

def conectar_google_sheets():
    """
    Conecta ao Google Sheets e retorna a worksheet.
    """
    try:
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            logger.error(f"Arquivo de credenciais nao encontrado: {SERVICE_ACCOUNT_FILE}")
            return None
        
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)
        
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_NAME)
        
        logger.info(f"Conectado ao Google Sheets - Planilha: {SHEET_NAME}, Aba: {WORKSHEET_NAME}")
        return worksheet
        
    except Exception as e:
        logger.error(f"Erro ao conectar ao Google Sheets: {str(e)}")
        return None

def buscar_variacoes_insumos():
    """
    Busca as variacoes dos insumos na aba 'base_insumos'.
    Retorna dicionario com medicamento como chave e lista de variacoes como valor.
    """
    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)
        
        sheet = client.open(SHEET_NAME)
        worksheet_insumos = sheet.worksheet("base_insumos")
        
        print("Conectado a aba base_insumos")
        
        # Le todos os dados da aba base_insumos
        dados_insumos = worksheet_insumos.get_all_records()
        print(f"Total de insumos na base: {len(dados_insumos)}")
        
        # Cria dicionario principal com medicamento -> variacoes
        mapa_variacoes = {}
        # Cria mapa reverso: variacao -> medicamento principal
        mapa_reverso = {}
        
        medicamentos_com_variacoes = 0
        
        for insumo in dados_insumos:
            descricao = insumo.get('descricao', '').strip()
            variacoes_str = insumo.get('variacoes', '').strip()
            
            if descricao:
                # Processa as variacoes (separadas por '-')
                if variacoes_str:
                    # Remove hifen final se existir
                    variacoes_str = variacoes_str.rstrip('-').strip()
                    
                    if variacoes_str:
                        variacoes_lista = [v.strip() for v in variacoes_str.split('-') if v.strip()]
                        
                        if variacoes_lista:  # So adiciona se realmente tem variacoes
                            mapa_variacoes[descricao] = variacoes_lista
                            medicamentos_com_variacoes += 1
                            
                            # Cria mapeamento reverso para cada variacao
                            for variacao in variacoes_lista:
                                mapa_reverso[variacao.lower()] = {
                                    'medicamento_principal': descricao,
                                    'todas_variacoes': variacoes_lista
                                }
                            
                            print(f"  {descricao} -> {len(variacoes_lista)} variacoes: {variacoes_lista}")
                        else:
                            mapa_variacoes[descricao] = []
                    else:
                        mapa_variacoes[descricao] = []
                else:
                    mapa_variacoes[descricao] = []
        
        print(f"Total de medicamentos na base: {len(mapa_variacoes)}")
        print(f"Medicamentos COM variacoes: {medicamentos_com_variacoes}")
        print(f"Mapa reverso criado com {len(mapa_reverso)} variacoes")
        
        # Adiciona o mapa reverso ao mapa principal para uso posterior
        mapa_variacoes['_mapa_reverso'] = mapa_reverso
        
        return mapa_variacoes
        
    except Exception as e:
        print(f"ERRO ao buscar variacoes de insumos: {str(e)}")
        return {}

def processar_medicamentos_com_variacoes(medicamentos_str, mapa_variacoes):
    """
    Processa a string de medicamentos e adiciona as variacoes encontradas.
    
    1. Busca EXATA na coluna 'descricao'
    2. Se nao encontrar, busca na coluna 'variacoes' separando por '-'
    3. Retorna todas as variacoes encontradas incluindo a descricao original
    
    Args:
        medicamentos_str: String com medicamentos separados por virgula
        mapa_variacoes: Dicionario com medicamento -> lista de variacoes
    
    Returns:
        String processada com variacoes no formato: "MedicamentoA:[Descricao,Var1,Var2], MedicamentoB"
    """
    if not medicamentos_str or not medicamentos_str.strip():
        return medicamentos_str
    
    # Extrai o mapa reverso
    mapa_reverso = mapa_variacoes.get('_mapa_reverso', {})
    
    # Cria um mapa case-insensitive para busca rapida nas descricoes principais
    mapa_insensitive = {}
    for med_original, variacoes in mapa_variacoes.items():
        if med_original != '_mapa_reverso':  # Ignora o mapa reverso
            mapa_insensitive[med_original.lower()] = (med_original, variacoes)
    
    # Separa os medicamentos por virgula
    medicamentos = [med.strip() for med in medicamentos_str.split(',') if med.strip()]
    
    medicamentos_processados = []
    
    for medicamento in medicamentos:
        medicamento_lower = medicamento.lower()
        encontrado = False
        
        print(f"  Buscando variacoes para: '{medicamento}'")
        
        # 1. Busca EXATA na coluna 'descricao'
        if medicamento_lower in mapa_insensitive:
            med_original, variacoes = mapa_insensitive[medicamento_lower]
            
            if variacoes:
                # Inclui a descricao original e as variacoes
                todas_opcoes = [med_original] + variacoes
                variacoes_str = ','.join(todas_opcoes)
                medicamento_com_variacoes = f"{medicamento}:[{variacoes_str}]"
                medicamentos_processados.append(medicamento_com_variacoes)
                print(f"    ENCONTRADO na descricao: '{med_original}' -> {len(todas_opcoes)} opcoes: {todas_opcoes}")
            else:
                medicamentos_processados.append(medicamento)
                print(f"    ENCONTRADO na descricao: '{med_original}' mas sem variacoes")
            encontrado = True
        
        # 2. Busca na coluna 'variacoes' (mapa reverso)
        elif medicamento_lower in mapa_reverso:
            info_reverso = mapa_reverso[medicamento_lower]
            med_principal = info_reverso['medicamento_principal']
            todas_variacoes = info_reverso['todas_variacoes']
            
            # Inclui a descricao principal e todas as variacoes
            todas_opcoes = [med_principal] + todas_variacoes
            variacoes_str = ','.join(todas_opcoes)
            medicamento_com_variacoes = f"{medicamento}:[{variacoes_str}]"
            medicamentos_processados.append(medicamento_com_variacoes)
            print(f"    ENCONTRADO nas variacoes de: '{med_principal}' -> {len(todas_opcoes)} opcoes: {todas_opcoes}")
            encontrado = True
        
        # 3. Busca parcial (caso nao encontre exato)
        if not encontrado:
            # Busca parcial na descricao
            melhor_match = None
            maior_score = 0
            
            palavras_medicamento = medicamento_lower.split()
            
            for descricao, variacoes in mapa_variacoes.items():
                if descricao != '_mapa_reverso':
                    descricao_lower = descricao.lower()
                    
                    # Conta quantas palavras do medicamento estao na descricao
                    score = 0
                    for palavra in palavras_medicamento:
                        if palavra in descricao_lower:
                            score += 1
                    
                    # Se encontrou pelo menos uma palavra
                    if score > 0 and score > maior_score:
                        maior_score = score
                        melhor_match = (descricao, variacoes)
            
            if melhor_match and maior_score > 0:
                descricao_encontrada, variacoes_encontradas = melhor_match
                
                if variacoes_encontradas:
                    # Inclui a descricao encontrada e as variacoes
                    todas_opcoes = [descricao_encontrada] + variacoes_encontradas
                    variacoes_str = ','.join(todas_opcoes)
                    medicamento_com_variacoes = f"{medicamento}:[{variacoes_str}]"
                    medicamentos_processados.append(medicamento_com_variacoes)
                    print(f"    ENCONTRADO parcial na descricao: '{descricao_encontrada}' -> {len(todas_opcoes)} opcoes: {todas_opcoes}")
                else:
                    medicamentos_processados.append(medicamento)
                    print(f"    ENCONTRADO parcial na descricao: '{descricao_encontrada}' mas sem variacoes")
                encontrado = True
        
        if not encontrado:
            # Se nao encontrou em lugar nenhum, mantem o nome original
            medicamentos_processados.append(medicamento)
            print(f"    NAO ENCONTRADO: {medicamento}")
    
    return ', '.join(medicamentos_processados)

def obter_dados_base_receita():
    """
    Funcao principal para obter dados da aba base_receita 
    com a estrutura especifica solicitada e incluir variacoes dos medicamentos.
    Retorna dados em formato JSON.
    """
    print("Iniciando integracao Chatwoot + Google Sheets (Base Receita)...")
    
    # 1. Buscar conversas no Chatwoot
    print("1. Buscando conversas no Chatwoot...")
    ids_conversas = buscar_conversas_chatwoot(TAG)
    
    if not ids_conversas:
        print("ERRO: Nenhuma conversa encontrada no Chatwoot.")
        return {"error": "Nenhuma conversa encontrada no Chatwoot", "data": []}
    
    # 2. Conectar ao Google Sheets (base_receita)
    print("2. Conectando ao Google Sheets (base_receita)...")
    worksheet = conectar_google_sheets()
    
    if not worksheet:
        print("ERRO: Nao foi possivel conectar ao Google Sheets.")
        return {"error": "Erro de conexao com Google Sheets", "data": []}
    
    # 3. Buscar variacoes de medicamentos
    print("3. Carregando variacoes de medicamentos da base_insumos...")
    mapa_variacoes = buscar_variacoes_insumos()
    
    # 4. Filtrar e processar dados da base_receita
    print("4. Processando dados da base_receita...")
    try:
        # Le todos os dados da planilha base_receita
        dados_receita = worksheet.get_all_records()
        print(f"Total de receitas na base: {len(dados_receita)}")
        
        # Filtra registros que tem conversation_id nas conversas do Chatwoot
        receitas_filtradas = []
        
        for receita in dados_receita:
            conversation_id = receita.get('conversation_id')
            status_receita = receita.get('status', '').lower().strip()
            
            # Filtra apenas receitas com status "consultado" e ignora "orçamento feito"
            if status_receita != 'consultado':
                if status_receita == 'orçamento feito':
                    print(f"Ignorando receita {conversation_id} - Status: '{status_receita}' (já processada)")
                else:
                    print(f"Ignorando receita {conversation_id} - Status: '{status_receita}' (não é 'consultado')")
                continue
            
            # Verifica se o conversation_id esta na lista de IDs do Chatwoot
            if conversation_id in ids_conversas:
                print(f"Processando receita {conversation_id} - Status: '{status_receita}'")
                
                # Processa medicamentos com variacoes
                medicamentos_originais = receita.get('medicamentos', '')
                
                if medicamentos_originais and mapa_variacoes:
                    print(f"\nProcessando medicamentos da receita {conversation_id}: {medicamentos_originais}")
                    medicamentos_processados = processar_medicamentos_com_variacoes(
                        medicamentos_originais, mapa_variacoes
                    )
                    receita['medicamentos_com_variacoes'] = medicamentos_processados
                    print(f"Resultado: {medicamentos_processados}")
                else:
                    receita['medicamentos_com_variacoes'] = medicamentos_originais
                
                # Estrutura os dados conforme solicitado
                receita_estruturada = {
                    'id': receita.get('id', ''),
                    'medicamentos': receita.get('medicamentos', ''),
                    'medicamentos_com_variacoes': receita.get('medicamentos_com_variacoes', ''),
                    'tipo': receita.get('tipo', ''),
                    'possologia': receita.get('possologia', ''),
                    'medico': receita.get('medico', ''),
                    'paciente': receita.get('paciente', ''),
                    'data_receita': receita.get('data_receita', ''),
                    'quantidade': receita.get('quantidade', ''),
                    'dosagem': receita.get('dosagem', ''),
                    'numero': str(receita.get('numero', '')),
                    'id_conversa': receita.get('id_conversa', ''),
                    'conversation_id': conversation_id,
                    'status': receita.get('status', '')
                }
                
                receitas_filtradas.append(receita_estruturada)
                print(f"Receita processada - ID: {conversation_id}")
        
        print(f"\nTotal de receitas processadas: {len(receitas_filtradas)}")
        
        # 5. Formatar resultado final em JSON
        resultado = {
            "status": "success",
            "total_conversas_chatwoot": len(ids_conversas),
            "total_receitas_processadas": len(receitas_filtradas),
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "data": receitas_filtradas
        }
        
        print("Dados estruturados em JSON com sucesso!")
        return resultado
        
    except Exception as e:
        print(f"ERRO ao processar dados da base_receita: {str(e)}")
        return {"error": f"Erro ao processar dados: {str(e)}", "data": []}

def main():
    """
    Funcao principal que executa o processo completo e retorna JSON formatado.
    """
    resultado = obter_dados_base_receita()
    
    # Imprime o JSON formatado
    print("\n" + "="*80)
    print("RESULTADO FINAL EM JSON:")
    print("="*80)
    
    json_formatado = json.dumps(resultado, indent=2, ensure_ascii=False)
    print(json_formatado)
    
    print("="*80)
    
    return resultado

def obter_dados_json():
    """
    Funcao especifica para obter os dados em formato JSON.
    Esta e a funcao principal a ser chamada para integracao com outros sistemas.
    """
    return obter_dados_base_receita()



def enviar_chatwoot_nota(num_id_conversa, num_orcamento):
    """
    Envia uma nota privada para uma conversa do Chatwoot com tag 'resolvido'.
    """
    url = f"https://chatwoot.atagenciaia.site/api/v1/accounts/1/conversations/{num_id_conversa}/messages"

    headers = {
        "Content-Type": "application/json",
        "api_access_token": API_TOKEN  # sua variável com token
    }

    payload = {
        "content": f"📢 Número do orçamento -> {num_orcamento}",
        "private": True
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"✅ Nota privada enviada para conversa {num_id_conversa} com tag 'resolvido'")
        return True
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro ao enviar nota para Chatwoot: {e}")
        print("Resposta:", response.text)
        return False
    


def atualizar_status_receita(id_receita, novo_status="orçamento feito"):
    """
    Atualiza o status de uma receita específica no Google Sheets baseado no ID único da receita.
    
    Args:
        id_receita: ID único da receita para localizar a linha (coluna 'id')
        novo_status: Novo status a ser definido (padrão: "orçamento feito")
    
    Returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário
    """
    try:
        # Conecta ao Google Sheets
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)
        
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_NAME)
        
        print(f"Atualizando status para ID da receita: {id_receita}")
        
        # Busca todos os dados
        dados = worksheet.get_all_records()
        
        # Procura a linha correspondente ao ID da receita
        linha_encontrada = None
        for i, linha in enumerate(dados, start=2):  # start=2 porque a linha 1 é cabeçalho
            if linha.get('id') == id_receita:
                linha_encontrada = i
                break
        
        if linha_encontrada:
            # Atualiza o status na coluna correspondente
            # Primeiro, precisa descobrir qual coluna é 'status'
            cabecalhos = worksheet.row_values(1)
            try:
                coluna_status = cabecalhos.index('status') + 1  # +1 porque gspread usa 1-indexado
                
                # Atualiza a célula
                worksheet.update_cell(linha_encontrada, coluna_status, novo_status)
                
                print(f"✅ Status atualizado para '{novo_status}' na linha {linha_encontrada}, coluna {coluna_status}")
                return True
                
            except ValueError:
                print("❌ Coluna 'status' não encontrada na planilha")
                return False
        else:
            print(f"❌ ID da receita {id_receita} não encontrado na planilha")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao atualizar status no Google Sheets: {str(e)}")
        return False


def atualizar_tags_chatwoot(num_id_conversa):
    url = f"https://chatwoot.atagenciaia.site/api/v1/accounts/1/conversations/{num_id_conversa}/labels"
    

    headers = {
        "Content-Type": "application/json",
        "api_access_token": API_TOKEN  # sua variável com token
    }

    # ✅ Aqui definimos as tags finais (sem 'orçamento', com 'resolvido')
    payload = {
        "labels": ["resolvida"]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"🏷️ Tags atualizadas para conversa {num_id_conversa}: {payload['labels']}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao atualizar tags: {e}")
        print("Resposta:", response.text)
        return False