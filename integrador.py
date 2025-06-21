import json
from url_collector import coletar_urls_categoria, salvar_dados
from scraper import processar_urls
import pandas as pd
from datetime import datetime

def coletar_e_processar(categorias, modo_teste=True):
    """
    Coleta URLs das categorias especificadas e processa os dados nutricionais.
    
    Args:
        categorias (dict): Dicionário com nome e URL das categorias
        modo_teste (bool): Se True, executa em modo de teste com limitações
    """
    print("Iniciando coleta e processamento de dados...")
    
    todas_urls = []
    
    # Parâmetros para modo de teste
    max_paginas = 2 if modo_teste else None
    max_urls_por_pagina = 25 if modo_teste else None
    max_scrolls = 3 if modo_teste else None
    
    # Coleta URLs de todas as categorias
    for nome, url in categorias.items():
        print(f"\nColetando URLs da categoria: {nome}")
        
        # Coleta URLs da categoria
        urls_categoria = coletar_urls_categoria(
            url,
            categoria_nome=nome,
            max_paginas=max_paginas,
            max_urls_por_pagina=max_urls_por_pagina,
            max_scrolls=max_scrolls
        )
        
        todas_urls.extend(urls_categoria)
        
        # Salva os dados desta categoria separadamente
        prefixo = 'teste_' if modo_teste else ''
        salvar_dados(urls_categoria, prefixo=f'{prefixo}{nome}_')
        
        # Se estiver em modo de teste e já tiver 100 URLs, para
        if modo_teste and len(todas_urls) >= 100:
            print("Limite de 100 URLs atingido!")
            break
    
    # Salva todas as URLs em um único arquivo
    prefixo = 'teste_' if modo_teste else ''
    salvar_dados(todas_urls, prefixo=f'{prefixo}todas_')
    
    # Extrai apenas as URLs do JSON para processar
    urls_para_processar = [item['url'] for item in todas_urls]
    
    print(f"\nIniciando coleta de dados nutricionais para {len(urls_para_processar)} URLs...")
    
    # Processa as URLs para coletar dados nutricionais
    processar_urls(urls_para_processar)
    
    print("\nProcesso completo!")
    print(f"Total de URLs processadas: {len(urls_para_processar)}")
    
    # Tenta combinar os dados nutricionais com as informações das categorias
    try:
        # Lê o CSV com dados nutricionais
        df_nutri = pd.read_csv('dados_nutricionais.csv')
        
        # Cria um DataFrame com as informações das URLs
        df_urls = pd.DataFrame(todas_urls)
        
        # Combina os dois DataFrames
        df_final = pd.merge(df_nutri, df_urls, left_on='URL', right_on='url', how='left')
        
        # Remove a coluna 'url' duplicada
        df_final = df_final.drop('url', axis=1)
        
        # Salva o arquivo final
        prefixo = 'teste_' if modo_teste else ''
        arquivo_final = f'{prefixo}dados_nutricionais_completos.csv'
        df_final.to_csv(arquivo_final, index=False)
        print(f"\nDados completos salvos em {arquivo_final}")
        
    except Exception as e:
        print(f"\nAviso: Não foi possível combinar os dados: {e}")
        print("Os dados nutricionais ainda estão disponíveis em 'dados_nutricionais.csv'")

if __name__ == "__main__":
    # Define as categorias para coleta
    categorias = {
        'alimentos_refrigerados': 'https://www.paodeacucar.com/categoria/alimentos/alimentos-refrigerados?s=relevance',
        'doces_sobremesas': 'https://www.paodeacucar.com/categoria/alimentos/doces-e-sobremesas?s=relevance'
    }
    
    # Executa sem limitações
    coletar_e_processar(categorias, modo_teste=False) 