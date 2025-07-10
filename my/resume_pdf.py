from datetime import datetime
from typing import List, Dict

from fpdf import FPDF


def _add_section(pdf: FPDF, title: str, lines: List[str]):
    if not lines:
        return
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, title, ln=1)
    pdf.set_font("Helvetica", size=11)
    for line in lines:
        pdf.multi_cell(0, 6, f"• {line}")
    pdf.ln(4)


def generate_resume(data: Dict) -> bytes:
    """Generate a simple one-page PDF résumé based on collected user data.

    Parameters
    ----------
    data : Dict
        Data dictionary stored in Streamlit session_state. Expected keys:
        - name, email, phone (str)
        - skills, languages (List[str])

    Returns
    -------
    bytes
        PDF binary.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, data.get("name", "Имя Фамилия"), ln=1)

    pdf.set_font("Helvetica", size=12)
    contact_line = " | ".join(
        [p for p in [data.get("email"), data.get("phone")] if p]
    )
    if contact_line:
        pdf.cell(0, 8, contact_line, ln=1)

    pdf.ln(4)

    # Sections
    _add_section(pdf, "Навыки", data.get("skills", []))
    # Education
    edu_lines = [
        f"{e['institution']} — {e['degree']} ({e['years']})" for e in data.get("education", [])
    ]
    _add_section(pdf, "Образование", edu_lines)

    # Experience
    exp_lines = [
        f"{e['company']} — {e['position']} ({e['period']}) | {e['description']}".strip()
        for e in data.get("experience", [])
    ]
    _add_section(pdf, "Опыт работы", exp_lines)

    _add_section(pdf, "Языки", data.get("languages", []))

    # Footer
    pdf.set_y(-20)
    pdf.set_font("Helvetica", size=8)
    pdf.cell(0, 10, f"Сгенерировано {datetime.now().strftime('%d.%m.%Y')}")

    pdf_bytes = pdf.output(dest="S")  # returns "bytes" or "bytearray" depending on fpdf version
    return bytes(pdf_bytes)