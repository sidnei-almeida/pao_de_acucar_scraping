# 🛒 Pão de Açúcar Categories – Complete List

**System updated with 16 categories ready for nutritional data collection**

---

## 📋 Category Index

| ID | Category | Emoji | Type |
|:--:|----------|:-----:|------|
| 1-13 | Specific Food | 🍽️ | Detailed subcategories |
| 14 | Food (All Items) | 🍽️ | Broad category |
| 15 | Beverages | 🥤 | Beverage lineup |
| 16 | Caras do Brasil | 🇧🇷 | Brazilian specialties |

---

## 🍽️ FOOD – SPECIFIC CATEGORIES (1-13)

### URL Pattern:
```
https://www.paodeacucar.com/categoria/alimentos/[slug]
```

### Detailed List:

#### [1] 🛒 Butcher
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/acougue`
- **Products:** Beef, pork, poultry, specialty cuts

#### [2] 🧊 Frozen Foods
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/alimentos-congelados`
- **Products:** Ready-made meals, frozen vegetables, pizzas

#### [3] 🥛 Refrigerated Foods
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/alimentos-refrigerados`
- **Products:** Dairy, deli meats, yogurts, cheeses

#### [4] 🏠 Pantry Staples
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/basico-da-despensa`
- **Products:** Rice, beans, sugar, salt, oil

#### [5] 🌾 Cereals
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/cereais`
- **Products:** Breakfast cereal, granola, cereal bars

#### [6] 📦 Pantry Add-ons
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/complemento-da-despensa`
- **Products:** Sauces, spices, seasonings, preserves

#### [7] 🍰 Sweets & Desserts
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/doces-e-sobremesas`
- **Products:** Chocolates, candies, cakes, puddings, gelatins

#### [8] 🥬 Produce
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/hortifruti`
- **Products:** Fresh fruits, vegetables, greens

#### [9] 🧂 Savory Grocery
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/mercearia-salgada`
- **Products:** Pasta, canned goods, soups, broths

#### [10] 🍞 Bakery
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/padaria`
- **Products:** Bread, cakes, pies, cookies

#### [11] 🐟 Seafood
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/peixaria`
- **Products:** Fish, shellfish, seafood products

#### [12] 🍗 Rotisserie
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/rotisserie`
- **Products:** Rotisserie chicken, prepared meats

#### [13] 🥨 Snacks & Appetizers
- **URL:** `https://www.paodeacucar.com/categoria/alimentos/salgadinhos-e-aperitivos`
- **Products:** Chips, peanuts, assorted snacks

---

## 🆕 NEWLY ADDED CATEGORIES (14-16)

### URL Pattern:
```
https://www.paodeacucar.com/categoria/[categoria]?s=relevance&p=1
```

**Note:** These URLs include sorting and pagination parameters.

### Detailed List:

#### [14] 🍽️ Food (All Items)
- **URL:** `https://www.paodeacucar.com/categoria/alimentos?s=relevance&p=1`
- **Products:** Every food product in a unified feed
- **Highlight:** Combines all food subcategories (1-13)
- **Parameters:**
  - `s=relevance` — Sort by relevance
  - `p=1` — First page

#### [15] 🥤 Beverages
- **URL:** `https://www.paodeacucar.com/categoria/bebidas?s=relevance&p=1`
- **Products:** Wine, beer, sodas, juices, water, energy drinks
- **Highlight:** Beverage-exclusive category
- **Parameters:**
  - `s=relevance` — Sort by relevance
  - `p=1` — First page

#### [16] 🇧🇷 Caras do Brasil
- **URL:** `https://www.paodeacucar.com/categoria/caras-do-brasil?s=relevance&p=1`
- **Products:** Curated Brazilian goods, artisanal and regional
- **Highlight:** Signature assortment featuring national brands
- **Parameters:**
  - `s=relevance` — Sort by relevance
  - `p=1` — First page

---

## 🔍 URL Pattern Analysis

### Pattern 1 – Clean URLs (Categories 1-13)
```
Format: https://www.paodeacucar.com/categoria/alimentos/[slug]
Example: https://www.paodeacucar.com/categoria/alimentos/acougue

Traits:
✅ Clean, direct URL  
✅ Friendly descriptive slug  
✅ No parameters in the base URL  
✅ System auto-appends pagination while scraping
```

### Pattern 2 – Parameterized URLs (Categories 14-16)
```
Format: https://www.paodeacucar.com/categoria/[categoria]?s=relevance&p=1
Example: https://www.paodeacucar.com/categoria/bebidas?s=relevance&p=1

Traits:
✅ Includes sorting parameter (`s=relevance`)  
✅ Explicitly sets the first page (`p=1`)  
✅ System scrolls to load more products dynamically  
✅ Supports custom ordering
```

---

## 🎯 Collection Strategy

### Phase 1: Capture Product URLs
```python
For each category (1-16):
1. Selenium navigates to the category URL
2. The system scrolls to the bottom of the page
3. All products are loaded dynamically
4. URLs are extracted via CSS selectors:
   - div[data-testid="product-card"]
   - a[href*="/produto/"]
   - div.product-card
5. Returns a list of unique URLs
```

### Phase 2: Extract Nutritional Data
```python
For each collected product URL:
1. Open the product detail page
2. Execute JavaScript to extract the nutrition facts table
3. Standardize values and measurement units
4. Save to dados_nutricionais.csv
```

---

## 📊 Stats Snapshot

- **Total categories:** 16  
- **Specific food:** 13 categories  
- **Food (general):** 1 category (aggregates everything)  
- **Beverages:** 1 category  
- **Caras do Brasil:** 1 category  
- **URL patterns:** 2 recognized variants  
- **Engine:** Selenium WebDriver  
- **Output formats:** CSV & Excel  

---

## 💡 Key Notes

### Parameterized URLs (14-16)
- ✅ `s=relevance` controls ordering  
- ✅ `p=1` sets the starting page  
- ✅ System ignores the page parameter during scrolling  
- ✅ Loads products dynamically to the end  

### Clean URLs (1-13)
- ✅ No base parameters  
- ✅ System adds `?p=X` automatically when needed  
- ✅ Uses traditional pagination  

### Anti-Bot Protection
- ⚠️ The website applies bot defenses  
- ✅ Selenium configured with appropriate headers  
- ✅ Updated User-Agent string  
- ✅ Built-in delays to avoid detection  

---

## 🚀 Usage

### Interactive CLI
```bash
python main.py
# Choose option 1 (Test Mode) or 2 (Full Collection)
# Select categories (example: 1,3,5,14,15)
```

### Command Line
```bash
# List categories
python main.py listar-categorias

# Collect specific categories
python main.py coletar --categorias 1 2 3 14 15 16 --teste
```

---

**Developed by:** Sidnei Almeida  
**Version:** 2.0 (Interactive CLI with 16 categories)  
**Date:** October 2025  

