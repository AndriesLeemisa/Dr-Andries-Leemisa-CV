import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas for header/footer decoration.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Footer text
        footer_text = f"Dr. Andries Napo Leemisa — Motivational Letter | Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 0.5 * inch, 0.35 * inch, footer_text)
        
        # Footer top line
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(0.5 * inch, 0.48 * inch, letter[0] - 0.5 * inch, 0.48 * inch)
        
        self.restoreState()


def build_letter_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.6 * inch
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY_COLOR = colors.HexColor("#0F172A")    # Midnight / Slate Dark
    SECONDARY_COLOR = colors.HexColor("#2563EB")  # Royal Sapphire Blue
    TEXT_COLOR = colors.HexColor("#1E293B")       # Deep Charcoal Text
    MUTED_COLOR = colors.HexColor("#64748B")      # Secondary Text

    title_style = ParagraphStyle(
        'LetterTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY_COLOR
    )

    subtitle_style = ParagraphStyle(
        'LetterSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=SECONDARY_COLOR
    )

    contact_style = ParagraphStyle(
        'LetterContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=MUTED_COLOR
    )

    salutation_style = ParagraphStyle(
        'LetterSalutation',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=PRIMARY_COLOR,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'LetterBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.2,
        leading=13.5,
        textColor=TEXT_COLOR,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )

    closing_style = ParagraphStyle(
        'LetterClosing',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.2,
        leading=13.5,
        textColor=TEXT_COLOR,
        spaceBefore=8,
        spaceAfter=4
    )

    signature_style = ParagraphStyle(
        'LetterSignature',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=PRIMARY_COLOR
    )

    story = []

    # --- HEADER SECTION ---
    header_data = [
        [
            Paragraph("<b>Dr. Andries Napo Leemisa</b>", title_style),
            Paragraph("<b>Email:</b> andriesnapo@gmail.com &nbsp;|&nbsp; <b>Phone:</b> +27 601896817<br/>"
                      "<b>Location:</b> Johannesburg, Gauteng, South Africa<br/>"
                      "<b>LinkedIn:</b> linkedin.com/in/andries-napo-leemisa-a97097332", contact_style)
        ],
        [
            Paragraph("<b>Biologist (PhD) &amp; AI Automation Entrepreneur</b>", subtitle_style),
            ""
        ]
    ]

    header_table = Table(header_data, colWidths=[4.2 * inch, 3.3 * inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('SPAN', (1,0), (1,1)),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.2, color=PRIMARY_COLOR, spaceBefore=1, spaceAfter=10))

    # --- RECIPIENT & DATE ---
    recip_data = [
        [
            Paragraph("<b>To:</b> Selection Committee / Hiring Manager<br/>"
                      "<b>RE:</b> Application to Executive Role", ParagraphStyle('SubHeader', fontName='Helvetica', fontSize=9, leading=12, textColor=PRIMARY_COLOR)),
            Paragraph("<b>Date:</b> July 29, 2026", ParagraphStyle('DateText', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=MUTED_COLOR, alignment=TA_RIGHT))
        ]
    ]
    recip_table = Table(recip_data, colWidths=[5.3 * inch, 2.2 * inch])
    recip_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(recip_table)
    story.append(Spacer(1, 10))

    # --- SALUTATION ---
    story.append(Paragraph("Dear Hiring Committee / To Whom It May Concern,", salutation_style))

    # --- BODY PARAGRAPHS ---
    p1 = (
        "I am writing to express my strong interest in joining your organization in a senior scientific, technological, "
        "or executive leadership capacity. As a doctoral-level <b>Biologist (PhD)</b> and active <b>AI Automation Entrepreneur</b>, "
        "I bring a rare dual background combining rigorous experimental life science research with production-grade artificial "
        "intelligence engineering. Over the past five years, my career has spanned high-impact academic institutes across "
        "Germany, Hungary, and South Africa, as well as founding a technology agency delivering autonomous AI workflows. "
        "I am eager to apply this unique interdisciplinary skill set to drive innovation and operational excellence within "
        "your esteemed organization."
    )
    story.append(Paragraph(p1, body_style))

    p2 = (
        "During my doctoral research at the Institute for Experimental Cardiovascular Medicine (IEKM), University of Freiburg, "
        "I led advanced investigations into novel light-gated potassium channels for cardiac optogenetics and anti-arrhythmic therapy. "
        "Executing high-throughput single-cell patch-clamp electrophysiology, engineering adenoviral expression vectors under strict S2 "
        "Good Laboratory Practice (GLP) standards, and co-developing quantitative photocycle models allowed me to publish primary findings "
        "in premier international journals including <i>Science Advances</i> (2025) and <i>Biophysical Journal</i> (2026). "
        "My prior master’s research at Eötvös Loránd University (ELTE) focused on RecQ helicases and recombinant protein purification, "
        "solidifying my expertise in biophysical assays and quantitative data science."
    )
    story.append(Paragraph(p2, body_style))

    p3 = (
        "Complementing my academic foundations, as Founder & Lead AI Solutions Architect at Scinovalities AI Automation Agency, "
        "I translate complex systemic challenges into scalable, high-throughput digital solutions. I have architected "
        "enterprise-grade autonomous voice agents, agentic workflows, and specialized operating systems that automated up to 40% "
        "of manual administrative workloads via modern technology and boosted client operational throughput by 28%+. This entrepreneurial "
        "journey has refined my capacity to lead multi-disciplinary technical teams, manage end-to-end product lifecycles, and bridge "
        "deep domain research with commercial deployment."
    )
    story.append(Paragraph(p3, body_style))

    p4 = (
        "Whether advancing cutting-edge biotechnology, architecting intelligent data pipelines, or leading strategic R&D initiatives, "
        "I thrive at the intersection of scientific curiosity and practical execution. I am a collaborative mentor, proven project leader, "
        "and clear communicator comfortable engaging with researchers, executive stakeholders, and global partners alike."
    )
    story.append(Paragraph(p4, body_style))

    p5 = (
        "Thank you for your time and consideration. I welcome the opportunity to discuss how my scientific background, AI engineering "
        "expertise, and strategic leadership can contribute to your team's ongoing success."
    )
    story.append(Paragraph(p5, body_style))

    # --- CLOSING & SIGNATURE ---
    story.append(Paragraph("Sincerely,", closing_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Dr. Andries Napo Leemisa, PhD</b>", signature_style))
    story.append(Paragraph("<font color='#64748B'>Biologist & AI Automation Entrepreneur</font>", ParagraphStyle('SignSub', fontName='Helvetica-Oblique', fontSize=8.5, leading=11, textColor=MUTED_COLOR)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Letter PDF generated successfully: {filename}")

if __name__ == "__main__":
    out_dir = "/home/andries/snap/antigravity/5/.gemini/antigravity/scratch/dr_andries_cv"
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, "Dr_Andries_Motivational_Letter.pdf")
    build_letter_pdf(pdf_path)
