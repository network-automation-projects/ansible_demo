"""Logging configuration for NATO Exercise application.

This module provides structured logging setup with file and console handlers,
formatted output, and proper log levels for production use.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from logging import Logger, FileHandler, StreamHandler, Formatter

from exceptions import ConfigurationError


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None
) -> Logger:
    """Configure structured logging for the application.
    
    This function sets up logging with:
        - Console handler for immediate output
        - File handler for persistent logs (if log_file specified)
        - Structured format with timestamps, levels, and messages
        - Configurable log levels
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file (if None, no file logging)
        log_format: Optional custom log format string
        date_format: Optional custom date format string
    
    Returns:
        Configured Logger instance
    
    Raises:
        ConfigurationError: If log_level is invalid or log_file cannot be created
    
    Example usage:
        logger = setup_logging(log_level="DEBUG", log_file="app.log")
        logger.info("Application started")
        logger.error("Error occurred", exc_info=True)
    
    Default log format:
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    Default date format:
        '%Y-%m-%d %H:%M:%S'
    
    TODO: Validate log_level parameter
    TODO: Create log directory if log_file specified
    TODO: Set up console handler with StreamHandler
    TODO: Set up file handler if log_file specified
    TODO: Configure formatters
    TODO: Set log level on logger and handlers
    TODO: Return configured logger
    """
    # TODO: Validate log_level (must be valid logging level)
    # TODO: Get or create logger instance
    # TODO: Clear existing handlers to avoid duplicates
    # TODO: Set logger level
    # TODO: Create console handler (StreamHandler to sys.stdout)
    # TODO: Create file handler if log_file specified
    # TODO: Create log directory if needed
    # TODO: Set up formatters with default or custom format
    # TODO: Add handlers to logger
    # TODO: Handle file creation errors (wrap in ConfigurationError)
    # TODO: Return logger
    pass


def get_logger(name: str = "NATOExercise") -> Logger:
    """Get or create a logger instance.
    
    This is a convenience function to get a logger with the application name.
    If logging hasn't been configured, uses basic configuration.
    
    Args:
        name: Logger name (default: "NATOExercise")
    
    Returns:
        Logger instance
    
    Example usage:
        logger = get_logger("NATOExercise.Converter")
        logger.info("Converting word")
    """
    # TODO: Get logger with specified name
    # TODO: If no handlers exist, call setup_logging() with defaults
    # TODO: Return logger
    pass


def configure_file_logging(logger: Logger, log_file: str, level: str = "INFO"):
    """Add file handler to an existing logger.
    
    This function adds a file handler to a logger that may already have
    console logging configured.
    
    Args:
        logger: Logger instance to configure
        log_file: Path to log file
        level: Log level for file handler
    
    Raises:
        ConfigurationError: If log file cannot be created
    
    TODO: Create log directory if needed
    TODO: Create FileHandler
    TODO: Set level on handler
    TODO: Create formatter
    TODO: Add handler to logger
    TODO: Handle file creation errors
    """
    # TODO: Create log directory if needed
    # TODO: Create FileHandler with log_file path
    # TODO: Set handler level
    # TODO: Create and set formatter
    # TODO: Add handler to logger
    # TODO: Handle PermissionError, OSError (wrap in ConfigurationError)
    pass


def log_error_with_context(
    logger: Logger,
    error: Exception,
    context: dict,
    level: str = "ERROR"
):
    """Log an error with additional context information.
    
    This function logs an exception with structured context data for better
    debugging and monitoring in production.
    
    Args:
        logger: Logger instance
        error: Exception that occurred
        context: Dictionary with additional context (e.g., {'word': 'hello', 'file': 'data.csv'})
        level: Log level (default: "ERROR")
    
    Example usage:
        try:
            result = convert_word("hello")
        except Exception as e:
            log_error_with_context(
                logger,
                e,
                {'word': 'hello', 'function': 'convert_word'}
            )
    
    TODO: Format context dictionary into log message
    TODO: Log exception with traceback
    TODO: Include context in log message
    TODO: Use appropriate log level method
    """
    # TODO: Format context dict into readable string
    # TODO: Log with exc_info=True to include traceback
    # TODO: Include context in message
    # TODO: Use getattr(logger, level.lower()) to call appropriate method
    pass

