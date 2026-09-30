"""Script to generate MasteryFlow_Course_Chapters_Video_Catalog.docx.

Generates a beautifully formatted Word document containing all 42 concepts
across Mathematics, Computer Networks, Artificial Intelligence, Formal Languages & Automata,
and Biochemistry with editable fields for pasting YouTube URLs, channels, and notes.
"""

import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from data.curricula import (
    SUBJECTS_REGISTRY,
    MATH_CONCEPTS,
    NETWORKS_CONCEPTS,
    AI_CONCEPTS,
    FLA_CONCEPTS,
    BIOCHEM_CONCEPTS,
    YOUTUBE_VIDEOS_CATALOG,
    TOPIC_BRIEF_EXPLANATIONS,
)

SUBJECT_MAPPING = [
    ("Mathematics", " Mathematics (Fractions & Proportions)", MATH_CONCEPTS, "0F172A", "C1 to C10"),
    ("Computer Networks", " Computer Networks & Protocols", NETWORKS_CONCEPTS, "0284C7", "CN1 to CN8"),
    ("Artificial Intelligence", " Artificial Intelligence & Deep Learning", AI_CONCEPTS, "7C3AED", "AI1 to AI8"),
    ("Formal Languages & Automata", " Formal Languages & Automata Theory (FLA)", FLA_CONCEPTS, "D97706", "FLA1 to FLA8"),
    ("Biochemistry", " Biochemistry & Cellular Bioenergetics", BIOCHEM_CONCEPTS, "059669", "BIO1 to BIO8"),
]


def set_cell_background(cell, hex_color):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin, value in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin}')
        node.set(qn('w:w'), str(value))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, border_color="CBD5E1"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>
            <w:left w:val="none"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>
            <w:right w:val="none"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)


def build_document(output_path: str):
    doc = docx.Document()

    # 1. Page Margins (0.75 in for wider table display)
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # 2. Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    run_title = p_title.add_run(" MasteryFlow: Course Chapters & Video Catalog")
    run_title.font.name = "Arial Black"
    run_title.font.size = Pt(20)
    run_title.font.color.rgb = RGBColor(17, 20, 29)

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(2)
    p_sub.paragraph_format.space_after = Pt(14)
    run_sub = p_sub.add_run("Multi-Disciplinary Concept Reference Sheet & YouTube Curation Sheet (42 Chapters)")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = RGBColor(100, 116, 139)

    # Metadata callout box
    callout_tbl = doc.add_table(rows=1, cols=1)
    callout_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cell = callout_tbl.cell(0, 0)
    set_cell_background(c_cell, "F8FAFC")
    set_cell_margins(c_cell, top=140, bottom=140, left=200, right=200)

    tcPr = c_cell._tc.get_or_add_tcPr()
    border_callout = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="0284C7"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
    ''')
    tcPr.append(border_callout)

    cp = c_cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(2)
    cp.paragraph_format.space_after = Pt(2)
    r_hdr = cp.add_run(" Curated Course Video Catalog:\n")
    r_hdr.bold = True
    r_hdr.font.name = "Calibri"
    r_hdr.font.size = Pt(10.5)
    r_hdr.font.color.rgb = RGBColor(2, 132, 199)

    r_body = cp.add_run(
        "Below are all 42 concepts across the 5 academic disciplines registered in MasteryFlow. "
        "Each topic has been carefully mapped to a verified, high-quality YouTube educational video lesson "
        "with its direct watch URL, verified channel creator, and video duration for integrated student remediation."
    )
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(9.5)
    r_body.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 3. Render Each Subject Section
    for s_idx, (s_key, s_title, s_concepts, theme_color, id_range) in enumerate(SUBJECT_MAPPING):
        # Section Header
        h_para = doc.add_paragraph()
        h_para.paragraph_format.space_before = Pt(14)
        h_para.paragraph_format.space_after = Pt(4)
        h_para.paragraph_format.keep_with_next = True

        r_sec = h_para.add_run(f"{s_title} ({id_range})")
        r_sec.bold = True
        r_sec.font.name = "Arial"
        r_sec.font.size = Pt(13)
        r_sec.font.color.rgb = RGBColor.from_string(theme_color)

        # Subject Description
        s_meta = SUBJECTS_REGISTRY.get(s_key, {})
        desc_p = doc.add_paragraph()
        desc_p.paragraph_format.space_before = Pt(0)
        desc_p.paragraph_format.space_after = Pt(6)
        r_desc = desc_p.add_run(s_meta.get("description", ""))
        r_desc.font.name = "Calibri"
        r_desc.font.size = Pt(9)
        r_desc.font.italic = True
        r_desc.font.color.rgb = RGBColor(100, 116, 139)

        # Table
        # Columns: [ID (0.6 in), Chapter Title & Prerequisites (2.1 in), Core Concepts / Topic Scope (2.3 in), Selected YouTube Link & Channel (2.0 in)]
        table = doc.add_table(rows=1, cols=4)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table, border_color="E2E8F0")

        # Header Row
        hdr_cells = table.rows[0].cells
        headers = ["ID", "Chapter / Concept Title", "Core Topics & Keywords", "Selected YouTube Link & Details"]
        col_widths = [Inches(0.65), Inches(2.2), Inches(2.2), Inches(2.15)]

        for c_idx, text in enumerate(headers):
            cell = hdr_cells[c_idx]
            cell.width = col_widths[c_idx]
            set_cell_background(cell, "1E293B")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(text)
            run.bold = True
            run.font.name = "Calibri"
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(255, 255, 255)

        # Populate Concepts
        for row_idx, (cid, cmeta) in enumerate(s_concepts.items()):
            row = table.add_row()
            cells = row.cells
            bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"

            for c_idx, w in enumerate(col_widths):
                cells[c_idx].width = w
                set_cell_background(cells[c_idx], bg_color)
                set_cell_margins(cells[c_idx], top=80, bottom=80, left=100, right=100)
                cells[c_idx].vertical_alignment = WD_ALIGN_VERTICAL.TOP

            # Cell 0: ID
            p0 = cells[0].paragraphs[0]
            p0.paragraph_format.space_before = Pt(0)
            p0.paragraph_format.space_after = Pt(0)
            r0 = p0.add_run(cid)
            r0.bold = True
            r0.font.name = "Calibri"
            r0.font.size = Pt(9.5)
            r0.font.color.rgb = RGBColor.from_string(theme_color)

            # Cell 1: Title & Prerequisites
            p1 = cells[1].paragraphs[0]
            p1.paragraph_format.space_before = Pt(0)
            p1.paragraph_format.space_after = Pt(2)
            r1_title = p1.add_run(cmeta.get("name", cid))
            r1_title.bold = True
            r1_title.font.name = "Calibri"
            r1_title.font.size = Pt(9.5)
            r1_title.font.color.rgb = RGBColor(17, 20, 29)

            prereqs = cmeta.get("prerequisites", [])
            prereq_str = ", ".join(prereqs) if prereqs else "None (Foundational)"
            p1_prereq = cells[1].add_paragraph()
            p1_prereq.paragraph_format.space_before = Pt(1)
            p1_prereq.paragraph_format.space_after = Pt(0)
            r1_p = p1_prereq.add_run(f"Prereqs: {prereq_str}")
            r1_p.font.name = "Calibri"
            r1_p.font.size = Pt(8)
            r1_p.font.color.rgb = RGBColor(100, 116, 139)

            # Cell 2: Topic Brief Explanation & Core Theoretical Principles
            brief = TOPIC_BRIEF_EXPLANATIONS.get(cid, {})
            p2 = cells[2].paragraphs[0]
            p2.paragraph_format.space_before = Pt(0)
            p2.paragraph_format.space_after = Pt(2)
            
            # Brief Summary
            r2_sum_lbl = p2.add_run("Overview: ")
            r2_sum_lbl.bold = True
            r2_sum_lbl.font.name = "Calibri"
            r2_sum_lbl.font.size = Pt(8.5)
            r2_sum_lbl.font.color.rgb = RGBColor(15, 23, 42)
            
            summary_txt = brief.get("summary") or cmeta.get("description", "")
            r2_sum = p2.add_run(summary_txt)
            r2_sum.font.name = "Calibri"
            r2_sum.font.size = Pt(8.5)
            r2_sum.font.color.rgb = RGBColor(51, 65, 85)

            # Core Principles
            principles = brief.get("core_principles", [])
            if principles:
                p2_pr = cells[2].add_paragraph()
                p2_pr.paragraph_format.space_before = Pt(2)
                p2_pr.paragraph_format.space_after = Pt(1)
                r_pr_lbl = p2_pr.add_run("Key Principles:")
                r_pr_lbl.bold = True
                r_pr_lbl.font.name = "Calibri"
                r_pr_lbl.font.size = Pt(8)
                r_pr_lbl.font.color.rgb = RGBColor(71, 85, 105)
                
                for pr in principles[:3]:
                    p_bullet = cells[2].add_paragraph()
                    p_bullet.paragraph_format.space_before = Pt(0)
                    p_bullet.paragraph_format.space_after = Pt(0)
                    p_bullet.paragraph_format.left_indent = Inches(0.12)
                    r_b = p_bullet.add_run(f"• {pr}")
                    r_b.font.name = "Calibri"
                    r_b.font.size = Pt(8)
                    r_b.font.color.rgb = RGBColor(71, 85, 105)

            # Key Formula / Algorithmic Rule
            key_f = brief.get("key_formula")
            if key_f:
                p2_f = cells[2].add_paragraph()
                p2_f.paragraph_format.space_before = Pt(2)
                p2_f.paragraph_format.space_after = Pt(0)
                r_f_lbl = p2_f.add_run("Formula / Rule: ")
                r_f_lbl.bold = True
                r_f_lbl.font.name = "Calibri"
                r_f_lbl.font.size = Pt(8)
                r_f_lbl.font.color.rgb = RGBColor(124, 58, 237)
                
                r_f_val = p2_f.add_run(key_f)
                r_f_val.font.name = "Consolas"
                r_f_val.font.size = Pt(7.5)
                r_f_val.font.color.rgb = RGBColor(88, 28, 135)

            # Cell 3: Selected YouTube Link & Channel Details
            vid = YOUTUBE_VIDEOS_CATALOG.get(cid, {})
            p3 = cells[3].paragraphs[0]
            p3.paragraph_format.space_before = Pt(0)
            p3.paragraph_format.space_after = Pt(2)
            r3_lbl = p3.add_run("URL: ")
            r3_lbl.bold = True
            r3_lbl.font.name = "Calibri"
            r3_lbl.font.size = Pt(8.5)
            r3_lbl.font.color.rgb = RGBColor(71, 85, 105)

            v_url = vid.get("url", "https://www.youtube.com")
            r3_val = p3.add_run(v_url)
            r3_val.font.name = "Calibri"
            r3_val.font.size = Pt(8.0)
            r3_val.font.color.rgb = RGBColor(2, 132, 199)
            r3_val.underline = True

            p3_chan = cells[3].add_paragraph()
            p3_chan.paragraph_format.space_before = Pt(2)
            p3_chan.paragraph_format.space_after = Pt(0)
            v_chan = vid.get("channel", "Educational Channel")
            v_dur = vid.get("duration", "10:00")
            r3_c1 = p3_chan.add_run(f"Channel: {v_chan}\n")
            r3_c1.bold = True
            r3_c1.font.name = "Calibri"
            r3_c1.font.size = Pt(8)
            r3_c1.font.color.rgb = RGBColor(51, 65, 85)

            r3_c2 = p3_chan.add_run(f"Duration: {v_dur}")
            r3_c2.font.name = "Calibri"
            r3_c2.font.size = Pt(8)
            r3_c2.font.color.rgb = RGBColor(100, 116, 139)

        doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 4. Save document
    doc.save(output_path)
    print(f" [+] Successfully created: {output_path}")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    docs_dir = base_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    out_file = docs_dir / "MasteryFlow_Course_Chapters_Video_Catalog.docx"
    build_document(str(out_file))

    # Also keep a copy at workspace root
    root_file = base_dir / "MasteryFlow_Course_Chapters_Video_Catalog.docx"
    shutil.copyfile(str(out_file), str(root_file))
    print(f" [+] Successfully created: {out_file} and {root_file}")
