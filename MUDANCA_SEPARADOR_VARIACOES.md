# 🔄 Mudança de Separador de Variações de Medicamentos

## 📋 Resumo da Mudança

O sistema foi atualizado para usar **ponto e vírgula (`;`)** em vez de **hífen (`-`)** como separador de variações de medicamentos na coluna `variacoes` da aba `base_insumos`.

---

## 🆚 Antes vs Depois

### **ANTES (Hífen como separador):**

```
GARCINIA CAMBOGIA-GARCINIA CAMBOGIA EXTRACT-GARCINIA
```

**Problemas:**
- ❌ Conflito com nomes de medicamentos que contêm hífen
- ❌ Ambiguidade na separação
- ❌ Difícil de distinguir hífen do nome vs hífen separador

### **DEPOIS (Ponto e vírgula como separador):**

```
GARCINIA CAMBOGIA;GARCINIA CAMBOGIA EXTRACT;GARCINIA
```

**Vantagens:**
- ✅ Separador mais claro e distinto
- ✅ Sem conflito com nomes de medicamentos
- ✅ Padrão mais usado em listas (CSV, etc.)
- ✅ Mais fácil de identificar visualmente

---

## 📊 Exemplos de Uso

### **Exemplo 1: Medicamento com 2 variações**

**Coluna `descricao`:** `GARCINIA CAMBOGIA`  
**Coluna `variacoes`:** `GARCINIA CAMBOGIA;GARCINIA CAMBOGIA EXTRACT`

**Resultado processado:**
```
GARCINIA CAMBOGIA:[GARCINIA CAMBOGIA,GARCINIA CAMBOGIA EXTRACT]
```

### **Exemplo 2: Medicamento com 3 variações**

**Coluna `descricao`:** `VITAMINA C`  
**Coluna `variacoes`:** `VITAMINA C;ACIDO ASCORBICO;VIT C`

**Resultado processado:**
```
VITAMINA C:[VITAMINA C,ACIDO ASCORBICO,VIT C]
```

### **Exemplo 3: Medicamento sem variações**

**Coluna `descricao`:** `PARACETAMOL`  
**Coluna `variacoes`:** *(vazio)*

**Resultado processado:**
```
PARACETAMOL
```

---

## 🔧 Como Atualizar a Planilha

### **Passo 1: Abrir Google Sheets**
Acesse a planilha `medicamentos-farmacia` → aba `base_insumos`

### **Passo 2: Localizar Coluna `variacoes`**
Encontre todas as células da coluna `variacoes` que contêm variações

### **Passo 3: Substituir Separadores**

**Opção A - Substituir Manualmente:**
1. Selecione a coluna `variacoes`
2. Pressione `Ctrl + H` (Localizar e Substituir)
3. **Localizar:** `-` (hífen)
4. **Substituir por:** `;` (ponto e vírgula)
5. Clique em "Substituir tudo"

**Opção B - Fórmula no Google Sheets:**
```excel
=SUBSTITUTE(A2, "-", ";")
```
Onde `A2` é a célula original com hífens

### **Passo 4: Verificar Resultados**

Antes:
```
GARCINIA CAMBOGIA-GARCINIA EXTRACT
```

Depois:
```
GARCINIA CAMBOGIA;GARCINIA EXTRACT
```

---

## 🧪 Validação

### **Teste 1: Medicamento com Variações**

**Entrada na planilha:**
| descricao | variacoes |
|-----------|-----------|
| GARCINIA CAMBOGIA | GARCINIA CAMBOGIA;GARCINIA CAMBOGIA EXTRACT;GARCINIA |

**Processamento esperado:**
```python
variacoes_lista = ['GARCINIA CAMBOGIA', 'GARCINIA CAMBOGIA EXTRACT', 'GARCINIA']
```

**Resultado no sistema:**
```
GARCINIA CAMBOGIA:[GARCINIA CAMBOGIA,GARCINIA CAMBOGIA EXTRACT,GARCINIA]
```

### **Teste 2: Múltiplos Medicamentos**

**Entrada na planilha:**
| descricao | variacoes |
|-----------|-----------|
| VITAMINA D | VITAMINA D;COLECALCIFEROL;VIT D |
| OMEGA 3 | OMEGA 3;FISH OIL;OLEO DE PEIXE |

**Resultado esperado:**
```
VITAMINA D:[VITAMINA D,COLECALCIFEROL,VIT D], OMEGA 3:[OMEGA 3,FISH OIL,OLEO DE PEIXE]
```

---

## 🔍 Como o Sistema Processa

### **Fluxo de Processamento:**

```
1. Sistema lê a coluna 'variacoes' da aba base_insumos
   ↓
2. Remove ponto e vírgula final (se existir)
   "GARCINIA;EXTRACT;" → "GARCINIA;EXTRACT"
   ↓
3. Divide a string por ';'
   ['GARCINIA', 'EXTRACT']
   ↓
4. Remove espaços em branco de cada item
   ['GARCINIA', 'EXTRACT']
   ↓
5. Cria mapa de variações
   {
     'GARCINIA CAMBOGIA': ['GARCINIA', 'EXTRACT'],
     '_mapa_reverso': {
       'garcinia': {...},
       'extract': {...}
     }
   }
   ↓
6. Sistema usa durante processamento de receitas
```

---

## 📝 Código Atualizado

### **Função: `buscar_variacoes_insumos()`**

```python
# Remove ponto e vírgula final se existir
variacoes_str = variacoes_str.rstrip(';').strip()

if variacoes_str:
    # Separa por ponto e vírgula
    variacoes_lista = [v.strip() for v in variacoes_str.split(';') if v.strip()]
```

**Localização:** `func/integrador_chatwoot_sheets.py` - Linha ~272

---

## ⚠️ Importante

### **Atenção ao Migrar:**

1. **Não misture separadores**
   - ❌ Errado: `GARCINIA-EXTRACT;VIT C`
   - ✅ Correto: `GARCINIA;EXTRACT;VIT C`

2. **Remova espaços extras**
   - ❌ Evite: `GARCINIA ; EXTRACT ; VIT C`
   - ✅ Prefira: `GARCINIA;EXTRACT;VIT C`
   - ℹ️ O sistema remove espaços automaticamente, mas é melhor manter limpo

3. **Evite ponto e vírgula no final**
   - ❌ Evite: `GARCINIA;EXTRACT;`
   - ✅ Prefira: `GARCINIA;EXTRACT`
   - ℹ️ O sistema remove automaticamente, mas é melhor evitar

---

## 🎯 Checklist de Migração

- [ ] Abrir Google Sheets → `medicamentos-farmacia` → `base_insumos`
- [ ] Selecionar coluna `variacoes`
- [ ] Usar `Ctrl + H` para substituir `-` por `;`
- [ ] Verificar visualmente alguns exemplos
- [ ] Remover ponto e vírgula extras no final (se houver)
- [ ] Salvar alterações
- [ ] Testar com o sistema executando uma receita
- [ ] Confirmar que variações são encontradas corretamente

---

## 📊 Impacto no Sistema

### **Arquivos Modificados:**

✅ `func/integrador_chatwoot_sheets.py`
- Função `buscar_variacoes_insumos()` - Linha ~270
- Documentação atualizada

### **Compatibilidade:**

- ✅ **Retrocompatível:** Não afeta dados já processados
- ✅ **Formato antigo:** Sistema continuará funcionando se não houver hífen nos nomes
- ⚠️ **Requer atualização:** Planilha `base_insumos` deve ser atualizada para usar `;`

---

## 🧪 Teste Rápido

### **Como testar se está funcionando:**

1. Adicione uma linha de teste na `base_insumos`:
   ```
   descricao: TESTE MEDICAMENTO
   variacoes: TESTE MEDICAMENTO;TESTE MED;MED TESTE
   ```

2. Execute o sistema com uma receita contendo "TESTE MEDICAMENTO"

3. Verifique nos logs se as 3 variações foram carregadas:
   ```
   TESTE MEDICAMENTO -> 3 variacoes: ['TESTE MEDICAMENTO', 'TESTE MED', 'MED TESTE']
   ```

---

## 📅 Informações da Mudança

**Data de Implementação:** 17/10/2025  
**Versão:** 2.2 - Separador Ponto e Vírgula  
**Status:** ✅ Implementado  
**Prioridade:** 🔴 Alta - Requer atualização da planilha  
**Impacto:** ⚠️ Médio - Necessário atualizar dados existentes  

---

## ❓ FAQ

**P: O que acontece se eu deixar hífen em vez de ponto e vírgula?**  
R: O sistema não encontrará as variações corretamente. Medicamentos que têm hífen no nome serão divididos incorretamente.

**P: Posso usar espaços ao redor do ponto e vírgula?**  
R: Sim, o sistema remove espaços automaticamente. Mas é recomendado não usar.

**P: E se eu tiver apenas 1 variação?**  
R: Funciona normalmente. Exemplo: `GARCINIA;` ou `GARCINIA` (ambos funcionam)

**P: Preciso atualizar todas as linhas de uma vez?**  
R: Recomendado, mas pode atualizar gradualmente. O sistema funciona linha por linha.

---

## ✅ Status: IMPLEMENTADO

A mudança foi implementada e está pronta para uso. **Ação necessária:** Atualizar a planilha `base_insumos` substituindo `-` por `;` na coluna `variacoes`.