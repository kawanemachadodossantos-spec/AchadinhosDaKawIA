import os
from dotenv import load_dotenv
from src.buscador import buscar_produtos_mercadolivre

# Carrega as variáveis de ambiente
load_dotenv()

def iniciar():
    print("=================================")
    print("       OFERTAS BOT (IA)")
    print("=================================")
    print("\nBuscando produtos no Mercado Livre...\n")

    # Teste de busca por um termo de exemplo
    produtos = buscar_produtos_mercadolivre("organizador de cozinha")

    if not produtos:
        print("Nenhum produto encontrado ou erro na busca.")
        return

    print(f"✅ Encontrados {len(produtos)} produtos:\n")
    for index, produto in enumerate(produtos, start=1):
        print(f"{index}. {produto['nome']}")
        print(f"   Preço: R$ {produto['preco']}")
        print(f"   Link: {produto['link']}\n")

if __name__ == "__main__":
    iniciar()
