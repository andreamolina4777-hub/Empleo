"""Genera un informe PDF profesional a partir de report/informe.qmd usando fpdf2."""

from pathlib import Path
import re
from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "report" / "informe.qmd"
TARGET_OUTPUT = ROOT / "outputs" / "reports" / "informe_final.pdf"
TARGET_PUBLIC = ROOT / "public" / "informe_final.pdf"

def sanitize(text: str) -> str:
    replacements = {
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "•": "*",
        "±": "+/-",
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    # Ensure text can be latin-1 encoded safely
    return text.encode("latin-1", "replace").decode("latin-1")

class PDFReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, sanitize("Universidad Técnica de Cotopaxi · Carrera de Economía"), border=0, new_x="LMARGIN", new_y="NEXT", align="R")
        self.ln(2)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, sanitize(f"Página {self.page_no()}/{{nb}} · Análisis del contexto nacional y global (2020-2024)"), align="C")

def build_pdf():
    pdf = PDFReport()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Title & Metadata
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(20, 40, 80)
    pdf.cell(0, 10, sanitize("Análisis del contexto nacional y global"), new_x="LMARGIN", new_y="NEXT", align="L")
    
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, sanitize("Transformación digital y empleo"), new_x="LMARGIN", new_y="NEXT", align="L")
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, sanitize("Ecuador, Argentina, Colombia y Venezuela - 2020-2024"), new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.ln(5)
    
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    
    in_yaml = False
    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        if line == "---":
            in_yaml = not in_yaml
            idx += 1
            continue
        if in_yaml or not line:
            idx += 1
            continue
            
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            heading_text = sanitize(line.lstrip("#").strip())
            
            pdf.ln(4)
            if level == 1:
                pdf.set_font("Helvetica", "B", 13)
                pdf.set_text_color(20, 40, 80)
                pdf.cell(0, 8, heading_text, new_x="LMARGIN", new_y="NEXT")
                pdf.set_draw_color(180, 190, 210)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(2)
            else:
                pdf.set_font("Helvetica", "B", 11)
                pdf.set_text_color(40, 60, 100)
                pdf.cell(0, 6, heading_text, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(1)
            idx += 1
            continue

        if line.startswith("|"):
            table_rows = []
            while idx < len(lines) and lines[idx].strip().startswith("|"):
                row_str = lines[idx].strip()
                if not set(row_str) <= {"|", "-", ":", " "}:
                    table_rows.append([sanitize(c.strip()) for c in row_str.strip("|").split("|")])
                idx += 1
            
            if table_rows:
                pdf.ln(2)
                pdf.set_font("Helvetica", "B", 8)
                pdf.set_fill_color(235, 240, 250)
                pdf.set_text_color(30, 30, 30)
                
                cols = len(table_rows[0])
                col_width = 190.0 / cols
                
                # Header
                for header_cell in table_rows[0]:
                    pdf.cell(col_width, 6, header_cell, border=1, align="C", fill=True)
                pdf.ln()
                
                # Data rows
                pdf.set_font("Helvetica", "", 8)
                for r_idx, row in enumerate(table_rows[1:]):
                    bg = (248, 249, 252) if r_idx % 2 == 1 else (255, 255, 255)
                    pdf.set_fill_color(*bg)
                    for c_idx, cell_text in enumerate(row):
                        align = "R" if c_idx > 0 else "L"
                        pdf.cell(col_width, 6, cell_text, border=1, align=align, fill=True)
                    pdf.ln()
                pdf.ln(3)
            continue
            
        # Paragraph or bullet
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(30, 30, 30)
        
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", line)
        text = text.replace("`", "").replace("$$", "").replace("$", "")
        text = sanitize(text)
        
        if line.startswith("- "):
            pdf.cell(5, 5, "-", border=0)
            pdf.multi_cell(0, 5, text[2:])
        else:
            pdf.multi_cell(0, 5, text)
        pdf.ln(1)
        idx += 1

    TARGET_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    TARGET_PUBLIC.parent.mkdir(parents=True, exist_ok=True)
    
    pdf.output(str(TARGET_OUTPUT))
    pdf.output(str(TARGET_PUBLIC))
    print(f"PDF generado exitosamente en:\n - {TARGET_OUTPUT}\n - {TARGET_PUBLIC}")

if __name__ == "__main__":
    build_pdf()
