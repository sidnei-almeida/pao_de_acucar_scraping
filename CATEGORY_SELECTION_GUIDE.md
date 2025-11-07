# 🎯 Category Selection Guide – Interactive CLI

**Intuitive workflow to choose exactly which categories you want to scrape**

---

## 📋 How Category Selection Works

### **Menu Option 3 – Custom Collection** 🎯

This option lets you pick **precisely** which categories to gather, giving you complete control over the run.

---

## 🚀 Custom Collection Walkthrough

### **1. Open the main menu**
```bash
python main.py
```

### **2. Choose Option 3 – Custom Collection**
```
═══════════════════════ MAIN MENU ════════════════════════

COLLECTION OPERATIONS:
  1. 🧪 Test Mode           - Quick validation crawl
  2. 🚀 Full Collection     - End-to-end extraction
  3. 🎯 Custom Collection   - Pick specific categories
```

### **3. Review the available categories**

The CLI displays all 16 categories in a structured format:

```
🎯 CATEGORY SELECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 AVAILABLE CATEGORIES:

🍽️ FOOD — Specific Categories:
   [ 1] 🛒 Butcher
   [ 2] 🧊 Frozen Foods
   [ 3] 🥛 Refrigerated Foods
   [ 4] 🏠 Pantry Staples
   [ 5] 🌾 Cereals
   [ 6] 📦 Pantry Add-ons
   [ 7] 🍰 Sweets & Desserts
   [ 8] 🥬 Produce
   [ 9] 🧂 Savory Grocery
   [10] 🍞 Bakery
   [11] 🐟 Seafood
   [12] 🍗 Rotisserie
   [13] 🥨 Snacks & Appetizers

🍽️ FOOD — General:
   [14] 🍽️ Food (All Items)

🥤 BEVERAGES:
   [15] 🥤 Beverages

🇧🇷 BRAZILIAN SPECIALTIES:
   [16] 🇧🇷 Caras do Brasil
```

### **4. Pick the categories you need**

You have **four flexible ways** to select categories:

#### **Option A: Quick shortcuts** ⚡

```
⚡ QUICK SHORTCUTS:
   • Type 'all' to select all 16 categories
   • Type 'food' to select categories 1–13
   • Type 'new' to select categories 14–16
   • Enter comma-separated IDs (e.g., 1,3,5,14,15)
```

**Examples:**

```bash
👉 Select categories: all
✅ All 16 categories selected
```

```bash
👉 Select categories: food
✅ 13 food categories selected
```

```bash
👉 Select categories: new
✅ 3 new categories selected (14–16)
```

#### **Option B: Manual selection** 🎯

Enter category IDs separated by commas:

**Example 1 – Only beverages**
```bash
👉 Select categories: 15
✅ 1 category selected:
   • 🥤 Beverages
```

**Example 2 – Produce + Beverages + Caras do Brasil**
```bash
👉 Select categories: 8,15,16
✅ 3 categories selected:
   • 🥬 Produce
   • 🥤 Beverages
   • 🇧🇷 Caras do Brasil
```

**Example 3 – Several food categories**
```bash
👉 Select categories: 1,3,5,7,9,11,13
✅ 7 categories selected:
   • 🛒 Butcher
   • 🥛 Refrigerated Foods
   • 🌾 Cereals
   • 🍰 Sweets & Desserts
   • 🧂 Savory Grocery
   • 🐟 Seafood
   • 🥨 Snacks & Appetizers
```

**Example 4 – Mixed set**
```bash
👉 Select categories: 1,2,3,14,15,16
✅ 6 categories selected:
   • 🛒 Butcher
   • 🧊 Frozen Foods
   • 🥛 Refrigerated Foods
   • 🍽️ Food (All Items)
   • 🥤 Beverages
   • 🇧🇷 Caras do Brasil
```

### **5. Choose the collection mode**

After selecting categories, pick a mode:

```
⚙️ COLLECTION MODE:
   1. 🧪 Test - Quick (5 products/category)
   2. 🚀 Full  - Unlimited (all products)

👉 Select mode (1-2): 1

✅ Mode selected: TEST
```

### **6. Confirm and launch**

```bash
🤔 Start test collection? (y/N): y

🔍 PHASE 1: URL HARVESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ... collection in progress ...
```

---

## 💡 Common Scenarios

### **Scenario 1: Smoke testing the scraper** 🧪
```
Option: 3 (Custom Collection)
Categories: 1
Mode: 1 (Test)
Outcome: Quick run with 5 butcher products
```

### **Scenario 2: Beverages-only run** 🥤
```
Option: 3 (Custom Collection)
Categories: 15
Mode: 2 (Full)
Outcome: Complete beverage dataset
```

### **Scenario 3: Sweets & snacks** 🍰
```
Option: 3 (Custom Collection)
Categories: 7,13
Mode: 2 (Full)
Outcome: Full sweets + snack categories
```

### **Scenario 4: All food categories** 🍽️
```
Option: 3 (Custom Collection)
Categories: food
Mode: 1 (Test)
Outcome: Test run across all 13 food categories
```

### **Scenario 5: Only the new categories** 🆕
```
Option: 3 (Custom Collection)
Categories: new
Mode: 2 (Full)
Outcome: Food (All Items) + Beverages + Caras do Brasil
```

### **Scenario 6: Full coverage** 🌟
```
Option: 3 (Custom Collection)
Categories: all
Mode: 2 (Full)
Outcome: Full crawl across all 16 categories
```

---

## 🎨 Why Custom Selection Rocks

### **✅ Total flexibility**
- Target exactly what you need
- Skip irrelevant categories
- Save time by focusing your crawl

### **✅ Smart shortcuts**
- **`all`** – All 16 categories
- **`food`** – Food-only (1–13)
- **`new`** – Recently added (14–16)

### **✅ Precise manual control**
- Enter any combination (comma-separated)
- Combine as many categories as you want
- Input is auto-validated

### **✅ Mode selection**
- **Test:** 5 products per category
- **Full:** Every product available

---

## 📊 Menu Option Comparison

| Option | Name | Categories | Mode | Best For |
|:------:|------|------------|------|----------|
| **1** | Test Mode | Selected | Test | Quick validation |
| **2** | Full Collection | Selected | Full | Deep crawl |
| **3** | Custom Collection | **You pick!** | **You pick!** | **Maximum control** |

---

## 🎯 Practical Examples

### **Example 1: Market research – beverages**
```
Goal: Analyze beverage pricing and nutrition
Categories: 15
Mode: Full
Estimated time: ~1–2 hours
```

### **Example 2: Nutrition analysis – fresh items**
```
Goal: Study fresh & natural products
Categories: 8,11 (Produce + Seafood)
Mode: Full
Estimated time: ~2–3 hours
```

### **Example 3: Brazilian products spotlight**
```
Goal: Map Brazilian specialty items
Category: 16
Mode: Full
Estimated time: ~30–60 minutes
```

### **Example 4: Build a master dataset**
```
Goal: Capture everything
Categories: all
Mode: Full
Estimated time: ~8–12 hours (all categories)
```

### **Example 5: Initial system test**
```
Goal: Validate the setup
Categories: 1,15,16 (Butcher + Beverages + Caras do Brasil)
Mode: Test
Estimated time: ~5–10 minutes
```

---

## 🔥 Pro Tips

### **💡 Tip 1: Start small**
```
Use TEST mode with 1–2 categories to learn the flow.
Example: 15 (beverages) in test mode.
```

### **💡 Tip 2: Lean on shortcuts**
```
To gather all food categories quickly:
Type: food
Much faster than: 1,2,3,4,5,6,7,8,9,10,11,12,13
```

### **💡 Tip 3: Incremental strategy**
```
Day 1: Categories 1–5 (Full)
Day 2: Categories 6–10 (Full)
Day 3: Categories 11–16 (Full)
```

### **💡 Tip 4: Focus on the new set**
```
If food categories are already covered, focus on the latest ones:
Type: new
Outcome: Beverages + Food (All Items) + Caras do Brasil
```

---

## ⚠️ Important Notes

- ✅ **Unlimited combinations:** Mix as many categories as you like
- ✅ **Automatic validation:** Invalid inputs are gracefully ignored
- ✅ **Confirmation prompts:** You can always cancel before the run begins
- ✅ **Flexible modes:** Test or Full, regardless of the categories selected

---

**Developed by:** Sidnei Almeida  
**Version:** 2.0 – Interactive CLI with custom selection  
**Date:** October 2025

