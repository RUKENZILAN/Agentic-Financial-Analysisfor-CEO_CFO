"""
Antigravity Excel Reader
financial_data.xlsx dosyasindan gercek finansal verileri okur ve oranlari hesaplar.
Desteklenen sayfalar: Mizan, Bilanco, Gelir Tablosu
"""
import logging
import os
from typing import Dict, Optional

logger = logging.getLogger("Antigravity.ExcelReader")

# pandas/openpyxl yuklu degilse hata vermemesi icin lazy import
try:
    import pandas as pd
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False
    logger.warning("pandas/openpyxl yuklu degil. 'pip install pandas openpyxl' calistirin.")


class ExcelReader:
    """Excel dosyasindan finansal tablolari okur ve standart oranlari hesaplar."""

    def __init__(self, file_path: str = "financial_data.xlsx"):
        self.file_path = file_path
        self.data = {}
        self.metrics = {}

    def is_available(self) -> bool:
        """Excel dosyasi var mi ve pandas yuklu mu?"""
        if not EXCEL_AVAILABLE:
            return False
        return os.path.exists(self.file_path)

    def read_all(self) -> Dict:
        """Excel'deki tum sayfalari oku"""
        if not self.is_available():
            logger.warning(f"{self.file_path} bulunamadi veya pandas yuklu degil")
            return {}

        try:
            xls = pd.ExcelFile(self.file_path)
            logger.info(f"Bulunan sayfalar: {xls.sheet_names}")

            for sheet in xls.sheet_names:
                sheet_lower = sheet.lower()
                df = pd.read_excel(self.file_path, sheet_name=sheet)

                if "mizan" in sheet_lower or "trial" in sheet_lower:
                    self.data["trial_balance"] = self._parse_trial_balance(df)
                elif "bilanco" in sheet_lower or "balance" in sheet_lower:
                    self.data["balance_sheet"] = self._parse_balance_sheet(df)
                elif "gelir" in sheet_lower or "income" in sheet_lower:
                    self.data["income_statement"] = self._parse_income_statement(df)
                else:
                    self.data[sheet] = df.to_dict(orient="records")

            # Oranlari hesapla
            self.metrics = self._calculate_ratios()
            return {"data": self.data, "metrics": self.metrics}

        except Exception as e:
            logger.error(f"Excel okuma hatasi: {e}")
            return {}

    def _parse_trial_balance(self, df) -> list:
        """Mizan verisini standart formata getirir"""
        records = []
        for _, row in df.iterrows():
            try:
                records.append({
                    "account": str(row.iloc[0]).strip(),
                    "debit": float(row.iloc[1]) if pd.notna(row.iloc[1]) else 0.0,
                    "credit": float(row.iloc[2]) if pd.notna(row.iloc[2]) else 0.0
                })
            except (ValueError, IndexError):
                continue
        return records

    def _parse_balance_sheet(self, df) -> Dict:
        """Bilanco kalemlerini sozluk olarak dondurur"""
        result = {}
        for _, row in df.iterrows():
            try:
                key = str(row.iloc[0]).strip().lower()
                if pd.notna(row.iloc[1]):
                    result[key] = float(row.iloc[1])
            except (ValueError, IndexError):
                continue
        return result

    def _parse_income_statement(self, df) -> Dict:
        """Gelir tablosunu sozluk olarak dondurur"""
        result = {}
        for _, row in df.iterrows():
            try:
                key = str(row.iloc[0]).strip().lower()
                if pd.notna(row.iloc[1]):
                    result[key] = float(row.iloc[1])
            except (ValueError, IndexError):
                continue
        return result

    def _calculate_ratios(self) -> Dict:
        """Bilanco ve gelir tablosundan finansal oranlari hesaplar"""
        bs = self.data.get("balance_sheet", {})
        is_ = self.data.get("income_statement", {})

        def g(d, *keys):
            for k in keys:
                for dk, dv in d.items():
                    if k in dk:
                        return dv
            return 0.0

        current_assets = g(bs, "donen varlik", "current asset")
        current_liab = g(bs, "kisa vadeli", "current liab")
        total_assets = g(bs, "toplam varlik", "total asset")
        total_liab = g(bs, "toplam borc", "toplam yukumluluk", "total liab")
        equity = g(bs, "ozsermaye", "oz kaynak", "equity")
        inventory = g(bs, "stok", "inventory")
        cash = g(bs, "nakit", "kasa", "cash")
        revenue = g(is_, "satis", "hasilat", "revenue", "sales")
        net_income = g(is_, "net kar", "net income", "net profit")
        cost = g(is_, "satilan malin", "cost of")

        ratios = {
            "current_ratio": round(current_assets / current_liab, 2) if current_liab else 0,
            "quick_ratio": round((current_assets - inventory) / current_liab, 2) if current_liab else 0,
            "debt_to_equity": round(total_liab / equity, 2) if equity else 0,
            "net_profit_margin_pct": round((net_income / revenue) * 100, 2) if revenue else 0,
            "return_on_equity_pct": round((net_income / equity) * 100, 2) if equity else 0,
            "asset_turnover": round(revenue / total_assets, 2) if total_assets else 0,
            "current_assets": current_assets,
            "total_assets": total_assets,
            "total_liabilities": total_liab,
            "equity": equity,
            "revenue": revenue,
            "net_income": net_income
        }

        # Altman Z-Skoru (Public manufacturing firm formulu)
        # Z = 1.2*A + 1.4*B + 3.3*C + 0.6*D + 1.0*E
        # A = Working Capital / Total Assets
        # B = Retained Earnings / Total Assets
        # C = EBIT / Total Assets
        # D = Market Value Equity / Total Liabilities
        # E = Sales / Total Assets
        wc = current_assets - current_liab
        z_score = 0
        if total_assets > 0:
            z_score = (
                1.2 * (wc / total_assets) +
                1.4 * (equity * 0.5 / total_assets) +
                3.3 * (net_income / total_assets) +
                0.6 * (equity / total_liab if total_liab else 0) +
                1.0 * (revenue / total_assets)
            )

        if z_score > 2.99:
            zone = "SAFE"
        elif z_score > 1.81:
            zone = "GREY"
        else:
            zone = "DISTRESS"

        ratios["altman_z_score"] = round(z_score, 2)
        ratios["altman_z_zone"] = zone

        # Cash runway (ay)
        if net_income < 0 and cash > 0:
            monthly_burn = abs(net_income) / 12
            ratios["cash_runway_months"] = round(cash / monthly_burn, 1) if monthly_burn else 0
        else:
            ratios["cash_runway_months"] = 24  # pozitifse 24 ay varsay

        return ratios


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reader = ExcelReader()
    if reader.is_available():
        result = reader.read_all()
        print("OK")
        print(result["metrics"])
    else:
        print("Excel dosyasi yok veya pandas yuklu degil")
