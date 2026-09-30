"""Script to generate the comprehensive, human-language 'ml_question_bank.docx' Word document.
Covers every single Machine Learning, Knowledge Tracing, Psychometrics, and Decision Engine
question a jury can ask, answered in simple, plain English with real-life analogies.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_ml_qa_doc():
    doc = docx.Document()

    # Page Margins (0.8 in)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

    def set_cell_background(cell, hex_color):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_cell_margins(cell, top=100, bottom=100, left=130, right=130):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for margin, value in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{margin}')
            node.set(qn('w:w'), str(value))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def add_callout(doc, text, title="PLAIN-ENGLISH CHEAT SHEET", bg_color="F0FDF4", border_color="16A34A"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
        
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
        r_title.font.color.rgb = RGBColor(22, 101, 52)
        
        r_text = p.add_run(text)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = RGBColor(30, 41, 59)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # DOCUMENT TITLE
    # -------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run(" MASTERYFLOW — ML JURY Q&A MASTER BANK")
    r_t.font.name = "Arial Black"
    r_t.font.size = Pt(21)
    r_t.font.color.rgb = RGBColor(14, 116, 144)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s = p_sub.add_run("Everything You Need to Know About the Machine Learning & Decision Engine\n"
                        "Written in Simple Everyday Language for Non-Technical & Technical Evaluators")
    r_s.font.name = "Calibri"
    r_s.font.size = Pt(11)
    r_s.font.italic = True
    r_s.font.color.rgb = RGBColor(100, 116, 139)

    add_callout(
        doc,
        "If a judge asks what you did in Machine Learning: 'We built an Explainable Cognitive Modeling Engine. "
        "It uses Bayesian Knowledge Tracing to track how confident we are in a student's skills, an Anti-Gaming model "
        "to stop guessing, an Ebbinghaus memory curve to handle forgetting, and Graph Theory to prevent skipping prerequisite basics.'",
        "THE 20-SECOND ML ELEVATOR PITCH"
    )

    # =============================================================
    # CATEGORY 1: THE CORE ML MODEL (BAYESIAN KNOWLEDGE TRACING)
    # =============================================================
    doc.add_heading("CATEGORY 1: THE CORE ML MODEL (How We Track What a Student Knows)", level=1)

    cat1_qa = [
        ("Q1: What Machine Learning model did you use, and what is its name?",
         "Simple Answer:",
         "We used **Bayesian Knowledge Tracing (BKT)**, which is a special type of Hidden Markov Model designed specifically for education.\n\n"
         "• **Why it's used**: When a student answers a question, we can't look inside their physical brain. Their true knowledge is 'hidden'. BKT watches their answers over time and updates a probability score between 0% and 100% representing how confident we are that they have mastered the skill.\n"
         "• **Real-Life Analogy**: Think of a driving instructor. If you parallel park once, they don't give you a license immediately. They watch you park a few times under different conditions until they are 95% sure you can drive safely."),

        ("Q2: How does your BKT model calculate a student's score in simple terms?",
         "Simple Answer:",
         "BKT uses 4 simple real-world factors every time an answer is submitted:\n\n"
         "1. **Prior (What we already knew)**: What was the student's score before this question? (e.g., 50%).\n"
         "2. **Slip (Accidental Mistake)**: Even good students make typos or calculation slips (we set this to 10%). So 1 wrong answer doesn't drop a good student to zero.\n"
         "3. **Guess (Lucky Guess)**: Weak students sometimes guess the right answer by luck (we set this to 20%). So 1 lucky guess doesn't trick the computer into thinking they're a genius.\n"
         "4. **Learn Rate (Transition)**: Every time a student practices, there is a natural chance that learning happens (we set this to 15%).\n\n"
         "Combining these, the math updates the score cleanly: a hard question answered correctly gives a big boost; an easy question answered with 3 hints gives almost no boost."),

        ("Q3: Why did you choose BKT instead of Deep Learning (like Deep Knowledge Tracing / LSTM / Transformers)?",
         "Simple Answer:",
         "Three huge reasons:\n\n"
         "1. **100% Explainable ('No Black Box')**: Deep neural networks cannot explain *why* they gave a score. BKT is a mathematical formula, so we can literally show the student and teacher the exact step-by-step reason on the screen.\n"
         "2. **Zero Training Delay & Works on Day 1**: Deep Learning needs millions of historical student clicks to train. BKT works instantly on the very first student from second one.\n"
         "3. **Super Fast Execution (<5 Milliseconds)**: Deep Learning takes heavy GPU power and 500ms+ latency. Our BKT engine runs locally in under 5 milliseconds on any regular laptop or mobile phone.")
    ]

    for q, a_lbl, a_txt in cat1_qa:
        doc.add_heading(q, level=2)
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        r_lbl = p.add_run(f"{a_lbl} ")
        r_lbl.bold = True
        r_lbl.font.size = Pt(9.5)
        r_lbl.font.color.rgb = RGBColor(14, 116, 144)
        r_txt = p.add_run(a_txt)
        r_txt.font.size = Pt(9.5)
        r_txt.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # =============================================================
    # CATEGORY 2: ANTI-GAMING & MULTI-SIGNAL TELEMETRY
    # =============================================================
    doc.add_heading("CATEGORY 2: ANTI-GAMING & SPEED DETECTION (Stopping Cheating & Guessing)", level=1)

    cat2_qa = [
        ("Q4: How does your ML catch students who rapidly click random options to cheat?",
         "Simple Answer:",
         "We created a **Multi-Signal Evidence Model** that calculates an Evidence Weight (called **w**, from 0.0 to 1.0).\n\n"
         "• **The 3-Second Speed Trap**: We measure the time taken to answer. If a student answers a word problem in under 3 seconds, the system knows they didn't even read the question. It immediately sets **w = 0.00**.\n"
         "• **The Result**: Even if their random guess happened to be correct, they get **0% mastery boost**. The system neutralizes rapid guessing completely."),

        ("Q5: What happens if a student uses all the hints or feels unconfident?",
         "Simple Answer:",
         "The system scales down the credit proportional to help received:\n\n"
         "• **0 Hints Used**: Student solved it independently -> Full 100% evidence weight (w = 1.0).\n"
         "• **1 Hint Used**: Minor guidance needed -> 60% evidence weight (w = 0.60).\n"
         "• **3 Hints Used**: The system basically gave away the answer -> 25% evidence weight (w = 0.25).\n"
         "• **Confidence Check**: If the student selected 'Low Confidence', the system lowers the update, treating it as an uncertain attempt.")
    ]

    for q, a_lbl, a_txt in cat2_qa:
        doc.add_heading(q, level=2)
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        r_lbl = p.add_run(f"{a_lbl} ")
        r_lbl.bold = True
        r_lbl.font.size = Pt(9.5)
        r_lbl.font.color.rgb = RGBColor(14, 116, 144)
        r_txt = p.add_run(a_txt)
        r_txt.font.size = Pt(9.5)
        r_txt.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # =============================================================
    # CATEGORY 3: FORGETTING, PREREQUISITES, & COLD-START
    # =============================================================
    doc.add_heading("CATEGORY 3: FORGETTING, PREREQUISITE GRAPHS, & COLD-START", level=1)

    cat3_qa = [
        ("Q6: How does the system handle forgetting over time (e.g. 3 weeks without practice)?",
         "Simple Answer:",
         "We implemented the famous **Ebbinghaus Forgetting Curve**.\n\n"
         "• **How it works**: Every concept has a 'Memory Stability' measured in days (e.g., 7 days). As days pass without practice, your effective score slowly decays along an exponential curve.\n"
         "• **The Smart Part**: If you return after 21 days and your score drops below 60%, the engine triggers an automatic 'Spaced Review'. Once you answer 1 review question correctly, your memory stability doubles (e.g., from 7 days to 14 days), modeling how long-term memory strengthens after review!"),

        ("Q7: What is the 'Prerequisite Graph' and why is it important?",
         "Simple Answer:",
         "Math has strict dependencies. You cannot learn **C4 (Adding Fractions)** if you don't know **C2 (Equivalent Fractions)**.\n\n"
         "• We built a **Directed Acyclic Graph (DAG)** of all 10 concepts.\n"
         "• **The 'Cracked Foundation' Rule**: If a student is attempting advanced Concept 7, but their score on prerequisite Concept 2 drops below 55%, the engine mathematically caps Concept 7 at 40% and forces them to repair Concept 2 first.\n"
         "• This stops students from getting demoralized by hard problems when their foundation has a gap."),

        ("Q8: How does the system test a brand-new student who just joined (Cold-Start)?",
         "Simple Answer:",
         "Instead of starting everyone at beginner Question 1, our **Diagnostic Engine** uses **Maximum Uncertainty (Shannon Entropy)**.\n\n"
         "• It picks 6 questions from central 'hub' topics that give the most information about the student's brain.\n"
         "• When the student answers, the system flows that evidence up and down the graph (propagating 30% of the weight to neighboring topics).\n"
         "• In just **6 questions**, we map out the student's entire knowledge boundary without wasting their time!")
    ]

    for q, a_lbl, a_txt in cat3_qa:
        doc.add_heading(q, level=2)
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        r_lbl = p.add_run(f"{a_lbl} ")
        r_lbl.bold = True
        r_lbl.font.size = Pt(9.5)
        r_lbl.font.color.rgb = RGBColor(14, 116, 144)
        r_txt = p.add_run(a_txt)
        r_txt.font.size = Pt(9.5)
        r_txt.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # =============================================================
    # CATEGORY 4: THE 6-RULE DECISION ENGINE & TEST 8
    # =============================================================
    doc.add_heading("CATEGORY 4: THE 6-RULE DECISION ENGINE & TEST 8 REPRODUCIBILITY", level=1)

    cat4_qa = [
        ("Q9: How does the engine decide what problem to give next? What are the 6 Rules?",
         "Simple Answer:",
         "The engine runs a strict 6-step priority checklist in under 5 milliseconds:\n\n"
         "1. **Priority 1 (Teacher Override)**: Did a human teacher manually assign a topic? If yes, do that immediately.\n"
         "2. **Priority 2 (Stuck Escalation)**: Has the student made <5% progress across 3 consecutive tries? If yes, alert the teacher and pause.\n"
         "3. **Priority 3 (Prerequisite Remediation)**: Is an earlier required topic broken (<55%)? If yes, send them back to fix it.\n"
         "4. **Priority 4 (Spaced Review)**: Has memory decayed due to time (<60%)? If yes, schedule a quick refresher.\n"
         "5. **Priority 5 (Active Practice in ZPD)**: Is the student currently learning this topic (score between 20% and 85%)? If yes, deliver deliberate practice.\n"
         "6. **Priority 6 (Advance Frontier)**: Has the student mastered this topic (>85%) and passed the hard transfer test? If yes, unlock the next concept!"),

        ("Q10: What is 'Test 8 Reproducibility Proof' that judges ask about?",
         "Simple Answer:",
         "Test 8 proves that our decision engine is **100% reliable and mathematical**, not random.\n\n"
         "• Every time the engine makes a choice, it saves a snapshot of the student's exact scores.\n"
         "• In Test 8, we load that snapshot and re-run the engine. It produces the **exact same next question, exact same target, and exact same reason with 0.00% variance**.\n"
         "• This proves there is zero hallucination and zero randomness in our pedagogical decisions.")
    ]

    for q, a_lbl, a_txt in cat4_qa:
        doc.add_heading(q, level=2)
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        r_lbl = p.add_run(f"{a_lbl} ")
        r_lbl.bold = True
        r_lbl.font.size = Pt(9.5)
        r_lbl.font.color.rgb = RGBColor(14, 116, 144)
        r_txt = p.add_run(a_txt)
        r_txt.font.size = Pt(9.5)
        r_txt.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # =============================================================
    # CATEGORY 5: QUICK RAPID-FIRE JURY QUESTIONS (ONE-LINERS)
    # =============================================================
    doc.add_heading("CATEGORY 5: RAPID-FIRE ML QUESTIONS (Quick 1-Line Answers)", level=1)

    rapid_fire = [
        ("How do you know when a concept is truly mastered?",
         "When effective mastery reaches 85% AND the student passes at least 1 hard, multi-step transfer question with high evidence weight (w >= 0.5)."),

        ("What is Zone of Proximal Development (ZPD)?",
         "The 'sweet spot' of learning — problems that are not too easy (boring) and not too hard (frustrating), keeping students in their optimal learning zone."),

        ("What is the uncertainty metric (Standard Error)?",
         "It measures how confident the computer is in its estimate. When a student has answered few questions, uncertainty is high; as more evidence comes in, uncertainty shrinks."),

        ("Can the system detect student misconceptions?",
         "Yes. For example, in fractions, if a student adds 1/2 + 1/3 and answers 2/5 (adding top and bottom straight across), our question evaluator flags the specific 'Part-to-Part Misconception'."),

        ("How does the 3D galaxy connect to your ML model?",
         "Every 3D celestial sphere's color (Green=Mastered, Cyan=Practicing, Red=Fragile, Amber=Decayed) and size are directly driven by the live BKT probability and stability values from the database.")
    ]

    for q, a in rapid_fire:
        p_rf = doc.add_paragraph()
        p_rf.paragraph_format.space_before = Pt(4)
        p_rf.paragraph_format.space_after = Pt(1)
        r_q = p_rf.add_run(f" {q}\n")
        r_q.bold = True
        r_q.font.name = "Calibri"
        r_q.font.size = Pt(9.5)
        r_q.font.color.rgb = RGBColor(180, 83, 9)

        r_a = p_rf.add_run(f" {a}")
        r_a.font.name = "Calibri"
        r_a.font.size = Pt(9.5)
        r_a.font.color.rgb = RGBColor(30, 41, 59)

    # Save documents with fallback handling
    saved = False
    for fname in ["ml_question_bank.docx", "MasteryFlow_ML_Jury_QA.docx", "ml_presentation_guide.docx"]:
        try:
            doc.save(fname)
            print(f"Successfully generated '{fname}'!")
            saved = True
            if fname == "ml_question_bank.docx":
                break
        except PermissionError:
            print(f"Note: '{fname}' is currently open in Word. Saved to backup name.")

    if not saved:
        doc.save("ml_qa_final.docx")
        print("Successfully generated 'ml_qa_final.docx'!")

if __name__ == "__main__":
    create_ml_qa_doc()
