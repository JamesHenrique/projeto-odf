# 📊 Sistema de Logging de Erros - Google Sheets

## 🎯 **Visão Geral**

Este sistema implementa um robusto mecanismo de logging de erros que automaticamente registra todos os erros ocorridos no sistema diretamente na aba `logs_erros` do Google Sheets. Isso permite monitoramento em tempo real, análise de padrões de erro e debugging eficiente.

## 🏗️ **Arquitetura do Sistema**

### **Componentes Principais:**

1. **📝 Função Principal**: `enviar_erro_para_sheets()`
2. **🤖 Helper Automático**: `registrar_erro_automatico()`
3. **🛡️ Handler Global**: `handler_global_exceptions()`
4. **🧪 Sistema de Testes**: `teste_logging_erros.py`

---

## 📋 **Estrutura da Aba logs_erros**

### **Colunas Automaticamente Criadas:**

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| `timestamp` | ISO timestamp preciso | 2025-10-05T14:30:15.123456 |
| `data_hora` | Data/hora legível | 05/10/2025 14:30:15 |
| `tipo_erro` | Categoria do erro | ConnectionError, ValueError |
| `mensagem` | Descrição completa | Falha ao conectar API Chatwoot |
| `contexto` | Onde ocorreu | buscar_conversas_chatwoot |
| `modulo` | Arquivo de origem | integrador_chatwoot_sheets.py |
| `linha` | Linha do erro | 45 |
| `severidade` | Nível crítico | HIGH, MEDIUM, LOW |
| `usuario_sistema` | Usuário Windows | Servidor |
| `detalhes_extras` | Info adicional | Python 3.13.0 |

---

## 🔧 **Como Usar**

### **1. Registro Manual de Erro**

```python
from func.integrador_chatwoot_sheets import enviar_erro_para_sheets

# Registra erro específico
enviar_erro_para_sheets(
    tipo_erro="APIConnectionError",
    mensagem_erro="Falha ao conectar com Chatwoot API",
    contexto="buscar_conversas_chatwoot",
    modulo="integrador_chatwoot_sheets.py",
    linha_erro="123"
)
```

### **2. Registro Automático de Exceção**

```python
from func.integrador_chatwoot_sheets import registrar_erro_automatico

try:
    # Código que pode gerar erro
    resultado = api_call()
except Exception as e:
    # Registra automaticamente com traceback
    registrar_erro_automatico(e, "processar_api", "meu_modulo.py")
```

### **3. Handler Global (Já Configurado)**

```python
# Captura AUTOMATICAMENTE qualquer exceção não tratada
# Nenhum código adicional necessário!
```

---

## 🏷️ **Categorias de Erro**

### **Severidades Automáticas:**

- **🔴 HIGH**: `critical`, `fatal`, `connection`, `auth`
- **🟡 MEDIUM**: Erros padrão
- **🟢 LOW**: `warning`, `deprecated`

### **Tipos Comum de Erro:**

| Tipo | Descrição | Contexto Típico |
|------|-----------|-----------------|
| `UIElementNotFound` | Elemento de interface não encontrado | Automação PyAutoGUI |
| `ChatwootAPIError` | Falha na API do Chatwoot | Integração externa |
| `DataStructureError` | Problema na estrutura de dados | Google Sheets |
| `ApplicationStartupError` | Falha ao iniciar aplicação | Login/Inicialização |
| `SystemRestartFailure` | Falha ao reiniciar sistema | Recovery automático |

---

## 🚀 **Funcionalidades Avançadas**

### **✨ Recursos Inteligentes:**

1. **🔄 Criação Automática da Aba**
   - Se `logs_erros` não existir, é criada automaticamente
   - Cabeçalhos são inseridos automaticamente

2. **📏 Truncamento Inteligente**
   - Mensagens limitadas a 500 caracteres
   - Contexto limitado a 200 caracteres
   - Evita células muito grandes

3. **🛡️ Proteção contra Loop Infinito**
   - Se o logging falhar, não gera mais erros
   - Fallback para logging local

4. **📊 Metadados Ricos**
   - Timestamp preciso
   - Informações do sistema
   - Severidade automática

---

## 🧪 **Sistema de Testes**

### **Executar Testes:**

```bash
# Navegar para o diretório do projeto
cd "c:\Users\Servidor\Documents\Project ODF"

# Executar testes
python teste_logging_erros.py
```

### **Testes Incluídos:**

1. ✅ **Erro Simples** - Teste básico de registro
2. ✅ **Erro com Exceção** - Teste com traceback real
3. ✅ **Erro Crítico** - Teste de severidade alta
4. ✅ **Erro UI Element** - Teste de elemento não encontrado
5. ✅ **Dados Longos** - Teste de truncamento

---

## 📊 **Monitoramento e Análise**

### **Consultas Úteis na Planilha:**

```
# Filtrar por severidade
=FILTER(logs_erros!A:J, logs_erros!H:H="HIGH")

# Contar erros por tipo
=COUNTIF(logs_erros!C:C, "ConnectionError")

# Erros nas últimas 24h
=FILTER(logs_erros!A:J, logs_erros!A:A>NOW()-1)
```

### **Indicadores de Saúde:**

- 🟢 **Sistema Saudável**: < 5 erros/hora
- 🟡 **Atenção Necessária**: 5-20 erros/hora
- 🔴 **Intervenção Urgente**: > 20 erros/hora

---

## ⚡ **Integração no Código Existente**

### **Pontos Já Integrados:**

✅ `main.py` - Loop principal e verificações  
✅ `integrador_chatwoot_sheets.py` - APIs e conexões  
✅ Todas as funções críticas do sistema  
✅ Handler global para exceções não tratadas  

### **Para Novos Módulos:**

```python
# No início do arquivo
from func.integrador_chatwoot_sheets import enviar_erro_para_sheets, registrar_erro_automatico

# Em pontos críticos
try:
    # código crítico
    pass
except Exception as e:
    registrar_erro_automatico(e, "contexto_da_operacao", "nome_do_modulo.py")
```

---

## 🔍 **Troubleshooting**

### **Problemas Comuns:**

1. **Aba não criada**
   - Verifique credenciais Google Sheets
   - Confirme permissões da conta de serviço

2. **Erros não aparecem**
   - Execute `teste_logging_erros.py`
   - Verifique logs locais em `/logs/`

3. **Performance lenta**
   - Erros são enviados assincronamente
   - Não impactam performance do sistema principal

---

## 📈 **Benefícios Implementados**

🎯 **Visibilidade Total** - Todos os erros são capturados  
⚡ **Resposta Rápida** - Detecção em tempo real  
📊 **Análise Histórica** - Padrões e tendências  
🔧 **Debug Eficiente** - Informações detalhadas  
🤖 **Automação Completa** - Zero intervenção manual  
📈 **Métricas de Qualidade** - KPIs de estabilidade  

---

## 🎉 **Status: ✅ IMPLEMENTADO E FUNCIONAL**

O sistema está completamente integrado e operacional. Todos os erros do sistema são automaticamente registrados na aba `logs_erros` do Google Sheets, proporcionando monitoramento completo e capacidade de análise avançada.