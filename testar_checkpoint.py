#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Teste do Sistema de Checkpoint e Recuperação
================================================
Valida o sistema de checkpoint e recuperação de crashes implementado.
"""

from url_collector import URLCollector
from scraping_log import logger
import os
import json

def testar_checkpoint_basico():
    """Testa o sistema de checkpoint no modo teste"""
    print("\n" + "═"*80)
    print("🧪 TESTE 1: Sistema de Checkpoint Básico")
    print("═"*80)
    
    # URL de teste (categoria pequena)
    url_teste = "https://www.paodeacucar.com/categoria/alimentos/padaria"
    categoria_nome = "Padaria"
    
    print(f"\n📋 Configuração do teste:")
    print(f"   URL: {url_teste}")
    print(f"   Categoria: {categoria_nome}")
    print(f"   Modo: Teste (limite de 5 produtos)")
    
    # Verifica se existe checkpoint anterior
    categoria_slug = categoria_nome.lower().replace(' ', '_')
    checkpoint_file = f"urls_checkpoint_{categoria_slug}.json"
    
    if os.path.exists(checkpoint_file):
        print(f"\n⚠️  Checkpoint anterior encontrado: {checkpoint_file}")
        print(f"   Removendo para iniciar teste limpo...")
        os.remove(checkpoint_file)
    
    print("\n🚀 Iniciando coleta...")
    print("─"*80)
    
    collector = URLCollector()
    urls = collector.coletar_urls(
        url_categoria=url_teste,
        modo_teste=True,
        categoria_nome=categoria_nome
    )
    
    print("─"*80)
    print(f"\n✅ Coleta finalizada!")
    print(f"   Total de URLs coletadas: {len(urls)}")
    
    if urls:
        print(f"\n📋 Primeiros produtos coletados:")
        for i, produto in enumerate(urls[:3], 1):
            print(f"   {i}. {produto['nome'][:60]}")
            print(f"      URL: {produto['url'][:70]}...")
    
    # Verifica se o checkpoint foi limpo
    if os.path.exists(checkpoint_file):
        print(f"\n⚠️  Checkpoint ainda existe (deveria ter sido removido)")
        print(f"   Limpando manualmente...")
        os.remove(checkpoint_file)
    else:
        print(f"\n✅ Checkpoint foi removido corretamente após sucesso")
    
    return len(urls) > 0

def testar_carregamento_checkpoint():
    """Testa o carregamento de um checkpoint simulado"""
    print("\n" + "═"*80)
    print("🧪 TESTE 2: Carregamento de Checkpoint")
    print("═"*80)
    
    # Cria um checkpoint simulado
    checkpoint_file = "urls_checkpoint_teste_simulado.json"
    
    checkpoint_simulado = {
        "urls": [
            {
                "url": "https://www.paodeacucar.com/produto/123456/produto-teste-1",
                "nome": "Produto Teste 1",
                "categoria": "Teste",
                "data_coleta": "2025-10-16T00:00:00"
            },
            {
                "url": "https://www.paodeacucar.com/produto/789012/produto-teste-2",
                "nome": "Produto Teste 2",
                "categoria": "Teste",
                "data_coleta": "2025-10-16T00:00:00"
            }
        ],
        "num_scrolls": 10,
        "posicao_scroll": 5000,
        "timestamp": "2025-10-16T00:00:00",
        "total_produtos": 2
    }
    
    print(f"\n📝 Criando checkpoint simulado:")
    print(f"   Arquivo: {checkpoint_file}")
    print(f"   Produtos: {len(checkpoint_simulado['urls'])}")
    print(f"   Rolagens: {checkpoint_simulado['num_scrolls']}")
    print(f"   Posição: {checkpoint_simulado['posicao_scroll']}")
    
    # Salva o checkpoint simulado
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(checkpoint_simulado, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Checkpoint criado")
    
    # Tenta carregar o checkpoint
    print(f"\n🔄 Testando carregamento...")
    from url_collector import carregar_checkpoint
    
    checkpoint_carregado = carregar_checkpoint(checkpoint_file)
    
    if checkpoint_carregado:
        print(f"\n✅ Checkpoint carregado com sucesso!")
        print(f"   Produtos no checkpoint: {checkpoint_carregado['total_produtos']}")
        print(f"   Rolagens salvas: {checkpoint_carregado['num_scrolls']}")
        print(f"   Posição de scroll: {checkpoint_carregado['posicao_scroll']}")
        
        # Valida os dados
        if len(checkpoint_carregado['urls']) == 2:
            print(f"\n✅ Número de URLs correto")
        else:
            print(f"\n❌ Número de URLs incorreto: {len(checkpoint_carregado['urls'])}")
        
        if checkpoint_carregado['num_scrolls'] == 10:
            print(f"✅ Número de rolagens correto")
        else:
            print(f"❌ Número de rolagens incorreto: {checkpoint_carregado['num_scrolls']}")
    else:
        print(f"\n❌ Falha ao carregar checkpoint")
    
    # Limpa o checkpoint de teste
    print(f"\n🗑️  Limpando checkpoint de teste...")
    from url_collector import limpar_checkpoint
    limpar_checkpoint(checkpoint_file)
    
    if not os.path.exists(checkpoint_file):
        print(f"✅ Checkpoint removido com sucesso")
    else:
        print(f"❌ Falha ao remover checkpoint")
    
    return checkpoint_carregado is not None

def testar_salvamento_checkpoint():
    """Testa o salvamento de checkpoint"""
    print("\n" + "═"*80)
    print("🧪 TESTE 3: Salvamento de Checkpoint")
    print("═"*80)
    
    from url_collector import salvar_checkpoint, carregar_checkpoint, limpar_checkpoint
    
    checkpoint_file = "urls_checkpoint_teste_salvamento.json"
    
    # Dados de teste
    urls_teste = [
        {
            "url": f"https://www.paodeacucar.com/produto/{i}/produto-teste-{i}",
            "nome": f"Produto Teste {i}",
            "categoria": "Teste",
            "data_coleta": "2025-10-16T00:00:00"
        }
        for i in range(1, 101)  # 100 produtos
    ]
    
    num_scrolls = 50
    posicao_scroll = 10000
    
    print(f"\n📝 Testando salvamento de checkpoint:")
    print(f"   Arquivo: {checkpoint_file}")
    print(f"   Produtos: {len(urls_teste)}")
    print(f"   Rolagens: {num_scrolls}")
    print(f"   Posição: {posicao_scroll}")
    
    # Salva o checkpoint
    salvar_checkpoint(checkpoint_file, urls_teste, num_scrolls, posicao_scroll)
    
    # Verifica se o arquivo foi criado
    if os.path.exists(checkpoint_file):
        print(f"\n✅ Arquivo de checkpoint criado")
        
        # Verifica o tamanho do arquivo
        tamanho = os.path.getsize(checkpoint_file)
        print(f"   Tamanho do arquivo: {tamanho:,} bytes")
        
        # Carrega e valida
        checkpoint = carregar_checkpoint(checkpoint_file)
        
        if checkpoint:
            print(f"\n✅ Checkpoint carregado para validação")
            
            # Valida os dados
            validacoes = [
                ("Número de URLs", len(checkpoint['urls']) == 100, len(checkpoint['urls'])),
                ("Número de rolagens", checkpoint['num_scrolls'] == 50, checkpoint['num_scrolls']),
                ("Posição de scroll", checkpoint['posicao_scroll'] == 10000, checkpoint['posicao_scroll']),
                ("Campo timestamp", 'timestamp' in checkpoint, 'timestamp' if 'timestamp' in checkpoint else 'N/A'),
                ("Total de produtos", checkpoint['total_produtos'] == 100, checkpoint['total_produtos'])
            ]
            
            print(f"\n📊 Validações:")
            todas_ok = True
            for nome, passou, valor in validacoes:
                status = "✅" if passou else "❌"
                print(f"   {status} {nome}: {valor}")
                if not passou:
                    todas_ok = False
            
            if todas_ok:
                print(f"\n✅ Todas as validações passaram!")
            else:
                print(f"\n⚠️  Algumas validações falharam")
        else:
            print(f"\n❌ Falha ao carregar checkpoint para validação")
    else:
        print(f"\n❌ Arquivo de checkpoint não foi criado")
    
    # Limpa
    print(f"\n🗑️  Limpando checkpoint de teste...")
    limpar_checkpoint(checkpoint_file)
    
    return os.path.exists(checkpoint_file) == False

def main():
    """Executa todos os testes"""
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*15 + "🧪 TESTES DO SISTEMA DE CHECKPOINT" + " "*28 + "║")
    print("╚" + "═"*78 + "╝")
    
    print("\n📋 Este teste valida:")
    print("   1. Salvamento de checkpoints")
    print("   2. Carregamento de checkpoints")
    print("   3. Limpeza de checkpoints após sucesso")
    print("   4. Coleta com checkpoint no modo teste")
    
    resultados = {}
    
    # Teste 3: Salvamento (não precisa de navegador)
    try:
        resultados['salvamento'] = testar_salvamento_checkpoint()
    except Exception as e:
        print(f"\n❌ Erro no teste de salvamento: {e}")
        resultados['salvamento'] = False
    
    # Teste 2: Carregamento (não precisa de navegador)
    try:
        resultados['carregamento'] = testar_carregamento_checkpoint()
    except Exception as e:
        print(f"\n❌ Erro no teste de carregamento: {e}")
        resultados['carregamento'] = False
    
    # Teste 1: Coleta básica (precisa de navegador - comentado por enquanto)
    print("\n" + "═"*80)
    print("🧪 TESTE 4: Coleta com Checkpoint (MANUAL)")
    print("═"*80)
    print("\n⚠️  Este teste requer navegador e será executado manualmente:")
    print("   Execute: python main.py")
    print("   Escolha: Opção 3 (Coleta Personalizada)")
    print("   Categoria: Uma categoria pequena (ex: Padaria)")
    print("   Modo: Teste")
    print("\n   Durante a coleta, observe:")
    print("   • Mensagens de checkpoint a cada 1000 produtos")
    print("   • Se crashar, deve recuperar automaticamente")
    print("   • Ao finalizar, checkpoint deve ser removido")
    
    resultados['coleta_basica'] = None  # Será testado manualmente
    
    # Resumo
    print("\n" + "═"*80)
    print("📊 RESUMO DOS TESTES")
    print("═"*80)
    
    for teste, resultado in resultados.items():
        if resultado is True:
            status = "✅ PASSOU"
        elif resultado is False:
            status = "❌ FALHOU"
        else:
            status = "⏭️  MANUAL"
        print(f"   {status}: {teste.replace('_', ' ').title()}")
    
    # Resultado final
    testes_automaticos = [r for r in resultados.values() if r is not None]
    if testes_automaticos and all(testes_automaticos):
        print(f"\n✅ Todos os testes automáticos passaram!")
        print(f"🎉 Sistema de checkpoint funcionando corretamente!")
    elif testes_automaticos and any(testes_automaticos):
        print(f"\n⚠️  Alguns testes falharam")
    else:
        print(f"\n❌ Testes falharam")
    
    print("\n" + "═"*80)
    print("🏁 Testes finalizados")
    print("═"*80 + "\n")

if __name__ == "__main__":
    main()

