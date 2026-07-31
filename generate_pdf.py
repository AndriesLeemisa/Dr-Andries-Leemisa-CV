import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically add total page numbers and footers.
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
        footer_text = f"Dr. Andries Napo Leemisa — Curriculum Vitae | Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 0.4 * inch, 0.3 * inch, footer_text)
        
        # Footer top line
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(0.4 * inch, 0.42 * inch, letter[0] - 0.4 * inch, 0.42 * inch)
        
        self.restoreState()


def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=0.4 * inch,
        rightMargin=0.4 * inch,
        topMargin=0.4 * inch,
        bottomMargin=0.55 * inch
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY_COLOR = colors.HexColor("#0F172A")    # Midnight / Slate Dark
    SECONDARY_COLOR = colors.HexColor("#2563EB")  # Royal Sapphire Blue
    TEXT_COLOR = colors.HexColor("#1E293B")       # Deep Charcoal Text
    MUTED_COLOR = colors.HexColor("#64748B")      # Secondary Text
    BG_LIGHT = colors.HexColor("#F8FAFC")         # Light Box Background
    BORDER_COLOR = colors.HexColor("#CBD5E1")     # Border Gray

    title_style = ParagraphStyle(
        'CVTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=21,
        textColor=PRIMARY_COLOR
    )

    subtitle_style = ParagraphStyle(
        'CVSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=SECONDARY_COLOR
    )

    contact_style = ParagraphStyle(
        'CVContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=MUTED_COLOR
    )

    section_heading = ParagraphStyle(
        'CVSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=PRIMARY_COLOR,
        spaceBefore=6,
        spaceAfter=2
    )

    item_title_style = ParagraphStyle(
        'ItemTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=11.5,
        textColor=PRIMARY_COLOR
    )

    item_subtitle_style = ParagraphStyle(
        'ItemSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=10.5,
        textColor=SECONDARY_COLOR
    )

    date_style = ParagraphStyle(
        'ItemDate',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10.5,
        textColor=MUTED_COLOR,
        alignment=TA_RIGHT
    )

    body_style = ParagraphStyle(
        'CVBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=10.8,
        textColor=TEXT_COLOR,
        spaceAfter=1
    )

    bullet_style = ParagraphStyle(
        'CVBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=10.8,
        textColor=TEXT_COLOR,
        leftIndent=8,
        spaceAfter=1.5
    )

    tag_style = ParagraphStyle(
        'CVTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=8.5,
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

    header_table = Table(header_data, colWidths=[4.3 * inch, 3.15 * inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('SPAN', (1,0), (1,1)),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=1.2, color=PRIMARY_COLOR, spaceBefore=1, spaceAfter=4))

    # --- HELPER FUNCTION FOR SECTIONS ---
    def make_section(title):
        p = Paragraph(f"<b>{title.upper()}</b>", section_heading)
        hr = HRFlowable(width="100%", thickness=0.6, color=SECONDARY_COLOR, spaceBefore=1, spaceAfter=3)
        return [p, hr]

    # --- EXECUTIVE PROFILE ---
    story.extend(make_section("Executive Profile"))
    profile_text = (
        "Talented <b>Biologist (PhD)</b> and <b>AI Automation Entrepreneur</b> with over 5 years of "
        "international research, analytical, and technological leadership experience in South Africa, Hungary, and Germany. "
        "Expertise encompasses cardiac optogenetics, single-cell patch-clamp electrophysiology, quantitative photocycle modeling, "
        "and production-grade agentic AI workflows. Proven track record of publishing high-impact research (<i>Science Advances</i>, "
        "<i>Biophysical Journal</i>), leading cross-functional teams, and engineering AI-driven operating systems that optimize "
        "operational throughput by 30%+. Seeking to leverage interdisciplinary scientific rigor and tech innovation in "
        "senior/executive roles across Biotechnology, Pharmaceuticals, R&amp;D, HealthTech, and Enterprise Solutions."
    )
    story.append(Paragraph(profile_text, body_style))
    story.append(Spacer(1, 4))

    # --- WORK EXPERIENCE ---
    story.extend(make_section("Professional & Research Experience"))

    def make_job(title, company_loc, dates, bullets, tags=None):
        t_cell = Paragraph(f"<b>{title}</b>", item_title_style)
        sub_cell = Paragraph(company_loc, item_subtitle_style)
        d_cell = Paragraph(dates, date_style)
        
        job_table = Table([[t_cell, d_cell], [sub_cell, ""]], colWidths=[5.45 * inch, 2.0 * inch])
        job_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('SPAN', (0,1), (1,1)),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        
        elements = [job_table, Spacer(1, 1.5)]
        for b in bullets:
            elements.append(Paragraph(f"• {b}", bullet_style))
            
        if tags:
            tag_cells = [[Paragraph(f"<b>{tag}</b>", tag_style) for tag in tags]]
            tag_table = Table(tag_cells, colWidths=[None]*len(tags))
            t_style = [
                ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 1.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
                ('LEFTPADDING', (0,0), (-1,-1), 4),
                ('RIGHTPADDING', (0,0), (-1,-1), 4),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.white),
                ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ]
            tag_table.setStyle(TableStyle(t_style))
            elements.append(Spacer(1, 1.5))
            elements.append(tag_table)
            
        elements.append(Spacer(1, 4))
        return KeepTogether(elements)

    # Roles
    j1_bullets = [
        "Architected enterprise-grade autonomous voice agents and agentic AI workflows, reducing candidate screening processing times by 60% and accelerating talent acquisition.",
        "Engineered a scalable Hospitality Operating System, automating 40% of manual administrative tasks via modern technology orchestration.",
        "Developed 'Autoflow AI' (Real Estate & Lodging Management System), reducing repetitive manual workflows and elevating team project delivery speed by 25%.",
        "Created 'Lead Genius SA', an automated B2B lead generation platform integrated with CRM, multi-channel outreach, bulk email automation, and marketing analytics.",
        "Designed and optimized digital presence and brand assets for enterprise clients, achieving a +28% increase in operational throughput."
    ]
    j1_tags = ["LLM Orchestration", "Agentic AI", "Voice Agent Deployment", "Modern Technology", "Scalable API Design"]
    story.append(make_job("Founder & Lead AI Solutions Architect", "Scinovalities AI Automation Agency — Johannesburg, South Africa", "Jan 2025 — Present", j1_bullets, j1_tags))

    j2_bullets = [
        "Investigated novel light-gated potassium channels for optical modulation and inhibition of cardiomyocyte action potentials and tissue excitability to advance anti-arrhythmic research.",
        "Orchestrated and executed high-throughput single-cell patch-clamp electrophysiology experiments using Axopatch 200B amplifiers and Digidata 1550A digitizers.",
        "Engineered adenoviral expression vectors and performed primary mammalian cardiomyocyte isolations under strict S2 Good Laboratory Practice (GLP) standards.",
        "Co-developed quantitative photocycle models for novel optogenetic channels, directly contributing to research published in <i>Science Advances</i> (2025) and <i>Biophysical Journal</i> (2026).",
        "Presented peer-reviewed scientific findings at premier international conferences across Europe, including NoTiCE (Glasgow), SPP1926 (Uslar), and DGK (Mannheim).",
        "Organized and led weekly IEKM PhD Journal Clubs (2022–2023), driving critical literature analysis and knowledge sharing among doctoral candidates."
    ]
    j2_tags = ["Quantitative Modeling", "Signal Processing", "Patch-Clamp Electrophysiology", "Data Mining", "S2 GLP"]
    story.append(make_job("Doctoral Research Scientist", "Institute for Experimental Cardiovascular Medicine (IEKM), University of Freiburg — Germany", "Nov 2021 — Mar 2026", j2_bullets, j2_tags))

    j3_bullets = [
        "Elucidated the biochemical mechanics of RecQ helicases in homologous recombination pathway selection to decipher fundamental genome stability mechanisms.",
        "Purified high-yield recombinant proteins and plasmid DNA, optimizing MaxPrep protocols and expression vector constructs.",
        "Quantified protein-DNA binding dynamics using advanced biophysical assays, including Fluorescence Anisotropy and Electrophoretic Mobility Shift Assays (EMSA).",
        "Evaluated molecular recombination pathways to characterize helicase-protein interactions within cell-free expression systems."
    ]
    j3_tags = ["Biophysical Modeling", "Statistical Analysis", "Protein Purification", "Fluorescence Anisotropy"]
    story.append(make_job("Master's Research Fellow", "Department of Biochemistry, Eötvös Loránd University (ELTE) — Budapest, Hungary", "Sep 2017 — Jul 2019", j3_bullets, j3_tags))

    j4_bullets = [
        "Evaluated toxicological medico-legal autopsy records (2013–2015) to identify mortality patterns and toxicological trends across Greater Johannesburg.",
        "Analyzed, sanitized, and categorized extensive laboratory case records, extracting critical toxicological data for statistical synthesis.",
        "Synthesized a comprehensive forensic thesis connecting toxic substance prevalence to medico-legal cause-of-death findings."
    ]
    j4_tags = ["Data Analytics", "Forensic Toxicology", "Statistical Synthesis", "Case Database Review"]
    story.append(make_job("Graduate Research Assistant", "Johannesburg Forensic Pathology Services / Wits University — South Africa", "Feb 2015 — Nov 2016", j4_bullets, j4_tags))

    j5_bullets = [
        "Delivered laboratory instruction and academic mentorship to top-performing Grade 12 STEM scholars.",
        "Demonstrated core chemistry experiments and molecular biology techniques to over 30 high-achieving scholars."
    ]
    story.append(make_job("Teaching Assistant & Demonstrator", "Targeting Talent Program, University of the Witwatersrand (Wits) — South Africa", "Jun 2015 — Jul 2015", j5_bullets))

    # --- EDUCATION ---
    story.extend(make_section("Education & Academic Qualifications"))

    def make_edu(degree, institution, dates, details=None):
        d_cell = Paragraph(f"<b>{degree}</b>", item_title_style)
        i_cell = Paragraph(institution, item_subtitle_style)
        dt_cell = Paragraph(dates, date_style)
        
        t = Table([[d_cell, dt_cell], [i_cell, ""]], colWidths=[5.45 * inch, 2.0 * inch])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('SPAN', (0,1), (1,1)),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        res = [t]
        if details:
            res.append(Paragraph(f"• <i>Research Focus:</i> {details}", bullet_style))
        res.append(Spacer(1, 3))
        return KeepTogether(res)

    story.append(make_edu("PhD in Biology (Cardiac Optogenetics)", "University of Freiburg — Freiburg, Germany", "Nov 2021 — Mar 2026", "Light-gated potassium channels and optical modulation of cardiac rhythm."))
    story.append(make_edu("MSc in Biology (Molecular, Cellular & Developmental Biology)", "Eötvös Loránd University (ELTE) — Budapest, Hungary", "Sep 2017 — Jul 2019", "Specialized in RecQ helicases and homologous recombination selection pathways."))
    story.append(make_edu("BHSc (Honours) in Forensic Sciences", "University of the Witwatersrand (Wits) — Johannesburg, South Africa", "Feb 2015 — Nov 2015", "Forensic toxicology, medico-legal pathology, and molecular diagnostics."))
    story.append(make_edu("BSc in Biological Sciences (Biochemistry, Cell Biology & Genetics)", "University of the Witwatersrand (Wits) — Johannesburg, South Africa", "Feb 2013 — Nov 2014", "Double major in Biochemistry & Cell Biology, and Genetics & Developmental Biology."))

    # --- TECHNICAL SKILLS ---
    story.extend(make_section("Technical Skills & Core Competencies"))

    skills_data = [
        [
            Paragraph("<b>AI & Automation:</b> LLM Orchestration, Agentic Workflows, Autonomous Voice Agents, API Design, Modern Tech Stack, Linux.", body_style),
            Paragraph("<b>Electrophysiology & Optics:</b> Single-Cell Patch-Clamp (Axopatch 200B, Digidata 1550A), Langendorff Perfusion, Optogenetics.", body_style)
        ],
        [
            Paragraph("<b>Data Science & Analytics:</b> Signal Processing, OriginPro 2024b, Clampfit, pClamp, IonOptix, Data Mining, Quantitative Modeling.", body_style),
            Paragraph("<b>Molecular & Cell Biology:</b> Adenoviral Vector Design, DNA/Protein Purification (MaxPrep), Cell Culture, EMSA, Anisotropy.", body_style)
        ],
        [
            Paragraph("<b>Forensic Pathology & Science:</b> Forensic Toxicology, Medico-Legal Database Review, Forensic Genetics.", body_style),
            Paragraph("<b>Leadership & Governance:</b> Research Mentorship, PhD Journal Club Lead, Student Council Secretary, FELASA B, S2 GLP.", body_style)
        ]
    ]

    skills_table = Table(skills_data, colWidths=[3.72 * inch, 3.72 * inch])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(KeepTogether([skills_table, Spacer(1, 4)]))

    # --- PUBLICATIONS ---
    story.extend(make_section("Publications & Academic Conferences"))

    pub1 = "<b>Spreen et al. (2025).</b> Optogenetic silencing by combining a rhodopsin cyclase with an engineered cGMP-gated potassium channel. <i>Science Advances</i>, 11(48)."
    pub2 = "<b>Ohnemus, Tillert, Leemisa et al. (2026).</b> Experimentally informed photocycle model of light-gated channel WiChR. <i>Biophysical Journal</i>, 1(17)."
    conf1 = "<b>NoTiCE International Symposium (2023):</b> Researcher & Poster Presenter — Glasgow, Scotland, UK."
    conf2 = "<b>SPP1926 Next Generation Optogenetics Conference (2023):</b> Co-Author & Presenter — Uslar, Germany."

    for p in [pub1, pub2, conf1, conf2]:
        story.append(Paragraph(f"• {p}", bullet_style))
    story.append(Spacer(1, 4))

    # --- CERTIFICATIONS ---
    story.extend(make_section("Certifications, Fellowships & Honors"))

    cert_data = [
        [
            Paragraph("<b>FELASA Category B &amp; S2 GLP Biosafety Certification</b><br/><font color='#64748B'>University of Cologne, Germany (2021/2022)</font>", body_style),
            Paragraph("<b>IEKM Doctoral Research Fellowship</b><br/><font color='#64748B'>University of Freiburg / IEKM (2021)</font>", body_style)
        ],
        [
            Paragraph("<b>Good Scientific Practice &amp; Advanced Biostatistics</b><br/><font color='#64748B'>Spemann Graduate School of Biology &amp; Medicine (2022)</font>", body_style),
            Paragraph("<b>Stipendium Hungaricum Master's Scholarship</b><br/><font color='#64748B'>Hungarian Government &amp; ELTE (2017)</font>", body_style)
        ],
        [
            Paragraph("<b>Mental Health in Academia Credential</b><br/><font color='#64748B'>Spemann Graduate School of Biology &amp; Medicine (2023)</font>", body_style),
            Paragraph("<b>NRF Honours Funding &amp; Wits Entrance Scholarship</b><br/><font color='#64748B'>National Research Foundation &amp; Wits Univ. (2013/2015)</font>", body_style)
        ]
    ]

    cert_table = Table(cert_data, colWidths=[3.72 * inch, 3.72 * inch])
    cert_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(KeepTogether([cert_table, Spacer(1, 4)]))

    # --- REFERENCES ---
    story.extend(make_section("Professional References"))

    ref_data = [
        [
            Paragraph("<b>Dr. Franziska Schneider-Warme</b><br/>Optogenetics Group Leader / PhD Supervisor<br/>IEKM, University of Freiburg, Germany<br/><font color='#2563EB'>franziska.schneider.uhz@uniklinik-freiburg.de</font>", body_style),
            Paragraph("<b>Prof. Dr. Med. Peter Kohl</b><br/>Director &amp; PhD Co-Supervisor<br/>IEKM, University Heart Center Freiburg, Germany<br/><font color='#2563EB'>peter.kohl@uniklinik-freiburg.de</font>", body_style)
        ],
        [
            Paragraph("<b>Dr. Gábor Harami</b><br/>MSc Thesis Supervisor<br/>Eötvös Loránd University (ELTE), Hungary<br/><font color='#2563EB'>gabor.harami@gmail.com</font>", body_style),
            Paragraph("<b>Mrs. Ildi Wainer</b><br/>BHSc Honours Supervisor<br/>University of the Witwatersrand, South Africa<br/><font color='#2563EB'>ildi.wainer@wits.ac.za</font>", body_style)
        ]
    ]

    ref_table = Table(ref_data, colWidths=[3.72 * inch, 3.72 * inch])
    ref_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(KeepTogether([ref_table]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully: {filename}")

if __name__ == "__main__":
    out_dir = "/home/andries/snap/antigravity/5/.gemini/antigravity/scratch/dr_andries_cv"
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, "Dr_Andries_Napo_Leemisa_CV.pdf")
    build_pdf(pdf_path)
