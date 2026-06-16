"""
Antigravity Company Manager
Birden fazla sirketin verilerini ayri ayri yonetir.
"""
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger("Antigravity.CompanyManager")


class CompanyManager:
    """Coklu sirket yonetimi"""

    def __init__(self, registry_file: str = "companies.json"):
        self.registry_file = registry_file
        self.companies: Dict[str, dict] = {}
        self.load()

    def load(self):
        """Sirket kayitlarini diskten yukle"""
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, "r", encoding="utf-8") as f:
                    self.companies = json.load(f)
                logger.info(f"{len(self.companies)} sirket yuklendi")
            except Exception as e:
                logger.error(f"Sirket kayitlari yuklenemedi: {e}")
                self.companies = {}
        else:
            # Varsayilan ornek
            self.companies = {
                "demo_corp": {
                    "name": "Demo Corporation",
                    "code": "DEMO",
                    "created_at": datetime.now().isoformat(),
                    "last_report": None
                }
            }
            self.save()

    def save(self):
        """Sirket kayitlarini diske yaz"""
        try:
            with open(self.registry_file, "w", encoding="utf-8") as f:
                json.dump(self.companies, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Kayit basarisiz: {e}")

    def add_company(self, code: str, name: str) -> bool:
        """Yeni sirket ekle"""
        code = code.strip().lower()
        if not code or not name:
            return False
        if code in self.companies:
            logger.warning(f"{code} zaten mevcut")
            return False

        self.companies[code] = {
            "name": name.strip(),
            "code": code.upper(),
            "created_at": datetime.now().isoformat(),
            "last_report": None
        }
        self.save()
        return True

    def remove_company(self, code: str) -> bool:
        """Sirketi sil"""
        code = code.lower()
        if code in self.companies:
            del self.companies[code]
            self.save()
            return True
        return False

    def get_company(self, code: str) -> Optional[dict]:
        """Sirket bilgisi getir"""
        return self.companies.get(code.lower())

    def list_companies(self) -> List[dict]:
        """Tum sirketleri listele"""
        return list(self.companies.values())

    def update_last_report(self, code: str):
        """Son rapor zamanini guncelle"""
        code = code.lower()
        if code in self.companies:
            self.companies[code]["last_report"] = datetime.now().isoformat()
            self.save()

    def get_companies_for_dropdown(self) -> list:
        """Frontend dropdown icin format"""
        return [
            {"value": code, "label": f"{info['code']} - {info['name']}"}
            for code, info in self.companies.items()
        ]
