"""Script to generate the comprehensive 'guide.docx' Word document for MasteryFlow.
Includes complete system explanation and a word-for-word human-language jury presentation script.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_guide_document():
    doc = docx.Document()

    # Set page margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

    # Styling helper functions
    def set_cell_background(cell, hex_color):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for margin, value in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{margin}')
            node.set(qn('w:w'), str(value))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def add_callout(doc, text, title="KEY TAKEAWAY", bg_color="F0F9FF", border_color="0284C7"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        
        # Left border only
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r_title = p.add_run(f" {title}: ")
        r_title.bold = True
        r_title.font.name = "Calibri"
        r_title.font.size = Pt(10.5)
        r_title.font.color.rgb = RGBColor(2, 132, 199)
        
        r_text = p.add_run(text)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = RGBColor(51, 65, 85)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # DOCUMENT HEADER / TITLE
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = title_p.add_run(" MASTERYFLOW")
    r_title.font.name = "Arial Black"
    r_title.font.size = Pt(24)
    r_title.font.color.rgb = RGBColor(14, 116, 144)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(14)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = sub_p.add_run("Complete Platform Architecture Guide & Non-Technical Jury Presentation Script\n"
                          "Domain 4: Intelligent Educational Systems | YUVA Megathon 2026")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_heading("PART 1: THE TEAM MASTER GUIDE (What Is Going On?)", level=1)
    
    p = doc.add_paragraph()
    p.add_run("MasteryFlow is not a typical online quiz app or simple video library. It is an ").font.size = Pt(10.5)
    r_b = p.add_run("Adaptive Cognitive Decision Engine for Mathematics")
    r_b.bold = True
    r_b.font.size = Pt(10.5)
    p.add_run(" (covering Fractions, Decimals, and Ratios across 10 structured concepts). It decides what problem a student should solve next, when to stop them if they are guessing, and when to send them back to fix missing prerequisites.").font.size = Pt(10.5)

    add_callout(
        doc,
        "Most digital learning platforms know what a student clicked, but NOT whether they truly mastered it. "
        "MasteryFlow maintains a probabilistic model of student understanding, respects prerequisite hierarchies, and guarantees 100% explainable actions with zero AI hallucinations.",
        "THE ONE-LINE ELEVATOR PITCH"
    )

    doc.add_heading("1.1 The Core Brain: How The Engine Works (Simple English)", level=2)
    
    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Engine Component"
    hdr_cells[1].text = "How It Works (Non-Tech Explanation)"
    hdr_cells[2].text = "Why It Matters"
    
    for c in hdr_cells:
        set_cell_background(c, "0F172A")
        set_cell_margins(c, top=120, bottom=120, left=120, right=120)
        for p in c.paragraphs:
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.bold = True
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(255, 255, 255)

    engine_data = [
        ("Bayesian Knowledge Tracing (BKT)", 
         "Instead of giving a fixed score like 8/10, the engine treats mastery as a probability (e.g., 85% sure you know this). Every correct or incorrect answer nudges this probability up or down based on problem difficulty.",
         "Accounts for lucky guesses and accidental slips so one wrong answer does not ruin a student's record."),
        
        ("Evidence Weighting & Anti-Gaming", 
         "The engine measures how fast a student answers, how many hints they took, and their confidence. If someone rapidly clicks in 1 second, the evidence weight drops to 0.00.",
         "Completely stops students from brute-force guessing or gaming the platform."),
        
        ("Prerequisite DAG Invariant Capping", 
         "Math is sequential. If a student is failing Concept 2 (Equivalent Fractions), the engine mathematically caps their ability to advance to Concept 4 (Adding Unlike Fractions).",
         "Prevents students from getting frustrated by jumping into hard problems before mastering fundamentals."),
        
        ("Ebbinghaus Memory Decay", 
         "Human brains forget over time. If a student mastered a concept but doesn't practice for 21 days, their retention drops. The engine schedules a quick 'Spaced Review'.",
         "Ensures long-term retention without forcing the student to re-do the entire curriculum from zero."),
        
        ("Maximum Uncertainty Cold-Start", 
         "New students take a 6-question diagnostic. The engine picks questions from central hub concepts to find their knowledge boundaries in just 6 clicks.",
         "No new student has to start from beginner Level 1 if they already know the basics."),
        
        ("Glass-Box Explainability ('Why This Next?')", 
         "Every time a problem appears, the system outputs a transparent badge explaining which pedagogical rule triggered it.",
         "Zero black-box confusion. Students and teachers always know why a decision was made.")
    ]

    for row_idx, (comp, expl, why) in enumerate(engine_data):
        row = table.add_row()
        bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
        for i, text in enumerate([comp, expl, why]):
            cell = row.cells[i]
            cell.text = text
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # 1.2 PLATFORM INTERFACES (4 HUBS)
    # -------------------------------------------------------------
    doc.add_heading("1.2 Tour of the 4 Main Platform Hubs", level=2)

    hubs = [
        (" 1. Learn (The Adaptive Practice Hub)",
         "This is where students spend their time. It has 4 tabs:\n"
         "• Tab 1 (Adaptive Learning Loop): Features the Glass-Box 'Why This Next?' card, self-agency requests, live math problem player with quick fraction chips (1/2, 3/4), hints, and confidence cards.\n"
         "• Tab 2 (Concept Knowledge Tree): Switch between 3D WebGL Galaxy and 2D Skill Constellation.\n"
         "• Tab 3 (6-Question Cold-Start Diagnostic): Rapid initial assessment engine.\n"
         "• Tab 4 (Psychometric Diagnostics): Live mathematical breakdown of BKT probabilities."),
        
        (" 2. Dashboard (Student Progress & 3D Universe)",
         "A high-level cockpit for the student:\n"
         "• Top KPIs: Global Mastery Percentage, Concepts Mastered count (X/10), and Day Streak.\n"
         "• 3D Interactive Galaxy: 360° rotatable WebGL universe.\n"
         "• Concept Overview Grid: 10 progress cards showing stability in days and mastery status."),
        
        ("‍ 3. Teach (Teacher Command Center)",
         "Designed for school educators and mentors:\n"
         "• Cohort Heatmap: Matrix of all students vs all 10 concepts color-coded by mastery.\n"
         "• Bottleneck Alerts: Automatically flags concepts where >40% of the class is stuck.\n"
         "• Stuck-Learner Escalation Queue: Identifies learners failing 3+ times in a row.\n"
         "• 1-Click Human Override Console: Teacher can redirect any student with SQLite audit logging."),
        
        (" 4. Explore (Curriculum Directory & Prerequisite Graph)",
         "A transparent pedagogical map showing all 10 math concepts (C1–C10), exact prerequisite dependencies, descriptions, and mastery progress.")
    ]

    for title, desc in hubs:
        h_p = doc.add_paragraph()
        h_p.paragraph_format.space_before = Pt(6)
        h_p.paragraph_format.space_after = Pt(2)
        r = h_p.add_run(title)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(14, 116, 144)

        d_p = doc.add_paragraph()
        d_p.paragraph_format.space_before = Pt(0)
        d_p.paragraph_format.space_after = Pt(4)
        r_d = d_p.add_run(desc)
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(10)
        r_d.font.color.rgb = RGBColor(51, 65, 85)

    # -------------------------------------------------------------
    # 1.3 THE 8 LEARNER PROFILES (Pre-Seeded Cognitive Archetypes)
    # -------------------------------------------------------------
    doc.add_heading("1.3 The 8 Pre-Seeded Learner Profiles (Visual Stats & Behavior)", level=2)
    p_prof = doc.add_paragraph()
    p_prof.add_run("MasteryFlow comes pre-loaded with 8 distinct learner profiles covering every cognitive scenario. Switching profiles in the sidebar immediately changes the 3D galaxy node colors, active concept target, progress bars, and pedagogical decisions:").font.size = Pt(10)

    tbl_prof = doc.add_table(rows=1, cols=4)
    tbl_prof.alignment = WD_TABLE_ALIGNMENT.CENTER
    p_hdr = tbl_prof.rows[0].cells
    p_hdr[0].text = "Learner Profile"
    p_hdr[1].text = "Active Focus"
    p_hdr[2].text = "Cognitive State & Stats"
    p_hdr[3].text = "3D Galaxy & Bar Visuals"

    for c in p_hdr:
        set_cell_background(c, "0F172A")
        set_cell_margins(c, top=100, bottom=100, left=100, right=100)
        for p in c.paragraphs:
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.bold = True
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(255, 255, 255)

    profile_rows = [
        (" Priya Singh (STU_001)", "C8: Proportions", "Top Performer: C1-C7 mastered (86-96%), practicing C8 (65%), C9 provisional (40%). Streak: 9d.", "Majority emerald glowing spheres, active corona on C8, 7/10 concepts mastered."),
        (" Diya Sharma (STU_042)", "C7: Ratios & Rates", "Prerequisite Gap: C1 mastered (88%), C2 broken (35% fragile), C7 fragile cap (40%). Streak: 4d.", "Bright red fragile glow on C2 & C7, green on C1, engine forces repair to C2."),
        (" Aarav Patel (STU_002)", "C2: Equivalent Fractions", "Stuck Plateau: C1 mastered (86%), stuck on C2 (40%) across 4 cycles. Streak: 0d.", "C1 green, C2 cyan with intervention flag on Teacher Escalation Queue."),
        (" Kabir Verma (STU_004)", "C1: Fraction Basics", "Memory Decay: C1 (38%) & C2 (42%) decayed after 21 days inactive. Streak: 0d.", "Amber/provisional spheres on C1 & C2, Rule 3 triggers Spaced Review."),
        (" Ananya Roy (STU_005)", "C5: Multiplying Fractions", "Mid-Level Achiever: C1-C4 mastered (86-92%), practicing C5 (65%). Streak: 6d.", "Solid green on foundation (C1-C4), bright cyan on C5, 4/10 mastered."),
        (" Meera Nair (STU_008)", "C9: Rates & Conversion", "Capstone Advanced: C1-C8 mastered (90-98%), active on C9 (75%) & C10 (60%). Streak: 14d.", "Almost entirely green galaxy with active pulses reaching top apex nodes."),
        (" Rohan Mehta (STU_006)", "C1: Fraction Basics", "Adversarial Guesser: C1 at 30%, rapid retry spam penalized to w=0.00. Streak: 0d.", "Low progress bars, telemetry shows latency warning & zero evidence weight."),
        (" Ishaan Gupta (STU_007)", "C1: Fraction Basics", "Novice Cold-Start: Fresh learner starting C1 at 25%, all others unseen (20%). Streak: 1d.", "Mostly dark gray unseen nodes, ready for 6-Question Cold-Start Diagnostic.")
    ]

    for r_idx, (p_name, p_focus, p_state, p_vis) in enumerate(profile_rows):
        r_cells = tbl_prof.add_row().cells
        bg_c = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for i, val in enumerate([p_name, p_focus, p_state, p_vis]):
            cell = r_cells[i]
            cell.text = val
            set_cell_background(cell, bg_c)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    doc.add_page_break()

    # -------------------------------------------------------------
    # PART 2: HUMAN-LANGUAGE JURY PRESENTATION SCRIPT
    # -------------------------------------------------------------
    doc.add_heading("PART 2: WORD-FOR-WORD JURY PRESENTATION SCRIPT", level=1)
    
    p_script_intro = doc.add_paragraph()
    p_script_intro.add_run("Use this exact script during your hackathon presentation. It is written in simple, confident, non-technical language that anyone can follow. Follow the visual actions step by step.").font.size = Pt(10)

    scenes = [
        (" PHASE 1: The Opening Hook (0:00 - 0:30)",
         "Open browser at http://localhost:8501 on the ' Learn' portal.",
         "\"Respected judges, most digital learning platforms today are simply video libraries with progress bars. They know that a student clicked 'Play', but they have no idea if the student actually understood the concept.\n\n"
         "We built MasteryFlow — an Explainable Adaptive Learning Engine for Mathematics. Instead of treating every student the same, our system builds a live model of each learner's brain, prevents guessing, respects prerequisite foundations, and explains every single recommendation with 100% transparency.\""),

        (" PHASE 2: Student Adaptive Loop & Glass-Box HUD (0:30 - 1:15)",
         "In ' Learn' portal, point to the 'Why This Next?' card, then interact with the question runner.",
         "\"Let's look at the student experience. Right here on the screen, we see Diya Sharma. Before she even touches a question, notice this Glass-Box card: 'Why This Next?'. It tells her in plain English: 'You are practicing Concept 1 because your mastery is at 20%.' Zero confusion, zero black-box AI.\n\n"
         "Now watch what happens when she interacts. We give her 1-click math chips, progressive hints, and a confidence meter. If a student tries to randomly spam answers in 1 second, our Anti-Gaming Guard immediately detects rapid guessing and drops the evidence weight to zero — neutralizing any attempts to game the system.\""),

        (" PHASE 3: 3D Holographic Knowledge Universe (1:15 - 1:55)",
         "Click on ' Dashboard' or ' Explore'. Left-click and rotate the 3D galaxy 360°, zoom in with scroll wheel, and click on a node.",
         "\"Now, let's explore how the student visualizes their curriculum. This is our 3D Holographic Knowledge Universe, running on hardware-accelerated WebGL at 60 frames per second.\n\n"
         "Each glowing sphere is a mathematics concept. These animated laser beams flowing between them represent prerequisite mastery. When I rotate 360 degrees or click on any node, it brings up real-time telemetry: showing effective mastery, memory stability in days, and prerequisite status. Learning feels like exploring a tech tree in a video game.\""),

        (" PHASE 4: Teacher Command Center & Human Override (1:55 - 2:35)",
         "Click on '‍ Teach' in the sidebar. Scroll through the Cohort Heatmap and Stuck-Learner Queue.",
         "\"Adaptive learning cannot succeed without teachers. This is the Teacher Command Center. Educators get an institutional heatmap of the entire class across all 10 concepts.\n\n"
         "If 40% of the class stumbles on the same concept, our engine automatically fires a Systemic Bottleneck Alert. If a student fails 3 times in a row, they are escalated to the Stuck-Learner Queue.\n\n"
         "And most importantly: the teacher is always in control. With our 1-Click Override Console, a teacher can manually redirect any student to a new concept, and it is instantly saved to an immutable SQLite audit log without destroying learning history.\""),

        (" PHASE 5: The 6-Step Proof & Edge Case Stress-Tests (2:35 - 3:00)",
         "Open sidebar 'Developer & Demo Tools' -> Click ' 6-Step Demo Tour' (Step 1 or Step 5).",
         "\"Finally, to prove mathematical integrity to the jury: here is our Divergent Paths proof. Two students with the exact same recent score of 80% receive completely different actions because their foundational prerequisite history is different — Priya advances forward while Diya is guided to remediate her foundation.\n\n"
         "MasteryFlow runs on pure deterministic Python, with zero LLM hallucinations in the decision loop, a live REST API, and 100% mathematical reproducibility. Thank you!\"")
    ]

    for title, action, speech in scenes:
        doc.add_heading(title, level=2)
        
        # Action Box
        tbl_act = doc.add_table(rows=1, cols=1)
        tbl_act.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_act = tbl_act.cell(0, 0)
        set_cell_background(c_act, "F1F5F9")
        set_cell_margins(c_act, top=80, bottom=80, left=140, right=140)
        p_act = c_act.paragraphs[0]
        r_act_lbl = p_act.add_run(" WHAT TO DO ON SCREEN: ")
        r_act_lbl.bold = True
        r_act_lbl.font.size = Pt(9.5)
        r_act_lbl.font.color.rgb = RGBColor(71, 85, 105)
        r_act_txt = p_act.add_run(action)
        r_act_txt.font.size = Pt(9.5)
        r_act_txt.font.color.rgb = RGBColor(15, 23, 42)

        # Speech Box
        tbl_spk = doc.add_table(rows=1, cols=1)
        tbl_spk.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_spk = tbl_spk.cell(0, 0)
        set_cell_background(c_spk, "ECFDF5")
        set_cell_margins(c_spk, top=120, bottom=120, left=160, right=160)
        
        tcPr = c_spk._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="059669"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)

        p_spk = c_spk.paragraphs[0]
        r_spk_lbl = p_spk.add_run(" WHAT TO SAY (EXACT SCRIPT):\n")
        r_spk_lbl.bold = True
        r_spk_lbl.font.size = Pt(10)
        r_spk_lbl.font.color.rgb = RGBColor(5, 150, 105)
        
        r_spk_txt = p_spk.add_run(speech)
        r_spk_txt.font.size = Pt(9.5)
        r_spk_txt.font.color.rgb = RGBColor(6, 78, 59)

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    doc.add_page_break()

    # -------------------------------------------------------------
    # PART 3: FAQ & JURY TRICK QUESTIONS
    # -------------------------------------------------------------
    doc.add_heading("PART 3: HOW TO ANSWER TOUGH JURY QUESTIONS", level=1)

    faqs = [
        ("Judge asks: 'Is an LLM making these decisions?'",
         "Answer: 'No, and that is our strongest feature. LLMs hallucinate and have seed variance. Our decision engine is pure deterministic Python using Bayesian Knowledge Tracing and Graph Theory. It gives 100% reproducible decisions with zero variance.'"),

        ("Judge asks: 'What happens if a student just clicks random answers really fast?'",
         "Answer: 'Our Multi-Signal Evidence Model monitors latency. Any attempt answered in under 3 seconds is flagged as rapid guessing, and its evidence weight is clamped to w = 0.00. The student gets no mastery credit.'"),

        ("Judge asks: 'How do you handle forgetting over summer vacation?'",
         "Answer: 'We model the Ebbinghaus Forgetting Curve: R(t) = exp(-t/S). If a student has been away for 21 days, their effective mastery decays past our threshold, automatically triggering Rule 3: Spaced Retrieval Review.'"),

        ("Judge asks: 'Can a teacher disagree with the AI?'",
         "Answer: 'Yes, absolutely. Our Teacher Command Center provides a 1-Click Human Override. The teacher's decision immediately supersedes the algorithm and is logged immutably to SQLite.'")
    ]

    for q, a in faqs:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(6)
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run(f" {q}")
        r_q.bold = True
        r_q.font.name = "Calibri"
        r_q.font.size = Pt(10.5)
        r_q.font.color.rgb = RGBColor(180, 83, 9)

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_before = Pt(0)
        p_a.paragraph_format.space_after = Pt(6)
        r_a = p_a.add_run(f" {a}")
        r_a.font.name = "Calibri"
        r_a.font.size = Pt(10)
        r_a.font.color.rgb = RGBColor(30, 41, 59)

    saved = False
    for fname in ["MasteryFlow_Complete_Guide.docx", "guide.docx", "guide_updated.docx"]:
        try:
            doc.save(fname)
            print(f"Successfully generated '{fname}'!")
            saved = True
            if fname == "guide.docx":
                break
        except PermissionError:
            print(f"Note: '{fname}' is currently open in Word. Saved to alternative name.")

    if not saved:
        doc.save("guide_new.docx")
        print("Successfully generated 'guide_new.docx'!")

if __name__ == "__main__":
    create_guide_document()
