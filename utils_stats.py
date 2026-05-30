# utils/stats.py
import json
import os
from datetime import datetime
from config import STATS_FILE

def load_stats():
    """Загружает статистику из JSON-файла"""
    if not os.path.exists(STATS_FILE):
        return {
            "total_donations": 0,
            "donations_count": 0,
            "history": []
        }
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_stats(stats):
    """Сохраняет статистику в JSON-файл"""
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def add_donation(user_id: int, username: str, amount: float = None):
    """
    Фиксирует донат в статистике.
    amount — опционально, если сумма известна.
    """
    stats = load_stats()
    stats["total_donations"] += amount if amount else 0
    stats["donations_count"] += 1
    stats["history"].append({
        "user_id": user_id,
        "username": username,
        "amount": amount,
        "timestamp": datetime.now().isoformat()
    })
    save_stats(stats)
    return stats