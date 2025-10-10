"""
NovaHouse Analytics System
Ekspert z 40-letnim doświadczeniem - system metryk i monitoringu
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from flask import current_app
import tiktoken
from src.models.chatbot import db, Conversation

@dataclass
class ConversationMetrics:
    """Metryki pojedynczej rozmowy"""
    session_id: str
    timestamp: datetime
    user_message: str
    bot_response: str
    intent: Optional[str]
    entities: Dict[str, Any]
    response_time_ms: int
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float
    lead_created: bool = False
    satisfaction_score: Optional[int] = None

@dataclass
class DailyMetrics:
    """Metryki dzienne"""
    date: str
    total_conversations: int
    total_messages: int
    total_tokens: int
    total_cost_usd: float
    leads_created: int
    avg_response_time_ms: float
    unique_sessions: int
    top_intents: List[Dict[str, Any]]
    cost_per_lead: float

class NovaHouseAnalytics:
    """System analytics dla chatbota NovaHouse"""
    
    def __init__(self):
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
        # Ceny GPT-4o (per 1M tokens)
        self.gpt4o_input_cost = 2.50  # $2.50/1M tokens
        self.gpt4o_output_cost = 10.00  # $10.00/1M tokens
        
    def count_tokens(self, text: str) -> int:
        """Liczenie tokenów w tekście"""
        try:
            return len(self.encoding.encode(text))
        except Exception:
            # Fallback - przybliżone liczenie
            return len(text.split()) * 1.3  # ~1.3 tokena na słowo w polskim
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Kalkulacja kosztu rozmowy"""
        input_cost = (input_tokens / 1_000_000) * self.gpt4o_input_cost
        output_cost = (output_tokens / 1_000_000) * self.gpt4o_output_cost
        return input_cost + output_cost
    
    def track_conversation(self, 
                          session_id: str,
                          user_message: str, 
                          bot_response: str,
                          intent: Optional[str] = None,
                          entities: Optional[Dict] = None,
                          response_time_ms: int = 0,
                          lead_created: bool = False) -> ConversationMetrics:
        """Tracking pojedynczej rozmowy"""
        
        # Liczenie tokenów
        input_tokens = self.count_tokens(user_message)
        output_tokens = self.count_tokens(bot_response)
        total_tokens = input_tokens + output_tokens
        
        # Kalkulacja kosztu
        cost = self.calculate_cost(input_tokens, output_tokens)
        
        # Tworzenie metryki
        metrics = ConversationMetrics(
            session_id=session_id,
            timestamp=datetime.now(),
            user_message=user_message,
            bot_response=bot_response,
            intent=intent,
            entities=entities or {},
            response_time_ms=response_time_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost_usd=cost,
            lead_created=lead_created
        )
        
        # Zapis do bazy danych (rozszerzenie tabeli conversations)
        self._save_metrics_to_db(metrics)
        
        return metrics
    
    def _save_metrics_to_db(self, metrics: ConversationMetrics):
        """Zapis metryk do bazy danych"""
        try:
            # Aktualizacja istniejącego rekordu conversation
            conversation = Conversation.query.filter_by(
                session_id=metrics.session_id,
                user_message=metrics.user_message
            ).first()
            
            if conversation:
                # Dodanie metryk do istniejącego rekordu
                conversation.response_time_ms = metrics.response_time_ms
                conversation.input_tokens = metrics.input_tokens
                conversation.output_tokens = metrics.output_tokens
                conversation.total_tokens = metrics.total_tokens
                conversation.cost_usd = metrics.cost_usd
                conversation.lead_created = metrics.lead_created
                
                db.session.commit()
                
        except Exception as e:
            current_app.logger.error(f"Błąd zapisu metryk: {e}")
            db.session.rollback()
    
    def get_daily_metrics(self, date: Optional[str] = None) -> DailyMetrics:
        """Pobranie metryk dziennych"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            # Query dla dnia
            start_date = datetime.strptime(date, '%Y-%m-%d')
            end_date = start_date + timedelta(days=1)
            
            conversations = Conversation.query.filter(
                Conversation.timestamp >= start_date,
                Conversation.timestamp < end_date
            ).all()
            
            if not conversations:
                return DailyMetrics(
                    date=date,
                    total_conversations=0,
                    total_messages=0,
                    total_tokens=0,
                    total_cost_usd=0.0,
                    leads_created=0,
                    avg_response_time_ms=0.0,
                    unique_sessions=0,
                    top_intents=[],
                    cost_per_lead=0.0
                )
            
            # Kalkulacje
            total_conversations = len(conversations)
            unique_sessions = len(set(c.session_id for c in conversations))
            total_tokens = sum(getattr(c, 'total_tokens', 0) for c in conversations)
            total_cost = sum(getattr(c, 'cost_usd', 0.0) for c in conversations)
            leads_created = sum(1 for c in conversations if getattr(c, 'lead_created', False))
            
            # Średni czas odpowiedzi
            response_times = [getattr(c, 'response_time_ms', 0) for c in conversations if getattr(c, 'response_time_ms', 0) > 0]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            # Top intencje
            intents = [c.intent for c in conversations if c.intent]
            intent_counts = {}
            for intent in intents:
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
            
            top_intents = [
                {"intent": intent, "count": count} 
                for intent, count in sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            ]
            
            # Koszt na lead
            cost_per_lead = total_cost / leads_created if leads_created > 0 else 0
            
            return DailyMetrics(
                date=date,
                total_conversations=total_conversations,
                total_messages=total_conversations,  # Każda rozmowa = 1 wiadomość
                total_tokens=total_tokens,
                total_cost_usd=total_cost,
                leads_created=leads_created,
                avg_response_time_ms=avg_response_time,
                unique_sessions=unique_sessions,
                top_intents=top_intents,
                cost_per_lead=cost_per_lead
            )
            
        except Exception as e:
            current_app.logger.error(f"Błąd pobierania metryk dziennych: {e}")
            return DailyMetrics(
                date=date,
                total_conversations=0,
                total_messages=0,
                total_tokens=0,
                total_cost_usd=0.0,
                leads_created=0,
                avg_response_time_ms=0.0,
                unique_sessions=0,
                top_intents=[],
                cost_per_lead=0.0
            )
    
    def get_budget_status(self, budget_usd: float = 10.0) -> Dict[str, Any]:
        """Status budżetu"""
        try:
            # Suma kosztów z bieżącego miesiąca
            start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            conversations = Conversation.query.filter(
                Conversation.timestamp >= start_of_month
            ).all()
            
            total_spent = sum(getattr(c, 'cost_usd', 0.0) for c in conversations)
            remaining = budget_usd - total_spent
            usage_percent = (total_spent / budget_usd) * 100 if budget_usd > 0 else 0
            
            # Prognoza na koniec miesiąca
            days_in_month = (datetime.now().replace(month=datetime.now().month + 1, day=1) - timedelta(days=1)).day
            current_day = datetime.now().day
            daily_avg = total_spent / current_day if current_day > 0 else 0
            projected_monthly = daily_avg * days_in_month
            
            return {
                "budget_usd": budget_usd,
                "spent_usd": round(total_spent, 4),
                "remaining_usd": round(remaining, 4),
                "usage_percent": round(usage_percent, 2),
                "daily_avg_usd": round(daily_avg, 4),
                "projected_monthly_usd": round(projected_monthly, 4),
                "days_remaining": max(0, int(remaining / daily_avg)) if daily_avg > 0 else 999,
                "status": "OK" if usage_percent < 80 else "WARNING" if usage_percent < 95 else "CRITICAL"
            }
            
        except Exception as e:
            current_app.logger.error(f"Błąd sprawdzania budżetu: {e}")
            return {
                "budget_usd": budget_usd,
                "spent_usd": 0.0,
                "remaining_usd": budget_usd,
                "usage_percent": 0.0,
                "daily_avg_usd": 0.0,
                "projected_monthly_usd": 0.0,
                "days_remaining": 999,
                "status": "OK"
            }
    
    def get_top_questions(self, days: int = 7, limit: int = 10) -> List[Dict[str, Any]]:
        """Najczęstsze pytania użytkowników"""
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            conversations = Conversation.query.filter(
                Conversation.timestamp >= start_date
            ).all()
            
            # Grupowanie podobnych pytań (uproszczone)
            question_counts = {}
            for conv in conversations:
                # Normalizacja pytania (lowercase, usunięcie znaków)
                question = conv.user_message.lower().strip()
                question = ''.join(c for c in question if c.isalnum() or c.isspace())
                
                if len(question) > 10:  # Filtruj bardzo krótkie
                    question_counts[question] = question_counts.get(question, 0) + 1
            
            # Sortowanie i zwracanie top pytań
            top_questions = [
                {
                    "question": question,
                    "count": count,
                    "percentage": round((count / len(conversations)) * 100, 1) if conversations else 0
                }
                for question, count in sorted(question_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
            ]
            
            return top_questions
            
        except Exception as e:
            current_app.logger.error(f"Błąd pobierania top pytań: {e}")
            return []

# Globalna instancja analytics
analytics = NovaHouseAnalytics()

