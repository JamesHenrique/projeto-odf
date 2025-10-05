# Sistema de Logging - Projeto ODF

## 📋 Estrutura de Logs

O sistema utiliza arquivos de log com rotação automática por hora no formato:
```
logs/dd-mm-yyyy-HH.log
```

### Exemplos:
- `05-10-2025-18.log` - Log do dia 05/10/2025 às 18h
- `06-10-2025-09.log` - Log do dia 06/10/2025 às 09h

## 🔧 Como Usar

### 1. Importar o Logger
```python
from func.logger_config import get_logger

# Logger específico para o módulo
logger = get_logger('nome_do_modulo')
```

### 2. Níveis de Log
```python
logger.debug('Informação detalhada para debug')
logger.info('Informação geral')
logger.warning('Aviso importante')
logger.error('Erro recoverto')
logger.critical('Erro crítico')
```

### 3. Estrutura das Mensagens
```
2025-10-05 18:30:45 - projeto_odf.main - INFO - inic_process:25 - Processo iniciado com sucesso
```

Formato: `TIMESTAMP - LOGGER_NAME - LEVEL - FUNCTION:LINE - MESSAGE`

## 📁 Localização dos Logs

- **Pasta**: `logs/`
- **Formato**: `dd-mm-yyyy-HH.log`
- **Encoding**: UTF-8
- **Rotação**: Por hora automaticamente

## 🔍 Níveis Implementados

| Nível | Uso | Exemplo |
|-------|-----|---------|
| `DEBUG` | Detalhes técnicos | Valores de variáveis, fluxo detalhado |
| `INFO` | Fluxo normal | Início/fim de processos, status |
| `WARNING` | Avisos | Situações não ideais mas recuperáveis |
| `ERROR` | Erros | Falhas recovertáveis |
| `CRITICAL` | Erros críticos | Falhas que impedem funcionamento |

## 🚀 Módulos Atualizados

- ✅ `main.py` - Sistema principal
- ✅ `integrador_chatwoot_sheets.py` - Integração APIs
- ✅ `interection_receita.py` - Processamento de receitas
- 🔄 `actions_btn.py` - Ações de interface (pendente)
- 🔄 `inic_login.py` - Login e inicialização (pendente)

## 📊 Monitoramento

Para monitorar logs em tempo real:
```bash
# Windows PowerShell
Get-Content "logs\05-10-2025-18.log" -Wait

# Linux/Mac
tail -f logs/05-10-2025-18.log
```

## 🔒 Segurança

- ❌ **Não logar**: Senhas, tokens, dados sensíveis
- ✅ **Logar**: Status, erros, fluxo de execução
- ✅ **Usar DEBUG**: Para dados detalhados apenas em desenvolvimento