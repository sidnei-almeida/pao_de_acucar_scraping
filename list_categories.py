#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📋 UPDATED CATEGORY LIST
========================
Displays all 16 categories currently available for data collection.
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
# 📊 ALL AVAILABLE CATEGORIES (UPDATED)
# ============================================================================
CATEGORIES = {
    # ═══════════════════════════════════════════════════════════════════
    # 🍽️ FOOD – SPECIFIC CATEGORIES
    # ═══════════════════════════════════════════════════════════════════
    "1": {"name": "🛒 Butcher", "url": "https://www.paodeacucar.com/categoria/alimentos/acougue"},
    "2": {"name": "🧊 Frozen Foods", "url": "https://www.paodeacucar.com/categoria/alimentos/alimentos-congelados"},
    "3": {"name": "🥛 Refrigerated Foods", "url": "https://www.paodeacucar.com/categoria/alimentos/alimentos-refrigerados"},
    "4": {"name": "🏠 Pantry Staples", "url": "https://www.paodeacucar.com/categoria/alimentos/basico-da-despensa"},
    "5": {"name": "🌾 Cereals", "url": "https://www.paodeacucar.com/categoria/alimentos/cereais"},
    "6": {"name": "📦 Pantry Add-ons", "url": "https://www.paodeacucar.com/categoria/alimentos/complemento-da-despensa"},
    "7": {"name": "🍰 Sweets & Desserts", "url": "https://www.paodeacucar.com/categoria/alimentos/doces-e-sobremesas"},
    "8": {"name": "🥬 Produce", "url": "https://www.paodeacucar.com/categoria/alimentos/hortifruti"},
    "9": {"name": "🧂 Savory Grocery", "url": "https://www.paodeacucar.com/categoria/alimentos/mercearia-salgada"},
    "10": {"name": "🍞 Bakery", "url": "https://www.paodeacucar.com/categoria/alimentos/padaria"},
    "11": {"name": "🐟 Seafood", "url": "https://www.paodeacucar.com/categoria/alimentos/peixaria"},
    "12": {"name": "🍗 Rotisserie", "url": "https://www.paodeacucar.com/categoria/alimentos/rotisserie"},
    "13": {"name": "🥨 Snacks & Appetizers", "url": "https://www.paodeacucar.com/categoria/alimentos/salgadinhos-e-aperitivos"},

    # ═══════════════════════════════════════════════════════════════════
    # 🍽️ FOOD – GENERAL CATEGORY (ALL FOOD)
    # ═══════════════════════════════════════════════════════════════════
    "14": {"name": "🍽️ Food (All Items)", "url": "https://www.paodeacucar.com/categoria/alimentos?s=relevance&p=1"},

    # ═══════════════════════════════════════════════════════════════════
    # 🥤 BEVERAGES
    # ═══════════════════════════════════════════════════════════════════
    "15": {"name": "🥤 Beverages", "url": "https://www.paodeacucar.com/categoria/bebidas?s=relevance&p=1"},

    # ═══════════════════════════════════════════════════════════════════
    # 🇧🇷 CARAS DO BRASIL (BRAZILIAN PRODUCTS)
    # ═══════════════════════════════════════════════════════════════════
    "16": {"name": "🇧🇷 Caras do Brasil", "url": "https://www.paodeacucar.com/categoria/caras-do-brasil?s=relevance&p=1"}
}

def show_banner():
    """Display the program banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════╗
║            🛒 PÃO DE AÇÚCAR CATEGORIES - UPDATED                        ║
║                                                                          ║
║              Complete catalog with 16 available categories               ║
╚══════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)

def main():
    """Main entry point."""
    show_banner()

    print(f"\n{Colors.GREEN}{Colors.BOLD}📋 FULL CATEGORY LIST{Colors.RESET}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

    # Group categories by section
    print(f"\n{Colors.CYAN}🍽️ FOOD – SPECIFIC CATEGORIES (13 total):{Colors.RESET}")
    print(f"{Colors.BLUE}{'─' * 85}{Colors.RESET}")

    for category_id in range(1, 14):
        info = CATEGORIES[str(category_id)]
        print(f"{Colors.YELLOW}{Colors.BOLD}[{category_id:2d}]{Colors.RESET} {info['name']}")
        print(f"     🔗 {Colors.WHITE}{info['url']}{Colors.RESET}")

    print(f"\n{Colors.CYAN}🍽️ FOOD – GENERAL CATEGORY:{Colors.RESET}")
    print(f"{Colors.BLUE}{'─' * 85}{Colors.RESET}")
    info = CATEGORIES["14"]
    print(f"{Colors.YELLOW}{Colors.BOLD}[14]{Colors.RESET} {info['name']}")
    print(f"     🔗 {Colors.WHITE}{info['url']}{Colors.RESET}")
    print(f"     {Colors.CYAN}💡 Includes every food product in one place{Colors.RESET}")

    print(f"\n{Colors.CYAN}🥤 BEVERAGES:{Colors.RESET}")
    print(f"{Colors.BLUE}{'─' * 85}{Colors.RESET}")
    info = CATEGORIES["15"]
    print(f"{Colors.YELLOW}{Colors.BOLD}[15]{Colors.RESET} {info['name']}")
    print(f"     🔗 {Colors.WHITE}{info['url']}{Colors.RESET}")
    print(f"     {Colors.CYAN}💡 Wine, beer, soft drinks, juices, water, and more{Colors.RESET}")

    print(f"\n{Colors.CYAN}🇧🇷 BRAZILIAN PRODUCTS:{Colors.RESET}")
    print(f"{Colors.BLUE}{'─' * 85}{Colors.RESET}")
    info = CATEGORIES["16"]
    print(f"{Colors.YELLOW}{Colors.BOLD}[16]{Colors.RESET} {info['name']}")
    print(f"     🔗 {Colors.WHITE}{info['url']}{Colors.RESET}")
    print(f"     {Colors.CYAN}💡 Curated, artisanal Brazilian products{Colors.RESET}")

    # Statistics
    print(f"\n{Colors.GREEN}📊 STATISTICS:{Colors.RESET}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

    print(f"\n   📈 Total categories: {Colors.WHITE}{Colors.BOLD}{len(CATEGORIES)}{Colors.RESET}")
    print(f"   🍽️ Food (specific): {Colors.WHITE}13{Colors.RESET}")
    print(f"   🍽️ Food (general): {Colors.WHITE}1{Colors.RESET}")
    print(f"   🥤 Beverages: {Colors.WHITE}1{Colors.RESET}")
    print(f"   🇧🇷 Caras do Brasil: {Colors.WHITE}1{Colors.RESET}")

    # URL pattern differences
    print(f"\n{Colors.GREEN}🔍 IDENTIFIED URL PATTERNS:{Colors.RESET}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

    print(f"\n   {Colors.CYAN}Pattern 1 – Specific food categories (1-13):{Colors.RESET}")
    print(f"   {Colors.WHITE}https://www.paodeacucar.com/categoria/alimentos/[slug]{Colors.RESET}")

    print(f"\n   {Colors.CYAN}Pattern 2 – Categories with pagination and sorting (14-16):{Colors.RESET}")
    print(f"   {Colors.WHITE}https://www.paodeacucar.com/categoria/[category]?s=relevance&p=1{Colors.RESET}")

    print(f"\n{Colors.YELLOW}💡 NOTES:{Colors.RESET}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

    print(f"\n   {Colors.CYAN}🎯 URLs with parameters (categories 14-16):{Colors.RESET}")
    print(f"      • {Colors.GREEN}s=relevance{Colors.RESET} – Sorting by relevance")
    print(f"      • {Colors.GREEN}p=1{Colors.RESET} – Initial page number")
    print(f"      • The system performs scroll operations to load all products")

    print(f"\n   {Colors.CYAN}🛒 Simple URLs (categories 1-13):{Colors.RESET}")
    print(f"      • Format: /categoria/alimentos/[slug]")
    print(f"      • No parameters on the base URL")
    print(f"      • Pagination is handled automatically when needed")

    print(f"\n{Colors.GREEN}✅ System updated and ready to collect all 16 categories!{Colors.RESET}")

if __name__ == "__main__":
    main()

