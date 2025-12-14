"""
Módulo de serviços para comunicação com microsserviços externos.
"""

from services.email_service import email_service
from services.aluguel_service import aluguel_service

__all__ = ["email_service", "aluguel_service"]
