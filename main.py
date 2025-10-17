#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🛒 Pão de Açúcar Scraping - CLI
===============================
Sistema profissional de coleta de dados nutricionais via linha de comando

✨ Interface elegante com cores, animações e experiência de usuário aprimorada
🎯 Especializado na coleta automatizada de informações nutricionais
📊 Geração de relatórios e estatísticas detalhadas
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

# Importa módulos essenciais
from url_collector import URLCollector
from scraper import Scraper
from scraping_log import logger

# ============================================================================
# 🎨 SISTEMA DE CORES ANSI PARA TERMINAL
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
# 🛠️ FUNÇÕES UTILITÁRIAS
# ============================================================================
def limpar_terminal():
    """Limpa o terminal"""
    os.system('clear' if os.name == 'posix' else 'cls')

def mostrar_banner():
    """Exibe o banner principal do programa"""
    banner = f"""
{Cores.CIANO}{Cores.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║                🛒 PÃO DE AÇÚCAR SCRAPING - CLI                 ║
║                                                                  ║
║             Sistema Profissional de Coleta Nutricional           ║
║                                                                  ║
║  📊 Coleta automatizada de dados nutricionais                   ║
║  🎯 Interface elegante com experiência aprimorada               ║
║  📈 Relatórios e estatísticas detalhadas                        ║
╚══════════════════════════════════════════════════════════════════╝
{Cores.RESET}"""
    print(banner)

def mostrar_barra_progresso(texto: str, duracao: float = 2.0):
    """Exibe uma barra de progresso animada"""
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
    """Exibe o menu principal interativo"""
    menu = f"""
{Cores.AZUL}{Cores.BOLD}═════════════════════ MENU PRINCIPAL ═════════════════════{Cores.RESET}

{Cores.VERDE}🛒 OPERAÇÕES DE COLETA:{Cores.RESET}
  {Cores.AMARELO}1.{Cores.RESET} 🧪 {Cores.BRANCO}Modo Teste{Cores.RESET}          - Coleta rápida para validação
  {Cores.AMARELO}2.{Cores.RESET} 🚀 {Cores.BRANCO}Coleta Completa{Cores.RESET}      - Extração completa de dados
  {Cores.AMARELO}3.{Cores.RESET} 🎯 {Cores.BRANCO}Coleta Personalizada{Cores.RESET} - Escolher categorias específicas

{Cores.VERDE}📊 CONSULTA E ANÁLISE:{Cores.RESET}
  {Cores.AMARELO}4.{Cores.RESET} 🔍 {Cores.BRANCO}Consultar Dados{Cores.RESET}  - Visualizar informações coletadas
  {Cores.AMARELO}5.{Cores.RESET} 📈 {Cores.BRANCO}Estatísticas{Cores.RESET}     - Análise e métricas detalhadas
  {Cores.AMARELO}6.{Cores.RESET} 📋 {Cores.BRANCO}Listar Arquivos{Cores.RESET}  - Ver arquivos gerados

{Cores.VERDE}📁 GERENCIAMENTO:{Cores.RESET}
  {Cores.AMARELO}7.{Cores.RESET} 💾 {Cores.BRANCO}Exportar Excel{Cores.RESET}   - Salvar dados em formato Excel
  {Cores.AMARELO}8.{Cores.RESET} 🗑️  {Cores.BRANCO}Limpar Dados{Cores.RESET}     - Remover arquivos antigos

{Cores.VERDE}ℹ️  INFORMAÇÕES:{Cores.RESET}
  {Cores.AMARELO}9.{Cores.RESET} 🛒 {Cores.BRANCO}Ver Categorias{Cores.RESET}   - Lista as 16 categorias disponíveis
  {Cores.AMARELO}A.{Cores.RESET} 📖 {Cores.BRANCO}Sobre{Cores.RESET}           - Informações do programa
  {Cores.AMARELO}0.{Cores.RESET} ❌ {Cores.BRANCO}Sair{Cores.RESET}            - Encerrar programa

{Cores.AZUL}═══════════════════════════════════════════════════════════{Cores.RESET}
"""
    print(menu)

def obter_escolha() -> str:
    """Obtém a escolha do usuário com tratamento de erros"""
    try:
        escolha = input(f"{Cores.MAGENTA}👉 Digite sua opção (0-9, A): {Cores.RESET}").strip().lower()
        return escolha
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}⚠️  Programa interrompido pelo usuário{Cores.RESET}")
        sys.exit(0)

def mostrar_sobre():
    """Exibe informações detalhadas sobre o programa"""
    sobre = f"""
{Cores.CIANO}{Cores.BOLD}📖 SOBRE O PÃO DE AÇÚCAR SCRAPING{Cores.RESET}
{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}

{Cores.VERDE}🎯 OBJETIVO:{Cores.RESET}
   Sistema automatizado para coleta de dados nutricionais de produtos
   do supermercado Pão de Açúcar, oferecendo interface elegante e
   funcionalidades avançadas de análise de dados.

{Cores.VERDE}📊 FUNCIONALIDADES PRINCIPAIS:{Cores.RESET}
   • Coleta automatizada de URLs de produtos por categoria
   • Extração inteligente de tabelas nutricionais via JavaScript
   • Interface interativa com cores e animações
   • Sistema de consulta avançada com filtros
   • Exportação para Excel e CSV
   • Estatísticas detalhadas e análise de dados
   • Gerenciamento de arquivos com limpeza automática

{Cores.VERDE}🛒 CATEGORIAS SUPORTADAS:{Cores.RESET}
   • 13 categorias de alimentos específicas
   • 1 categoria geral de alimentos (todos os produtos)
   • 1 categoria de bebidas (vinhos, cervejas, refrigerantes)
   • 1 categoria Caras do Brasil (produtos brasileiros)
   • TOTAL: 16 categorias disponíveis para coleta

{Cores.VERDE}🛠️ TECNOLOGIAS UTILIZADAS:{Cores.RESET}
   • Python 3.8+ com tipagem estática
   • Selenium WebDriver para automação web
   • Pandas para manipulação de dados
   • BeautifulSoup para parsing HTML
   • Sistema de cores ANSI para interface bonita
   • argparse para interface de linha de comando

{Cores.VERDE}📂 DADOS COLETADOS POR PRODUTO:{Cores.RESET}
   • Nome completo do produto
   • URL da página do produto
   • Categoria de classificação
   • Porção recomendada (g/ml)
   • Valor calórico (kcal)
   • Carboidratos totais (g)
   • Proteínas (g)
   • Gorduras totais (g)
   • Gorduras saturadas (g)
   • Fibras alimentares (g)
   • Açúcares totais (g)
   • Sódio (mg)
   • Data e hora da coleta

{Cores.VERDE}⚡ CARACTERÍSTICAS:{Cores.RESET}
   • Interface interativa com cores vibrantes
   • Barras de progresso animadas
   • Tratamento robusto de erros
   • Logs detalhados das operações
   • Modo teste para validações rápidas
   • Sistema de cancelamento seguro
   • Configuração automática do navegador
   • Compatibilidade multiplataforma

{Cores.VERDE}📝 DESENVOLVIDO POR:{Cores.RESET}
   • Sidnei Almeida
   • Versão: 2.0 (CLI Interativa)
   • Data: {datetime.now().strftime('%B %Y')}
   • Repositório: https://github.com/sidnei-almeida/pao_de_acucar_scraping

{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}
"""
    print(sobre)

def listar_arquivos_gerados():
    """Lista arquivos gerados pelo programa"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📋 ARQUIVOS GERADOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    pasta_dados = "dados_coletados"

    if not os.path.exists(pasta_dados):
        print(f"{Cores.AMARELO}📁 Pasta '{pasta_dados}' não encontrada{Cores.RESET}")
        return

    arquivos = []
    for ext in ["*.csv", "*.xlsx"]:
        arquivos.extend(glob.glob(f"{pasta_dados}/{ext}"))

    if not arquivos:
        print(f"{Cores.AMARELO}📄 Nenhum arquivo encontrado em '{pasta_dados}'{Cores.RESET}")
        return

    print(f"\n{Cores.VERDE}📊 Total de arquivos: {len(arquivos)}{Cores.RESET}\n")

    for i, arquivo in enumerate(sorted(arquivos, reverse=True), 1):
        nome_arquivo = os.path.basename(arquivo)
        tamanho = os.path.getsize(arquivo)
        data_modificacao = datetime.fromtimestamp(os.path.getmtime(arquivo))

        # Calcula o tamanho em formato legível
        if tamanho < 1024:
            tamanho_str = f"{tamanho} B"
        elif tamanho < 1024 * 1024:
            tamanho_str = f"{tamanho / 1024:.1f} KB"
        else:
            tamanho_str = f"{tamanho / (1024 * 1024):.1f} MB"

        print(f"{Cores.AMARELO}{i:2d}.{Cores.RESET} {Cores.BRANCO}{nome_arquivo}{Cores.RESET}")
        print(f"     📅 {data_modificacao.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"     📏 {tamanho_str}")
        print()

def limpar_dados_antigos():
    """Remove arquivos antigos com confirmação"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🗑️  LIMPAR DADOS ANTIGOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    pasta_dados = "dados_coletados"

    if not os.path.exists(pasta_dados):
        print(f"{Cores.AMARELO}📁 Pasta '{pasta_dados}' não encontrada{Cores.RESET}")
        return

    arquivos = []
    for ext in ["*.csv", "*.xlsx"]:
        arquivos.extend(glob.glob(f"{pasta_dados}/{ext}"))

    if not arquivos:
        print(f"{Cores.VERDE}✅ Nenhum arquivo para limpar{Cores.RESET}")
        return

    print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO:{Cores.RESET}")
    print(f"   • Serão removidos {Cores.VERMELHO}{len(arquivos)} arquivos{Cores.RESET}")
    print(f"   • Esta ação {Cores.VERMELHO}NÃO PODE ser desfeita{Cores.RESET}")
    print(f"\n{Cores.VERDE}📋 Arquivos que serão removidos:{Cores.RESET}")

    for arquivo in sorted(arquivos):
        nome_arquivo = os.path.basename(arquivo)
        print(f"   • {nome_arquivo}")

    confirmar = input(f"\n{Cores.MAGENTA}🤔 Tem certeza? Digite 'CONFIRMAR' para prosseguir: {Cores.RESET}")

    if confirmar == "CONFIRMAR":
        try:
            for arquivo in arquivos:
                os.remove(arquivo)
            print(f"\n{Cores.VERDE}✅ {len(arquivos)} arquivos removidos com sucesso!{Cores.RESET}")
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro ao remover arquivos: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def pausar():
    """Pausa o programa aguardando input do usuário"""
    input(f"\n{Cores.CIANO}⏯️  Pressione Enter para continuar...{Cores.RESET}")

class PaoDeAcucarCLI:
    """CLI principal para coleta de dados nutricionais"""

    def __init__(self):
        self.categorias_disponiveis = {
            # ═══════════════════════════════════════════════════════════════════
            # 🍽️ ALIMENTOS - CATEGORIAS ESPECÍFICAS
            # ═══════════════════════════════════════════════════════════════════
            "1": {"nome": "🛒 Açougue", "url": "https://www.paodeacucar.com/categoria/alimentos/acougue"},
            "2": {"nome": "🧊 Alimentos Congelados", "url": "https://www.paodeacucar.com/categoria/alimentos/alimentos-congelados"},
            "3": {"nome": "🥛 Alimentos Refrigerados", "url": "https://www.paodeacucar.com/categoria/alimentos/alimentos-refrigerados"},
            "4": {"nome": "🏠 Básicos da Despensa", "url": "https://www.paodeacucar.com/categoria/alimentos/basico-da-despensa"},
            "5": {"nome": "🌾 Cereais", "url": "https://www.paodeacucar.com/categoria/alimentos/cereais"},
            "6": {"nome": "📦 Complemento da Despensa", "url": "https://www.paodeacucar.com/categoria/alimentos/complemento-da-despensa"},
            "7": {"nome": "🍰 Doces e Sobremesas", "url": "https://www.paodeacucar.com/categoria/alimentos/doces-e-sobremesas"},
            "8": {"nome": "🥬 Hortifruti", "url": "https://www.paodeacucar.com/categoria/alimentos/hortifruti"},
            "9": {"nome": "🧂 Mercearia Salgada", "url": "https://www.paodeacucar.com/categoria/alimentos/mercearia-salgada"},
            "10": {"nome": "🍞 Padaria", "url": "https://www.paodeacucar.com/categoria/alimentos/padaria"},
            "11": {"nome": "🐟 Peixaria", "url": "https://www.paodeacucar.com/categoria/alimentos/peixaria"},
            "12": {"nome": "🍗 Rotisserie", "url": "https://www.paodeacucar.com/categoria/alimentos/rotisserie"},
            "13": {"nome": "🥨 Salgadinhos e Aperitivos", "url": "https://www.paodeacucar.com/categoria/alimentos/salgadinhos-e-aperitivos"},
            
            # ═══════════════════════════════════════════════════════════════════
            # 🍽️ ALIMENTOS - CATEGORIA GERAL (TODOS OS ALIMENTOS)
            # ═══════════════════════════════════════════════════════════════════
            "14": {"nome": "🍽️ Alimentos (Geral)", "url": "https://www.paodeacucar.com/categoria/alimentos?s=relevance&p=1"},
            
            # ═══════════════════════════════════════════════════════════════════
            # 🥤 BEBIDAS
            # ═══════════════════════════════════════════════════════════════════
            "15": {"nome": "🥤 Bebidas", "url": "https://www.paodeacucar.com/categoria/bebidas?s=relevance&p=1"},
            
            # ═══════════════════════════════════════════════════════════════════
            # 🇧🇷 CARAS DO BRASIL (PRODUTOS BRASILEIROS)
            # ═══════════════════════════════════════════════════════════════════
            "16": {"nome": "🇧🇷 Caras do Brasil", "url": "https://www.paodeacucar.com/categoria/caras-do-brasil?s=relevance&p=1"}
        }

        # Cria diretório de saída se não existir
        self.output_dir = Path("dados_coletados")
        self.output_dir.mkdir(exist_ok=True)

    def listar_categorias(self):
        """Lista todas as categorias disponíveis"""
        print(f"\n{Cores.CIANO}{Cores.BOLD}🛒 CATEGORIAS DISPONÍVEIS{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        for id_cat, info in self.categorias_disponiveis.items():
            print(f"{Cores.AMARELO}{Cores.BOLD}[{id_cat:2d}]{Cores.RESET} {Cores.BRANCO}{info['nome']}{Cores.RESET}")
            print(f"     🔗 {Cores.CIANO}{info['url']}{Cores.RESET}")
            print()

    def selecionar_categorias_interativo(self):
        """Interface interativa aprimorada para seleção de categorias"""
        print(f"\n{Cores.CIANO}{Cores.BOLD}🎯 SELEÇÃO DE CATEGORIAS{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        # Mostra categorias organizadas
        print(f"\n{Cores.VERDE}📋 CATEGORIAS DISPONÍVEIS:{Cores.RESET}\n")

        # Alimentos específicos
        print(f"{Cores.CIANO}🍽️ ALIMENTOS - Categorias Específicas:{Cores.RESET}")
        for i in range(1, 14):
            info = self.categorias_disponiveis[str(i)]
            print(f"   {Cores.AMARELO}[{i:2d}]{Cores.RESET} {info['nome']}")

        # Categoria geral
        print(f"\n{Cores.CIANO}🍽️ ALIMENTOS - Categoria Geral:{Cores.RESET}")
        print(f"   {Cores.AMARELO}[14]{Cores.RESET} {self.categorias_disponiveis['14']['nome']}")

        # Bebidas
        print(f"\n{Cores.CIANO}🥤 BEBIDAS:{Cores.RESET}")
        print(f"   {Cores.AMARELO}[15]{Cores.RESET} {self.categorias_disponiveis['15']['nome']}")

        # Caras do Brasil
        print(f"\n{Cores.CIANO}🇧🇷 PRODUTOS BRASILEIROS:{Cores.RESET}")
        print(f"   {Cores.AMARELO}[16]{Cores.RESET} {self.categorias_disponiveis['16']['nome']}")

        # Opções rápidas
        print(f"\n{Cores.VERDE}⚡ OPÇÕES RÁPIDAS:{Cores.RESET}")
        print(f"   {Cores.CIANO}•{Cores.RESET} Digite {Cores.BRANCO}'todos'{Cores.RESET} para selecionar todas as 16 categorias")
        print(f"   {Cores.CIANO}•{Cores.RESET} Digite {Cores.BRANCO}'alimentos'{Cores.RESET} para categorias 1-13")
        print(f"   {Cores.CIANO}•{Cores.RESET} Digite {Cores.BRANCO}'novas'{Cores.RESET} para categorias 14-16")
        print(f"   {Cores.CIANO}•{Cores.RESET} Digite números separados por vírgula (ex: {Cores.AMARELO}1,3,5,14,15{Cores.RESET})")

        while True:
            try:
                entrada = input(f"\n{Cores.MAGENTA}👉 Selecione as categorias: {Cores.RESET}").strip().lower()

                if not entrada:
                    print(f"{Cores.VERMELHO}❌ Selecione pelo menos uma categoria{Cores.RESET}")
                    continue

                categorias_selecionadas = []

                # Opções rápidas
                if entrada == 'todos':
                    print(f"\n{Cores.VERDE}✅ Selecionadas TODAS as 16 categorias{Cores.RESET}")
                    return [self.categorias_disponiveis[str(i)] for i in range(1, 17)]

                elif entrada == 'alimentos':
                    print(f"\n{Cores.VERDE}✅ Selecionadas 13 categorias de alimentos{Cores.RESET}")
                    return [self.categorias_disponiveis[str(i)] for i in range(1, 14)]

                elif entrada == 'novas':
                    print(f"\n{Cores.VERDE}✅ Selecionadas 3 novas categorias (14-16){Cores.RESET}")
                    return [self.categorias_disponiveis[str(i)] for i in range(14, 17)]

                else:
                    # Seleção por números
                    ids = [id.strip() for id in entrada.split(',') if id.strip()]

                    for cat_id in ids:
                        if cat_id in self.categorias_disponiveis:
                            categorias_selecionadas.append(self.categorias_disponiveis[cat_id])
                        else:
                            print(f"{Cores.VERMELHO}❌ Categoria inválida: {cat_id}{Cores.RESET}")

                    if categorias_selecionadas:
                        print(f"\n{Cores.VERDE}✅ {len(categorias_selecionadas)} categoria(s) selecionada(s):{Cores.RESET}")
                        for cat in categorias_selecionadas:
                            print(f"   • {cat['nome']}")
                        return categorias_selecionadas
                    else:
                        print(f"{Cores.VERMELHO}❌ Nenhuma categoria válida selecionada{Cores.RESET}")

            except KeyboardInterrupt:
                print(f"\n{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")
                return []

    def executar_coleta_teste(self):
        """Executa coleta em modo teste"""
        print(f"\n{Cores.CIANO}{Cores.BOLD}🧪 MODO TESTE - COLETA RÁPIDA{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        print(f"\n{Cores.VERDE}🔬 Características do modo teste:{Cores.RESET}")
        print(f"   • Coleta limitada a {Cores.AMARELO}5 produtos{Cores.RESET} por categoria")
        print(f"   • Ideal para {Cores.CIANO}validações rápidas{Cores.RESET}")
        print(f"   • Processo {Cores.VERDE}acelerado{Cores.RESET} para desenvolvimento")

        categorias = self.selecionar_categorias_interativo()
        if not categorias:
            return False

        confirmar = input(f"\n{Cores.MAGENTA}🤔 Iniciar coleta teste? (s/N): {Cores.RESET}").lower()

        if confirmar in ['s', 'sim', 'y', 'yes']:
            return self.executar_coleta(categorias, modo_teste=True)
        else:
            print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")
            return False

    def executar_coleta_completa(self):
        """Executa coleta completa"""
        print(f"\n{Cores.CIANO}{Cores.BOLD}🚀 MODO COMPLETO - COLETA ILIMITADA{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO:{Cores.RESET}")
        print(f"   • Esta operação pode {Cores.VERMELHO}demorar várias horas{Cores.RESET}")
        print(f"   • Pode consumir {Cores.VERMELHO}muita largura de banda{Cores.RESET}")
        print(f"   • Todos os produtos das categorias serão processados")

        categorias = self.selecionar_categorias_interativo()
        if not categorias:
            return False

        confirmar = input(f"\n{Cores.MAGENTA}🤔 Iniciar coleta completa? (s/N): {Cores.RESET}").lower()

        if confirmar in ['s', 'sim', 'y', 'yes']:
            return self.executar_coleta(categorias, modo_teste=False)
        else:
            print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")
            return False

    def executar_coleta(self, categorias, modo_teste=False):
        """Executa o processo de coleta"""
        try:
            mostrar_barra_progresso("Preparando sistema de coleta", 1.5)

            # Coleta URLs
            urls = self.coletar_urls(categorias, modo_teste)

            if urls:
                # Extrai dados nutricionais
                sucesso = self.extrair_dados_nutricionais(urls)
                if sucesso:
                    print(f"\n{Cores.VERDE}🎉 Coleta concluída com sucesso!{Cores.RESET}")
                    return True
                else:
                    print(f"\n{Cores.VERMELHO}❌ Erro durante a coleta{Cores.RESET}")
                    return False
            else:
                print(f"\n{Cores.VERMELHO}❌ Nenhuma URL coletada{Cores.RESET}")
                return False

        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro durante execução: {e}{Cores.RESET}")
            return False

    def coletar_urls(self, categorias: List[Dict], modo_teste: bool = False) -> List[Dict]:
        """Coleta URLs dos produtos das categorias selecionadas"""
        print(f"\n{Cores.CIANO}{Cores.BOLD}🔍 FASE 1: COLETA DE URLs{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        todas_urls = []

        for categoria in categorias:
            print(f"\n{Cores.VERDE}📂 Processando categoria: {Cores.BRANCO}{categoria['nome']}{Cores.RESET}")

            try:
                mostrar_barra_progresso(f"Acessando {categoria['nome']}", 1.0)

                collector = URLCollector()
                urls = collector.coletar_urls(
                    categoria['url'],
                    modo_teste=modo_teste,
                    categoria_nome=categoria['nome']
                )

                if urls:
                    print(f"{Cores.VERDE}  ✅ {len(urls)} produtos encontrados{Cores.RESET}")
                    todas_urls.extend(urls)

                    # Mostra alguns exemplos
                    print(f"{Cores.CIANO}  📝 Exemplos de produtos:{Cores.RESET}")
                    for i, produto in enumerate(urls[:3], 1):
                        nome = produto['nome'][:50] + "..." if len(produto['nome']) > 50 else produto['nome']
                        print(f"    {Cores.AMARELO}{i}.{Cores.RESET} {nome}")
                    if len(urls) > 3:
                        print(f"    {Cores.CIANO}... e mais {len(urls) - 3} produtos{Cores.RESET}")
                else:
                    print(f"{Cores.AMARELO}  ⚠️ Nenhum produto encontrado{Cores.RESET}")

            except Exception as e:
                print(f"{Cores.VERMELHO}  ❌ Erro ao coletar URLs: {e}{Cores.RESET}")

        print(f"\n{Cores.VERDE}📊 Total de URLs coletadas: {Cores.BRANCO}{len(todas_urls)}{Cores.RESET}")
        return todas_urls

    def extrair_dados_nutricionais(self, urls: List[Dict]) -> bool:
        """Extrai dados nutricionais das URLs coletadas"""
        if not urls:
            print(f"{Cores.VERMELHO}❌ Nenhuma URL para processar{Cores.RESET}")
            return False

        print(f"\n{Cores.CIANO}{Cores.BOLD}🍽️ FASE 2: EXTRAÇÃO DE DADOS NUTRICIONAIS{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        print(f"{Cores.VERDE}📊 Processando {Cores.BRANCO}{len(urls)}{Cores.RESET} produtos...{Cores.RESET}")

        try:
            mostrar_barra_progresso("Configurando scraper", 1.0)

            scraper = Scraper()

            # Salva URLs em arquivo temporário
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_urls = f"urls_temp_{timestamp}.csv"

            print(f"{Cores.CIANO}💾 Salvando URLs temporárias...{Cores.RESET}")
            df_urls = pd.DataFrame(urls)
            df_urls.to_csv(arquivo_urls, index=False)

            # Processa o arquivo
            mostrar_barra_progresso("Extraindo dados nutricionais", 2.0)
            scraper.processar_arquivo_urls(arquivo_urls)

            # Remove arquivo temporário
            if os.path.exists(arquivo_urls):
                os.remove(arquivo_urls)
                print(f"{Cores.CIANO}🗑️ Arquivo temporário removido{Cores.RESET}")

            # Verifica se dados foram salvos
            arquivo_saida = "dados_nutricionais.csv"
            if os.path.exists(arquivo_saida):
                df_resultado = pd.read_csv(arquivo_saida)
                produtos_coletados = len(df_resultado)
                print(f"\n{Cores.VERDE}✅ Dados salvos em '{Cores.BRANCO}{arquivo_saida}{Cores.RESET}'{Cores.VERDE}")
                print(f"📊 Total de produtos com dados nutricionais: {Cores.BRANCO}{produtos_coletados}{Cores.RESET}")
                return True
            else:
                print(f"{Cores.VERMELHO}❌ Erro: Nenhum dado foi salvo{Cores.RESET}")
                return False

        except Exception as e:
            print(f"{Cores.VERMELHO}❌ Erro durante extração: {e}{Cores.RESET}")
            return False

    def consultar_dados(self, filtros: Optional[Dict] = None):
        """Consulta os dados coletados"""
        print(f"\n{Cores.CIANO}{Cores.BOLD}🔍 CONSULTA DE DADOS NUTRICIONAIS{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        arquivo_dados = "dados_nutricionais.csv"

        if not os.path.exists(arquivo_dados):
            print(f"{Cores.VERMELHO}❌ Nenhum dado coletado ainda. Execute coleta primeiro.{Cores.RESET}")
            return

        try:
            mostrar_barra_progresso("Carregando dados", 1.0)

            df = pd.read_csv(arquivo_dados)

            # Aplica filtros se fornecidos
            filtros_aplicados = []
            if filtros:
                if filtros.get('categoria'):
                    df = df[df['categoria'].str.contains(filtros['categoria'], case=False, na=False)]
                    filtros_aplicados.append(f"categoria: {filtros['categoria']}")
                if filtros.get('nome'):
                    df = df[df['nome'].str.contains(filtros['nome'], case=False, na=False)]
                    filtros_aplicados.append(f"nome: {filtros['nome']}")

            if df.empty:
                print(f"{Cores.AMARELO}⚠️ Nenhum produto encontrado com os filtros aplicados{Cores.RESET}")
                if filtros_aplicados:
                    print(f"{Cores.CIANO}Filtros: {', '.join(filtros_aplicados)}{Cores.RESET}")
                return

            print(f"\n{Cores.VERDE}📊 {Cores.BRANCO}{len(df)}{Cores.RESET} produtos encontrados{Cores.RESET}")
            if filtros_aplicados:
                print(f"{Cores.CIANO}Filtros aplicados: {Cores.BRANCO}{', '.join(filtros_aplicados)}{Cores.RESET}")

            print(f"\n{Cores.AZUL}📋 DADOS NUTRICIONAIS:{Cores.RESET}")
            print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

            # Cabeçalho da tabela
            header = f"{Cores.BOLD}{'Produto':<50} {'Categoria':<20} {'Calorias':<10} {'Proteínas':<10} {'Carboidratos':<12}{Cores.RESET}"
            print(header)
            print(f"{Cores.AZUL}{'-' * 110}{Cores.RESET}")

            # Mostra dados em formato tabular (máximo 20 produtos)
            produtos_mostrados = 0
            for _, produto in df.iterrows():
                if produtos_mostrados >= 20:
                    break

                nome = produto['nome'][:48] + "..." if len(produto['nome']) > 48 else produto['nome']
                categoria = produto.get('categoria', 'N/A')[:18] + "..." if len(str(produto.get('categoria', 'N/A'))) > 18 else str(produto.get('categoria', 'N/A'))

                linha = f"{nome:<50} {categoria:<20} {produto['calorias']:<10} {produto['proteinas']:<10} {produto['carboidratos']:<12}"
                print(linha)
                produtos_mostrados += 1

            if len(df) > 20:
                print(f"\n{Cores.CIANO}... e mais {len(df) - 20} produtos (total: {len(df)}){Cores.RESET}")

            # Salva consulta em arquivo se solicitado
            if filtros:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                arquivo_consulta = self.output_dir / f"consulta_{timestamp}.csv"
                df.to_csv(arquivo_consulta, index=False)
                print(f"\n{Cores.VERDE}💾 Consulta salva em: {Cores.BRANCO}{arquivo_consulta}{Cores.RESET}")

        except Exception as e:
            print(f"{Cores.VERMELHO}❌ Erro ao consultar dados: {e}{Cores.RESET}")

    def exportar_excel(self, filtros: Optional[Dict] = None):
        """Exporta dados para Excel"""
        print(f"\n{Cores.CIANO}{Cores.BOLD}💾 EXPORTAÇÃO PARA EXCEL{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        arquivo_dados = "dados_nutricionais.csv"

        if not os.path.exists(arquivo_dados):
            print(f"{Cores.VERMELHO}❌ Nenhum dado coletado ainda. Execute coleta primeiro.{Cores.RESET}")
            return

        try:
            mostrar_barra_progresso("Carregando dados para exportação", 1.0)

            df = pd.read_csv(arquivo_dados)

            # Aplica filtros se fornecidos
            filtros_aplicados = []
            if filtros:
                if filtros.get('categoria'):
                    df = df[df['categoria'].str.contains(filtros['categoria'], case=False, na=False)]
                    filtros_aplicados.append(f"categoria: {filtros['categoria']}")
                if filtros.get('nome'):
                    df = df[df['nome'].str.contains(filtros['nome'], case=False, na=False)]
                    filtros_aplicados.append(f"nome: {filtros['nome']}")

            if df.empty:
                print(f"{Cores.AMARELO}⚠️ Nenhum produto encontrado com os filtros aplicados{Cores.RESET}")
                return

            # Gera nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_excel = self.output_dir / f"dados_nutricionais_{timestamp}.xlsx"

            print(f"\n{Cores.VERDE}📊 Preparando exportação de {Cores.BRANCO}{len(df)}{Cores.RESET} produtos...{Cores.RESET}")
            if filtros_aplicados:
                print(f"{Cores.CIANO}Filtros aplicados: {Cores.BRANCO}{', '.join(filtros_aplicados)}{Cores.RESET}")

            # Exporta para Excel
            mostrar_barra_progresso("Gerando arquivo Excel", 1.5)
            df.to_excel(arquivo_excel, index=False, engine='openpyxl')

            print(f"\n{Cores.VERDE}✅ Dados exportados com sucesso!{Cores.RESET}")
            print(f"{Cores.CIANO}📁 Arquivo: {Cores.BRANCO}{arquivo_excel}{Cores.RESET}")
            print(f"{Cores.CIANO}📊 Produtos exportados: {Cores.BRANCO}{len(df)}{Cores.RESET}")
            print(f"{Cores.CIANO}📏 Tamanho: {Cores.BRANCO}{arquivo_excel.stat().st_size / 1024:.1f} KB{Cores.RESET}")

        except Exception as e:
            print(f"{Cores.VERMELHO}❌ Erro ao exportar para Excel: {e}{Cores.RESET}")

    def mostrar_estatisticas(self):
        """Mostra estatísticas detalhadas dos dados coletados"""
        print(f"\n{Cores.CIANO}{Cores.BOLD}📈 ESTATÍSTICAS DOS DADOS COLETADOS{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

        arquivo_dados = "dados_nutricionais.csv"

        if not os.path.exists(arquivo_dados):
            print(f"{Cores.VERMELHO}❌ Nenhum dado coletado ainda. Execute coleta primeiro.{Cores.RESET}")
            return

        try:
            mostrar_barra_progresso("Calculando estatísticas", 1.0)

            df = pd.read_csv(arquivo_dados)

            if df.empty:
                print(f"{Cores.AMARELO}⚠️ Nenhum dado disponível para análise{Cores.RESET}")
                return

            print(f"\n{Cores.VERDE}📊 RESUMO GERAL:{Cores.RESET}")
            print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
            print(f"   📈 Total de produtos: {Cores.BRANCO}{len(df)}{Cores.RESET}")
            print(f"   📂 Categorias distintas: {Cores.BRANCO}{df['categoria'].nunique()}{Cores.RESET}")

            if 'data_coleta' in df.columns and df['data_coleta'].notna().any():
                ultima_coleta = df['data_coleta'].max()
                print(f"   📅 Última coleta: {Cores.BRANCO}{ultima_coleta}{Cores.RESET}")

            # Estatísticas nutricionais
            print(f"\n{Cores.VERDE}🥗 MÉDIAS NUTRICIONAIS (por 100g):{Cores.RESET}")
            print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

            colunas_nutricionais = ['calorias', 'proteinas', 'carboidratos', 'gorduras']
            medias = df[colunas_nutricionais].mean()

            print(f"   🔥 Calorias:     {Cores.BRANCO}{medias['calorias']:7.1f}{Cores.RESET} kcal")
            print(f"   💪 Proteínas:    {Cores.BRANCO}{medias['proteinas']:7.1f}{Cores.RESET} g")
            print(f"   🌾 Carboidratos: {Cores.BRANCO}{medias['carboidratos']:7.1f}{Cores.RESET} g")
            print(f"   🧈 Gorduras:     {Cores.BRANCO}{medias['gorduras']:7.1f}{Cores.RESET} g")

            # Top categorias
            print(f"\n{Cores.VERDE}🏆 TOP 5 CATEGORIAS:{Cores.RESET}")
            print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

            top_categorias = df['categoria'].value_counts().head()
            for i, (categoria, count) in enumerate(top_categorias.items(), 1):
                porcentagem = (count / len(df)) * 100
                emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1] if i <= 5 else "📊"
                print(f"   {emoji} {categoria}")
                print(f"      📊 {count} produtos ({porcentagem:5.1f}%)")

            # Estatísticas adicionais
            print(f"\n{Cores.VERDE}📋 INFORMAÇÕES DETALHADAS:{Cores.RESET}")
            print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

            # Valores mínimos e máximos
            print(f"   📉 Produto com menos calorias: {Cores.BRANCO}{df.loc[df['calorias'].idxmin(), 'nome'][:40]}...{Cores.RESET} ({df['calorias'].min()} kcal)")
            print(f"   📈 Produto com mais calorias:  {Cores.BRANCO}{df.loc[df['calorias'].idxmax(), 'nome'][:40]}...{Cores.RESET} ({df['calorias'].max()} kcal)")

            # Distribuição por categorias
            print(f"\n{Cores.CIANO}📊 Distribuição detalhada por categoria:{Cores.RESET}")
            distribuicao = df['categoria'].value_counts()
            for categoria, count in distribuicao.items():
                print(f"   • {categoria}: {count} produtos")

        except Exception as e:
            print(f"{Cores.VERMELHO}❌ Erro ao calcular estatísticas: {e}{Cores.RESET}")

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
                    print(f"\n{Cores.VERDE}🎉 Coleta de teste concluída com sucesso!{Cores.RESET}")
                pausar()

            elif escolha == "2":
                sucesso = cli.executar_coleta_completa()
                if sucesso:
                    print(f"\n{Cores.VERDE}🎉 Coleta completa concluída com sucesso!{Cores.RESET}")
                pausar()

            elif escolha == "3":
                # Coleta personalizada - escolher categorias
                print(f"\n{Cores.CIANO}{Cores.BOLD}🎯 COLETA PERSONALIZADA{Cores.RESET}")
                print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

                print(f"\n{Cores.VERDE}📋 Escolha quais categorias deseja coletar:{Cores.RESET}")
                print(f"   • Você pode selecionar categorias específicas")
                print(f"   • Escolher modo teste (rápido) ou completo (ilimitado)")

                # Seleciona categorias
                categorias = cli.selecionar_categorias_interativo()
                if not categorias:
                    pausar()
                    continue

                # Escolhe o modo
                print(f"\n{Cores.VERDE}⚙️ MODO DE COLETA:{Cores.RESET}")
                print(f"   {Cores.AMARELO}1.{Cores.RESET} 🧪 {Cores.BRANCO}Teste{Cores.RESET} - Rápido (5 produtos/categoria)")
                print(f"   {Cores.AMARELO}2.{Cores.RESET} 🚀 {Cores.BRANCO}Completo{Cores.RESET} - Ilimitado (todos os produtos)")

                modo_escolha = input(f"\n{Cores.MAGENTA}👉 Escolha o modo (1-2): {Cores.RESET}").strip()

                modo_teste = modo_escolha == "1"
                modo_nome = "teste" if modo_teste else "completo"

                print(f"\n{Cores.VERDE}✅ Modo selecionado: {Cores.BRANCO}{modo_nome.upper()}{Cores.RESET}")

                confirmar = input(f"\n{Cores.MAGENTA}🤔 Iniciar coleta {modo_nome}? (s/N): {Cores.RESET}").lower()

                if confirmar in ['s', 'sim', 'y', 'yes']:
                    sucesso = cli.executar_coleta(categorias, modo_teste)
                    if sucesso:
                        print(f"\n{Cores.VERDE}🎉 Coleta personalizada concluída com sucesso!{Cores.RESET}")
                else:
                    print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

                pausar()

            elif escolha == "4":
                # Consulta interativa
                print(f"\n{Cores.CIANO}{Cores.BOLD}🔍 CONSULTA INTERATIVA{Cores.RESET}")
                print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

                print(f"\n{Cores.VERDE}📋 Filtros disponíveis:{Cores.RESET}")
                print(f"   • Digite o nome da categoria (ex: Hortifruti)")
                print(f"   • Digite o nome do produto (ex: leite)")
                print(f"   • Deixe em branco para ver todos os dados")

                categoria = input(f"\n{Cores.MAGENTA}🏷️ Categoria (opcional): {Cores.RESET}").strip()
                nome = input(f"{Cores.MAGENTA}🔍 Nome do produto (opcional): {Cores.RESET}").strip()

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
                # Exportação interativa
                print(f"\n{Cores.CIANO}{Cores.BOLD}💾 EXPORTAÇÃO INTERATIVA{Cores.RESET}")
                print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

                print(f"\n{Cores.VERDE}📋 Filtros para exportação:{Cores.RESET}")
                categoria = input(f"{Cores.MAGENTA}🏷️ Categoria (opcional): {Cores.RESET}").strip()
                nome = input(f"{Cores.MAGENTA}🔍 Nome do produto (opcional): {Cores.RESET}").strip()

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
                # Mostra todas as categorias disponíveis
                cli.listar_categorias()
                pausar()

            elif escolha == "a":
                mostrar_sobre()
                pausar()

            elif escolha == "0":
                print(f"\n{Cores.VERDE}👋 Obrigado por usar o Pão de Açúcar Scraping CLI!{Cores.RESET}")
                print(f"{Cores.CIANO}🚀 Até a próxima!{Cores.RESET}\n")
                break

            else:
                print(f"\n{Cores.VERMELHO}❌ Opção inválida! Por favor, escolha entre 0-9 ou A{Cores.RESET}")
                time.sleep(2)

    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}👋 Programa encerrado pelo usuário. Até logo!{Cores.RESET}\n")
    except Exception as e:
        print(f"\n{Cores.VERMELHO}❌ Erro inesperado: {e}{Cores.RESET}")
        logger.error(f"Erro no programa principal: {str(e)}")

# ============================================================================
# 📋 EXEMPLOS DE USO VIA LINHA DE COMANDO (PARA COMPATIBILIDADE)
# ============================================================================
def main_cli():
    """Interface de linha de comando tradicional (para scripts)"""
    parser = argparse.ArgumentParser(
        description="🛒 Pão de Açúcar Scraping - Coleta de dados nutricionais",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py listar-categorias
  python main.py coletar --categorias 1 2 3 --teste
  python main.py consultar --categoria "Hortifruti"
  python main.py exportar --categoria "Doces" --formato excel
  python main.py estatisticas
        """
    )

    subparsers = parser.add_subparsers(dest='comando', help='Comandos disponíveis')

    # Comando: listar categorias
    subparsers.add_parser('listar-categorias', help='Lista todas as categorias disponíveis')

    # Comando: coletar
    coletar_parser = subparsers.add_parser('coletar', help='Coleta dados nutricionais')
    coletar_parser.add_argument('--categorias', nargs='+', required=True,
                               help='IDs das categorias para coletar (ex: 1 2 3)')
    coletar_parser.add_argument('--teste', action='store_true',
                               help='Modo teste (coleta limitada)')

    # Comando: consultar
    consultar_parser = subparsers.add_parser('consultar', help='Consulta dados coletados')
    consultar_parser.add_argument('--categoria', help='Filtrar por categoria')
    consultar_parser.add_argument('--nome', help='Filtrar por nome do produto')

    # Comando: exportar
    exportar_parser = subparsers.add_parser('exportar', help='Exporta dados para arquivo')
    exportar_parser.add_argument('--categoria', help='Filtrar por categoria')
    exportar_parser.add_argument('--nome', help='Filtrar por nome do produto')
    exportar_parser.add_argument('--formato', choices=['excel', 'csv'], default='excel',
                                help='Formato de exportação (padrão: excel)')

    # Comando: estatisticas
    subparsers.add_parser('estatisticas', help='Mostra estatísticas dos dados coletados')

    # Parse dos argumentos
    args = parser.parse_args()

    # Se nenhum comando foi fornecido, usa interface interativa
    if not args.comando:
        main()
        return

    # Inicializa o CLI
    cli = PaoDeAcucarCLI()

    try:
        if args.comando == 'listar-categorias':
            cli.listar_categorias()

        elif args.comando == 'coletar':
            # Valida categorias
            categorias = cli.validar_categorias(args.categorias)
            if not categorias:
                print("❌ Nenhuma categoria válida selecionada")
                return

            # Coleta URLs
            urls = cli.coletar_urls(categorias, args.teste)

            if urls:
                # Extrai dados nutricionais
                sucesso = cli.extrair_dados_nutricionais(urls)
                if sucesso:
                    print("\n🎉 Coleta concluída com sucesso!")
                else:
                    print("\n❌ Erro durante a coleta")
            else:
                print("\n❌ Nenhuma URL coletada")

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
                print("❌ Formato CSV ainda não implementado")

        elif args.comando == 'estatisticas':
            cli.mostrar_estatisticas()

    except KeyboardInterrupt:
        print("\n\n⚠️ Operação interrompida pelo usuário")
        return
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
        logger.error(f"Erro no CLI: {str(e)}")
        return

if __name__ == "__main__":
    main()
