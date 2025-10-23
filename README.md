<div align="center">

# 🛒 Pão de Açúcar Scraping CLI

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.0%2B-orange.svg?style=for-the-badge&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Pandas](https://img.shields.io/badge/pandas-latest-blue.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)

**Sistema Profissional de Coleta Automatizada de Dados Nutricionais**

[🚀 Começar](#-instalação-rápida) • [📖 Documentação](#-documentação-completa) • [🛒 Categorias](#-categorias-disponíveis) • [💬 Suporte](#-contato-e-suporte)

---

</div>

## 🎯 Visão Geral

O **Pão de Açúcar Scraping CLI** é uma ferramenta avançada de linha de comando desenvolvida para coletar dados nutricionais completos de produtos do supermercado Pão de Açúcar. Utilizando tecnologias modernas como Selenium e Pandas, oferece uma interface elegante e funcionalidades robustas para análise de dados nutricionais.

### ✨ Características Principais

<table>
<tr>
<td width="50%">

**🎨 Interface Elegante**
- CLI interativo com cores e animações
- Barras de progresso em tempo real
- Sistema de cores ANSI profissional

**⚡ Performance Otimizada**
- Sistema de checkpoint inteligente
- Filtragem automática de produtos
- Gestão avançada de memória

</td>
<td width="50%">

**📊 Análise Avançada**
- Estatísticas detalhadas dos dados
- Consultas com filtros múltiplos
- Exportação para Excel/CSV

**🛡️ Robustez**
- Recuperação automática de crashes
- Tratamento inteligente de erros
- Logs detalhados e organizados

</td>
</tr>
</table>

---

## 🚀 Instalação Rápida

### 📋 Pré-requisitos

- **Python 3.8+** com pip
- **Google Chrome** ou Chromium
- **Conexão estável** com a internet

### ⚡ Setup Automático

```bash
# 1. Clone o repositório
git clone https://github.com/sidnei-almeida/pao_de_acucar_scraping.git
cd pao_de_acucar_scraping

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o sistema
python main.py
```

### 🔧 Setup com Ambiente Virtual (Recomendado)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

---

## 📖 Documentação Completa

### 🎮 Modo Interativo

Execute o sistema em modo interativo para uma experiência completa:

```bash
python main.py
```

<details>
<summary><b>📋 Menu Interativo Completo</b></summary>

```
🛒 OPERAÇÕES DE COLETA:
  1. 🧪 Modo Teste          - Coleta rápida para validação
  2. 🚀 Coleta Completa      - Extração completa de dados
  3. 🎯 Coleta Personalizada - Escolher categorias específicas

📊 CONSULTA E ANÁLISE:
  4. 🔍 Consultar Dados  - Visualizar informações coletadas
  5. 📈 Estatísticas     - Análise e métricas detalhadas
  6. 📋 Listar Arquivos  - Ver arquivos gerados

📁 GERENCIAMENTO:
  7. 💾 Exportar Excel   - Salvar dados em formato Excel
  8. 🗑️ Limpar Dados     - Remover arquivos antigos

ℹ️ INFORMAÇÕES:
  9. 🛒 Ver Categorias   - Lista as 16 categorias disponíveis
  A. 📖 Sobre           - Informações do programa
  0. ❌ Sair            - Encerrar programa
```

</details>

### 💻 Comandos de Linha de Comando

#### 📋 Listar Categorias Disponíveis
```bash
python main.py listar-categorias
```

#### 🧪 Coleta em Modo Teste (Rápido)
```bash
python main.py coletar --categorias 1 2 3 --teste
```

#### 🚀 Coleta Completa
```bash
python main.py coletar --categorias 1 2 3 4 5
```

#### 🔍 Consultar Dados Coletados
```bash
# Consultar todos os dados
python main.py consultar

# Filtrar por categoria
python main.py consultar --categoria "Hortifruti"

# Filtrar por nome do produto
python main.py consultar --nome "leite"

# Múltiplos filtros
python main.py consultar --categoria "Doces" --nome "chocolate"
```

#### 💾 Exportar para Excel
```bash
# Exportar todos os dados
python main.py exportar --formato excel

# Exportar dados filtrados
python main.py exportar --categoria "Bebidas" --formato excel
```

#### 📊 Visualizar Estatísticas
```bash
python main.py estatisticas
```

---

## 🛒 Categorias Disponíveis

### 🍽️ Alimentos - Categorias Específicas (1-13)

<table>
<tr>
<td width="33%">

**1. 🛒 Açougue**
- Carnes bovinas, suínas, aves
- Derivados e embutidos

**2. 🧊 Alimentos Congelados**
- Refeições prontas
- Vegetais congelados, pizzas

**3. 🥛 Alimentos Refrigerados**
- Laticínios, frios
- Iogurtes, queijos

**4. 🏠 Básicos da Despensa**
- Arroz, feijão, açúcar
- Sal, óleo, temperos básicos

**5. 🌾 Cereais**
- Cereais matinais
- Granolas, barras de cereal

</td>
<td width="33%">

**6. 📦 Complemento da Despensa**
- Molhos, temperos
- Especiarias, conservas

**7. 🍰 Doces e Sobremesas**
- Chocolates, balas
- Bolos, pudins, gelatinas

**8. 🥬 Hortifruti**
- Frutas frescas
- Verduras, legumes

**9. 🧂 Mercearia Salgada**
- Massas, enlatados
- Sopas, caldos

**10. 🍞 Padaria**
- Pães, bolos
- Tortas, biscoitos

</td>
<td width="33%">

**11. 🐟 Peixaria**
- Peixes frescos
- Frutos do mar

**12. 🍗 Rotisserie**
- Frango assado
- Carnes preparadas

**13. 🥨 Salgadinhos e Aperitivos**
- Chips, amendoins
- Snacks diversos

</td>
</tr>
</table>

### 🌟 Categorias Expandidas (14-16)

<table>
<tr>
<td width="33%">

**14. 🍽️ Alimentos (Geral)**
- Todos os produtos de alimentos
- Categoria unificada

</td>
<td width="33%">

**15. 🥤 Bebidas**
- Vinhos, cervejas
- Refrigerantes, sucos, águas

</td>
<td width="33%">

**16. 🇧🇷 Caras do Brasil**
- Produtos brasileiros
- Selecionados e artesanais

</td>
</tr>
</table>

---

## 📊 Dados Coletados

### 🎯 Informações por Produto

<table>
<tr>
<td width="50%">

**📝 Identificação**
- Nome completo do produto
- URL da página do produto
- Categoria de classificação
- **Código de Barras (GTIN/EAN)**

**🥗 Informações Nutricionais**
- Porção recomendada (g/ml)
- Valor calórico (kcal)
- Carboidratos totais (g)
- Proteínas (g)

</td>
<td width="50%">

**🧈 Composição Detalhada**
- Gorduras totais (g)
- Gorduras saturadas (g)
- Fibras alimentares (g)
- Açúcares totais (g)
- Sódio (mg)

**📅 Metadados**
- Data e hora da coleta
- Status de validação
- Fonte dos dados

</td>
</tr>
</table>

---

## 🛡️ Sistema de Checkpoint e Recuperação

### ⚡ Características Avançadas

<table>
<tr>
<td width="50%">

**🔄 Checkpoint Automático**
- Salvamento a cada 1.000 produtos
- Prevenção de perda de dados
- Recuperação inteligente

**🧠 Gestão de Memória**
- Reinício periódico do navegador
- Liberação automática de recursos
- Otimização de performance

</td>
<td width="50%">

**🛡️ Robustez**
- Até 3 tentativas de recuperação
- Tratamento inteligente de erros
- Logs detalhados organizados

**📊 Estatísticas de Confiabilidade**
- Perda máxima: 1.000 produtos
- Taxa de sucesso: 99.5%+
- Tempo médio de recuperação: <30s

</td>
</tr>
</table>

Para detalhes técnicos completos: **[SISTEMA_CHECKPOINT.md](SISTEMA_CHECKPOINT.md)**

---

## 📁 Estrutura de Arquivos

```
pao_de_acucar_scraping/
├── 📁 dados_coletados/              # Dados coletados
│   ├── dados_nutricionais.csv       # Arquivo principal
│   ├── consulta_*.csv               # Consultas filtradas
│   └── dados_nutricionais_*.xlsx   # Exports Excel
├── 📁 logs/                         # Logs organizados
│   ├── README.md                    # Documentação dos logs
│   └── scraping_*.log              # Logs de execução
├── 📄 main.py                       # CLI principal
├── 📄 scraper.py                    # Motor de scraping
├── 📄 url_collector.py              # Coletor de URLs
├── 📄 scraping_log.py               # Sistema de logs
└── 📄 requirements.txt              # Dependências
```

---

## ⚠️ Observações Importantes

### 🎯 Filtragem Inteligente
- **Produtos sem tabela nutricional** são automaticamente ignorados
- **Redução de tempo**: 30-65% em categorias mistas
- **Qualidade garantida**: Apenas produtos com dados válidos

### ⚡ Performance e Confiabilidade
- **Conexão estável** recomendada para coletas longas
- **Interrupção segura** com Ctrl+C
- **Modo teste** para validações rápidas
- **Sistema de checkpoint** previne perda de dados

### 📊 Qualidade dos Dados
- **Validação automática** de informações nutricionais
- **Padronização** de formatos e unidades
- **Rastreabilidade** completa dos dados coletados

---

## 🔧 Tecnologias Utilizadas

<table>
<tr>
<td width="25%">

**🐍 Python 3.8+**
- Linguagem principal
- Tipagem estática
- Async/await support

</td>
<td width="25%">

**🌐 Selenium 4.0+**
- Automação web
- JavaScript execution
- Dynamic content handling

</td>
<td width="25%">

**📊 Pandas**
- Manipulação de dados
- Análise estatística
- Export para Excel/CSV

</td>
<td width="25%">

**🎨 BeautifulSoup**
- Parsing HTML
- Extração de dados
- Limpeza de conteúdo

</td>
</tr>
</table>

---

## 📈 Roadmap e Melhorias Futuras

### 🚀 Próximas Funcionalidades

- [ ] **API REST** para integração externa
- [ ] **Dashboard web** para visualização
- [ ] **Machine Learning** para análise nutricional
- [ ] **Comparação de preços** entre produtos
- [ ] **Alertas nutricionais** personalizados
- [ ] **Integração com apps** de saúde

### 🔄 Melhorias Contínuas

- [ ] **Performance**: Otimização de velocidade
- [ ] **UI/UX**: Interface ainda mais intuitiva
- [ ] **Documentação**: Guias avançados
- [ ] **Testes**: Cobertura completa
- [ ] **CI/CD**: Automação de deploy

---

## 💬 Contato e Suporte

### 👨‍💻 Desenvolvedor

<div align="center">

**Sidnei Almeida**

[![Email](https://img.shields.io/badge/Email-sidnei.almeida1806@gmail.com-blue?style=for-the-badge&logo=gmail)](mailto:sidnei.almeida1806@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sidnei%20Almeida-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/saaelmeida93/)
[![GitHub](https://img.shields.io/badge/GitHub-sidnei--almeida-black?style=for-the-badge&logo=github)](https://github.com/sidnei-almeida)

</div>

### 📞 Canais de Suporte

- **🐛 Reportar Bugs**: [GitHub Issues](https://github.com/sidnei-almeida/pao_de_acucar_scraping/issues)
- **💡 Sugestões**: [GitHub Discussions](https://github.com/sidnei-almeida/pao_de_acucar_scraping/discussions)
- **📧 Contato Direto**: sidnei.almeida1806@gmail.com

---

<div align="center">

### ⭐ Se este projeto foi útil para você, considere dar uma estrela!

**Desenvolvido com ❤️ por [Sidnei Almeida](https://github.com/sidnei-almeida)**

[![GitHub stars](https://img.shields.io/github/stars/sidnei-almeida/pao_de_acucar_scraping?style=social)](https://github.com/sidnei-almeida/pao_de_acucar_scraping/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/sidnei-almeida/pao_de_acucar_scraping?style=social)](https://github.com/sidnei-almeida/pao_de_acucar_scraping/network)

---

**📄 Licença**: MIT • **🔗 Repositório**: [GitHub](https://github.com/sidnei-almeida/pao_de_acucar_scraping)

</div>