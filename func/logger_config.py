#!/usr/bin/env python3
"""
Sistema de Logging para Projeto ODF
Configura logs com estrutura de pastas: logs/MES_ANO/DIA/HH.log
"""
import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

def criar_estrutura_logs():
    """
    Cria a estrutura de diretórios para logs: logs/MES_ANO/DIA/
    
    Returns:
        str: Caminho completo do diretório de logs do dia
    """
    # Diretório base de logs
    base_dir = os.path.dirname(os.path.dirname(__file__))
    logs_base = os.path.join(base_dir, 'logs')
    
    # Data atual
    agora = datetime.now()
    mes_ano = agora.strftime("%m_%Y")  # Formato: 10_2025
    dia = agora.strftime("%d")         # Formato: 28
    
    # Cria estrutura: logs/10_2025/28/
    log_dir = os.path.join(logs_base, mes_ano, dia)
    
    # Cria todos os diretórios se não existirem
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"📁 Estrutura de logs criada: {log_dir}")
    
    return log_dir

def setup_logger(name='projeto_odf', level=logging.INFO):
    """
    Configura o sistema de logging com arquivo rotativo por hora
    Estrutura: logs/MES_ANO/DIA/HH.log
    
    Args:
        name: Nome do logger
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        logger: Instância configurada do logger
    """
    
    # Cria a estrutura de diretórios
    log_dir = criar_estrutura_logs()
    
    # Nome do arquivo com formato HH (apenas hora)
    hora = datetime.now().strftime("%H")
    log_filename = os.path.join(log_dir, f"{hora}.log")
    
    # Configura o logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove handlers existentes para evitar duplicação
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Formato das mensagens
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler para console (opcional - pode ser removido em produção)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(module_name=None):
    """
    Obtém uma instância do logger para um módulo específico
    
    Args:
        module_name: Nome do módulo (usado para identificar a origem do log)
    
    Returns:
        logger: Instância do logger
    """
    if module_name:
        logger_name = f"projeto_odf.{module_name}"
    else:
        logger_name = "projeto_odf"
    
    return setup_logger(logger_name)

# Logger global para uso direto
logger = get_logger()