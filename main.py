#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🛒 Pão de Açúcar Scraping - CLI
===============================
Professional command-line toolkit for collecting nutritional data

✨ Polished interface with colors, animations, and elevated UX
🎯 Tailored for automated nutritional intelligence gathering
📊 Generates reports and detailed statistics
"""

import argparse
import sys
import pandas as pd
import os
import json
import time
import glob
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Import core modules
from url_collector import URLCollector
from scraper import Scraper
from scraping_log import logger

# ============================================================================
# 🎨 ANSI COLOR SYSTEM FOR TERMINAL OUTPUT
# ============================================================================
class Cores:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    CIANO = '\033[96m'
    MAGENTA = '\033[95m'
    BRANCO = '\033[97m'

# ============================================================================
# 🛠️ UTILITY FUNCTIONS
# ============================================================================
def limpar_terminal():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def mostrar_banner():
    """Render the CLI banner."""
    banner = f"""
{Cores.CIANO}{Cores.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║                🛒 PÃO DE AÇÚCAR SCRAPING - CLI                 ║
║                                                                  ║
║            Professional Nutritional Data Collection              ║
║                                                                  ║
║  📊 Automated nutritional data workflows                         ║
║  🎯 Polished, animation-rich interface                           ║
║  📈 Detailed reporting and analytics                             ║
╚══════════════════════════════════════════════════════════════════╝
{Cores.RESET}"""
    print(banner)

def mostrar_barra_progresso(texto: str, duracao: float = 2.0):
    """Display an animated progress bar."""
    print(f"\n{Cores.AMARELO}⏳ {texto}...{Cores.RESET}")
    barra_tamanho = 40
    for i in range(barra_tamanho + 1):
        progresso = i / barra_tamanho
        barra = "█" * i + "░" * (barra_tamanho - i)
        porcentagem = int(progresso * 100)
        print(f"\r{Cores.VERDE}[{barra}] {porcentagem}%{Cores.RESET}", end="", flush=True)
        time.sleep(duracao / barra_tamanho)
    print()

def mostrar_menu():
    """Display the interactive main menu."""
    menu = f"""
{Cores.AZUL}{Cores.BOLD}═══════════════════════ MAIN MENU ═══════════════════════{Cores.RESET}

{Cores.VERDE}🛒 COLLECTION OPERATIONS:{Cores.RESET}
  {Cores.AMARELO}1.{Cores.RESET} 🧪 {Cores.BRANCO}Test Mode{Cores.RESET}           - Quick validation crawl
  {Cores.AMARELO}2.{Cores.RESET} 🚀 {Cores.BRANCO}Full Collection{Cores.RESET}     - End-to-end extraction
  {Cores.AMARELO}3.{Cores.RESET} 🎯 {Cores.BRANCO}Custom Collection{Cores.RESET}   - Pick specific categories

{Cores.VERDE}📊 QUERY & ANALYTICS:{Cores.RESET}
  {Cores.AMARELO}4.{Cores.RESET} 🔍 {Cores.BRANCO}Browse Data{Cores.RESET}     - Review collected records
  {Cores.AMARELO}5.{Cores.RESET} 📈 {Cores.BRANCO}Statistics{Cores.RESET}      - Metrics and insights
  {Cores.AMARELO}6.{Cores.RESET} 📋 {Cores.BRANCO}List Files{Cores.RESET}      - Inspect generated files

{Cores.VERDE}📁 MANAGEMENT:{Cores.RESET}
  {Cores.AMARELO}7.{Cores.RESET} 💾 {Cores.BRANCO}Export to Excel{Cores.RESET}  - Save data as Excel
  {Cores.AMARELO}8.{Cores.RESET} 🗑️  {Cores.BRANCO}Clear Data{Cores.RESET}      - Remove legacy exports

{Cores.VERDE}ℹ️  INFORMATION:{Cores.RESET}
  {Cores.AMARELO}9.{Cores.RESET} 🛒 {Cores.BRANCO}View Categories{Cores.RESET}  - List the 16 categories
  {Cores.AMARELO}A.{Cores.RESET} 📖 {Cores.BRANCO}About{Cores.RESET}            - Program details
  {Cores.AMARELO}0.{Cores.RESET} ❌ {Cores.BRANCO}Exit{Cores.RESET}             - Close the CLI

{Cores.AZUL}═════════════════════════════════════════════════════════════════════{Cores.RESET}
"""
    print(menu)

def obter_escolha() -> str:
    """Get user input with graceful error handling."""
    try:
        escolha = input(f"{Cores.MAGENTA}👉 Choose an option (0-9, A): {Cores.RESET}").strip().lower()
        return escolha
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}⚠️  Program interrupted by user{Cores.RESET}")
        sys.exit(0)
    except EOFError:
        print(f"\n\n{Cores.AMARELO}⚠️  Input unavailable (non-interactive mode){Cores.RESET}")
        sys.exit(0)

def mostrar_sobre():
    """Display detailed information about the program."""
    sobre = f"""
{Cores.CIANO}{Cores.BOLD}📖 ABOUT PÃO DE AÇÚCAR SCRAPING{Cores.RESET}
{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}

{Cores.VERDE}🎯 PURPOSE:{Cores.RESET}
   Automated toolkit for capturing nutritional data from products
   available at the Brazilian retailer Pão de Açúcar, built with a polished
   interface and advanced analytics for data-driven teams.

{Cores.VERDE}📊 CORE CAPABILITIES:{Cores.RESET}
   • Automated product URL harvesting by category
   • JavaScript-powered extraction of nutrition tables
   • Interactive, color-rich terminal experience
   • Advanced querying with multi-filter support
   • Excel and CSV export workflows
   • Detailed statistics and analytics
   • File management with safe cleanup routines

{Cores.VERDE}🛒 SUPPORTED CATEGORIES:{Cores.RESET}
   • 13 specific food categories
   • 1 general food category (all products)
   • 1 beverage category (wine, beer, soda)
   • 1 Caras do Brasil category (Brazilian specialties)
   • TOTAL: 16 categories available for collection

{Cores.VERDE}🛠️ TECHNOLOGY STACK:{Cores.RESET}
   • Python 3.8+ with static typing
   • Selenium WebDriver for browser automation
   • Pandas for data manipulation
   • BeautifulSoup for HTML parsing
   • ANSI color system powering the CLI visuals
   • argparse for command-line UX

{Cores.VERDE}📂 DATA CAPTURED PER PRODUCT:{Cores.RESET}
   • Full product name
   • Product page URL
   • Category classification
   • Serving size (g/ml)
   • Calories (kcal)
   • Total carbohydrates (g)
   • Protein (g)
   • Total fat (g)
   • Saturated fat (g)
   • Dietary fiber (g)
   • Total sugars (g)
   • Sodium (mg)
   • Collection timestamp

{Cores.VERDE}⚡ SIGNATURE FEATURES:{Cores.RESET}
   • Vibrant, interactive interface
   • Animated progress indicators
   • Resilient error handling
   • Detailed operational logging
   • Test mode for quick validation
   • Safe cancellation flow
   • Automated browser setup
   • Cross-platform compatibility

{Cores.VERDE}📝 BUILT BY:{Cores.RESET}
   • Sidnei Almeida
   • Version: 2.0 (Interactive CLI)
   • Date: {datetime.now().strftime('%B %Y')}
   • Repository: https://github.com/sidnei-almeida/pao_de_acucar_scraping

{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}
"""
    print(sobre)

def listar_arquivos_gerados():
    """List files generated by the program."""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📋 GENERATED FILES{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    pasta_dados = "dados_coletados"

    if not os.path.exists(pasta_dados):
        print(f"{Cores.AMARELO}📁 Folder '{pasta_dados}' was not found{Cores.RESET}")
        return

    arquivos = []
    for ext in ["*.csv", "*.xlsx"]:
        arquivos.extend(glob.glob(f"{pasta_dados}/{ext}"))

    if not arquivos:
        print(f"{Cores.AMARELO}📄 No files were found inside '{pasta_dados}'{Cores.RESET}")
        return

    print(f"\n{Cores.VERDE}📊 Total files: {len(arquivos)}{Cores.RESET}\n")

    for i, arquivo in enumerate(sorted(arquivos, reverse=True), 1):
        nome_arquivo = os.path.basename(arquivo)
        tamanho = os.path.getsize(arquivo)
        data_modificacao = datetime.fromtimestamp(os.path.getmtime(arquivo))

        # Format size for readability
        if tamanho < 1024:
            tamanho_str = f"{tamanho} B"
        elif tamanho < 1024 * 1024:
            tamanho_str = f"{tamanho / 1024:.1f} KB"
        else:
            tamanho_str = f"{tamanho / (1024 * 1024):.1f} MB"

        print(f"{Cores.AMARELO}{i:2d}.{Cores.RESET} {Cores.BRANCO}{nome_arquivo}{Cores.RESET}")
        print(f"     📅 {data_modificacao.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"     📏 {tamanho_str}")
        print()

def limpar_dados_antigos():
    """Remove old files after explicit confirmation."""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🗑️  CLEAR PREVIOUS DATA{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    pasta_dados = "dados_coletados"

    if not os.path.exists(pasta_dados):
        print(f"{Cores.AMARELO}📁 Folder '{pasta_dados}' was not found{Cores.RESET}")
        return

    arquivos = []
    for ext in ["*.csv", "*.xlsx"]:
        arquivos.extend(glob.glob(f"{pasta_dados}/{ext}"))

    if not arquivos:
        print(f"{Cores.VERDE}✅ No files to clean up{Cores.RESET}")
        return

    print(f"\n{Cores.AMARELO}⚠️  WARNING:{Cores.RESET}")
    print(f"   • This will delete {Cores.VERMELHO}{len(arquivos)} file(s){Cores.RESET}")
    print(f"   • This action {Cores.VERMELHO}CANNOT be undone{Cores.RESET}")
    print(f"\n{Cores.VERDE}📋 Files scheduled for deletion:{Cores.RESET}")

    for arquivo in sorted(arquivos):
        nome_arquivo = os.path.basename(arquivo)
        print(f"   • {nome_arquivo}")

    confirmar = input(f"\n{Cores.MAGENTA}🤔 Type 'CONFIRM' to proceed: {Cores.RESET}")

    if confirmar.strip().upper() == "CONFIRM":
        try:
            for arquivo in arquivos:
                os.remove(arquivo)
            print(f"\n{Cores.VERDE}✅ {len(arquivos)} file(s) removed successfully!{Cores.RESET}")
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Failed to remove files: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operation canceled{Cores.RESET}")

def pausar():
    """Pause execution until the user confirms."""
    try:
        input(f"\n{Cores.CIANO}⏯️  Press Enter to continue...{Cores.RESET}")
    except EOFError:
        print(f"\n{Cores.AMARELO}⏭️  Non-interactive mode detected — continuing automatically...{Cores.RESET}")
        time.sleep(1)

class PaoDeAcucarCLI:
    """CLI principal para coleta de dados nutricionais"""

    def __init__(self):
        self.categorias_disponiveis = {
            # ═══════════════════════════════════════════════════════════════════
            # 🍽️ FOOD - SPECIFIC CATEGORIES
            # ═══════════════════════════════════════════════════════════════════
            "1": {"nome": "🛒 Butcher", "url": "https://www.paodeacucar.com/categoria/alimentos/acougue"},
            "2": {"nome": "🧊 Frozen Foods", "url": "https://www.paodeacucar.com/categoria/alimentos/alimentos-congelados"},
            "3": {"nome": "🥛 Refrigerated Foods", "url": "https://www.paodeacucar.com/categoria/alimentos/alimentos-refrigerados"},
            "4": {"nome": "🏠 Pantry Staples", "url": "https://www.paodeacucar.com/categoria/alimentos/basico-da-despensa"},
            "5": {"nome": "🌾 Cereals", "url": "https://www.paodeacucar.com/categoria/alimentos/cereais"},
            "6": {"nome": "📦 Pantry Add-ons", "url": "https://www.paodeacucar.com/categoria/alimentos/complemento-da-despensa"},
            "7": {"nome": "🍰 Sweets & Desserts", "url": "https://www.paodeacucar.com/categoria/alimentos/doces-e-sobremesas"},
            "8": {"nome": "🥬 Produce", "url": "https://www.paodeacucar.com/categoria/alimentos/hortifruti"},
            "9": {"nome": "🧂 Savory Grocery", "url": "https://www.paodeacucar.com/categoria/alimentos/mercearia-salgada"},
            "10": {"nome": "🍞 Bakery", "url": "https://www.paodeacucar.com/categoria/alimentos/padaria"},
            "11": {"nome": "🐟 Seafood", "url": "https://www.paodeacucar.com/categoria/alimentos/peixaria"},
            "12": {"nome": "🍗 Rotisserie", "url": "https://www.paodeacucar.com/categoria/alimentos/rotisserie"},
            "13": {"nome": "🥨 Snacks & Appetizers", "url": "https://www.paodeacucar.com/categoria/alimentos/salgadinhos-e-aperitivos"},
            
            # ═══════════════════════════════════════════════════════════════════
            # 🍽️ FOOD - GENERAL CATEGORY (ALL FOOD)
            # ═══════════════════════════════════════════════════════════════════
            "14": {"nome": "🍽️ Food (All Items)", "url": "https://www.paodeacucar.com/categoria/alimentos?s=relevance&p=1"},
            
            # ═══════════════════════════════════════════════════════════════════
            # 🥤 BEVERAGES
            # ═══════════════════════════════════════════════════════════════════
            "15": {"nome": "🥤 Beverages", "url": "https://www.paodeacucar.com/categoria/bebidas?s=relevance&p=1"},
            
            # ═══════════════════════════════════════════════════════════════════
            # 🇧🇷 CARAS DO BRASIL (BRAZILIAN PRODUCTS)
            # ═══════════════════════════════════════════════════════════════════
            "16": {"nome": "🇧🇷 Caras do Brasil", "url": "https://www.paodeacucar.com/categoria/caras-do-brasil?s=relevance&p=1"}
        }

        # Cria diretório de saída se não existir
        self.output_dir = Path("dados_coletados")
        self.output_dir.mkdir(exist_ok=True)

    def list_categories(self):
        """List every available category."""
        print(f"\n{Cores.CIANO}{Cores.BOLD}🛒 AVAILABLE CATEGORIES{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        for id_cat, info in self.categorias_disponiveis.items():
            print(f"{Cores.AMARELO}{Cores.BOLD}[{int(id_cat):2d}]{Cores.RESET} {Cores.BRANCO}{info['nome']}{Cores.RESET}")
            print(f"     🔗 {Cores.CIANO}{info['url']}{Cores.RESET}")
            print()

    def selecionar_categorias_interativo(self):
        """Enhanced interactive interface for choosing categories."""
        print(f"\n{Cores.CIANO}{Cores.BOLD}🎯 CATEGORY SELECTION{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        # Organized view
        print(f"\n{Cores.VERDE}📋 AVAILABLE CATEGORIES:{Cores.RESET}\n")

        # Specific food categories
        print(f"{Cores.CIANO}🍽️ FOOD — Specific Categories:{Cores.RESET}")
        for i in range(1, 14):
            info = self.categorias_disponiveis[str(i)]
            print(f"   {Cores.AMARELO}[{i:2d}]{Cores.RESET} {info['nome']}")

        # General food category
        print(f"\n{Cores.CIANO}🍽️ FOOD — General:{Cores.RESET}")
        print(f"   {Cores.AMARELO}[14]{Cores.RESET} {self.categorias_disponiveis['14']['nome']}")

        # Beverages
        print(f"\n{Cores.CIANO}🥤 BEVERAGES:{Cores.RESET}")
        print(f"   {Cores.AMARELO}[15]{Cores.RESET} {self.categorias_disponiveis['15']['nome']}")

        # Caras do Brasil
        print(f"\n{Cores.CIANO}🇧🇷 BRAZILIAN SPECIALTIES:{Cores.RESET}")
        print(f"   {Cores.AMARELO}[16]{Cores.RESET} {self.categorias_disponiveis['16']['nome']}")

        # Quick shortcuts
        print(f"\n{Cores.VERDE}⚡ QUICK SHORTCUTS:{Cores.RESET}")
        print(f"   {Cores.CIANO}•{Cores.RESET} Type {Cores.BRANCO}'all'{Cores.RESET} to select all 16 categories")
        print(f"   {Cores.CIANO}•{Cores.RESET} Type {Cores.BRANCO}'food'{Cores.RESET} for categories 1-13")
        print(f"   {Cores.CIANO}•{Cores.RESET} Type {Cores.BRANCO}'new'{Cores.RESET} for categories 14-16")
        print(f"   {Cores.CIANO}•{Cores.RESET} Or enter comma-separated IDs (e.g., {Cores.AMARELO}1,3,5,14,15{Cores.RESET})")

        while True:
            try:
                entrada = input(f"\n{Cores.MAGENTA}👉 Select categories: {Cores.RESET}").strip().lower()

                if not entrada:
                    print(f"{Cores.VERMELHO}❌ Select at least one category{Cores.RESET}")
                    continue

                categorias_selecionadas = []

                # Quick shortcuts (accept English and legacy Portuguese keywords)
                if entrada in {'all', 'todos'}:
                    print(f"\n{Cores.VERDE}✅ All 16 categories selected{Cores.RESET}")
                    return [self.categorias_disponiveis[str(i)] for i in range(1, 17)]

                elif entrada in {'food', 'alimentos'}:
                    print(f"\n{Cores.VERDE}✅ 13 food categories selected{Cores.RESET}")
                    return [self.categorias_disponiveis[str(i)] for i in range(1, 14)]

                elif entrada in {'new', 'novas'}:
                    print(f"\n{Cores.VERDE}✅ New categories 14-16 selected{Cores.RESET}")
                    return [self.categorias_disponiveis[str(i)] for i in range(14, 17)]

                else:
                    # Manual selection via IDs
                    ids = [id.strip() for id in entrada.split(',') if id.strip()]

                    for cat_id in ids:
                        if cat_id in self.categorias_disponiveis:
                            categorias_selecionadas.append(self.categorias_disponiveis[cat_id])
                        else:
                            print(f"{Cores.VERMELHO}❌ Invalid category: {cat_id}{Cores.RESET}")

                    if categorias_selecionadas:
                        print(f"\n{Cores.VERDE}✅ {len(categorias_selecionadas)} category(ies) selected:{Cores.RESET}")
                        for cat in categorias_selecionadas:
                            print(f"   • {cat['nome']}")
                        return categorias_selecionadas
                    else:
                        print(f"{Cores.VERMELHO}❌ No valid categories selected{Cores.RESET}")

            except KeyboardInterrupt:
                print(f"\n{Cores.AMARELO}⏭️  Operation canceled{Cores.RESET}")
                return []

    def executar_coleta_teste(self):
        """Run the collection workflow in test mode."""
        print(f"\n{Cores.CIANO}{Cores.BOLD}🧪 TEST MODE — QUICK RUN{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        print(f"\n{Cores.VERDE}🔬 Test mode highlights:{Cores.RESET}")
        print(f"   • Limits to {Cores.AMARELO}5 products{Cores.RESET} per category")
        print(f"   • Perfect for {Cores.CIANO}rapid validation{Cores.RESET}")
        print(f"   • {Cores.VERDE}Accelerated{Cores.RESET} flow for development")

        categorias = self.selecionar_categorias_interativo()
        if not categorias:
            return False

        confirmar = input(f"\n{Cores.MAGENTA}🤔 Start test collection? (y/N): {Cores.RESET}").lower()

        if confirmar in {'y', 'yes', 's', 'sim'}:
            return self.executar_coleta(categorias, modo_teste=True)
        else:
            print(f"{Cores.AMARELO}⏭️  Operation canceled{Cores.RESET}")
            return False

    def executar_coleta_completa(self):
        """Run the full collection workflow."""
        print(f"\n{Cores.CIANO}{Cores.BOLD}🚀 FULL MODE — COMPLETE COLLECTION{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        print(f"\n{Cores.AMARELO}⚠️  PLEASE NOTE:{Cores.RESET}")
        print(f"   • This run may {Cores.VERMELHO}take several hours{Cores.RESET}")
        print(f"   • It can consume {Cores.VERMELHO}significant bandwidth{Cores.RESET}")
        print(f"   • Every product in each category will be processed")

        categorias = self.selecionar_categorias_interativo()
        if not categorias:
            return False

        confirmar = input(f"\n{Cores.MAGENTA}🤔 Start full collection? (y/N): {Cores.RESET}").lower()

        if confirmar in {'y', 'yes', 's', 'sim'}:
            return self.executar_coleta(categorias, modo_teste=False)
        else:
            print(f"{Cores.AMARELO}⏭️  Operation canceled{Cores.RESET}")
            return False

    def executar_coleta(self, categorias, modo_teste=False):
        """Execute the collection workflow."""
        try:
            mostrar_barra_progresso("Preparing collection engine", 1.5)

            # Collect URLs
            urls = self.coletar_urls(categorias, modo_teste)

            if urls:
                # Extract nutritional data
                sucesso = self.extrair_dados_nutricionais(urls)
                if sucesso:
                    print(f"\n{Cores.VERDE}🎉 Collection finished successfully!{Cores.RESET}")
                    return True
                else:
                    print(f"\n{Cores.VERMELHO}❌ Error during collection{Cores.RESET}")
                    return False
            else:
                print(f"\n{Cores.VERMELHO}❌ No URLs were collected{Cores.RESET}")
                return False

        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Unexpected error: {e}{Cores.RESET}")
            return False

    def coletar_urls(self, categorias: List[Dict], modo_teste: bool = False) -> List[Dict]:
        """Collect product URLs for the selected categories."""
        print(f"\n{Cores.CIANO}{Cores.BOLD}🔍 PHASE 1: URL HARVESTING{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        todas_urls = []

        for categoria in categorias:
            print(f"\n{Cores.VERDE}📂 Processing category: {Cores.BRANCO}{categoria['nome']}{Cores.RESET}")

            try:
                mostrar_barra_progresso(f"Opening {categoria['nome']}", 1.0)

                collector = URLCollector()
                urls = collector.coletar_urls(
                    categoria['url'],
                    modo_teste=modo_teste,
                    categoria_nome=categoria['nome']
                )

                if urls:
                    print(f"{Cores.VERDE}  ✅ {len(urls)} product(s) found{Cores.RESET}")
                    todas_urls.extend(urls)

                    # Display sample products
                    print(f"{Cores.CIANO}  📝 Sample products:{Cores.RESET}")
                    for i, produto in enumerate(urls[:3], 1):
                        nome = produto['nome'][:50] + "..." if len(produto['nome']) > 50 else produto['nome']
                        print(f"    {Cores.AMARELO}{i}.{Cores.RESET} {nome}")
                    if len(urls) > 3:
                        print(f"    {Cores.CIANO}... plus {len(urls) - 3} more product(s){Cores.RESET}")
                else:
                    print(f"{Cores.AMARELO}  ⚠️ No products found{Cores.RESET}")

            except Exception as e:
                print(f"{Cores.VERMELHO}  ❌ Error collecting URLs: {e}{Cores.RESET}")

        print(f"\n{Cores.VERDE}📊 Total URLs collected: {Cores.BRANCO}{len(todas_urls)}{Cores.RESET}")
        return todas_urls

    def extrair_dados_nutricionais(self, urls: List[Dict]) -> bool:
        """Extract nutritional data from the collected URLs."""
        if not urls:
            print(f"{Cores.VERMELHO}❌ No URLs to process{Cores.RESET}")
            return False

        print(f"\n{Cores.CIANO}{Cores.BOLD}🍽️ PHASE 2: NUTRITION DATA EXTRACTION{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        print(f"{Cores.VERDE}📊 Processing {Cores.BRANCO}{len(urls)}{Cores.RESET} product(s)...{Cores.RESET}")

        try:
            mostrar_barra_progresso("Configuring scraper", 1.0)

            scraper = Scraper()

            # Save URLs into a temporary file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_urls = f"urls_temp_{timestamp}.csv"

            print(f"{Cores.CIANO}💾 Saving temporary URLs...{Cores.RESET}")
            df_urls = pd.DataFrame(urls)
            df_urls.to_csv(arquivo_urls, index=False)

            # Process the file
            mostrar_barra_progresso("Extracting nutritional data", 2.0)
            scraper.processar_arquivo_urls(arquivo_urls)

            # Remove temp file
            if os.path.exists(arquivo_urls):
                os.remove(arquivo_urls)
                print(f"{Cores.CIANO}🗑️ Temporary file removed{Cores.RESET}")

            # Confirm output file was generated
            arquivo_saida = "dados_coletados/dados_nutricionais.csv"
            if os.path.exists(arquivo_saida):
                df_resultado = pd.read_csv(arquivo_saida)
                produtos_coletados = len(df_resultado)
                print(f"\n{Cores.VERDE}✅ Data saved to '{Cores.BRANCO}{arquivo_saida}{Cores.RESET}{Cores.VERDE}'")
                print(f"📊 Products with nutritional data: {Cores.BRANCO}{produtos_coletados}{Cores.RESET}")
                return True
            else:
                print(f"{Cores.VERMELHO}❌ Error: no data was saved{Cores.RESET}")
                return False

        except Exception as e:
            print(f"{Cores.VERMELHO}❌ Error during extraction: {e}{Cores.RESET}")
            return False

    def consultar_dados(self, filtros: Optional[Dict] = None):
        """Query the collected dataset."""
        print(f"\n{Cores.CIANO}{Cores.BOLD}🔍 NUTRITION DATA QUERY{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        arquivo_dados = "dados_coletados/dados_nutricionais.csv"

        if not os.path.exists(arquivo_dados):
            print(f"{Cores.VERMELHO}❌ No data collected yet. Run a collection first.{Cores.RESET}")
            return

        try:
            mostrar_barra_progresso("Loading dataset", 1.0)

            df = pd.read_csv(arquivo_dados)

            # Apply filters if provided
            filtros_aplicados = []
            if filtros:
                if filtros.get('categoria'):
                    df = df[df['categoria'].str.contains(filtros['categoria'], case=False, na=False)]
                    filtros_aplicados.append(f"category: {filtros['categoria']}")
                if filtros.get('nome'):
                    df = df[df['nome'].str.contains(filtros['nome'], case=False, na=False)]
                    filtros_aplicados.append(f"name: {filtros['nome']}")

            if df.empty:
                print(f"{Cores.AMARELO}⚠️ No products found with the selected filters{Cores.RESET}")
                if filtros_aplicados:
                    print(f"{Cores.CIANO}Filters: {', '.join(filtros_aplicados)}{Cores.RESET}")
                return

            print(f"\n{Cores.VERDE}📊 {Cores.BRANCO}{len(df)}{Cores.RESET} product(s) found{Cores.RESET}")
            if filtros_aplicados:
                print(f"{Cores.CIANO}Applied filters: {Cores.BRANCO}{', '.join(filtros_aplicados)}{Cores.RESET}")

            print(f"\n{Cores.AZUL}📋 NUTRITIONAL SNAPSHOT:{Cores.RESET}")
            print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

            # Table header
            header = f"{Cores.BOLD}{'Product':<50} {'Category':<20} {'Calories':<10} {'Protein':<10} {'Carbohydrates':<12}{Cores.RESET}"
            print(header)
            print(f"{Cores.AZUL}{'-' * 110}{Cores.RESET}")

            # Show up to 20 products
            produtos_mostrados = 0
            for _, produto in df.iterrows():
                if produtos_mostrados >= 20:
                    break

                nome = produto['nome'][:48] + "..." if len(produto['nome']) > 48 else produto['nome']
                categoria = produto.get('categoria', 'N/A')
                categoria = categoria[:18] + "..." if len(str(categoria)) > 18 else str(categoria)

                linha = f"{nome:<50} {categoria:<20} {produto['calorias']:<10} {produto['proteinas']:<10} {produto['carboidratos']:<12}"
                print(linha)
                produtos_mostrados += 1

            if len(df) > 20:
                print(f"\n{Cores.CIANO}... plus {len(df) - 20} additional product(s) (total: {len(df)}){Cores.RESET}")

            # Save filtered result if filters were applied
            if filtros:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                arquivo_consulta = self.output_dir / f"consulta_{timestamp}.csv"
                df.to_csv(arquivo_consulta, index=False)
                print(f"\n{Cores.VERDE}💾 Query saved to: {Cores.BRANCO}{arquivo_consulta}{Cores.RESET}")

        except Exception as e:
            print(f"{Cores.VERMELHO}❌ Error while querying data: {e}{Cores.RESET}")

    def exportar_excel(self, filtros: Optional[Dict] = None):
        """Export data to an Excel spreadsheet."""
        print(f"\n{Cores.CIANO}{Cores.BOLD}💾 EXCEL EXPORT{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        arquivo_dados = "dados_nutricionais.csv"

        if not os.path.exists(arquivo_dados):
            print(f"{Cores.VERMELHO}❌ No data collected yet. Run a collection first.{Cores.RESET}")
            return

        try:
            mostrar_barra_progresso("Loading data for export", 1.0)

            df = pd.read_csv(arquivo_dados)

            # Apply filters if provided
            filtros_aplicados = []
            if filtros:
                if filtros.get('categoria'):
                    df = df[df['categoria'].str.contains(filtros['categoria'], case=False, na=False)]
                    filtros_aplicados.append(f"category: {filtros['categoria']}")
                if filtros.get('nome'):
                    df = df[df['nome'].str.contains(filtros['nome'], case=False, na=False)]
                    filtros_aplicados.append(f"name: {filtros['nome']}")

            if df.empty:
                print(f"{Cores.AMARELO}⚠️ No products matched the provided filters{Cores.RESET}")
                return

            # Generate file name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_excel = self.output_dir / f"dados_nutricionais_{timestamp}.xlsx"

            print(f"\n{Cores.VERDE}📊 Preparing to export {Cores.BRANCO}{len(df)}{Cores.RESET} product(s)...{Cores.RESET}")
            if filtros_aplicados:
                print(f"{Cores.CIANO}Applied filters: {Cores.BRANCO}{', '.join(filtros_aplicados)}{Cores.RESET}")

            # Export to Excel
            mostrar_barra_progresso("Generating Excel file", 1.5)
            df.to_excel(arquivo_excel, index=False, engine='openpyxl')

            print(f"\n{Cores.VERDE}✅ Export completed successfully!{Cores.RESET}")
            print(f"{Cores.CIANO}📁 File: {Cores.BRANCO}{arquivo_excel}{Cores.RESET}")
            print(f"{Cores.CIANO}📊 Products exported: {Cores.BRANCO}{len(df)}{Cores.RESET}")
            print(f"{Cores.CIANO}📏 Size: {Cores.BRANCO}{arquivo_excel.stat().st_size / 1024:.1f} KB{Cores.RESET}")

        except Exception as e:
            print(f"{Cores.VERMELHO}❌ Error exporting to Excel: {e}{Cores.RESET}")

    def validar_categorias(self, categorias_ids: List[str]) -> List[Dict]:
        """Validate and return selected categories."""
        categorias_validas = []
        
        for cat_id in categorias_ids:
            if cat_id in self.categorias_disponiveis:
                categorias_validas.append(self.categorias_disponiveis[cat_id])
            else:
                print(f"❌ Invalid category: {cat_id}")
        
        return categorias_validas

    def mostrar_estatisticas(self):
        """Display detailed statistics for the collected dataset."""
        print(f"\n{Cores.CIANO}{Cores.BOLD}📈 DATASET STATISTICS{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        arquivo_dados = "dados_coletados/dados_nutricionais.csv"

        if not os.path.exists(arquivo_dados):
            print(f"{Cores.VERMELHO}❌ No data collected yet. Run a collection first.{Cores.RESET}")
            return

        try:
            mostrar_barra_progresso("Calculating statistics", 1.0)

            df = pd.read_csv(arquivo_dados)

            if df.empty:
                print(f"{Cores.AMARELO}⚠️ No data available for analysis{Cores.RESET}")
                return

            print(f"\n{Cores.VERDE}📊 OVERVIEW:{Cores.RESET}")
            print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
            print(f"   📈 Total products: {Cores.BRANCO}{len(df)}{Cores.RESET}")
            print(f"   📂 Distinct categories: {Cores.BRANCO}{df['categoria'].nunique()}{Cores.RESET}")

            if 'data_coleta' in df.columns and df['data_coleta'].notna().any():
                ultima_coleta = df['data_coleta'].max()
                print(f"   📅 Latest collection: {Cores.BRANCO}{ultima_coleta}{Cores.RESET}")

            # Nutritional averages
            print(f"\n{Cores.VERDE}🥗 NUTRITIONAL AVERAGES (per 100g):{Cores.RESET}")
            print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

            colunas_nutricionais = ['calorias', 'proteinas', 'carboidratos', 'gorduras']
            medias = df[colunas_nutricionais].mean()

            print(f"   🔥 Calories:      {Cores.BRANCO}{medias['calorias']:7.1f}{Cores.RESET} kcal")
            print(f"   💪 Protein:       {Cores.BRANCO}{medias['proteinas']:7.1f}{Cores.RESET} g")
            print(f"   🌾 Carbohydrates: {Cores.BRANCO}{medias['carboidratos']:7.1f}{Cores.RESET} g")
            print(f"   🧈 Fat:           {Cores.BRANCO}{medias['gorduras']:7.1f}{Cores.RESET} g")

            # Top categories
            print(f"\n{Cores.VERDE}🏆 TOP 5 CATEGORIES:{Cores.RESET}")
            print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

            top_categorias = df['categoria'].value_counts().head()
            for i, (categoria, count) in enumerate(top_categorias.items(), 1):
                porcentagem = (count / len(df)) * 100
                emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1] if i <= 5 else "📊"
                print(f"   {emoji} {categoria}")
                print(f"      📊 {count} product(s) ({porcentagem:5.1f}%)")

            # Additional stats
            print(f"\n{Cores.VERDE}📋 DETAILED INSIGHTS:{Cores.RESET}")
            print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

            # Min and max calorie products
            produto_menos_calorias = df.loc[df['calorias'].idxmin(), 'nome']
            produto_mais_calorias = df.loc[df['calorias'].idxmax(), 'nome']
            print(f"   📉 Lowest-calorie product: {Cores.BRANCO}{produto_menos_calorias[:40]}...{Cores.RESET} ({df['calorias'].min()} kcal)")
            print(f"   📈 Highest-calorie product: {Cores.BRANCO}{produto_mais_calorias[:40]}...{Cores.RESET} ({df['calorias'].max()} kcal)")

            # Distribution by category
            print(f"\n{Cores.CIANO}📊 Category distribution:{Cores.RESET}")
            distribuicao = df['categoria'].value_counts()
            for categoria, count in distribuicao.items():
                print(f"   • {categoria}: {count} product(s)")

        except Exception as e:
            print(f"{Cores.VERMELHO}❌ Error calculating statistics: {e}{Cores.RESET}")

def main():
    """Função principal - Interface interativa do programa"""
    try:
        while True:
            limpar_terminal()
            mostrar_banner()
            mostrar_menu()

            escolha = obter_escolha()

            # Inicializa o CLI
            cli = PaoDeAcucarCLI()

            if escolha == "1":
                sucesso = cli.executar_coleta_teste()
                if sucesso:
                    print(f"\n{Cores.VERDE}🎉 Test collection completed successfully!{Cores.RESET}")
                pausar()

            elif escolha == "2":
                sucesso = cli.executar_coleta_completa()
                if sucesso:
                    print(f"\n{Cores.VERDE}🎉 Full collection completed successfully!{Cores.RESET}")
                pausar()

            elif escolha == "3":
                # Custom collection - choose categories
                print(f"\n{Cores.CIANO}{Cores.BOLD}🎯 CUSTOM COLLECTION{Cores.RESET}")
                print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

                print(f"\n{Cores.VERDE}📋 Choose which categories to collect:{Cores.RESET}")
                print(f"   • Select specific categories")
                print(f"   • Choose between test (quick) or full (complete) modes")

                # Select categories
                categorias = cli.selecionar_categorias_interativo()
                if not categorias:
                    pausar()
                    continue

                # Choose mode
                print(f"\n{Cores.VERDE}⚙️ COLLECTION MODE:{Cores.RESET}")
                print(f"   {Cores.AMARELO}1.{Cores.RESET} 🧪 {Cores.BRANCO}Test{Cores.RESET} - Quick (5 products/category)")
                print(f"   {Cores.AMARELO}2.{Cores.RESET} 🚀 {Cores.BRANCO}Full{Cores.RESET} - Unlimited (all products)")

                modo_escolha = input(f"\n{Cores.MAGENTA}👉 Select mode (1-2): {Cores.RESET}").strip()

                modo_teste = modo_escolha == "1"
                modo_nome = "test" if modo_teste else "full"

                print(f"\n{Cores.VERDE}✅ Mode selected: {Cores.BRANCO}{modo_nome.upper()}{Cores.RESET}")

                confirmar = input(f"\n{Cores.MAGENTA}🤔 Start {modo_nome} collection? (y/N): {Cores.RESET}").lower()

                if confirmar in {'y', 'yes', 's', 'sim'}:
                    sucesso = cli.executar_coleta(categorias, modo_teste)
                    if sucesso:
                        print(f"\n{Cores.VERDE}🎉 Custom collection completed successfully!{Cores.RESET}")
                else:
                    print(f"{Cores.AMARELO}⏭️  Operation canceled{Cores.RESET}")

                pausar()

            elif escolha == "4":
                # Interactive query
                print(f"\n{Cores.CIANO}{Cores.BOLD}🔍 INTERACTIVE QUERY{Cores.RESET}")
                print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

                print(f"\n{Cores.VERDE}📋 Available filters:{Cores.RESET}")
                print(f"   • Enter a category name (e.g., Produce)")
                print(f"   • Enter a product name (e.g., milk)")
                print(f"   • Leave blank to show all data")

                categoria = input(f"\n{Cores.MAGENTA}🏷️ Category (optional): {Cores.RESET}").strip()
                nome = input(f"{Cores.MAGENTA}🔍 Product name (optional): {Cores.RESET}").strip()

                filtros = {}
                if categoria:
                    filtros['categoria'] = categoria
                if nome:
                    filtros['nome'] = nome

                cli.consultar_dados(filtros)
                pausar()

            elif escolha == "5":
                cli.mostrar_estatisticas()
                pausar()

            elif escolha == "6":
                listar_arquivos_gerados()
                pausar()

            elif escolha == "7":
                # Interactive export
                print(f"\n{Cores.CIANO}{Cores.BOLD}💾 INTERACTIVE EXPORT{Cores.RESET}")
                print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

                print(f"\n{Cores.VERDE}📋 Filters for export:{Cores.RESET}")
                categoria = input(f"{Cores.MAGENTA}🏷️ Category (optional): {Cores.RESET}").strip()
                nome = input(f"{Cores.MAGENTA}🔍 Product name (optional): {Cores.RESET}").strip()

                filtros = {}
                if categoria:
                    filtros['categoria'] = categoria
                if nome:
                    filtros['nome'] = nome

                cli.exportar_excel(filtros)
                pausar()

            elif escolha == "8":
                limpar_dados_antigos()
                pausar()

            elif escolha == "9":
                # Show all categories
                cli.list_categories()
                pausar()

            elif escolha == "a":
                mostrar_sobre()
                pausar()

            elif escolha == "0":
                print(f"\n{Cores.VERDE}👋 Thanks for using the Pão de Açúcar Scraping CLI!{Cores.RESET}")
                print(f"{Cores.CIANO}🚀 See you next time!{Cores.RESET}\n")
                break

            else:
                print(f"\n{Cores.VERMELHO}❌ Invalid option! Please choose between 0-9 or A{Cores.RESET}")
                time.sleep(2)

    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}👋 Program terminated by user. See you soon!{Cores.RESET}\n")
    except Exception as e:
        print(f"\n{Cores.VERMELHO}❌ Unexpected error: {e}{Cores.RESET}")
        logger.error(f"Unexpected error in main program: {str(e)}")

# ============================================================================
# 📋 COMMAND-LINE USAGE EXAMPLES (LEGACY COMPATIBILITY)
# ============================================================================
def main_cli():
    """Traditional command-line interface (for scripting)."""
    parser = argparse.ArgumentParser(
        description="🛒 Pão de Açúcar Scraping — Nutritional data collection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py list-categories
  python main.py coletar --categorias 1 2 3 --teste
  python main.py consultar --categoria "Produce"
  python main.py exportar --categoria "Snacks" --formato excel
  python main.py estatisticas
        """
    )

    subparsers = parser.add_subparsers(dest='comando', help='Available commands')

    # Command: list categories
    subparsers.add_parser(
        'list-categories',
        aliases=['listar-categorias'],
        help='List all available categories'
    )

    # Command: collect
    coletar_parser = subparsers.add_parser('coletar', help='Collect nutritional data')
    coletar_parser.add_argument('--categorias', nargs='+', required=True,
                               help='Category IDs to collect (e.g., 1 2 3)')
    coletar_parser.add_argument('--teste', action='store_true',
                               help='Test mode (limited collection)')

    # Command: query
    consultar_parser = subparsers.add_parser('consultar', help='Query collected data')
    consultar_parser.add_argument('--categoria', help='Filter by category name')
    consultar_parser.add_argument('--nome', help='Filter by product name')

    # Command: export
    exportar_parser = subparsers.add_parser('exportar', help='Export data to a file')
    exportar_parser.add_argument('--categoria', help='Filter by category name')
    exportar_parser.add_argument('--nome', help='Filter by product name')
    exportar_parser.add_argument('--formato', choices=['excel', 'csv'], default='excel',
                                help='Export format (default: excel)')

    # Command: statistics
    subparsers.add_parser('estatisticas', help='Show statistics from the collected data')

    # Parse arguments
    args = parser.parse_args()

    # No command provided: fall back to interactive interface
    if not args.comando:
        main()
        return

    # Initialize CLI
    cli = PaoDeAcucarCLI()

    try:
        if args.comando in {'list-categories', 'listar-categorias'}:
            cli.list_categories()

        elif args.comando == 'coletar':
            # Validate categories
            categorias = cli.validar_categorias(args.categorias)
            if not categorias:
                print("❌ No valid categories selected")
                return

            # Collect URLs
            urls = cli.coletar_urls(categorias, args.teste)

            if urls:
                # Extract nutritional data
                sucesso = cli.extrair_dados_nutricionais(urls)
                if sucesso:
                    print("\n🎉 Collection completed successfully!")
                else:
                    print("\n❌ Error during collection")
            else:
                print("\n❌ No URLs collected")

        elif args.comando == 'consultar':
            filtros = {}
            if args.categoria:
                filtros['categoria'] = args.categoria
            if args.nome:
                filtros['nome'] = args.nome
            cli.consultar_dados(filtros)

        elif args.comando == 'exportar':
            filtros = {}
            if args.categoria:
                filtros['categoria'] = args.categoria
            if args.nome:
                filtros['nome'] = args.nome

            if args.formato == 'excel':
                cli.exportar_excel(filtros)
            else:
                print("❌ CSV output not implemented yet")

        elif args.comando == 'estatisticas':
            cli.mostrar_estatisticas()

    except KeyboardInterrupt:
        print("\n\n⚠️ Operation interrupted by user")
        return
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        logger.error(f"Error in CLI: {str(e)}")
        return

if __name__ == "__main__":
    main_cli()
