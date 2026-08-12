import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente a partir do arquivo .env
load_dotenv()

class Config:
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    # Shopee Afiliados
    SHOPEE_APP_ID = os.getenv("SHOPEE_APP_ID")
    SHOPEE_SECRET = os.getenv("SHOPEE_SECRET")
    
    # Mercado Livre (se for utilizar)
    MERCADOLIVRE_CLIENT_ID = os.getenv("MERCADOLIVRE_CLIENT_ID")
    MERCADOLIVRE_CLIENT_SECRET = os.getenv("MERCADOLIVRE_CLIENT_SECRET")
