import requests
import os
from dotenv import load_dotenv

# 🔧 Carrega variáveis do .env
load_dotenv()

# 🔧 CONFIGURAÇÕES
CHATWOOT_URL = "https://chatwoot.atagenciaia.site"
ACCOUNT_ID = 1
TAG = "orçamento"

headers = {
    "Content-Type": "application/json",
    "api_access_token": os.getenv("API_TOKEN")
}

def filtrar_conversas_por_label(label):
    """
    Busca conversas filtrando por label específica.
    """
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

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"❌ Erro {response.status_code}: {response.text}")
        return []

    data = response.json()
    return data.get("payload") or data.get("data", {}).get("payload") or []

if __name__ == "__main__":
    print(f"🔎 Buscando conversas com a tag '{TAG}'...")
    conversas = filtrar_conversas_por_label(TAG)

    print(f"✅ Encontradas {len(conversas)} conversas com a tag '{TAG}'\n")

    for conv in conversas:
        contato = conv.get('meta', {}).get('sender', {})
        print(f"🗨️  ID: {conv.get('id')}")
        print(f"👤 Contato: {contato.get('name', 'Desconhecido')}")
        print(f"📞 Telefone: {contato.get('phone_number', 'Não disponível')}")
        print(f"📌 Labels: {conv.get('labels')}")
        print("-" * 80)
