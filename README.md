# 🛒 Pão de Açúcar Scraping

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.0%2B-orange.svg)](https://www.selenium.dev/)
[![Pandas](https://img.shields.io/badge/pandas-latest-blue.svg)](https://pandas.pydata.org/)

## 📝 Descrição

O Pão de Açúcar Scraping é uma aplicação web desenvolvida por Sidnei Almeida para coletar dados nutricionais de produtos do site do Pão de Açúcar. O projeto utiliza Selenium para navegar pelo site e extrair informações detalhadas sobre os produtos, apresentando uma interface web amigável para controle e visualização dos dados.

## 🚀 Como Usar

### 1. Requisitos do Sistema

- Python 3.8 ou superior
- Google Chrome ou Chromium
- Conexão com a Internet

### 2. Instalação

```bash
# Criar e ativar ambiente virtual
python -m venv venv

# No Windows:
.\venv\Scripts\activate

# No Linux/macOS:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Iniciando a Aplicação

1. Com o ambiente virtual ativado, execute:
```bash
python api.py
```

2. Você verá uma mensagem no terminal com a URL local, algo como:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

3. Copie a URL que aparece (ex: http://0.0.0.0:8000 ou http://127.0.0.1:8000) e cole no seu navegador

### 4. Usando a Interface Web

1. Na página inicial, você verá três opções:
   - **Coletar Dados**: Para iniciar uma nova coleta
   - **Consultar Dados**: Para ver os dados já coletados
   - **Baixar Excel**: Para baixar os dados em formato Excel

2. Para coletar dados:
   - Clique em "Coletar Dados"
   - Selecione as categorias desejadas
   - Escolha o modo de coleta (teste ou completo)
   - Clique em "Iniciar Coleta"
   - Acompanhe o progresso em tempo real

## 📊 Dados Coletados

Para cada produto, são coletadas as seguintes informações:
- Nome do produto
- URL do produto
- Categoria
- Porção (g/ml)
- Calorias
- Carboidratos (g)
- Proteínas (g)
- Gorduras totais (g)
- Gorduras saturadas (g)
- Fibras (g)
- Açúcares (g)
- Sódio (mg)

## ⚠️ Observações Importantes

- A coleta pode levar alguns minutos dependendo da quantidade de produtos
- Mantenha a janela do navegador aberta durante a coleta
- Uma conexão estável com a internet é necessária
- Os dados são salvos automaticamente em formato CSV
- É possível cancelar a coleta a qualquer momento

## 📞 Contato

Para dúvidas, sugestões ou reportar problemas, entre em contato com o desenvolvedor:

**Sidnei Almeida**
- Email: sidnei.almeida1806@gmail.com
- LinkedIn: [Sidnei Almeida](https://www.linkedin.com/in/saaelmeida93/)
- GitHub: [sidnei-almeida](https://github.com/sidnei-almeida)

---
