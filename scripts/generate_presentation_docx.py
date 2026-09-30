"""Script to generate the ultra-simple, human-language 'presentation.docx' Word document.
Written in plain, everyday conversational English that anyone (even a non-tech person) can easily understand and present to judges.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_simple_presentation_doc():
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

    def add_simple_callout(doc, text, title="IN SIMPLE WORDS", bg_color="F0FDF4", border_color="16A34A"):
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
    r_t = p_title.add_run(" MASTERYFLOW — THE SIMPLE GUIDE")
    r_t.font.name = "Arial Black"
    r_t.font.size = Pt(22)
    r_t.font.color.rgb = RGBColor(14, 116, 144)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s = p_sub.add_run("Plain English Presentation Guide & Jury Q&A Manual\n"
                        "How to Explain Everything on Our Website to Anyone (No Tech Jargon Required!)")
    r_s.font.name = "Calibri"
    r_s.font.size = Pt(11)
    r_s.font.italic = True
    r_s.font.color.rgb = RGBColor(100, 116, 139)

    add_simple_callout(
        doc,
        "Imagine a math teacher who sits right beside you. This teacher watches not just if you got the answer right, "
        "but how fast you answered, whether you guessed, and if you forgot older lessons. That is MasteryFlow! "
        "It's an intelligent math coach that knows exactly what you should learn next, without any guesswork.",
        "THE 10-SECOND SUMMARY"
    )

    # =============================================================
    # PART 1: WHAT IS OUR WEBSITE & HOW DOES IT WORK?
    # =============================================================
    doc.add_heading("PART 1: WHAT IS OUR WEBSITE? (The Big Picture)", level=1)
    
    p = doc.add_paragraph()
    p.add_run("Most educational websites (like YouTube or basic quiz apps) are just ").font.size = Pt(10)
    r_b = p.add_run("digital textbooks with a progress bar")
    r_b.bold = True
    r_b.font.size = Pt(10)
    p.add_run(". If you click 'Next', the website assumes you learned it. But in real life, math doesn't work that way!\n\n"
              "Math is like building a tower. If your foundation is weak, the top floors will collapse. "
              "MasteryFlow is a smart system that teaches 10 Math Concepts (Fractions, Decimals, and Ratios). "
              "It makes sure you genuinely understand step 1 before pushing you to step 2.").font.size = Pt(10)

    # 4 Pillars of the Brain in Plain English
    doc.add_heading("1.1 The 4 Smart Things the Brain Does Behind the Scenes", level=2)
    
    pillars = [
        ("1. It Catches Lucky Guesses and Fast Clickers",
         "If a student clicks a random option in 1 second and gets it right by pure luck, our system notices the speed and gives them 0 credit. You only get credit if you actually spend time solving it."),

        ("2. It Stops You from Skipping Basics (The 'Cracked Foundation' Rule)",
         "If you are struggling with basic fractions (Concept 2), the system will NOT let you do hard ratio word problems (Concept 7). It politely pauses and says: 'Let's fix your basics first so you don't get frustrated!'"),

        ("3. It Remembers When You Forget (The 'Summer Vacation' Rule)",
         "If a student was great at fractions 3 weeks ago, but hasn't practiced since, human memory naturally fades. When they log back in, the system gives them a quick 2-minute refresher instead of making them restart from zero."),

        ("4. It Explains Every Single Choice in Plain Words ('Glass-Box')",
         "There are no mysterious AI secrets here. Above every single problem, a green badge tells the student: 'You are doing this problem because your score is 40% and you need 1 more correct answer to level up.'")
    ]

    for title, body in pillars:
        p_p = doc.add_paragraph()
        p_p.paragraph_format.space_before = Pt(5)
        p_p.paragraph_format.space_after = Pt(1)
        r = p_p.add_run(title)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(14, 116, 144)

        p_b = doc.add_paragraph()
        p_b.paragraph_format.space_before = Pt(0)
        p_b.paragraph_format.space_after = Pt(4)
        r_b = p_b.add_run(body)
        r_b.font.name = "Calibri"
        r_b.font.size = Pt(9.5)
        r_b.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # =============================================================
    # PART 2: EVERY SCREEN & BUTTON EXPLAINED IN SIMPLE WORDS
    # =============================================================
    doc.add_heading("PART 2: EVERY SCREEN & BUTTON ON THE WEBSITE (What Does Each Do?)", level=1)
    
    p_scr = doc.add_paragraph()
    p_scr.add_run("When you open the website, look at the sidebar on the left. There are ").font.size = Pt(10)
    r_b = p_scr.add_run("4 Main Pages")
    r_b.bold = True
    r_b.font.size = Pt(10)
    p_scr.add_run(" and a few special helper tools. Here is what every single option does:").font.size = Pt(10)

    screens = [
        (" 1. Learn (The Practice Room)",
         "This is where the student actually solves math problems. When you open it, you see:\n"
         "• 'Why This Next?' Box: A clear message explaining why this problem was picked for you.\n"
         "• The Math Question: Clear math problems with easy click buttons for fractions (like 1/2, 3/4) so you don't have to type weird symbols.\n"
         "• The Hint Button: If you are stuck, you can unlock up to 3 helpful hints.\n"
         "• Confidence Meter: You can say if you felt 'High', 'Medium', or 'Low' confidence in your answer.\n"
         "• The Result Breakdown: After submitting, it shows if you got it right, how much your score improved, and if you fell into a common math trap."),

        (" 2. Dashboard (The Student's Report Card & 3D Galaxy)",
         "This is the student's personal progress center:\n"
         "• Big Number Cards at Top: Shows your Overall Math Score (e.g. 75%), how many skills you mastered (e.g. 7 out of 10), and your day streak.\n"
         "• 3D Knowledge Universe: A stunning 3D galaxy where every math topic is a glowing star! You can spin it around with your mouse, zoom in, and click any star to see your score.\n"
         "• Progress Bar Grid: 10 clean progress bars showing your exact percentage on every topic from Concept 1 to Concept 10."),

        ("‍ 3. Teach (The Teacher's Radar Screen)",
         "This is built for teachers and school mentors:\n"
         "• Classroom Heatmap: A color-coded grid showing the whole class. Green means the student knows it; red means they need help.\n"
         "• Red Alert Warnings: If 40% of the class is failing the same topic, the system warns the teacher: 'Hey! Most students are stuck on Equivalent Fractions. You might want to explain this on the blackboard today.'\n"
         "• Stuck Student List: Shows students who got stuck 3 times in a row so the teacher can give them 1-on-1 help.\n"
         "• Teacher Override Button: If a teacher wants to manually assign a topic, they just pick the student, click 'Assign', and the system updates immediately."),

        (" 4. Explore (The Math Map)",
         "A clean map showing all 10 math concepts in order. It shows how Concept 1 (basics) connects to Concept 2 (simplifying), and how that leads all the way to Concept 10 (advanced word problems)."),

        (" 5. Switch Learner Profile (In the Sidebar)",
         "Lets you instantly switch between 8 different pre-made students:\n"
         "• Priya Singh: A top student who has mastered almost everything (mostly green stars in 3D).\n"
         "• Diya Sharma: A student who forgot basic fractions, so the system stopped her from doing hard ratios (red glowing stars in 3D).\n"
         "• Kabir Verma: A student who hasn't practiced in 21 days, so his skills faded to yellow (triggers a refresher).\n"
         "• Aarav Patel: A student stuck on Concept 2 across several tries."),

        (" 6. Developer & Demo Tools (In the Sidebar)",
         "Special tools for presenting to judges:\n"
         "• 6-Step Demo Tour: A guided sequence showing proof of how the engine works step-by-step.\n"
         "• Stress-Test Suite: Shows that the system never crashes or gets tricked by edge cases.")
    ]

    for title, desc in screens:
        doc.add_heading(title, level=2)
        p_d = doc.add_paragraph()
        p_d.paragraph_format.space_before = Pt(0)
        p_d.paragraph_format.space_after = Pt(4)
        r_d = p_d.add_run(desc)
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(9.5)
        r_d.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # =============================================================
    # PART 3: BACKEND, FRONTEND, AND API EXPLAINED FOR NON-TECH PEOPLE
    # =============================================================
    doc.add_heading("PART 3: WHAT IS USED IN BACKEND, FRONTEND, & API? (Simple Explanations)", level=1)
    
    p_t = doc.add_paragraph()
    p_t.add_run("If the jury asks: ").font.size = Pt(10)
    r_b = p_t.add_run("\"What technology did you use and why?\"")
    r_b.bold = True
    r_b.italic = True
    r_b.font.size = Pt(10)
    p_t.add_run(", here is how to explain every piece in 2 simple sentences:").font.size = Pt(10)

    tech_simple = [
        ("The Frontend (The Face of the Website)",
         "What is used: Python Streamlit, Three.js (WebGL 3D graphics), and custom dark glass styling.\n"
         "Why it is used: Streamlit makes the web app fast and responsive. Three.js gives us the video-game style 3D galaxy running at super smooth 60 frames per second. The dark glass design makes it look like a futuristic, professional platform instead of a boring school form."),

        ("The Backend (The Brain of the Website)",
         "What is used: Pure Python algorithmic decision engine (Bayesian Knowledge Tracing & Graph Theory).\n"
         "Why it is used: We deliberately did NOT use a random AI chatbot (like ChatGPT) to decide what students should learn next. Chatbots can make things up or give random answers. Our engine uses 100% reliable math rules — so it is always fast (<5 milliseconds), never hallucinates, and can explain every single decision."),

        ("The Database (The Memory of the Website)",
         "What is used: SQLite database with 9 organized tables.\n"
         "Why it is used: It stores all 8 student profiles, all 50 math questions, every single answer submitted, and an unchangeable history log. It ensures that no student's score is ever lost, even if they refresh the page."),

        ("The API (The Messenger Between Screen and Brain)",
         "What is used: FastAPI and Uvicorn running on Port 8000.\n"
         "Why it is used: It acts like a waiter in a restaurant. When a student submits an answer on the screen, the API quickly delivers it to the Brain, the Brain calculates the new score, and the API sends it back to update the screen in a fraction of a second.")
    ]

    for title, desc in tech_simple:
        doc.add_heading(title, level=2)
        p_d = doc.add_paragraph()
        p_d.paragraph_format.space_before = Pt(0)
        p_d.paragraph_format.space_after = Pt(4)
        r_d = p_d.add_run(desc)
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(9.5)
        r_d.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # =============================================================
    # PART 4: HOW TO ANSWER JURY QUESTIONS IN SIMPLE WORDS
    # =============================================================
    doc.add_heading("PART 4: JURY Q&A — HOW TO ANSWER TOUGH QUESTIONS IN EASY WORDS", level=1)
    
    p_qa = doc.add_paragraph()
    p_qa.add_run("Judges love to test if you understand your project. Memorize these simple everyday answers:").font.size = Pt(10)

    simple_qa_list = [
        ("Judge asks: 'Why didn't you just use an AI like ChatGPT to teach the student?'",
         "Say this: 'Because large AI chatbots can hallucinate, make up facts, and give different answers every time. In education, you cannot gamble with a child's learning. Our engine uses pure deterministic math rules — it is 100% reliable, never hallucinates, and runs in under 5 milliseconds.'"),

        ("Judge asks: 'What if a student just clicks random options really fast to finish early?'",
         "Say this: 'Our system tracks how many seconds you took. If you answer in less than 3 seconds, the Anti-Gaming Guard catches you and gives you 0 credit for that question. You have to actually spend time thinking to gain mastery.'"),

        ("Judge asks: 'What happens if a student only solves the easy questions and skips hard ones?'",
         "Say this: 'We have a rule called the Transfer Barrier. Easy questions only give you a 'provisional' pass. You can never unlock the next concept until you successfully solve at least one hard, multi-step problem.'"),

        ("Judge asks: 'What if a student forgets something they learned a month ago?'",
         "Say this: 'We model natural human forgetting. If 21 days pass without practice, your score gently decays. When you return, the system gives you a quick 2-minute refresher to restore your memory before moving forward.'"),

        ("Judge asks: 'Can a human teacher override the computer if they disagree?'",
         "Say this: 'Yes! The teacher is always in control. In the Teacher Command Center, an instructor can click 1 button to send a student to any topic they choose, and the computer immediately obeys while saving a permanent record in the database.'"),

        ("Judge asks: 'How does your 3D Galaxy work?'",
         "Say this: 'It's built with WebGL Three.js. Each glowing star represents a math topic, and the glowing laser lines show which topics unlock the next ones. When you switch between a top student and a struggling student, the colors in the 3D galaxy change live on screen!'"),

        ("Judge asks: 'Why is your website better than Khan Academy or normal quiz apps?'",
         "Say this: 'Normal apps are just video libraries with checkboxes. They don't know if you guessed, they don't stop you when your foundation is broken, and they can't explain their logic. MasteryFlow actively tracks your brain's state, fixes your gaps before you get stuck, and explains every step with total transparency.'")
    ]

    for q, a in simple_qa_list:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(5)
        p_q.paragraph_format.space_after = Pt(1)
        r_q = p_q.add_run(f" {q}")
        r_q.bold = True
        r_q.font.name = "Calibri"
        r_q.font.size = Pt(10)
        r_q.font.color.rgb = RGBColor(180, 83, 9)

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_before = Pt(0)
        p_a.paragraph_format.space_after = Pt(5)
        r_a = p_a.add_run(f" {a}")
        r_a.font.name = "Calibri"
        r_a.font.size = Pt(9.5)
        r_a.font.color.rgb = RGBColor(30, 41, 59)

    # Save with fallback
    saved = False
    for fname in ["presentation.docx", "MasteryFlow_Presentation_Simple.docx", "presentation_guide.docx"]:
        try:
            doc.save(fname)
            print(f"Successfully generated '{fname}'!")
            saved = True
            if fname == "presentation.docx":
                break
        except PermissionError:
            print(f"Note: '{fname}' is currently open in Word. Saved to backup name.")

    if not saved:
        doc.save("presentation_simple.docx")
        print("Successfully generated 'presentation_simple.docx'!")

if __name__ == "__main__":
    create_simple_presentation_doc()
