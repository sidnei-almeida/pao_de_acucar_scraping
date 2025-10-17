# 🛒 Pão de Açúcar Scraping - CLI

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.0%2B-orange.svg)](https://www.selenium.dev/)
[![Pandas](https://img.shields.io/badge/pandas-latest-blue.svg)](https://pandas.pydata.org/)

## 📝 Descrição

O Pão de Açúcar Scraping CLI é uma ferramenta de linha de comando desenvolvida para coletar dados nutricionais de produtos do site do Pão de Açúcar. O projeto utiliza Selenium para navegar pelo site e extrair informações detalhadas sobre os produtos, oferecendo comandos simples e diretos para coleta, consulta e exportação de dados.

## 🚀 Como Usar

### 1. Requisitos do Sistema

- Python 3.8 ou superior
- Google Chrome ou Chromium
- Conexão com a Internet

### 2. Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

### 3. Comandos Disponíveis

#### Listar Categorias
```bash
python main.py listar-categorias
```
Mostra todas as 13 categorias disponíveis para coleta.

#### Coletar Dados
```bash
# Modo teste (coleta limitada)
python main.py coletar --categorias 1 2 3 --teste

# Modo completo (coleta ilimitada)
python main.py coletar --categorias 1 2 3 4 5
```

#### Consultar Dados
```bash
# Consultar todos os dados
python main.py consultar

# Filtrar por categoria
python main.py consultar --categoria "Hortifruti"

# Filtrar por nome do produto
python main.py consultar --nome "leite"
```

#### Exportar para Excel
```bash
# Exportar todos os dados
python main.py exportar --formato excel

# Exportar dados filtrados
python main.py exportar --categoria "Doces" --formato excel
```

#### Ver Estatísticas
```bash
python main.py estatisticas
```
Mostra estatísticas dos dados coletados.

## 📊 Dados Coletados

Para cada produto, são coletadas as seguintes informações:
- Nome do produto
- URL do produto
- Categoria
- Porção (g/ml)
- Calorias (kcal)
- Carboidratos (g)
- Proteínas (g)
- Gorduras totais (g)
- Gorduras saturadas (g)
- Fibras (g)
- Açúcares (g)
- Sódio (mg)
- Data da coleta
- **Código de Barras (GTIN/EAN)** - Código de identificação do produto

## 🛒 Categorias Disponíveis

### Alimentos - Categorias Específicas (1-13)
1. **🛒 Açougue** - Carnes bovinas, suínas, aves e derivados
2. **🧊 Alimentos Congelados** - Refeições prontas, vegetais congelados, pizzas
3. **🥛 Alimentos Refrigerados** - Laticínios, frios, iogurtes, queijos
4. **🏠 Básicos da Despensa** - Arroz, feijão, açúcar, sal, óleo
5. **🌾 Cereais** - Cereais matinais, granolas, barras de cereal
6. **📦 Complemento da Despensa** - Molhos, temperos, especiarias, conservas
7. **🍰 Doces e Sobremesas** - Chocolates, balas, bolos, pudins, gelatinas
8. **🥬 Hortifruti** - Frutas, verduras, legumes frescos
9. **🧂 Mercearia Salgada** - Massas, enlatados, sopas, caldos
10. **🍞 Padaria** - Pães, bolos, tortas, biscoitos
11. **🐟 Peixaria** - Peixes, frutos do mar, produtos marinhos
12. **🍗 Rotisserie** - Frango assado, carnes preparadas
13. **🥨 Salgadinhos e Aperitivos** - Chips, amendoins, snacks diversos

### Novas Categorias Adicionadas (14-16)
14. **🍽️ Alimentos (Geral)** - Todos os produtos de alimentos em uma categoria
15. **🥤 Bebidas** - Vinhos, cervejas, refrigerantes, sucos, águas
16. **🇧🇷 Caras do Brasil** - Produtos brasileiros selecionados e artesanais

## ⚠️ Observações Importantes

- A coleta pode levar algumas horas dependendo da quantidade de produtos
- Mantenha uma conexão estável com a internet
- Os dados são salvos automaticamente em formato CSV na pasta do repositório
- É possível interromper a coleta com Ctrl+C
- Use o modo teste (`--teste`) para validações rápidas
- **🎯 Filtragem inteligente:** Produtos sem tabela nutricional (fraldas, limpeza, etc.) são automaticamente ignorados
- **⚡ Otimização:** A filtragem reduz o tempo de coleta em 30-65% em categorias mistas
- **📊 Qualidade:** Apenas produtos com dados nutricionais válidos são salvos
- **💾 Sistema de checkpoint:** Salvamento automático a cada 1.000 produtos coletados
- **🔄 Recuperação de crashes:** Retoma automaticamente de onde parou em caso de erros
- **🧠 Gestão de memória:** Reinício periódico do navegador para evitar crashes

## 📁 Estrutura de Arquivos

```
dados_coletados/          # Diretório criado automaticamente
├── dados_nutricionais.csv    # Arquivo principal com todos os dados
├── consulta_YYYYMMDD_HHMMSS.csv  # Arquivos de consultas filtradas
├── dados_nutricionais_YYYYMMDD_HHMMSS.xlsx  # Arquivos Excel exportados
└── urls_checkpoint_*.json    # Checkpoints temporários (removidos após sucesso)
```

## 🔄 Sistema de Checkpoint e Recuperação

O sistema possui um mecanismo robusto de checkpoint que previne perda de dados:

- **Salvamento automático:** A cada 1.000 produtos coletados
- **Reinício periódico:** Navegador reinicia a cada 100 rolagens para liberar memória
- **Recuperação automática:** Até 3 tentativas em caso de crashes
- **Perda máxima:** Máximo de 1.000 produtos (contra 10.000+ sem checkpoint)

Para mais detalhes, consulte: [SISTEMA_CHECKPOINT.md](SISTEMA_CHECKPOINT.md)

## 📞 Contato

Para dúvidas, sugestões ou reportar problemas, entre em contato com o desenvolvedor:

**Sidnei Almeida**
- Email: sidnei.almeida1806@gmail.com
- LinkedIn: [Sidnei Almeida](https://www.linkedin.com/in/saaelmeida93/)
- GitHub: [sidnei-almeida](https://github.com/sidnei-almeida)

---
