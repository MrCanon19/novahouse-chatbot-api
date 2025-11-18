"""
Analytics API Routes
Endpointy dla dashboard analytics
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from src.analytics import analytics

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/metrics/daily", methods=["GET"])
def get_daily_metrics():
    """Pobranie metryk dziennych"""
    try:
        date = request.args.get('date')  # Format: YYYY-MM-DD
        metrics = analytics.get_daily_metrics(date)
        
        return jsonify({
            "success": True,
            "data": {
                "date": metrics.date,
                "total_conversations": metrics.total_conversations,
                "total_messages": metrics.total_messages,
                "total_tokens": metrics.total_tokens,
                "total_cost_usd": round(metrics.total_cost_usd, 4),
                "leads_created": metrics.leads_created,
                "avg_response_time_ms": round(metrics.avg_response_time_ms, 2),
                "unique_sessions": metrics.unique_sessions,
                "top_intents": metrics.top_intents,
                "cost_per_lead": round(metrics.cost_per_lead, 4)
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@analytics_bp.route("/metrics/weekly", methods=["GET"])
def get_weekly_metrics():
    """Pobranie metryk tygodniowych"""
    try:
        # Ostatnie 7 dni
        weekly_data = []
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            daily_metrics = analytics.get_daily_metrics(date)
            weekly_data.append({
                "date": date,
                "conversations": daily_metrics.total_conversations,
                "cost_usd": round(daily_metrics.total_cost_usd, 4),
                "leads": daily_metrics.leads_created,
                "avg_response_time": round(daily_metrics.avg_response_time_ms, 2)
            })
        
        # Sumy tygodniowe
        total_conversations = sum(d["conversations"] for d in weekly_data)
        total_cost = sum(d["cost_usd"] for d in weekly_data)
        total_leads = sum(d["leads"] for d in weekly_data)
        avg_response_time = sum(d["avg_response_time"] for d in weekly_data if d["avg_response_time"] > 0)
        avg_response_time = avg_response_time / len([d for d in weekly_data if d["avg_response_time"] > 0]) if avg_response_time else 0
        
        return jsonify({
            "success": True,
            "data": {
                "period": "7_days",
                "daily_breakdown": list(reversed(weekly_data)),  # Najstarsze pierwsze
                "summary": {
                    "total_conversations": total_conversations,
                    "total_cost_usd": round(total_cost, 4),
                    "total_leads": total_leads,
                    "avg_response_time_ms": round(avg_response_time, 2),
                    "conversion_rate": round((total_leads / total_conversations) * 100, 2) if total_conversations > 0 else 0
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@analytics_bp.route("/budget/status", methods=["GET"])
def get_budget_status():
    """Status budżetu"""
    try:
        budget = float(request.args.get('budget', 10.0))  # Default $10
        status = analytics.get_budget_status(budget)
        
        return jsonify({
            "success": True,
            "data": status
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@analytics_bp.route("/questions/top", methods=["GET"])
def get_top_questions():
    """Najczęstsze pytania"""
    try:
        days = int(request.args.get('days', 7))
        limit = int(request.args.get('limit', 10))
        
        questions = analytics.get_top_questions(days, limit)
        
        return jsonify({
            "success": True,
            "data": {
                "period_days": days,
                "questions": questions
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@analytics_bp.route("/dashboard/summary", methods=["GET"])
def get_dashboard_summary():
    """Podsumowanie dla dashboard"""
    try:
        # Dzisiejsze metryki
        today_metrics = analytics.get_daily_metrics()
        
        # Status budżetu
        budget = float(request.args.get('budget', 10.0))
        budget_status = analytics.get_budget_status(budget)
        
        # Top pytania (ostatnie 7 dni)
        top_questions = analytics.get_top_questions(7, 5)
        
        # Metryki tygodniowe dla trendu
        weekly_data = []
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            daily = analytics.get_daily_metrics(date)
            weekly_data.append({
                "date": date,
                "conversations": daily.total_conversations,
                "cost": round(daily.total_cost_usd, 4)
            })
        
        return jsonify({
            "success": True,
            "data": {
                "today": {
                    "conversations": today_metrics.total_conversations,
                    "leads": today_metrics.leads_created,
                    "cost_usd": round(today_metrics.total_cost_usd, 4),
                    "avg_response_time_ms": round(today_metrics.avg_response_time_ms, 2)
                },
                "budget": budget_status,
                "top_questions": top_questions,
                "weekly_trend": list(reversed(weekly_data)),
                "last_updated": datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

