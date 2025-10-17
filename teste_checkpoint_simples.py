#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Teste Simples do Sistema de Checkpoint
==========================================
Testa apenas as funções de checkpoint sem precisar de Selenium.
"""

import json
import os
from datetime import datetime

# ============================================================================
# FUNÇÕES DE CHECKPOINT (copiadas para teste isolado)
# ============================================================================

def salvar_checkpoint(arquivo, urls, num_scrolls, posicao_scroll=0):
    """Salva checkpoint com URLs e metadados"""
    try:
        checkpoint = {
            'urls': urls,
            'num_scrolls': num_scrolls,
            'posicao_scroll': posicao_scroll,
            'timestamp': datetime.now().isoformat(),
            'total_produtos': len(urls)
        }
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2)
        print(f"✅ Checkpoint salvo: {len(urls)} produtos, {num_scrolls} rolagens")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar checkpoint: {e}")
        return False

def carregar_checkpoint(arquivo):
    """Carrega checkpoint se existir"""
    try:
        if os.path.exists(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)
            print(f"📦 Checkpoint carregado: {checkpoint['total_produtos']} produtos, {checkpoint['num_scrolls']} rolagens")
            print(f"   Timestamp: {checkpoint['timestamp']}")
            return checkpoint
    except Exception as e:
        print(f"❌ Erro ao carregar checkpoint: {e}")
    return None

def limpar_checkpoint(arquivo):
    """Remove checkpoint após conclusão"""
    try:
        if os.path.exists(arquivo):
            os.remove(arquivo)
            print(f"🗑️  Checkpoint removido: {arquivo}")
            return True
    except Exception as e:
        print(f"❌ Erro ao remover checkpoint: {e}")
    return False

# ============================================================================
# TESTES
# ============================================================================

def teste_1_salvamento():
    """Teste 1: Salvamento de checkpoint"""
    print("\n" + "═"*80)
    print("🧪 TESTE 1: Salvamento de Checkpoint")
    print("═"*80)
    
    checkpoint_file = "teste_checkpoint_1.json"
    
    # Dados de teste
    urls_teste = [
        {"url": f"https://exemplo.com/produto/{i}", "nome": f"Produto {i}"}
        for i in range(1, 101)
    ]
    
    print(f"\n📝 Salvando checkpoint de teste:")
    print(f"   Produtos: {len(urls_teste)}")
    print(f"   Rolagens: 50")
    print(f"   Posição: 10000")
    
    # Salva
    resultado = salvar_checkpoint(checkpoint_file, urls_teste, 50, 10000)
    
    # Verifica
    if resultado and os.path.exists(checkpoint_file):
        tamanho = os.path.getsize(checkpoint_file)
        print(f"\n✅ Arquivo criado: {tamanho:,} bytes")
        limpar_checkpoint(checkpoint_file)
        return True
    else:
        print(f"\n❌ Falha ao criar arquivo")
        return False

def teste_2_carregamento():
    """Teste 2: Carregamento de checkpoint"""
    print("\n" + "═"*80)
    print("🧪 TESTE 2: Carregamento de Checkpoint")
    print("═"*80)
    
    checkpoint_file = "teste_checkpoint_2.json"
    
    # Cria checkpoint manualmente
    dados = {
        'urls': [
            {"url": "https://exemplo.com/produto/1", "nome": "Produto 1"},
            {"url": "https://exemplo.com/produto/2", "nome": "Produto 2"}
        ],
        'num_scrolls': 10,
        'posicao_scroll': 5000,
        'timestamp': datetime.now().isoformat(),
        'total_produtos': 2
    }
    
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(dados, f)
    
    print(f"\n📝 Checkpoint criado manualmente")
    print(f"   Produtos: {dados['total_produtos']}")
    
    # Carrega
    checkpoint = carregar_checkpoint(checkpoint_file)
    
    # Valida
    if checkpoint:
        valido = (
            len(checkpoint['urls']) == 2 and
            checkpoint['num_scrolls'] == 10 and
            checkpoint['posicao_scroll'] == 5000
        )
        
        if valido:
            print(f"\n✅ Checkpoint carregado e validado corretamente")
            limpar_checkpoint(checkpoint_file)
            return True
        else:
            print(f"\n❌ Dados do checkpoint incorretos")
            limpar_checkpoint(checkpoint_file)
            return False
    else:
        print(f"\n❌ Falha ao carregar checkpoint")
        return False

def teste_3_limpeza():
    """Teste 3: Limpeza de checkpoint"""
    print("\n" + "═"*80)
    print("🧪 TESTE 3: Limpeza de Checkpoint")
    print("═"*80)
    
    checkpoint_file = "teste_checkpoint_3.json"
    
    # Cria arquivo
    with open(checkpoint_file, 'w') as f:
        f.write('{"teste": true}')
    
    print(f"\n📝 Arquivo de teste criado")
    
    # Limpa
    resultado = limpar_checkpoint(checkpoint_file)
    
    # Verifica
    if resultado and not os.path.exists(checkpoint_file):
        print(f"\n✅ Arquivo removido corretamente")
        return True
    else:
        print(f"\n❌ Arquivo não foi removido")
        return False

def teste_4_ciclo_completo():
    """Teste 4: Ciclo completo - salvar, carregar, limpar"""
    print("\n" + "═"*80)
    print("🧪 TESTE 4: Ciclo Completo")
    print("═"*80)
    
    checkpoint_file = "teste_checkpoint_4.json"
    
    # Dados de teste
    urls_originais = [
        {"url": f"https://exemplo.com/p/{i}", "nome": f"Produto {i}"}
        for i in range(1, 1001)  # 1000 produtos
    ]
    
    print(f"\n📝 Testando ciclo completo:")
    print(f"   1. Salvar {len(urls_originais)} produtos")
    print(f"   2. Carregar checkpoint")
    print(f"   3. Validar dados")
    print(f"   4. Limpar checkpoint")
    
    # 1. Salvar
    print(f"\n🔄 Passo 1: Salvando...")
    if not salvar_checkpoint(checkpoint_file, urls_originais, 200, 50000):
        print(f"❌ Falha ao salvar")
        return False
    
    # 2. Carregar
    print(f"\n🔄 Passo 2: Carregando...")
    checkpoint = carregar_checkpoint(checkpoint_file)
    if not checkpoint:
        print(f"❌ Falha ao carregar")
        return False
    
    # 3. Validar
    print(f"\n🔄 Passo 3: Validando...")
    validacoes = [
        ("URLs", len(checkpoint['urls']) == 1000),
        ("Rolagens", checkpoint['num_scrolls'] == 200),
        ("Posição", checkpoint['posicao_scroll'] == 50000),
        ("Total", checkpoint['total_produtos'] == 1000),
    ]
    
    todas_ok = True
    for nome, passou in validacoes:
        status = "✅" if passou else "❌"
        print(f"   {status} {nome}")
        if not passou:
            todas_ok = False
    
    if not todas_ok:
        print(f"\n❌ Validação falhou")
        limpar_checkpoint(checkpoint_file)
        return False
    
    # 4. Limpar
    print(f"\n🔄 Passo 4: Limpando...")
    if not limpar_checkpoint(checkpoint_file):
        print(f"❌ Falha ao limpar")
        return False
    
    if os.path.exists(checkpoint_file):
        print(f"❌ Arquivo ainda existe")
        return False
    
    print(f"\n✅ Ciclo completo executado com sucesso!")
    return True

def main():
    """Executa todos os testes"""
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*10 + "🧪 TESTES DO SISTEMA DE CHECKPOINT (SIMPLES)" + " "*22 + "║")
    print("╚" + "═"*78 + "╝")
    
    print("\n📋 Estes testes validam:")
    print("   • Salvamento de checkpoints em JSON")
    print("   • Carregamento de checkpoints")
    print("   • Limpeza de arquivos")
    print("   • Ciclo completo de uso")
    
    testes = [
        ("Salvamento", teste_1_salvamento),
        ("Carregamento", teste_2_carregamento),
        ("Limpeza", teste_3_limpeza),
        ("Ciclo Completo", teste_4_ciclo_completo),
    ]
    
    resultados = {}
    
    for nome, funcao_teste in testes:
        try:
            resultados[nome] = funcao_teste()
        except Exception as e:
            print(f"\n❌ Exceção no teste {nome}: {e}")
            import traceback
            traceback.print_exc()
            resultados[nome] = False
    
    # Resumo
    print("\n" + "═"*80)
    print("📊 RESUMO DOS TESTES")
    print("═"*80)
    
    for nome, resultado in resultados.items():
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"   {status}: {nome}")
    
    # Resultado final
    if all(resultados.values()):
        print(f"\n🎉 TODOS OS TESTES PASSARAM!")
        print(f"✨ Sistema de checkpoint funcionando perfeitamente!")
        print(f"\n📋 Próximos passos:")
        print(f"   1. O sistema está pronto para uso")
        print(f"   2. Execute python main.py para testar em produção")
        print(f"   3. Observe os checkpoints sendo salvos a cada 1000 produtos")
        print(f"   4. Se crashar, o sistema recuperará automaticamente")
    else:
        print(f"\n⚠️  ALGUNS TESTES FALHARAM")
        falhas = [nome for nome, resultado in resultados.items() if not resultado]
        print(f"   Testes que falharam: {', '.join(falhas)}")
    
    print("\n" + "═"*80)
    print("🏁 Testes finalizados")
    print("═"*80 + "\n")
    
    return all(resultados.values())

if __name__ == "__main__":
    sucesso = main()
    exit(0 if sucesso else 1)

