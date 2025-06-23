# 🛒 Pão de Queijo Scraping

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Selenium](https://img.shields.io/badge/selenium-4.0%2B-orange.svg)](https://www.selenium.dev/)
[![Pandas](https://img.shields.io/badge/pandas-latest-blue.svg)](https://pandas.pydata.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-green.svg)](https://fastapi.tiangolo.com/)

## 📝 Descrição

O Pão de Queijo Scraping é um web scraper automatizado desenvolvido para coletar dados nutricionais de produtos do site do Pão de Açúcar. O projeto utiliza técnicas avançadas de web scraping com Selenium para navegar de forma eficiente pelo site e extrair informações detalhadas sobre os produtos. Além disso, disponibiliza uma API RESTful para consulta dos dados coletados.

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

- 🌐 **API RESTful**
  - Consulta de dados nutricionais via HTTP
  - Filtros por categoria e nome do produto
  - Paginação de resultados
  - Documentação interativa com Swagger UI

## 🏗️ Arquitetura do Projeto

```
pao_de_queijo_scraping/
├── browser_config.py      # Configurações do navegador e Selenium
├── url_collector.py       # Módulo de coleta de URLs
├── scraper.py            # Core do scraping de dados
├── scraping_log.py       # Sistema de logging
├── main.py               # Ponto de entrada da aplicação
├── api.py               # API RESTful para consulta dos dados
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
- Chromedriver compatível com a versão do Chrome

## 🚀 Como Usar

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/pao-de-queijo-scraping.git
cd pao-de-queijo-scraping
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executando o Scraper

1. Para coletar URLs:
```bash
python main.py coletar-urls
```

2. Para fazer o scraping dos dados:
```bash
python main.py scraping
```

### Executando a API

1. Inicie o servidor da API:
```bash
python api.py
```

2. Acesse a documentação da API:
- Abra o navegador e acesse: http://localhost:8000/docs

### Endpoints da API

- `GET /`: Informações básicas da API
- `GET /produtos`: Lista produtos com dados nutricionais
  - Parâmetros:
    - `skip`: Número de registros para pular (paginação)
    - `limit`: Número máximo de registros
    - `categoria`: Filtrar por categoria
    - `nome`: Filtrar por nome do produto
- `POST /coletar`: Inicia uma nova coleta de dados
  - Parâmetro:
    - `url_categoria`: URL da categoria para coletar

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

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


## 📞 Suporte

- Abra uma issue para reportar bugs
- Sugestões de melhorias são bem-vindas
- Para questões de segurança, envie um email para [sidnei.almeida1806@gmail.com]

## 🙏 Agradecimentos

- Equipe do Selenium pelo excelente framework
- Comunidade Python pelos pacotes utilizados
- Contribuidores do projeto

---
Desenvolvido com ❤️

# API de Dados Nutricionais - Pão de Açúcar

API para coleta e consulta de dados nutricionais de produtos do Pão de Açúcar.

## Funcionalidades

- Coleta automática de dados nutricionais
- Interface web para configuração da coleta
- Feedback em tempo real do processo de coleta
- Consulta aos dados coletados
- Suporte a múltiplas categorias de produtos

## Tecnologias

- Python 3.11+
- FastAPI
- Socket.IO
- Selenium
- BeautifulSoup4
- Pandas
- Uvicorn

## Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/pao_de_queijo_scraping.git
cd pao_de_queijo_scraping
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
python api.py
```

A aplicação estará disponível em `http://localhost:8000`

## Deploy no Render

1. Crie uma conta no [Render](https://render.com)
2. Conecte seu repositório GitHub
3. Crie um novo Web Service
4. Configure as seguintes opções:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api:socket_app --host 0.0.0.0 --port $PORT`
   - Python Version: 3.11

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
PORT=8000
```

## Licença

MIT
