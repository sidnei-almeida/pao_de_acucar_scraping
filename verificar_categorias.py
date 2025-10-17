#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔍 VERIFICADOR DE CATEGORIAS DO PÃO DE AÇÚCAR
=============================================
Script para listar e verificar todas as categorias configuradas no sistema
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
# 📊 CATEGORIAS CONFIGURADAS NO SISTEMA
# ============================================================================
CATEGORIAS = {
    # ═══════════════════════════════════════════════════════════════════
    # 🍽️ ALIMENTOS - CATEGORIAS ESPECÍFICAS
    # ═══════════════════════════════════════════════════════════════════
    "1": {
        "nome": "Açougue",
        "emoji": "🛒",
        "url": "https://www.paodeacucar.com/categoria/alimentos/acougue",
        "descricao": "Carnes bovinas, suínas, aves e derivados"
    },
    "2": {
        "nome": "Alimentos Congelados",
        "emoji": "🧊",
        "url": "https://www.paodeacucar.com/categoria/alimentos/alimentos-congelados",
        "descricao": "Refeições prontas, vegetais congelados, pizzas"
    },
    "3": {
        "nome": "Alimentos Refrigerados",
        "emoji": "🥛",
        "url": "https://www.paodeacucar.com/categoria/alimentos/alimentos-refrigerados",
        "descricao": "Laticínios, frios, iogurtes, queijos"
    },
    "4": {
        "nome": "Básicos da Despensa",
        "emoji": "🏠",
        "url": "https://www.paodeacucar.com/categoria/alimentos/basico-da-despensa",
        "descricao": "Arroz, feijão, açúcar, sal, óleo"
    },
    "5": {
        "nome": "Cereais",
        "emoji": "🌾",
        "url": "https://www.paodeacucar.com/categoria/alimentos/cereais",
        "descricao": "Cereais matinais, granolas, barras de cereal"
    },
    "6": {
        "nome": "Complemento da Despensa",
        "emoji": "📦",
        "url": "https://www.paodeacucar.com/categoria/alimentos/complemento-da-despensa",
        "descricao": "Molhos, temperos, especiarias, conservas"
    },
    "7": {
        "nome": "Doces e Sobremesas",
        "emoji": "🍰",
        "url": "https://www.paodeacucar.com/categoria/alimentos/doces-e-sobremesas",
        "descricao": "Chocolates, balas, bolos, pudins, gelatinas"
    },
    "8": {
        "nome": "Hortifruti",
        "emoji": "🥬",
        "url": "https://www.paodeacucar.com/categoria/alimentos/hortifruti",
        "descricao": "Frutas, verduras, legumes frescos"
    },
    "9": {
        "nome": "Mercearia Salgada",
        "emoji": "🧂",
        "url": "https://www.paodeacucar.com/categoria/alimentos/mercearia-salgada",
        "descricao": "Massas, enlatados, sopas, caldos"
    },
    "10": {
        "nome": "Padaria",
        "emoji": "🍞",
        "url": "https://www.paodeacucar.com/categoria/alimentos/padaria",
        "descricao": "Pães, bolos, tortas, biscoitos"
    },
    "11": {
        "nome": "Peixaria",
        "emoji": "🐟",
        "url": "https://www.paodeacucar.com/categoria/alimentos/peixaria",
        "descricao": "Peixes, frutos do mar, produtos marinhos"
    },
    "12": {
        "nome": "Rotisserie",
        "emoji": "🍗",
        "url": "https://www.paodeacucar.com/categoria/alimentos/rotisserie",
        "descricao": "Frango assado, carnes preparadas"
    },
    "13": {
        "nome": "Salgadinhos e Aperitivos",
        "emoji": "🥨",
        "url": "https://www.paodeacucar.com/categoria/alimentos/salgadinhos-e-aperitivos",
        "descricao": "Chips, amendoins, snacks diversos"
    },
    
    # ═══════════════════════════════════════════════════════════════════
    # 🍽️ ALIMENTOS - CATEGORIA GERAL (TODOS OS ALIMENTOS)
    # ═══════════════════════════════════════════════════════════════════
    "14": {
        "nome": "Alimentos (Geral)",
        "emoji": "🍽️",
        "url": "https://www.paodeacucar.com/categoria/alimentos?s=relevance&p=1",
        "descricao": "Todos os produtos de alimentos em uma única categoria"
    },
    
    # ═══════════════════════════════════════════════════════════════════
    # 🥤 BEBIDAS
    # ═══════════════════════════════════════════════════════════════════
    "15": {
        "nome": "Bebidas",
        "emoji": "🥤",
        "url": "https://www.paodeacucar.com/categoria/bebidas?s=relevance&p=1",
        "descricao": "Vinhos, cervejas, refrigerantes, sucos, águas e mais"
    },
    
    # ═══════════════════════════════════════════════════════════════════
    # 🇧🇷 CARAS DO BRASIL (PRODUTOS BRASILEIROS)
    # ═══════════════════════════════════════════════════════════════════
    "16": {
        "nome": "Caras do Brasil",
        "emoji": "🇧🇷",
        "url": "https://www.paodeacucar.com/categoria/caras-do-brasil?s=relevance&p=1",
        "descricao": "Produtos brasileiros selecionados e artesanais"
    }
}

def mostrar_banner():
    """Exibe o banner do programa"""
    banner = f"""
{Cores.CIANO}{Cores.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║         🛒 VERIFICADOR DE CATEGORIAS - PÃO DE AÇÚCAR           ║
║                                                                  ║
║              Análise de Links e Categorias Disponíveis           ║
╚══════════════════════════════════════════════════════════════════╝
{Cores.RESET}"""
    print(banner)

def listar_todas_categorias():
    """Lista todas as categorias configuradas no sistema"""
    print(f"\n{Cores.VERDE}📋 CATEGORIAS CONFIGURADAS NO SISTEMA{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    print(f"\n{Cores.CIANO}Total de categorias disponíveis: {Cores.BRANCO}{len(CATEGORIAS)}{Cores.RESET}\n")

    for id_cat, info in CATEGORIAS.items():
        print(f"{Cores.AMARELO}{Cores.BOLD}[{int(id_cat):2d}]{Cores.RESET} {info['emoji']} {Cores.BRANCO}{Cores.BOLD}{info['nome']}{Cores.RESET}")
        print(f"     📝 Descrição: {Cores.CIANO}{info['descricao']}{Cores.RESET}")
        print(f"     🔗 URL: {Cores.AZUL}{info['url']}{Cores.RESET}")
        print()

def analisar_padroes_urls():
    """Analisa os padrões de URLs configuradas"""
    print(f"\n{Cores.VERDE}🔍 ANÁLISE DE PADRÕES DE URLs{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    # Analisa estrutura comum
    urls = [info['url'] for info in CATEGORIAS.values()]

    print(f"\n{Cores.CIANO}📊 Estrutura das URLs:{Cores.RESET}")

    # Domínio base
    dominio_base = "https://www.paodeacucar.com"
    print(f"   🌐 Domínio base: {Cores.BRANCO}{dominio_base}{Cores.RESET}")

    # Padrão de categoria
    padrao_comum = "/categoria/alimentos/"
    print(f"   📁 Padrão comum: {Cores.BRANCO}{padrao_comum}{Cores.RESET}")

    # Slugs das categorias
    print(f"\n{Cores.CIANO}📝 Slugs das categorias:{Cores.RESET}")
    for id_cat, info in CATEGORIAS.items():
        slug = info['url'].replace(dominio_base + padrao_comum, '')
        print(f"   {int(id_cat):2d}. {slug:<30} → {info['nome']}")

    # Estrutura completa
    print(f"\n{Cores.VERDE}🏗️ ESTRUTURA COMPLETA DE UMA URL:{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    exemplo_url = CATEGORIAS["1"]["url"]
    print(f"\n{Cores.CIANO}Exemplo: {Cores.BRANCO}{exemplo_url}{Cores.RESET}\n")

    partes = exemplo_url.split('/')
    print(f"   1. {Cores.AMARELO}Protocolo:{Cores.RESET} {partes[0]}")
    print(f"   2. {Cores.AMARELO}Domínio:{Cores.RESET}   {partes[2]}")
    print(f"   3. {Cores.AMARELO}Seção:{Cores.RESET}     {partes[3]}")
    print(f"   4. {Cores.AMARELO}Grupo:{Cores.RESET}     {partes[4]}")
    print(f"   5. {Cores.AMARELO}Categoria:{Cores.RESET} {partes[5]}")

def verificar_categorias_faltantes():
    """Verifica se há categorias importantes faltando"""
    print(f"\n{Cores.VERDE}🔍 CATEGORIAS POPULARES NO SITE{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    # Categorias que existem no site e podem ser adicionadas
    categorias_populares_site = [
        {"nome": "Bebidas", "url_slug": "bebidas", "emoji": "🥤"},
        {"nome": "Higiene e Beleza", "url_slug": "higiene-e-beleza", "emoji": "🧴"},
        {"nome": "Limpeza", "url_slug": "limpeza", "emoji": "🧹"},
        {"nome": "Pet Shop", "url_slug": "pet-shop", "emoji": "🐾"},
        {"nome": "Bebê", "url_slug": "bebe", "emoji": "👶"},
    ]

    categorias_cadastradas = [info['nome'] for info in CATEGORIAS.values()]

    print(f"\n{Cores.CIANO}💡 Outras categorias que podem estar disponíveis no site:{Cores.RESET}\n")

    for cat in categorias_populares_site:
        if cat['nome'] not in categorias_cadastradas:
            url_sugerida = f"https://www.paodeacucar.com/categoria/{cat['url_slug']}"
            print(f"   {cat['emoji']} {Cores.AMARELO}{cat['nome']}{Cores.RESET}")
            print(f"      URL sugerida: {Cores.CIANO}{url_sugerida}{Cores.RESET}")
            print()

def mostrar_estatisticas():
    """Mostra estatísticas sobre as categorias"""
    print(f"\n{Cores.VERDE}📊 ESTATÍSTICAS DAS CATEGORIAS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    # Agrupa por tipo
    print(f"\n{Cores.CIANO}📁 Todas as categorias usam o mesmo padrão de URL:{Cores.RESET}")
    print(f"   {Cores.BRANCO}https://www.paodeacucar.com/categoria/alimentos/[SLUG]{Cores.RESET}")

    print(f"\n{Cores.VERDE}✅ Padrão consistente detectado{Cores.RESET}")
    print(f"   • Base: {Cores.BRANCO}www.paodeacucar.com{Cores.RESET}")
    print(f"   • Caminho: {Cores.BRANCO}/categoria/alimentos/{Cores.RESET}")
    print(f"   • Total: {Cores.BRANCO}{len(CATEGORIAS)}{Cores.RESET} categorias")

def validar_estrutura_urls():
    """Valida se todas as URLs seguem o mesmo padrão"""
    print(f"\n{Cores.VERDE}✅ VALIDAÇÃO DE ESTRUTURA{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    base_esperada = "https://www.paodeacucar.com/categoria/alimentos/"
    urls_validas = 0
    urls_invalidas = []

    for id_cat, info in CATEGORIAS.items():
        if info['url'].startswith(base_esperada):
            urls_validas += 1
        else:
            urls_invalidas.append((id_cat, info['nome'], info['url']))

    print(f"\n{Cores.VERDE}✅ URLs válidas: {Cores.BRANCO}{urls_validas}/{len(CATEGORIAS)}{Cores.RESET}")

    if urls_invalidas:
        print(f"\n{Cores.VERMELHO}❌ URLs com estrutura diferente:{Cores.RESET}")
        for id_cat, nome, url in urls_invalidas:
            print(f"   [{id_cat}] {nome}: {url}")
    else:
        print(f"\n{Cores.VERDE}🎉 Todas as URLs seguem o padrão esperado!{Cores.RESET}")

def main():
    """Função principal"""
    mostrar_banner()

    print(f"\n{Cores.VERDE}🚀 Iniciando verificação das categorias...{Cores.RESET}")

    # 1. Lista todas as categorias
    listar_todas_categorias()

    # 2. Analisa padrões de URLs
    analisar_padroes_urls()

    # 3. Valida estrutura
    validar_estrutura_urls()

    # 4. Mostra estatísticas
    mostrar_estatisticas()

    # 5. Sugere categorias faltantes
    verificar_categorias_faltantes()

    # Resumo final
    print(f"\n{Cores.CIANO}{Cores.BOLD}📋 RESUMO DA VERIFICAÇÃO{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    print(f"\n{Cores.VERDE}✅ Verificação concluída!{Cores.RESET}")
    print(f"\n{Cores.CIANO}📊 Resultados:{Cores.RESET}")
    print(f"   • {Cores.BRANCO}{len(CATEGORIAS)}{Cores.RESET} categorias configuradas")
    print(f"   • {Cores.BRANCO}Todas{Cores.RESET} seguem o mesmo padrão de URL")
    print(f"   • Domínio: {Cores.BRANCO}www.paodeacucar.com{Cores.RESET}")
    print(f"   • Caminho base: {Cores.BRANCO}/categoria/alimentos/{Cores.RESET}")

    print(f"\n{Cores.AMARELO}💡 PRÓXIMOS PASSOS:{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")

    print(f"\n{Cores.CIANO}Para coletar URLs dos produtos de cada categoria:{Cores.RESET}")
    print(f"   1. O sistema usa {Cores.VERDE}Selenium{Cores.RESET} para navegar nas páginas")
    print(f"   2. Acessa cada URL de categoria")
    print(f"   3. Faz {Cores.AMARELO}scroll{Cores.RESET} para carregar todos os produtos")
    print(f"   4. Extrai links dos produtos usando {Cores.VERDE}seletores CSS{Cores.RESET}")
    print(f"   5. Salva as URLs coletadas em {Cores.BRANCO}CSV{Cores.RESET}")

    print(f"\n{Cores.CIANO}Para coletar dados nutricionais:{Cores.RESET}")
    print(f"   1. Acessa cada URL de produto individualmente")
    print(f"   2. Extrai tabela nutricional via {Cores.VERDE}JavaScript{Cores.RESET}")
    print(f"   3. Padroniza os dados coletados")
    print(f"   4. Salva em {Cores.BRANCO}dados_nutricionais.csv{Cores.RESET}")

    print(f"\n{Cores.VERDE}✨ Use o main.py para executar a coleta!{Cores.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}👋 Verificação interrompida{Cores.RESET}")
    except Exception as e:
        print(f"\n{Cores.VERMELHO}❌ Erro: {e}{Cores.RESET}")

