# 🎯 Guia de Seleção de Categorias - CLI Interativo

**Sistema intuitivo para escolher exatamente quais categorias você deseja coletar**

---

## 📋 Como Funciona a Seleção de Categorias

### **Opção 3 do Menu - Coleta Personalizada** 🎯

Esta opção permite que você escolha **especificamente** quais categorias deseja coletar, oferecendo total controle sobre o processo.

---

## 🚀 Passo a Passo da Coleta Personalizada

### **1. Acesse o Menu Principal**
```bash
python main.py
```

### **2. Escolha Opção 3 - Coleta Personalizada**
```
═════════════════════ MENU PRINCIPAL ═════════════════════

🛒 OPERAÇÕES DE COLETA:
  1. 🧪 Modo Teste          - Coleta rápida para validação
  2. 🚀 Coleta Completa      - Extração completa de dados
  3. 🎯 Coleta Personalizada - Escolher categorias específicas
```

### **3. Visualize as Categorias Disponíveis**

O sistema mostrará automaticamente todas as 16 categorias organizadas:

```
🎯 SELEÇÃO DE CATEGORIAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 CATEGORIAS DISPONÍVEIS:

🍽️ ALIMENTOS - Categorias Específicas:
   [ 1] 🛒 Açougue
   [ 2] 🧊 Alimentos Congelados
   [ 3] 🥛 Alimentos Refrigerados
   [ 4] 🏠 Básicos da Despensa
   [ 5] 🌾 Cereais
   [ 6] 📦 Complemento da Despensa
   [ 7] 🍰 Doces e Sobremesas
   [ 8] 🥬 Hortifruti
   [ 9] 🧂 Mercearia Salgada
   [10] 🍞 Padaria
   [11] 🐟 Peixaria
   [12] 🍗 Rotisserie
   [13] 🥨 Salgadinhos e Aperitivos

🍽️ ALIMENTOS - Categoria Geral:
   [14] 🍽️ Alimentos (Geral)

🥤 BEBIDAS:
   [15] 🥤 Bebidas

🇧🇷 PRODUTOS BRASILEIROS:
   [16] 🇧🇷 Caras do Brasil
```

### **4. Selecione as Categorias Desejadas**

Você tem **4 opções diferentes** de seleção:

#### **Opção A: Atalhos Rápidos** ⚡

```
⚡ OPÇÕES RÁPIDAS:
   • Digite 'todos' para selecionar todas as 16 categorias
   • Digite 'alimentos' para categorias 1-13
   • Digite 'novas' para categorias 14-16
   • Digite números separados por vírgula (ex: 1,3,5,14,15)
```

**Exemplos:**

```bash
👉 Selecione as categorias: todos
✅ Selecionadas TODAS as 16 categorias
```

```bash
👉 Selecione as categorias: alimentos
✅ Selecionadas 13 categorias de alimentos
```

```bash
👉 Selecione as categorias: novas
✅ Selecionadas 3 novas categorias (14-16)
```

#### **Opção B: Seleção Manual de Categorias Específicas** 🎯

Digite os números das categorias separados por vírgula:

**Exemplo 1 - Somente bebidas:**
```bash
👉 Selecione as categorias: 15
✅ 1 categoria(s) selecionada(s):
   • 🥤 Bebidas
```

**Exemplo 2 - Hortifruti + Bebidas + Caras do Brasil:**
```bash
👉 Selecione as categorias: 8,15,16
✅ 3 categoria(s) selecionada(s):
   • 🥬 Hortifruti
   • 🥤 Bebidas
   • 🇧🇷 Caras do Brasil
```

**Exemplo 3 - Várias categorias de alimentos:**
```bash
👉 Selecione as categorias: 1,3,5,7,9,11,13
✅ 7 categoria(s) selecionada(s):
   • 🛒 Açougue
   • 🥛 Alimentos Refrigerados
   • 🌾 Cereais
   • 🍰 Doces e Sobremesas
   • 🧂 Mercearia Salgada
   • 🐟 Peixaria
   • 🥨 Salgadinhos e Aperitivos
```

**Exemplo 4 - Mix de categorias:**
```bash
👉 Selecione as categorias: 1,2,3,14,15,16
✅ 6 categoria(s) selecionada(s):
   • 🛒 Açougue
   • 🧊 Alimentos Congelados
   • 🥛 Alimentos Refrigerados
   • 🍽️ Alimentos (Geral)
   • 🥤 Bebidas
   • 🇧🇷 Caras do Brasil
```

### **5. Escolha o Modo de Coleta**

Após selecionar as categorias, escolha o modo:

```
⚙️ MODO DE COLETA:
   1. 🧪 Teste - Rápido (5 produtos/categoria)
   2. 🚀 Completo - Ilimitado (todos os produtos)

👉 Escolha o modo (1-2): 1

✅ Modo selecionado: TESTE
```

### **6. Confirme e Inicie**

```bash
🤔 Iniciar coleta teste? (s/N): s

🔍 FASE 1: COLETA DE URLs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ... Coleta iniciada ...
```

---

## 💡 Casos de Uso Comuns

### **Caso 1: Testar o Sistema** 🧪
```
Opção: 3 (Coleta Personalizada)
Categorias: 1
Modo: 1 (Teste)
Resultado: Coleta rápida de 5 produtos do açougue
```

### **Caso 2: Coletar Somente Bebidas** 🥤
```
Opção: 3 (Coleta Personalizada)
Categorias: 15
Modo: 2 (Completo)
Resultado: Todos os produtos de bebidas
```

### **Caso 3: Categorias Relacionadas** 🍰
```
Opção: 3 (Coleta Personalizada)
Categorias: 7,13
Modo: 2 (Completo)
Resultado: Doces + Salgadinhos completos
```

### **Caso 4: Tudo de Alimentos** 🍽️
```
Opção: 3 (Coleta Personalizada)
Categorias: alimentos
Modo: 1 (Teste)
Resultado: Teste rápido de todas as 13 categorias de alimentos
```

### **Caso 5: Somente Novas Categorias** 🆕
```
Opção: 3 (Coleta Personalizada)
Categorias: novas
Modo: 2 (Completo)
Resultado: Alimentos Geral + Bebidas + Caras do Brasil completos
```

### **Caso 6: Coletar Tudo** 🌟
```
Opção: 3 (Coleta Personalizada)
Categorias: todos
Modo: 2 (Completo)
Resultado: TODAS as 16 categorias em modo completo
```

---

## 🎨 Vantagens da Seleção Personalizada

### **✅ Flexibilidade Total**
- Escolha exatamente o que precisa coletar
- Evite processar categorias desnecessárias
- Economize tempo focando no que importa

### **✅ Atalhos Inteligentes**
- **`todos`** - Todas as 16 categorias
- **`alimentos`** - Somente alimentos (1-13)
- **`novas`** - Novas categorias (14-16)

### **✅ Seleção Manual Precisa**
- Digite números separados por vírgula
- Combine qualquer quantidade de categorias
- Validação automática de entradas

### **✅ Escolha de Modo**
- **Teste:** 5 produtos por categoria (rápido)
- **Completo:** Todos os produtos (exaustivo)

---

## 📊 Comparação das Opções do Menu

| Opção | Nome | Categorias | Modo | Ideal Para |
|:-----:|------|------------|------|------------|
| **1** | Modo Teste | Selecionadas | Teste | Validação rápida |
| **2** | Coleta Completa | Selecionadas | Completo | Coleta profunda |
| **3** | Coleta Personalizada | **Você escolhe!** | **Você escolhe!** | **Máximo controle** |

---

## 🎯 Exemplos Práticos

### **Exemplo 1: Pesquisa de Mercado - Apenas Bebidas**
```
Objetivo: Analisar preços e informações de bebidas
Categorias: 15
Modo: Completo
Tempo estimado: ~1-2 horas
```

### **Exemplo 2: Análise Nutricional - Produtos Frescos**
```
Objetivo: Estudar produtos frescos e naturais
Categorias: 8,11 (Hortifruti + Peixaria)
Modo: Completo
Tempo estimado: ~2-3 horas
```

### **Exemplo 3: Estudo de Mercado - Produtos Brasileiros**
```
Objetivo: Mapear produtos nacionais
Categorias: 16
Modo: Completo
Tempo estimado: ~30-60 minutos
```

### **Exemplo 4: Base de Dados Completa**
```
Objetivo: Criar base de dados completa
Categorias: todos
Modo: Completo
Tempo estimado: ~8-12 horas (todas as categorias)
```

### **Exemplo 5: Teste Inicial do Sistema**
```
Objetivo: Validar se tudo funciona
Categorias: 1,15,16 (Açougue + Bebidas + Caras do Brasil)
Modo: Teste
Tempo estimado: ~5-10 minutos
```

---

## 🔥 Dicas Avançadas

### **💡 Dica 1: Comece Pequeno**
```
Use modo TESTE com 1-2 categorias primeiro para entender o processo
Exemplo: 15 (somente bebidas em modo teste)
```

### **💡 Dica 2: Use Atalhos**
```
Para coletar rapidamente todas as categorias de alimentos:
Digite: alimentos
Muito mais rápido que: 1,2,3,4,5,6,7,8,9,10,11,12,13
```

### **💡 Dica 3: Estratégia Incremental**
```
Dia 1: Categorias 1-5 (modo completo)
Dia 2: Categorias 6-10 (modo completo)
Dia 3: Categorias 11-16 (modo completo)
```

### **💡 Dica 4: Foco em Novas Categorias**
```
Se você já coletou alimentos, foque nas novas:
Digite: novas
Resultado: Bebidas + Alimentos Geral + Caras do Brasil
```

---

## ⚠️ Observações Importantes

- ✅ **Sem limite de combinações:** Combine qualquer quantidade de categorias
- ✅ **Validação automática:** Sistema valida entradas e ignora valores inválidos
- ✅ **Confirmação antes de iniciar:** Você sempre pode cancelar antes de começar
- ✅ **Modo flexível:** Escolha teste ou completo independente das categorias

---

**Desenvolvido por:** Sidnei Almeida  
**Versão:** 2.0 - CLI Interativo com Seleção Personalizada  
**Data:** Outubro 2025

