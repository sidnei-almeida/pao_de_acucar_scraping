# 🛒 Pão de Açucar Scraping

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Selenium](https://img.shields.io/badge/selenium-4.0%2B-orange.svg)](https://www.selenium.dev/)
[![Pandas](https://img.shields.io/badge/pandas-latest-blue.svg)](https://pandas.pydata.org/)

## 📝 Descrição

O Pão de Açucar Scraping é um web scraper automatizado desenvolvido para coletar dados nutricionais de produtos do site do Pão de Açúcar. O projeto utiliza técnicas avançadas de web scraping com Selenium para navegar de forma eficiente pelo site e extrair informações detalhadas sobre os produtos.

## 🌟 Funcionalidades Principais

- 🔍 **Coleta Inteligente de URLs**
  - Navegação automática por categorias de produtos
  - Sistema de scrolling dinâmico para carregamento de mais produtos
  - Coleta de URLs únicas evitando duplicatas

- 📊 **Extração de Dados Nutricionais**
  - Informações nutricionais detalhadas
  - Dados de porções e medidas
  - Categorização dos produtos

- 💾 **Armazenamento e Exportação**
  - Exportação em formato CSV e JSON
  - Logs detalhados do processo de scraping
  - Sistema de backup automático

## 🏗️ Arquitetura do Projeto

```
pao_de_acucar_scraping/
├── browser_config.py      # Configurações do navegador e Selenium
├── url_collector.py       # Módulo de coleta de URLs
├── scraper.py            # Core do scraping de dados
├── scraping_log.py       # Sistema de logging
├── main.py               # Ponto de entrada da aplicação
└── requirements.txt      # Dependências do projeto
```

## 🔧 Requisitos do Sistema

### Requisitos de Hardware
- Processador: 1.6 GHz ou superior
- Memória RAM: 4GB mínimo (8GB recomendado)
- Espaço em Disco: 500MB livre
- Conexão com a Internet: 5Mbps ou superior

### Requisitos de Software
- Python 3.8 ou superior
- Google Chrome ou Chromium
- Sistema Operacional:
  - Windows 10/11
  - Linux (kernel 4.x ou superior)
  - macOS 10.14 ou superior

## 📦 Instalação

### Via pip (Recomendado)

```bash
# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
.\venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt
```

### Via Docker

```bash
# Construir a imagem
docker build -t pao-de-acucar-scraper .

# Executar o container
docker run -v $(pwd)/data:/app/data pao-de-acucar-scraper
```

## 🚀 Uso

### Execução Básica

```bash
python main.py
```

### Opções de Configuração

```bash
python main.py --max-urls 100 --categories "Alimentos,Bebidas" --debug
```

### Parâmetros Disponíveis

| Parâmetro | Descrição | Padrão |
|-----------|-----------|--------|
| --max-urls | Número máximo de URLs | 10 |
| --scroll-limit | Limite de rolagens | 2 |
| --page-limit | Limite de páginas | 1 |
| --debug | Modo debug | False |

## 📊 Estrutura dos Dados

### Formato do CSV de Saída

```csv
produto,energia_kcal,proteinas_g,carboidratos_g,gorduras_totais_g,gorduras_saturadas_g,fibra_alimentar_g,sodio_mg
Produto A,150,8,20,6,2,1,200
```

### Campos Coletados

- **Informações Básicas**
  - Nome do produto
  - Marca
  - Categoria
  - Subcategoria

- **Dados Nutricionais**
  - Valor energético (kcal)
  - Proteínas (g)
  - Carboidratos (g)
  - Gorduras totais (g)
  - Gorduras saturadas (g)
  - Fibra alimentar (g)
  - Sódio (mg)

## 📝 Logs e Monitoramento

O sistema mantém logs detalhados em `scraping_log.py`:
- Sucesso/falha na coleta de URLs
- Tempo de execução
- Erros encontrados
- Estatísticas de coleta

## ⚠️ Limitações Conhecidas

- Rate limiting do site (máximo de 100 requisições/minuto)
- Produtos sem informação nutricional são ignorados
- Algumas categorias podem estar temporariamente indisponíveis

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📜 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

- Abra uma issue para reportar bugs
- Sugestões de melhorias são bem-vindas
- Para questões de segurança, envie um email para [seu-email@exemplo.com]

## 🙏 Agradecimentos

- Equipe do Selenium pelo excelente framework
- Comunidade Python pelos pacotes utilizados
- Contribuidores do projeto

---
Desenvolvido com ❤️ pela comunidade open source
