"""
Antigravity Historical Comparison
Gecmis donem verileri ile simdiki verileri karsilastirir.
"""
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

logger = logging.getLogger("Antigravity.HistoricalData")


class HistoricalComparison:
    """Tarihsel donem karsilastirmasi yapar"""

    def __init__(self, storage_file: str = "historical_snapshots.json"):
        self.storage_file = storage_file
        self.snapshots: List[dict] = []
        self.load()

    def load(self):
        """Onceki snapshotlari yukle"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    self.snapshots = json.load(f)
                logger.info(f"{len(self.snapshots)} tarihsel snapshot yuklendi")
            except Exception as e:
                logger.error(f"Snapshot yuklenemedi: {e}")
                self.snapshots = []
        else:
            # Demo verisi olustur
            self.snapshots = self._generate_demo_snapshots()
            self.save()

    def save(self):
        """Snapshotlari diske yaz"""
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.snapshots, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Snapshot kaydedilemedi: {e}")

    def add_snapshot(self, dashboard_data: dict, label: str = None):
        """Mevcut dashboard verisini snapshot olarak kaydet"""
        metrics = dashboard_data.get("EXECUTIVE_METRICS", {})
        ratios = dashboard_data.get("RATIO_ANALYTICS", {})

        snapshot = {
            "date": datetime.now().isoformat(),
            "label": label or datetime.now().strftime("%d.%m.%Y"),
            "financial_health_score": metrics.get("financial_health_score", 0),
            "altman_z_score": metrics.get("altman_z_score", {}).get("value", 0),
            "cash_runway_months": metrics.get("cash_runway_months", 0),
            "roe_pct": metrics.get("return_on_equity_pct", 0),
            "current_ratio": ratios.get("current_ratio", 0),
            "quick_ratio": ratios.get("quick_ratio", 0),
            "debt_to_equity": ratios.get("debt_to_equity_ratio", 0),
            "net_margin_pct": ratios.get("net_profit_margin_pct", 0)
        }

        self.snapshots.append(snapshot)
        # Son 12 snapshot'i tut
        if len(self.snapshots) > 12:
            self.snapshots = self.snapshots[-12:]
        self.save()

    def get_comparison(self) -> dict:
        """Onceki donemle karsilastirma"""
        if len(self.snapshots) < 2:
            return {"has_comparison": False, "message": "Karsilastirma icin en az 2 snapshot gerekli"}

        current = self.snapshots[-1]
        previous = self.snapshots[-2]

        def delta(key, reverse=False):
            curr = current.get(key, 0)
            prev = previous.get(key, 0)
            if prev == 0:
                return {"current": curr, "previous": prev, "change": 0, "change_pct": 0, "trend": "stable"}
            change = curr - prev
            change_pct = (change / prev) * 100
            if abs(change_pct) < 1:
                trend = "stable"
            elif change_pct > 0:
                trend = "down" if reverse else "up"
            else:
                trend = "up" if reverse else "down"
            return {
                "current": round(curr, 2),
                "previous": round(prev, 2),
                "change": round(change, 2),
                "change_pct": round(change_pct, 1),
                "trend": trend
            }

        return {
            "has_comparison": True,
            "current_date": current.get("date"),
            "previous_date": previous.get("date"),
            "metrics": {
                "financial_health_score": delta("financial_health_score"),
                "altman_z_score": delta("altman_z_score"),
                "cash_runway_months": delta("cash_runway_months"),
                "roe_pct": delta("roe_pct"),
                "current_ratio": delta("current_ratio"),
                "debt_to_equity": delta("debt_to_equity", reverse=True),
                "net_margin_pct": delta("net_margin_pct")
            }
        }

    def get_timeline(self) -> List[dict]:
        """Grafik icin zaman serisi"""
        return [
            {
                "label": s.get("label", s.get("date", "")[:10]),
                "health": s.get("financial_health_score", 0),
                "roe": s.get("roe_pct", 0),
                "z_score": s.get("altman_z_score", 0)
            }
            for s in self.snapshots
        ]

    def _generate_demo_snapshots(self) -> List[dict]:
        """Demo icin 4 onceki ceyrek snapshot uret"""
        snapshots = []
        base_date = datetime.now()
        base_health = 6.8
        base_roe = 18.5
        base_z = 2.5

        for i in range(4, 0, -1):
            d = base_date - timedelta(days=90 * i)
            base_health += random.uniform(-0.2, 0.5)
            base_roe += random.uniform(-0.5, 1.2)
            base_z += random.uniform(-0.1, 0.2)

            snapshots.append({
                "date": d.isoformat(),
                "label": f"Q{((d.month - 1) // 3) + 1} {d.year}",
                "financial_health_score": round(base_health, 2),
                "altman_z_score": round(base_z, 2),
                "cash_runway_months": round(15 + (4 - i) * 0.5, 1),
                "roe_pct": round(base_roe, 2),
                "current_ratio": round(2.0 + (4 - i) * 0.05, 2),
                "quick_ratio": round(1.3 + (4 - i) * 0.04, 2),
                "debt_to_equity": round(0.6 - (4 - i) * 0.01, 2),
                "net_margin_pct": round(13.0 + (4 - i) * 0.3, 2)
            })

        return snapshots
