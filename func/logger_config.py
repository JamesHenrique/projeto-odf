#!/usr/bin/env python3
"""
Sistema de Logging para Projeto ODF
Configura logs com rotação diária no formato dd-mm-horas.log
"""
import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

def setup_logger(name='projeto_odf', level=logging.INFO):
    """
    Configura o sistema de logging com arquivo rotativo diário
    
    Args:
        name: Nome do logger
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        logger: Instância configurada do logger
    """
    
    # Cria o diretório de logs se não existir
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Nome do arquivo com formato dd-mm-yyyy-HH
    timestamp = datetime.now().strftime("%d-%m-%Y-%H")
    log_filename = os.path.join(log_dir, f"{timestamp}.log")
    
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
    
    # Handler para arquivo com rotação por hora
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