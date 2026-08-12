import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def iniciar_bot():
    print("=================================")
    print("    ACHADINHOS DA KAW IA BOT")
    print("=================================")
    
    if not TELEGRAM_BOT_TOKEN:
        print("⚠️ Token do Telegram não configurado no arquivo .env!")
        return

    # Teste de conexão com a API do Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        nome_bot = dados.get("result", {}).get("first_name")
        print(f"✅ Sucesso! Bot conectado: {nome_bot}")
    else:
        print("❌ Erro ao conectar com a API do Telegram. Verifique o Token.")

if __name__ == "__main__":
    iniciar_bot()
