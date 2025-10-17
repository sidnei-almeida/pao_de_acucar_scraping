#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📋 LISTADOR DE CATEGORIAS ATUALIZADO
===================================
Mostra todas as 16 categorias disponíveis para coleta
"""

# ============================================================================
# 🎨 SISTEMA DE CORES ANSI
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
# 📊 TODAS AS CATEGORIAS DISPONÍVEIS (ATUALIZADO)
# ============================================================================
CATEGORIAS = {
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

def mostrar_banner():
    """Exibe o banner do programa"""
    banner = f"""
{Cores.CIANO}{Cores.BOLD}
╔══════════════════════════════════════════════════════════════════════════╗
║            🛒 CATEGORIAS DO PÃO DE AÇÚCAR - ATUALIZADO                  ║
║                                                                          ║
║              Sistema completo com 16 categorias disponíveis              ║
╚══════════════════════════════════════════════════════════════════════════╝
{Cores.RESET}"""
    print(banner)

def main():
    """Função principal"""
    mostrar_banner()

    print(f"\n{Cores.VERDE}{Cores.BOLD}📋 LISTA COMPLETA DE CATEGORIAS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    # Agrupa categorias por seção
    print(f"\n{Cores.CIANO}🍽️ ALIMENTOS - CATEGORIAS ESPECÍFICAS (13 categorias):{Cores.RESET}")
    print(f"{Cores.AZUL}{'─' * 85}{Cores.RESET}")

    for id_cat in range(1, 14):
        info = CATEGORIAS[str(id_cat)]
        print(f"{Cores.AMARELO}{Cores.BOLD}[{id_cat:2d}]{Cores.RESET} {info['nome']}")
        print(f"     🔗 {Cores.BRANCO}{info['url']}{Cores.RESET}")

    print(f"\n{Cores.CIANO}🍽️ ALIMENTOS - CATEGORIA GERAL:{Cores.RESET}")
    print(f"{Cores.AZUL}{'─' * 85}{Cores.RESET}")
    info = CATEGORIAS["14"]
    print(f"{Cores.AMARELO}{Cores.BOLD}[14]{Cores.RESET} {info['nome']}")
    print(f"     🔗 {Cores.BRANCO}{info['url']}{Cores.RESET}")
    print(f"     {Cores.CIANO}💡 Engloba todos os produtos de alimentos em um único lugar{Cores.RESET}")

    print(f"\n{Cores.CIANO}🥤 BEBIDAS:{Cores.RESET}")
    print(f"{Cores.AZUL}{'─' * 85}{Cores.RESET}")
    info = CATEGORIAS["15"]
    print(f"{Cores.AMARELO}{Cores.BOLD}[15]{Cores.RESET} {info['nome']}")
    print(f"     🔗 {Cores.BRANCO}{info['url']}{Cores.RESET}")
    print(f"     {Cores.CIANO}💡 Vinhos, cervejas, refrigerantes, sucos, águas, etc.{Cores.RESET}")

    print(f"\n{Cores.CIANO}🇧🇷 PRODUTOS BRASILEIROS:{Cores.RESET}")
    print(f"{Cores.AZUL}{'─' * 85}{Cores.RESET}")
    info = CATEGORIAS["16"]
    print(f"{Cores.AMARELO}{Cores.BOLD}[16]{Cores.RESET} {info['nome']}")
    print(f"     🔗 {Cores.BRANCO}{info['url']}{Cores.RESET}")
    print(f"     {Cores.CIANO}💡 Produtos brasileiros selecionados e artesanais{Cores.RESET}")

    # Estatísticas
    print(f"\n{Cores.VERDE}📊 ESTATÍSTICAS:{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    print(f"\n   📈 Total de categorias: {Cores.BRANCO}{Cores.BOLD}{len(CATEGORIAS)}{Cores.RESET}")
    print(f"   🍽️ Alimentos específicos: {Cores.BRANCO}13{Cores.RESET}")
    print(f"   🍽️ Alimentos geral: {Cores.BRANCO}1{Cores.RESET}")
    print(f"   🥤 Bebidas: {Cores.BRANCO}1{Cores.RESET}")
    print(f"   🇧🇷 Caras do Brasil: {Cores.BRANCO}1{Cores.RESET}")

    # Diferenças nos padrões de URL
    print(f"\n{Cores.VERDE}🔍 PADRÕES DE URLs IDENTIFICADOS:{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    print(f"\n   {Cores.CIANO}Padrão 1 - Categorias específicas de alimentos (1-13):{Cores.RESET}")
    print(f"   {Cores.BRANCO}https://www.paodeacucar.com/categoria/alimentos/[slug]{Cores.RESET}")

    print(f"\n   {Cores.CIANO}Padrão 2 - Categorias com paginação e ordenação (14-16):{Cores.RESET}")
    print(f"   {Cores.BRANCO}https://www.paodeacucar.com/categoria/[categoria]?s=relevance&p=1{Cores.RESET}")

    print(f"\n{Cores.AMARELO}💡 OBSERVAÇÕES:{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    print(f"\n   {Cores.CIANO}🎯 URLs com parâmetros (categorias 14-16):{Cores.RESET}")
    print(f"      • {Cores.VERDE}s=relevance{Cores.RESET} - Ordenação por relevância")
    print(f"      • {Cores.VERDE}p=1{Cores.RESET} - Número da página inicial")
    print(f"      • Sistema fará scroll para carregar todos os produtos")

    print(f"\n   {Cores.CIANO}🛒 URLs simples (categorias 1-13):{Cores.RESET}")
    print(f"      • Formato: /categoria/alimentos/[slug]")
    print(f"      • Não possuem parâmetros na URL base")
    print(f"      • Sistema adiciona paginação automaticamente se necessário")

    print(f"\n{Cores.VERDE}✅ Sistema atualizado e pronto para coleta das 16 categorias!{Cores.RESET}")

if __name__ == "__main__":
    main()

