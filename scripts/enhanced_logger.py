#!/usr/bin/env python3
"""
Ulepszony logger dla aplikacji
Dodaje szczegółowe informacje o kontekście, stack trace, i timing
"""

import logging
import os
import sys
import traceback
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional

# Konfiguracja logowania
LOG_FORMAT = "%(asctime)s [%(levelname)8s] %(name)s:%(lineno)d - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class EnhancedLogger:
    """Ulepszony logger z dodatkowymi funkcjami"""
    
    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Dodaj handler jeśli jeszcze nie ma
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(level)
            formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _format_context(self, **kwargs) -> str:
        """Formatuj dodatkowy kontekst"""
        if not kwargs:
            return ""
        
        context_parts = []
        for key, value in kwargs.items():
            # Skróć długie wartości
            if isinstance(value, str) and len(value) > 100:
                value = value[:100] + "..."
            context_parts.append(f"{key}={value}")
        
        return " | " + " | ".join(context_parts)
    
    def info(self, message: str, **context):
        """Log info z kontekstem"""
        ctx = self._format_context(**context)
        self.logger.info(f"{message}{ctx}")
    
    def warning(self, message: str, **context):
        """Log warning z kontekstem"""
        ctx = self._format_context(**context)
        self.logger.warning(f"{message}{ctx}")
    
    def error(self, message: str, exc_info: bool = False, **context):
        """Log error z kontekstem i opcjonalnym stack trace"""
        ctx = self._format_context(**context)
        self.logger.error(f"{message}{ctx}", exc_info=exc_info)
    
    def debug(self, message: str, **context):
        """Log debug z kontekstem"""
        ctx = self._format_context(**context)
        self.logger.debug(f"{message}{ctx}")
    
    def exception(self, message: str, **context):
        """Log exception z pełnym stack trace"""
        ctx = self._format_context(**context)
        self.logger.exception(f"{message}{ctx}")
    
    def log_function_call(self, func_name: str, args: tuple, kwargs: dict, **context):
        """Log wywołanie funkcji"""
        args_str = ", ".join([str(arg)[:50] for arg in args[:3]])
        if len(args) > 3:
            args_str += f" ... (+{len(args)-3} więcej)"
        
        kwargs_str = ", ".join([f"{k}={str(v)[:30]}" for k, v in list(kwargs.items())[:3]])
        if len(kwargs) > 3:
            kwargs_str += f" ... (+{len(kwargs)-3} więcej)"
        
        self.debug(f"→ {func_name}({args_str}, {kwargs_str})", **context)
    
    def log_function_result(self, func_name: str, result: Any, duration: float, **context):
        """Log wynik funkcji z czasem wykonania"""
        result_str = str(result)[:100]
        if len(str(result)) > 100:
            result_str += "..."
        
        self.debug(f"← {func_name}() = {result_str} [{duration:.3f}s]", **context)
    
    def log_api_call(self, method: str, url: str, status_code: Optional[int] = None, 
                     duration: Optional[float] = None, **context):
        """Log wywołanie API"""
        status = f" [{status_code}]" if status_code else ""
        time_str = f" [{duration:.3f}s]" if duration else ""
        ctx = self._format_context(**context)
        self.info(f"🌐 {method} {url}{status}{time_str}{ctx}")
    
    def log_database_query(self, query: str, duration: Optional[float] = None, **context):
        """Log zapytanie do bazy danych"""
        query_short = query[:100] + "..." if len(query) > 100 else query
        time_str = f" [{duration:.3f}s]" if duration else ""
        ctx = self._format_context(**context)
        self.debug(f"💾 {query_short}{time_str}{ctx}")

def log_function_execution(logger: EnhancedLogger):
    """Decorator do logowania wykonania funkcji"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = f"{func.__module__}.{func.__name__}"
            start_time = datetime.now()
            
            try:
                logger.log_function_call(func_name, args, kwargs)
                result = func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds()
                logger.log_function_result(func_name, result, duration)
                return result
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                logger.exception(f"❌ {func_name}() failed after {duration:.3f}s", 
                               error=str(e), error_type=type(e).__name__)
                raise
        
        return wrapper
    return decorator

def log_api_call(logger: EnhancedLogger):
    """Decorator do logowania wywołań API"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = f"{func.__module__}.{func.__name__}"
            start_time = datetime.now()
            
            try:
                result = func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds()
                
                # Spróbuj wyciągnąć informacje o request/response
                url = kwargs.get("url", args[0] if args else "unknown")
                method = kwargs.get("method", "GET")
                status = getattr(result, "status_code", None) if hasattr(result, "status_code") else None
                
                logger.log_api_call(method, url, status, duration)
                return result
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                logger.error(f"❌ API call failed: {func_name}", 
                           error=str(e), duration=duration, url=kwargs.get("url", "unknown"))
                raise
        
        return wrapper
    return decorator

# Global logger instance
_app_logger = None

def get_logger(name: str = "app") -> EnhancedLogger:
    """Pobierz globalny logger"""
    global _app_logger
    if _app_logger is None:
        level = logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO
        _app_logger = EnhancedLogger(name, level)
    return _app_logger

# Przykład użycia:
if __name__ == "__main__":
    logger = get_logger("test")
    
    logger.info("Test info message", user_id=123, session_id="abc")
    logger.warning("Test warning", api_key="sk-...")
    logger.error("Test error", exc_info=False, error_code=500)
    
    @log_function_execution(logger)
    def test_function(x, y):
        return x + y
    
    result = test_function(1, 2)
    print(f"Result: {result}")

