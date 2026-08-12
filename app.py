import os
import requests
from dotenv import load_dotenv
from src.buscador import buscar_produtos_mercadolivre

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") # Seu ID privado no Telegram

def enviar_para_aprovacao(produto):
    """Envia o achadinho para o seu Telegram privado com botões de aprovação"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Token ou Chat ID do Telegram não configurados!")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    texto = (
        f"🔎 <b>OFERTA ENCONTRADA PARA REVISÃO</b>\n\n"
        f"📦 <b>Produto:</b> {produto['nome']}\n"
        f"💰 <b>Preço:</b> R$ {produto['preco']}\n"
        f"🔗 <b>Link:</b> {produto['link']}\n\n"
        f"<i>Deseja enviar esta oferta para o grupo do WhatsApp?</i>"
    )

    # Botões interativos
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "🟢 Aprovar e Enviar p/ WhatsApp", "callback_data": f"aprovar_{produto['id']}"},
                    {"text": "🔴 Recusar", "callback_data": f"recusar_{produto['id']}"}
                ]
            ]
        }
    }

    resposta = requests.post(url, json=payload)
    if resposta.status_code == 200:
        print("✅ Oferta enviada para o seu Telegram para aprovação!")
    else:
        print(f"❌ Erro ao enviar mensagem de aprovação: {resposta.text}")

def iniciar():
    print("=================================")
    print("   SISTEMA DE PAINEL DE APROVAÇÃO")
    print("=================================")
    
    produtos = buscar_produtos_mercadolivre("organizador de cozinha")
    if produtos:
        # Envia a primeira oferta encontrada para sua aprovação
        enviar_para_aprovacao(produtos[0])

if __name__ == "__main__":
    iniciar()
