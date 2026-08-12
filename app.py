import os
import requests
from dotenv import load_dotenv
from src.buscador import buscar_produtos_mercadolivre

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def formatar_mensagem_mercadolivre(produto, cupom=""):
    """Gera o texto padronizado para ofertas do Mercado Livre"""
    nome = produto.get("nome", "")
    preco_antigo = produto.get("preco_antigo", produto.get("preco", 0))
    preco_atual = produto.get("preco", 0)
    link = produto.get("link", "")
    
    texto = (
        "💥💥 *CUPOM DE DESCONTO* 💥💥\n\n"
        f"🛍️ {nome}\n\n"
        f"~De R$ {preco_antigo}~\n"
        f"💥 *Por R$ {preco_atual}*\n\n"
        f"🏷️ *Use o Cupom: * {cupom}\n\n"
        f"🛒 Compre aqui 👉 {link}\n\n"
        "⚠️ *Promoção sujeita à alteração de preço e estoque do site*\n\n"
        "⚠️🚨 *ATENÇÃO: Valor promocional apenas utilizando o Cupom de Desconto*"
    )
    return texto

def formatar_mensagem_shopee(produto, parcelamento="Em até 6x sem juros"):
    """Gera o texto padronizado para ofertas da Shopee"""
    nome = produto.get("nome", "")
    preco_antigo = produto.get("preco_antigo", produto.get("preco", 0))
    preco_atual = produto.get("preco", 0)
    link = produto.get("link", "")
    
    texto = (
        f"🛍️ {nome}\n\n"
        f"~De R$ {preco_antigo}~\n"
        f"🔥*Por R$ {preco_atual}*\n\n"
        f"💳 {parcelamento}\n\n"
        f"🛒 Compre aqui 👉 {link}\n\n"
        "⚠️ *Preço e estoque sujeitos a alterações no site.*\n\n"
        "⭐ *Oferta Exclusiva por Tempo Limitado!* Só para quem viu aqui 🤝\n\n"
        "🎟️ *CUPONS DISPONÍVEIS AQUI:*\n"
        "https://s.shopee.com.br/30mGe2PWLQ"
    )
    return texto

def enviar_para_aprovacao(produto, origem="mercadolivre"):
    """Envia a oferta para o seu Telegram privado para você aprovar ou rejeitar"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Token ou Chat ID do Telegram não configurados!")
        return

    # Gera a prévia da mensagem final formatada
    if origem == "shopee":
        mensagem_formatada = formatar_mensagem_shopee(produto)
    else:
        mensagem_formatada = formatar_mensagem_mercadolivre(produto)

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    texto_revisao = (
        f"🔎 <b>NOVA OFERTA ENCONTRADA ({origem.upper()})</b>\n"
        "-----------------------------------\n\n"
        f"{mensagem_formatada}\n\n"
        "-----------------------------------\n"
        "<i>Deseja aprovar e enviar esta oferta formatada?</i>"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto_revisao,
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "🟢 Aprovar", "callback_data": f"aprovar_{origem}_{produto['id']}"},
                    {"text": "🔴 Rejeitar", "callback_data": f"rejeitar_{produto['id']}"}
                ]
            ]
        }
    }

    resposta = requests.post(url, json=payload)
    if resposta.status_code == 200:
        print("✅ Oferta enviada para sua aprovação no Telegram!")
    else:
        print(f"❌ Erro ao enviar mensagem: {resposta.text}")

def iniciar():
    print("=================================")
    print("   SISTEMA DE PAINEL DE APROVAÇÃO")
    print("=================================")
    
    # Exemplo testando busca no Mercado Livre
    produtos = buscar_produtos_mercadolivre("organizador de cozinha")
    if produtos:
        enviar_para_aprovacao(produtos[0], origem="mercadolivre")

if __name__ == "__main__":
    iniciar()
