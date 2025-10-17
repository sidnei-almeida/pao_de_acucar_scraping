# 🛒 Categorias do Pão de Açúcar - Lista Completa

**Sistema atualizado com 16 categorias disponíveis para coleta de dados nutricionais**

---

## 📋 Índice de Categorias

| ID | Categoria | Emoji | Tipo |
|:--:|-----------|:-----:|------|
| 1-13 | Alimentos Específicos | 🍽️ | Subcategorias detalhadas |
| 14 | Alimentos Geral | 🍽️ | Categoria abrangente |
| 15 | Bebidas | 🥤 | Bebidas em geral |
| 16 | Caras do Brasil | 🇧🇷 | Produtos brasileiros |

---

## 🍽️ ALIMENTOS - CATEGORIAS ESPECÍFICAS (1-13)

### Padrão de URL:
```
https://www.paodeacucar.com/categoria/alimentos/[slug]
```

### Lista Detalhada:

#### [1] 🛒 Açougue
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/acougue`
- **Produtos:** Carnes bovinas, suínas, aves e derivados

#### [2] 🧊 Alimentos Congelados
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/alimentos-congelados`
- **Produtos:** Refeições prontas, vegetais congelados, pizzas

#### [3] 🥛 Alimentos Refrigerados
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/alimentos-refrigerados`
- **Produtos:** Laticínios, frios, iogurtes, queijos

#### [4] 🏠 Básicos da Despensa
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/basico-da-despensa`
- **Produtos:** Arroz, feijão, açúcar, sal, óleo

#### [5] 🌾 Cereais
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/cereais`
- **Produtos:** Cereais matinais, granolas, barras de cereal

#### [6] 📦 Complemento da Despensa
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/complemento-da-despensa`
- **Produtos:** Molhos, temperos, especiarias, conservas

#### [7] 🍰 Doces e Sobremesas
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/doces-e-sobremesas`
- **Produtos:** Chocolates, balas, bolos, pudins, gelatinas

#### [8] 🥬 Hortifruti
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/hortifruti`
- **Produtos:** Frutas, verduras, legumes frescos

#### [9] 🧂 Mercearia Salgada
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/mercearia-salgada`
- **Produtos:** Massas, enlatados, sopas, caldos

#### [10] 🍞 Padaria
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/padaria`
- **Produtos:** Pães, bolos, tortas, biscoitos

#### [11] 🐟 Peixaria
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/peixaria`
- **Produtos:** Peixes, frutos do mar, produtos marinhos

#### [12] 🍗 Rotisserie
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/rotisserie`
- **Produtos:** Frango assado, carnes preparadas

#### [13] 🥨 Salgadinhos e Aperitivos
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/salgadinhos-e-aperitivos`
- **Produtos:** Chips, amendoins, snacks diversos

---

## 🆕 NOVAS CATEGORIAS ADICIONADAS (14-16)

### Padrão de URL:
```
https://www.paodeacucar.com/categoria/[categoria]?s=relevance&p=1
```

**Observação:** Estas URLs incluem parâmetros de ordenação e paginação

### Lista Detalhada:

#### [14] 🍽️ Alimentos (Geral)
- **URL:** `https://www.paodeacucar.com/categoria/alimentos?s=relevance&p=1`
- **Produtos:** Todos os produtos de alimentos em uma única categoria
- **Característica:** Engloba todas as subcategorias de alimentos (1-13)
- **Parâmetros:**
  - `s=relevance` - Ordenação por relevância
  - `p=1` - Página inicial

#### [15] 🥤 Bebidas
- **URL:** `https://www.paodeacucar.com/categoria/bebidas?s=relevance&p=1`
- **Produtos:** Vinhos, cervejas, refrigerantes, sucos, águas, energéticos
- **Característica:** Categoria exclusiva de bebidas
- **Parâmetros:**
  - `s=relevance` - Ordenação por relevância
  - `p=1` - Página inicial

#### [16] 🇧🇷 Caras do Brasil
- **URL:** `https://www.paodeacucar.com/categoria/caras-do-brasil?s=relevance&p=1`
- **Produtos:** Produtos brasileiros selecionados, artesanais, regionais
- **Característica:** Linha especial de produtos nacionais
- **Parâmetros:**
  - `s=relevance` - Ordenação por relevância
  - `p=1` - Página inicial

---

## 🔍 Análise dos Padrões de URLs

### Padrão 1 - URLs Simples (Categorias 1-13)
```
Formato: https://www.paodeacucar.com/categoria/alimentos/[slug]
Exemplo: https://www.paodeacucar.com/categoria/alimentos/acougue

Características:
✅ URL limpa e direta
✅ Slug descritivo e amigável
✅ Sem parâmetros na URL base
✅ Sistema adiciona paginação automaticamente durante coleta
```

### Padrão 2 - URLs com Parâmetros (Categorias 14-16)
```
Formato: https://www.paodeacucar.com/categoria/[categoria]?s=relevance&p=1
Exemplo: https://www.paodeacucar.com/categoria/bebidas?s=relevance&p=1

Características:
✅ Inclui parâmetros de ordenação (s=relevance)
✅ Especifica página inicial (p=1)
✅ Sistema faz scroll para carregar mais produtos
✅ Permite ordenação personalizada
```

---

## 🎯 Estratégia de Coleta

### Fase 1: Coleta de URLs dos Produtos
```python
Para cada categoria (1-16):
1. Selenium acessa a URL da categoria
2. Sistema faz scroll até o fim da página
3. Carrega todos os produtos dinamicamente
4. Extrai URLs usando seletores CSS:
   - div[data-testid="product-card"]
   - a[href*="/produto/"]
   - div.product-card
5. Retorna lista de URLs únicas
```

### Fase 2: Extração de Dados Nutricionais
```python
Para cada URL de produto coletada:
1. Acessa página individual do produto
2. Executa JavaScript para extrair tabela nutricional
3. Padroniza valores e unidades
4. Salva em dados_nutricionais.csv
```

---

## 📊 Estatísticas

- **Total de categorias:** 16
- **Alimentos específicos:** 13 categorias
- **Alimentos geral:** 1 categoria (engloba todas)
- **Bebidas:** 1 categoria
- **Caras do Brasil:** 1 categoria
- **Padrões de URL:** 2 tipos identificados
- **Sistema:** Selenium WebDriver
- **Formato de saída:** CSV e Excel

---

## 💡 Observações Importantes

### URLs com Parâmetros (14-16)
- ✅ Parâmetro `s=relevance` define ordenação
- ✅ Parâmetro `p=1` define página inicial
- ✅ Sistema ignora parâmetro de página durante scroll
- ✅ Carrega produtos dinamicamente até o fim

### URLs Simples (1-13)
- ✅ URLs limpas sem parâmetros
- ✅ Sistema adiciona `?p=X` automaticamente se necessário
- ✅ Navegação por paginação tradicional

### Proteção Anti-Bot
- ⚠️ Site usa proteção contra bots
- ✅ Selenium configurado com headers apropriados
- ✅ User-Agent atualizado
- ✅ Delays implementados para evitar detecção

---

## 🚀 Como Usar

### Via Interface Interativa
```bash
python main.py
# Escolha opção 1 (Modo Teste) ou 2 (Coleta Completa)
# Selecione as categorias desejadas (ex: 1,3,5,14,15)
```

### Via Linha de Comando
```bash
# Listar categorias
python main.py listar-categorias

# Coletar categorias específicas
python main.py coletar --categorias 1 2 3 14 15 16 --teste
```

---

**Desenvolvido por:** Sidnei Almeida  
**Versão:** 2.0 (CLI Interativa com 16 categorias)  
**Data:** Outubro 2025

