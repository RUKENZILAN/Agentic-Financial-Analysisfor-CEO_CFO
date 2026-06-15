"""
Antigravity PDF Export
Dashboard verilerini profesyonel bir PDF raporuna donusturur.
"""
import logging
import os
import json
from datetime import datetime

logger = logging.getLogger("Antigravity.PdfExport")

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("reportlab yuklu degil. 'pip install reportlab' calistirin.")


class PdfExporter:
    """dashboard_data.js icerigini PDF'e aktarir"""

    def __init__(self, dashboard_data: dict, company_name: str = "Sirket"):
        self.data = dashboard_data
        self.company = company_name
        # FIX: only call getSampleStyleSheet and font methods if reportlab is available
        if PDF_AVAILABLE:
            self.styles = getSampleStyleSheet()
            self._register_fonts()
        else:
            self.styles = None
            self.font_name = "Helvetica"

    def _register_fonts(self):
        """Turkce karakter destegi icin font kaydet"""
        try:
            pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
            self.styles.add(ParagraphStyle(name="TrTitle", fontName="DejaVu", fontSize=20, spaceAfter=12))
            self.styles.add(ParagraphStyle(name="TrBody", fontName="DejaVu", fontSize=10, leading=14))
            self.styles.add(ParagraphStyle(name="TrHeader", fontName="DejaVu", fontSize=14, textColor=colors.HexColor("#10b981")))
            self.font_name = "DejaVu"
        except Exception:
            # Font not found — fall back to built-in Helvetica and register plain styles
            self.font_name = "Helvetica"
            if "TrTitle" not in self.styles.byName:
                self.styles.add(ParagraphStyle(name="TrTitle", fontName="Helvetica", fontSize=20, spaceAfter=12))
            if "TrBody" not in self.styles.byName:
                self.styles.add(ParagraphStyle(name="TrBody", fontName="Helvetica", fontSize=10, leading=14))
            if "TrHeader" not in self.styles.byName:
                self.styles.add(ParagraphStyle(name="TrHeader", fontName="Helvetica", fontSize=14,
                                               textColor=colors.HexColor("#10b981")))

    def is_available(self) -> bool:
        return PDF_AVAILABLE

    def export(self, output_path: str = None) -> str:
        """PDF olustur ve dosya yolunu dondur"""
        if not PDF_AVAILABLE:
            logger.error("reportlab yuklu degil")
            return None

        if output_path is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_company = "".join(c for c in self.company if c.isalnum() or c in (' ', '_')).strip()
            output_path = f"Antigravity_Report_{safe_company}_{ts}.pdf"

        try:
            doc = SimpleDocTemplate(
                output_path, pagesize=A4,
                leftMargin=2 * cm, rightMargin=2 * cm,
                topMargin=2 * cm, bottomMargin=2 * cm
            )
            story = []

            story.append(Paragraph(f"<b>{self.company} - Yonetici Ozeti Raporu</b>", self.styles["TrTitle"]))
            story.append(Paragraph(f"Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}", self.styles["TrBody"]))
            story.append(Spacer(1, 0.5 * cm))

            story.append(Paragraph("YONETICI OZETI", self.styles["TrHeader"]))
            md = self.data.get("markdown_content", "Veri yok")
            md_clean = md.replace("**", "").replace("#", "").replace("\n", "<br/>")
            story.append(Paragraph(md_clean, self.styles["TrBody"]))
            story.append(Spacer(1, 0.5 * cm))

            story.append(Paragraph("FINANSAL SAGLIK METRIKLERI", self.styles["TrHeader"]))
            metrics = self.data.get("EXECUTIVE_METRICS", {})
            metrics_data = [
                ["Metrik", "Deger"],
                ["Finansal Saglik Skoru", str(metrics.get("financial_health_score", "-"))],
                ["Altman Z-Skoru", str(metrics.get("altman_z_score", {}).get("value", "-"))],
                ["Z-Skoru Bolgesi", str(metrics.get("altman_z_score", {}).get("zone", "-"))],
                ["Nakit Omru (Ay)", str(metrics.get("cash_runway_months", "-"))],
                ["Ozsermaye Karlligi (ROE) %", str(metrics.get("return_on_equity_pct", "-"))]
            ]
            t = Table(metrics_data, colWidths=[8 * cm, 8 * cm])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#10b981")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), self.font_name),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0fdf4")])
            ]))
            story.append(t)
            story.append(Spacer(1, 0.5 * cm))

            story.append(Paragraph("FINANSAL RASYOLAR", self.styles["TrHeader"]))
            ratios = self.data.get("RATIO_ANALYTICS", {})
            ratio_data = [["Rasyo", "Deger"]] + [[k, str(v)] for k, v in ratios.items()]
            t2 = Table(ratio_data, colWidths=[8 * cm, 8 * cm])
            t2.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3b82f6")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), self.font_name),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            story.append(t2)
            story.append(Spacer(1, 0.5 * cm))

            story.append(PageBreak())
            story.append(Paragraph("STRATEJIK AKSIYON PLANI", self.styles["TrHeader"]))
            for item in self.data.get("strategic_action_plan", []):
                story.append(Paragraph(f"<b>*</b> {item}", self.styles["TrBody"]))
                story.append(Spacer(1, 0.2 * cm))
            story.append(Spacer(1, 0.3 * cm))

            story.append(Paragraph("KRITIK RISKLER", self.styles["TrHeader"]))
            for item in self.data.get("critical_risks", []):
                story.append(Paragraph(f"<b>*</b> {item}", self.styles["TrBody"]))
                story.append(Spacer(1, 0.2 * cm))
            story.append(Spacer(1, 0.3 * cm))

            story.append(Paragraph("BUYUME FIRSATLARI", self.styles["TrHeader"]))
            for item in self.data.get("growth_opportunities", []):
                story.append(Paragraph(f"<b>*</b> {item}", self.styles["TrBody"]))
                story.append(Spacer(1, 0.2 * cm))

            story.append(Spacer(1, 1 * cm))
            story.append(Paragraph(
                "<font size=8 color='grey'>YASAL UYARI: Bu rapor tamamen otomatik olarak uretilmis olup "
                "yatirim tavsiyesi niteligi tasimamaktadir. Karar almadan once lisansli bir "
                "profesyonele danisiniz.</font>",
                self.styles["TrBody"]
            ))

            doc.build(story)
            logger.info(f"PDF olusturuldu: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"PDF olusturma hatasi: {e}")
            return None
