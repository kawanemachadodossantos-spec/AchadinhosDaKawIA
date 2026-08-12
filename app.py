import os
import sys
import time
import requests
from dotenv import load_dotenv

# 1. Garante que o Python encontre o buscador.py no servidor do PythonAnywhere
PASTA_SRC = '/home/Kawane/bot/src'
if PASTA_SRC not in sys.path:
    sys.path.insert(0, PASTA_SRC)

# Também adiciona o diretório atual como fallback
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
if DIRETORIO_ATUAL not in sys.path:
    sys.path.insert(0, DIRETORIO_ATUAL)

# 2. Importação do buscador
from buscador import buscar_ofertas_mercadolivre, buscar_ofertas_shopee

# 3. Carrega as variáveis do arquivo .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_mensagem_telegram(mensagem):
    """Envia uma mensagem de texto para o canal/grupo do Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Token do Telegram ou Chat ID não configurados no arquivo .env!")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Mensagem enviada com sucesso para o Telegram!")
        else:
            print(f"❌ Erro ao enviar mensagem ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Erro de conexão ao enviar para o Telegram: {e}")

def executar_busca():
    """Executa as buscas nos buscadores e envia os resultados."""
    print("🔎 Iniciando busca por ofertas...")
    
    # Busca ofertas do Mercado Livre
    try:
        ofertas_ml = buscar_ofertas_mercadolivre()
        if ofertas_ml:
            print(f"📦 Encontradas {len(ofertas_ml)} ofertas no Mercado Livre.")
            for oferta in ofertas_ml:
                # Adapte os campos conforme o retorno da sua função no buscador.py
                texto = f"🔥 <b>{oferta.get('titulo', 'Oferta')}</b>\n\n💰 Preço: {oferta.get('preco', 'Confira no site')}\n🔗 Link: {oferta.get('link', '')}"
                enviar_mensagem_telegram(texto)
                time.sleep(2) # Pausa rápida para não estourar limite de mensagens da API
        else:
            print("Nenhuma oferta encontrada no Mercado Livre.")
    except Exception as e:
        print(f"❌ Erro ao buscar ofertas do Mercado Livre: {e}")

    # Busca ofertas da Shopee
    try:
        ofertas_shopee = buscar_ofertas_shopee()
        if ofertas_shopee:
            print(f"📦 Encontradas {len(ofertas_shopee)} ofertas na Shopee.")
            for oferta in ofertas_shopee:
                texto = f"🛍️ <b>{oferta.get('titulo', 'Oferta Shopee')}</b>\n\n💰 Preço: {oferta.get('preco', 'Confira no site')}\n🔗 Link: {oferta.get('link', '')}"
                enviar_mensagem_telegram(texto)
                time.sleep(2)
        else:
            print("Nenhuma oferta encontrada na Shopee.")
    except Exception as e:
        print(f"❌ Erro ao buscar ofertas da Shopee: {e}")

if __name__ == "__main__":
    print("🚀 Bot Achadinhos iniciado com sucesso!")
    executar_busca()
