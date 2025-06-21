# Pão de Queijo Scraping

Este projeto coleta dados nutricionais de produtos do site do Pão de Açúcar.

## Funcionalidades

- Coleta URLs de produtos das categorias:
  - Alimentos Refrigerados
  - Doces e Sobremesas
- Extrai informações nutricionais de cada produto
- Salva os dados em formato CSV e JSON

## Requisitos do Sistema

- Windows 10 ou superior
- Chromium ou Google Chrome instalado
- Conexão com a internet

## Instalação

### Usuários Windows (Executável)

1. Baixe o arquivo `PaoDeQueijo_Scraper.exe` da pasta `dist`
2. Execute o arquivo clicando duas vezes

### Desenvolvedores (Código Fonte)

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/pao_de_queijo_scraping.git
cd pao_de_queijo_scraping
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Para gerar o executável:
```bash
python build.py
```

## Uso

1. Execute o programa (executável ou via Python)
2. O programa irá:
   - Coletar URLs dos produtos
   - Extrair dados nutricionais
   - Salvar os resultados em arquivos CSV e JSON

## Arquivos Gerados

- `dados_nutricionais.csv`: Dados nutricionais de todos os produtos
- `dados_nutricionais_completos.csv`: Dados nutricionais + informações das categorias
- `[categoria]_urls.csv`: URLs dos produtos por categoria
- `[categoria]_urls.json`: URLs e metadados por categoria

## Observações

- O programa pode levar alguns minutos para coletar todos os dados
- É necessário ter uma conexão estável com a internet
- O Chromium/Chrome deve estar instalado no sistema

## Suporte

Para problemas ou sugestões, abra uma issue no GitHub.
