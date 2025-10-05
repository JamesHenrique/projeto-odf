import gspread
from google.oauth2.service_account import Credentials
import os

# 🔧 Caminho para suas credenciais (no diretório pai)
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credenciais.json")

# 🔧 Escopos de permissão (mais completos)
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    # 🔐 Cria a credencial
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Arquivo de credenciais não encontrado: {SERVICE_ACCOUNT_FILE}")
        exit(1)
    
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    
    # 🔗 Conecta ao Google Sheets
    client = gspread.authorize(creds)
    
    # 🔍 Abre a planilha pelo nome ou ID
    SHEET_NAME = "medicamentos-farmacia"
    print(f"🔍 Tentando abrir a planilha: {SHEET_NAME}")
    
    sheet = client.open(SHEET_NAME)
    print(f"✅ Planilha '{SHEET_NAME}' aberta com sucesso!")
    
    # 📘 Seleciona uma aba específica (por nome)
    worksheet = sheet.worksheet("base_receita")
    print(f"✅ Aba 'base_receita' selecionada com sucesso!")
    
    # 🔄 Lê todos os dados da aba
    dados = worksheet.get_all_records()
    
    print(f"📋 Dados da aba ({len(dados)} registros):")
    for i, linha in enumerate(dados[:5], 1):  # Mostra apenas os primeiros 5 registros
        print(f"  {i}. {linha}")
    
    if len(dados) > 5:
        print(f"  ... e mais {len(dados) - 5} registros")

except gspread.exceptions.SpreadsheetNotFound:
    print(f"❌ Planilha '{SHEET_NAME}' não encontrada.")
    print("   Verifique se:")
    print("   - O nome da planilha está correto")
    print("   - A planilha foi compartilhada com: odf-project@n8n-farm-manipulacao.iam.gserviceaccount.com")
    print("   - O email de serviço tem permissão de visualização/edição")

except gspread.exceptions.WorksheetNotFound:
    print(f"❌ Aba 'base_receita' não encontrada na planilha.")
    print("   Abas disponíveis:")
    try:
        for ws in sheet.worksheets():
            print(f"   - {ws.title}")
    except:
        print("   Não foi possível listar as abas")

except Exception as e:
    print(f"❌ Erro geral: {str(e)}")
    print(f"   Tipo do erro: {type(e).__name__}")
