import os
import time
from url_collector import URLCollector
from scraper import Scraper
from datetime import datetime

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu():
    print("\n=== Menu do Coletor de Dados do Pão de Açúcar ===")
    print("1. Coletar URLs dos produtos (Modo Teste - máx. 50 URLs)")
    print("2. Coletar URLs dos produtos (Modo Completo)")
    print("3. Fazer scraping dos dados nutricionais")
    print("4. Executar coleta completa (URLs + Dados)")
    print("5. Sair")
    print("\n")

def escolher_categoria():
    print("\nEscolha a categoria para coletar URLs:")
    print("1. Alimentos Congelados")
    print("2. Doces e Sobremesas")
    print("3. Ambas as categorias")
    
    while True:
        opcao = input("\nDigite o número da categoria (1-3): ")
        if opcao in ['1', '2', '3']:
            return opcao
        print("Opção inválida! Por favor, escolha entre 1 e 3.")

def coletar_urls(modo_teste=True):
    print("\nIniciando coleta de URLs...")
    collector = URLCollector(modo_teste=modo_teste)
    
    # URLs das categorias
    urls_categorias = {
        '1': {
            'url': "https://www.paodeacucar.com/categoria/alimentos/alimentos-congelados?s=relevance&p=1",
            'nome': "Alimentos Congelados"
        },
        '2': {
            'url': "https://www.paodeacucar.com/categoria/alimentos/doces-e-sobremesas?s=relevance&p=1",
            'nome': "Doces e Sobremesas"
        }
    }
    
    categoria = escolher_categoria()
    todas_urls = []
    
    if categoria == '3':
        # Coletar de ambas as categorias
        for cat_info in urls_categorias.values():
            print(f"\nColetando URLs da categoria: {cat_info['nome']}")
            urls = collector.coletar_urls(cat_info['url'])
            todas_urls.extend(urls)
    else:
        # Coletar de uma categoria específica
        cat_info = urls_categorias[categoria]
        print(f"\nColetando URLs da categoria: {cat_info['nome']}")
        todas_urls = collector.coletar_urls(cat_info['url'])
    
    # Salvar todas as URLs coletadas
    collector.salvar_urls_csv(todas_urls)
    print("\nURLs coletadas e salvas em urls_coletadas.csv")
    return "urls_coletadas.csv"

def fazer_scraping(arquivo_urls=None):
    arquivo_urls = arquivo_urls or "urls_coletadas.csv"
    
    if not os.path.exists(arquivo_urls):
        print("\nArquivo de URLs não encontrado! Execute a coleta de URLs primeiro.")
        return

    print(f"\nIniciando scraping dos dados usando o arquivo {arquivo_urls}...")
    scraper = Scraper()
    scraper.processar_arquivo_urls(arquivo_urls)
    print("\nScraping concluído! Dados salvos em dados_nutricionais.csv")

def main():
    while True:
        limpar_tela()
        exibir_menu()
        
        try:
            opcao = input("Escolha uma opção (1-5): ")
            
            if opcao == "1":
                arquivo_urls = coletar_urls(modo_teste=True)
                input("\nPressione Enter para continuar...")
                
            elif opcao == "2":
                arquivo_urls = coletar_urls(modo_teste=False)
                input("\nPressione Enter para continuar...")
                
            elif opcao == "3":
                fazer_scraping()
                input("\nPressione Enter para continuar...")
                
            elif opcao == "4":
                print("\nIniciando processo completo...")
                modo_teste = input("\nDeseja executar em modo de teste? (s/n): ").lower() == 's'
                arquivo_urls = coletar_urls(modo_teste=modo_teste)
                time.sleep(2)  # Pequena pausa para o usuário ler a mensagem
                fazer_scraping(arquivo_urls)
                input("\nPressione Enter para continuar...")
                
            elif opcao == "5":
                print("\nSaindo do programa...")
                break
                
            else:
                print("\nOpção inválida! Por favor, escolha uma opção entre 1 e 5.")
                time.sleep(2)
                
        except Exception as e:
            print(f"\nOcorreu um erro: {str(e)}")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main() 