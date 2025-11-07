#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔍 PÃO DE AÇÚCAR CATEGORY INSPECTOR
===================================
Utility script to list and verify every category configured in the scraping system.
"""

# ============================================================================
# 🎨 ANSI COLOR SYSTEM
# ============================================================================
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'

# ============================================================================
# 📊 CONFIGURED CATEGORIES
# ============================================================================
CATEGORIES = {
    # ═══════════════════════════════════════════════════════════════════
    # 🍽️ FOOD – SPECIFIC CATEGORIES
    # ═══════════════════════════════════════════════════════════════════
    "1": {
        "name": "Butcher",
        "emoji": "🛒",
        "url": "https://www.paodeacucar.com/categoria/alimentos/acougue",
        "description": "Beef, pork, poultry, and specialty cuts"
    },
    "2": {
        "name": "Frozen Foods",
        "emoji": "🧊",
        "url": "https://www.paodeacucar.com/categoria/alimentos/alimentos-congelados",
        "description": "Ready-made meals, frozen vegetables, pizzas"
    },
    "3": {
        "name": "Refrigerated Foods",
        "emoji": "🥛",
        "url": "https://www.paodeacucar.com/categoria/alimentos/alimentos-refrigerados",
        "description": "Dairy, deli meats, yogurts, cheeses"
    },
    "4": {
        "name": "Pantry Staples",
        "emoji": "🏠",
        "url": "https://www.paodeacucar.com/categoria/alimentos/basico-da-despensa",
        "description": "Rice, beans, sugar, salt, oil"
    },
    "5": {
        "name": "Cereals",
        "emoji": "🌾",
        "url": "https://www.paodeacucar.com/categoria/alimentos/cereais",
        "description": "Breakfast cereals, granola, cereal bars"
    },
    "6": {
        "name": "Pantry Add-ons",
        "emoji": "📦",
        "url": "https://www.paodeacucar.com/categoria/alimentos/complemento-da-despensa",
        "description": "Sauces, spices, preserves"
    },
    "7": {
        "name": "Sweets & Desserts",
        "emoji": "🍰",
        "url": "https://www.paodeacucar.com/categoria/alimentos/doces-e-sobremesas",
        "description": "Chocolate, candy, cakes, puddings"
    },
    "8": {
        "name": "Produce",
        "emoji": "🥬",
        "url": "https://www.paodeacucar.com/categoria/alimentos/hortifruti",
        "description": "Fresh fruits, vegetables, greens"
    },
    "9": {
        "name": "Savory Grocery",
        "emoji": "🧂",
        "url": "https://www.paodeacucar.com/categoria/alimentos/mercearia-salgada",
        "description": "Pasta, canned goods, soups"
    },
    "10": {
        "name": "Bakery",
        "emoji": "🍞",
        "url": "https://www.paodeacucar.com/categoria/alimentos/padaria",
        "description": "Bread, cakes, pies, cookies"
    },
    "11": {
        "name": "Seafood",
        "emoji": "🐟",
        "url": "https://www.paodeacucar.com/categoria/alimentos/peixaria",
        "description": "Fish, shellfish, seafood products"
    },
    "12": {
        "name": "Rotisserie",
        "emoji": "🍗",
        "url": "https://www.paodeacucar.com/categoria/alimentos/rotisserie",
        "description": "Rotisserie chicken, prepared meats"
    },
    "13": {
        "name": "Snacks & Appetizers",
        "emoji": "🥨",
        "url": "https://www.paodeacucar.com/categoria/alimentos/salgadinhos-e-aperitivos",
        "description": "Chips, peanuts, assorted snacks"
    },

    # ═══════════════════════════════════════════════════════════════════
    # 🍽️ FOOD – GENERAL CATEGORY (ALL FOOD)
    # ═══════════════════════════════════════════════════════════════════
    "14": {
        "name": "Food (All Items)",
        "emoji": "🍽️",
        "url": "https://www.paodeacucar.com/categoria/alimentos?s=relevance&p=1",
        "description": "Unified feed with every food product"
    },

    # ═══════════════════════════════════════════════════════════════════
    # 🥤 BEVERAGES
    # ═══════════════════════════════════════════════════════════════════
    "15": {
        "name": "Beverages",
        "emoji": "🥤",
        "url": "https://www.paodeacucar.com/categoria/bebidas?s=relevance&p=1",
        "description": "Wine, beer, sodas, juices, water, energy drinks"
    },

    # ═══════════════════════════════════════════════════════════════════
    # 🇧🇷 CARAS DO BRASIL (BRAZILIAN PRODUCTS)
    # ═══════════════════════════════════════════════════════════════════
    "16": {
        "name": "Caras do Brasil",
        "emoji": "🇧🇷",
        "url": "https://www.paodeacucar.com/categoria/caras-do-brasil?s=relevance&p=1",
        "description": "Curated, artisanal Brazilian products"
    }
}

def show_banner():
    """Display the program banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║            🛒 PÃO DE AÇÚCAR CATEGORY INSPECTOR                  ║
║                                                                  ║
║              Available Category & Link Diagnostics                ║
╚══════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)

def list_all_categories():
    """List every configured category with details."""
    print(f"\n{Colors.GREEN}📋 CONFIGURED CATEGORIES{Colors.RESET}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

    print(f"\n{Colors.CYAN}Total categories available: {Colors.WHITE}{len(CATEGORIES)}{Colors.RESET}\n")

    for id_cat, info in CATEGORIES.items():
        print(f"{Colors.YELLOW}{Colors.BOLD}[{int(id_cat):2d}]{Colors.RESET} {info['emoji']} {Colors.WHITE}{Colors.BOLD}{info['name']}{Colors.RESET}")
        print(f"     📝 Description: {Colors.CYAN}{info['description']}{Colors.RESET}")
        print(f"     🔗 URL: {Colors.BLUE}{info['url']}{Colors.RESET}")
        print()

def analyze_url_patterns():
    """Inspect URL patterns used by the category catalog."""
    print(f"\n{Colors.GREEN}🔍 URL PATTERN ANALYSIS{Colors.RESET}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

    urls = [info['url'] for info in CATEGORIES.values()]

    print(f"\n{Colors.CYAN}📊 URL Structure:{Colors.RESET}")

    base_domain = "https://www.paodeacucar.com"
    print(f"   🌐 Base domain: {Colors.WHITE}{base_domain}{Colors.RESET}")

    common_path = "/categoria/alimentos/"
    print(f"   📁 Common path: {Colors.WHITE}{common_path}{Colors.RESET}")

    print(f"\n{Colors.CYAN}📝 Category slugs:{Colors.RESET}")
    for id_cat, info in CATEGORIES.items():
        slug = info['url'].replace(base_domain + common_path, '')
        print(f"   {int(id_cat):2d}. {slug:<30} → {info['name']}")

    print(f"\n{Colors.GREEN}🏗️ FULL URL STRUCTURE:{Colors.RESET}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

    example_url = CATEGORIES["1"]["url"]
    print(f"\n{Colors.CYAN}Example: {Colors.WHITE}{example_url}{Colors.RESET}\n")

    parts = example_url.split('/')
    print(f"   1. {Colors.YELLOW}Protocol:{Colors.RESET} {parts[0]}")
    print(f"   2. {Colors.YELLOW}Domain:{Colors.RESET}   {parts[2]}")
    print(f"   3. {Colors.YELLOW}Section:{Colors.RESET}  {parts[3]}")
    print(f"   4. {Colors.YELLOW}Category:{Colors.RESET} {parts[4]}")
    print(f"   5. {Colors.YELLOW}Slug:{Colors.RESET}     {parts[5] if len(parts) > 5 else ''}")

def main():
    show_banner()
    list_all_categories()
    analyze_url_patterns()

if __name__ == "__main__":
    main()

