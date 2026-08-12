import requests

CATEGORIAS = [
    "cozinha", 
    "casa", 
    "decoracao", 
    "achadinhos", 
    "automoveis", 
    "limpeza"
]

def buscar_ofertas_mercadolivre(quantidade_total=50):
    """
    Busca Ofertas e Promoções por categoria no Mercado Livre via API oficial.
    """
    url = "https://api.mercadolibre.com/sites/MLB/search"
    todas_ofertas = []
    ids_processados = set() # Evita produtos duplicados
    
    # Quantidade de itens para buscar por categoria
    qtd_por_cat = max(5, quantidade_total // len(CATEGORIAS))
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    for cat in CATEGORIAS:
        params = {
            "q": cat,
            "limit": qtd_por_cat,
            "sort": "relevance"
        }
        
        try:
            res = requests.get(url, params=params, headers=headers, timeout=10)
            if res.status_code == 200:
                dados = res.json()
                for item in dados.get("results", []):
                    item_id = item.get("id")
                    
                    # Filtra para não adicionar o mesmo produto duas vezes
                    if item_id in ids_processados:
                        continue
                        
                    ids_processados.add(item_id)
                    
                    preco_atual = item.get("price", 0)
                    preco_antigo = item.get("original_price") or preco_atual
                    
                    todas_ofertas.append({
                        "id": item_id,
                        "nome": item.get("title", "Sem título"),
                        "preco": preco_atual,
                        "preco_antigo": preco_antigo,
                        "link": item.get("permalink", ""),
                        "imagem": item.get("thumbnail", ""),
                        "tipo_oferta": f"🔥 ACHADINHO: {cat.upper()}",
                        "origem": "mercadolivre"
                    })
            else:
                print(f"⚠️ Alerta ML [{cat}]: Status {res.status_code}")
                
        except Exception as e:
            print(f"❌ Erro ao buscar categoria '{cat}' no ML: {e}")

    return todas_ofertas[:quantidade_total]


def buscar_ofertas_shopee(quantidade_total=50):
    """
    Busca Ofertas via API Pública de Busca da Shopee.
    """
    url = "https://shopee.com.br/api/v4/search/search_items"
    todas_ofertas = []
    ids_processados = set()
    
    qtd_por_cat = max(5, quantidade_total // len(CATEGORIAS))
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://shopee.com.br/"
    }

    for cat in CATEGORIAS:
        params = {
            "keyword": cat,
            "limit": qtd_por_cat,
            "newest": 0,
            "order": "desc",
            "page_type": "search",
            "scenario": "PAGE_GLOBAL_SEARCH"
        }
        
        try:
            res = requests.get(url, params=params, headers=headers, timeout=10)
            if res.status_code == 200:
                dados = res.json()
                items = dados.get("items", [])
                
                for entry in items:
                    item_info = entry.get("item_basic", {})
                    item_id = item_info.get("itemid")
                    shop_id = item_info.get("shopid")
                    
                    if not item_id or item_id in ids_processados:
                        continue
                        
                    ids_processados.add(item_id)
                    
                    # Shopee retorna preços multiplicados por 100.000 (cents/unit)
                    preco_atual = item_info.get("price", 0) / 100000
                    preco_antigo = item_info.get("price_before_discount", 0) / 100000
                    if preco_antigo == 0:
                        preco_antigo = preco_atual

                    # Monta o link do produto na Shopee
                    nome = item_info.get("name", "Produto Shopee")
                    nome_slug = nome.lower().replace(" ", "-")
                    link = f"https://shopee.com.br/{nome_slug}-i.{shop_id}.{item_id}"

                    todas_ofertas.append({
                        "id": str(item_id),
                        "nome": nome,
                        "preco": round(preco_atual, 2),
                        "preco_antigo": round(preco_antigo, 2),
                        "link": link,
                        "imagem": f"https://down-br.img.susercontent.com/file/{item_info.get('image')}",
                        "tipo_oferta": f"🟠 SHOPEE: {cat.upper()}",
                        "origem": "shopee"
                    })
            else:
                print(f"⚠️ Alerta Shopee [{cat}]: Status {res.status_code}")
                
        except Exception as e:
            print(f"❌ Erro ao buscar categoria '{cat}' na Shopee: {e}")

    return todas_ofertas[:quantidade_total]
