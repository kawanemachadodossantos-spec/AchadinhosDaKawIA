import os
import sys
import time
import requests
from dotenv import load_dotenv

# Adiciona o diretório atual e a pasta 'src' ao caminho de busca do Python
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
sys.path.append(DIRETORIO_ATUAL)
sys.path.append(os.path.join(DIRETORIO_ATUAL, "src"))

# Tenta importar com ou sem o namespace 'src' para evitar falhas no Render
try:
    from buscador import buscar_ofertas_mercadolivre, buscar_ofertas_shopee
except ImportError:
    from src.buscador import buscar_ofertas_mercadolivre, buscar_ofertas_shopee

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def formatar_mensagem_mercadolivre(produto, cupom=""):
    """Gera o texto padronizado para ofertas do Mercado Livre"""
    nome = produto.get("nome", "")
    preco_antigo = produto.get("preco_antigo", produto.get("preco", 0))
    preco_atual = produto.get("preco", 0)
    link = produto.get("link", "")
    
    return (
        "💥💥 *CUPOM DE DESCONTO* 💥💥\n\n"
        f"🛍️ {nome}\n\n"
        f"~De R$ {preco_antigo}~\n"
        f"💥 *Por R$ {preco_atual}*\n\n"
        f"🏷️ *Use o Cupom: * {cupom}\n\n"
        f"🛒 Compre aqui 👉 {link}\n\n"
        "⚠️ *Promoção sujeita à alteração de preço e estoque do site*\n\n"
        "⚠️🚨 *ATENÇÃO: Valor promocional apenas utilizando o Cupom de Desconto*"
    )

def formatar_mensagem_shopee(produto, parcelamento="Em até 6x sem juros"):
    """Gera o texto padronizado para ofertas da Shopee"""
    nome = produto.get("nome", "")
    preco_antigo = produto.get("preco_antigo", produto.get("preco", 0))
    preco_atual = produto.get("preco", 0)
    link = produto.get("link", "")
    
    return (
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

def enviar_para_aprovacao(produto):
    """Envia a oferta formatada para aprovação no Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Token ou Chat ID do Telegram não configurados!")
        return

    origem = produto.get("origem", "mercadolivre")
    
    if origem == "shopee":
        mensagem_formatada = formatar_mensagem_shopee(produto)
    else:
        mensagem_formatada = formatar_mensagem_mercadolivre(produto)

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    texto_revisao = (
        f"🔎 <b>{produto.get('tipo_oferta', 'OFERTA ENCONTRADA')}</b>\n"
        "-----------------------------------\n\n"
        f"{mensagem_formatada}\n\n"
        "-----------------------------------\n"
        "<i>Deseja aprovar e enviar esta oferta?</i>"
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

    try:
        requests.post(url, json=payload)
        print(f"✅ Oferta enviada para aprovação: {produto['nome'][:30]}...")
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")

def iniciar():
    print("=================================")
    print("   INICIANDO BUSCA DE 100 OFERTAS")
    print("=================================")
    
    # 1. Busca 50 ofertas do Mercado Livre
    ofertas_ml = buscar_ofertas_mercadolivre(quantidade_total=50)
    print(f"📦 Encontradas {len(ofertas_ml)} ofertas do Mercado Livre.")

    # 2. Busca 50 ofertas da Shopee
    ofertas_shopee = buscar_ofertas_shopee(quantidade_total=50)
    print(f"📦 Encontradas {len(ofertas_shopee)} ofertas da Shopee.")

    # Junta todas as ofertas encontradas
    todas_ofertas = ofertas_ml + ofertas_shopee

    # Envia uma por uma para o seu painel de aprovação no Telegram
    for produto in todas_ofertas:
        enviar_para_aprovacao(produto)
        time.sleep(1) # Pausa de 1 segundo para não sobrecarregar a API do Telegram

if __name__ == "__main__":
    iniciar()
