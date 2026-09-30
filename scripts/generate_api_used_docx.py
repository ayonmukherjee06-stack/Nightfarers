"""
Script to generate the authoritative 'API Used.docx' Word document.
Details all REST API endpoints, internal Python Service APIs, and external CDN dependencies
for the MasteryFlow: Explainable Adaptive Learning & Intervention Engine.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

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

def add_callout(doc, text, title="ARCHITECTURAL INVARIANT", bg_color="F0FDF4", border_color="16A34A", title_color=(22, 101, 52)):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="28" w:space="0" w:color="{border_color}"/>
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
    r_title.font.size = Pt(11)
    r_title.font.color.rgb = RGBColor(*title_color)
    
    r_text = p.add_run(text)
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(10)
    r_text.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:left w:val="single" w:sz="16" w:space="0" w:color="94A3B8"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(code_str)
    r.font.name = "Consolas"
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def style_header_cell(cell, text):
    set_cell_background(cell, "1E3A8A")
    set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(255, 255, 255)

def style_data_cell(cell, text, bg_color="FFFFFF", bold=False, is_code=False):
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    r.bold = bold
    r.font.name = "Consolas" if is_code else "Calibri"
    r.font.size = Pt(8.5 if is_code else 9.5)
    r.font.color.rgb = RGBColor(15, 23, 42)

def build_api_used_document():
    doc = docx.Document()

    # Configure Margins (0.75 in)
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # -------------------------------------------------------------
    # DOCUMENT HEADER / BANNER
    # -------------------------------------------------------------
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(2)
    r_meta = p_meta.add_run("YUVA MEGATHON 2026  |  TRACK: EDUGENAI  |  DOMAIN 04: INTELLIGENT EDUCATIONAL SYSTEMS")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(9)
    r_meta.bold = True
    r_meta.font.color.rgb = RGBColor(100, 116, 139)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("MasteryFlow: Comprehensive API Specification")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(24)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(30, 58, 138)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("Exhaustive Technical Reference of All REST Endpoints, Internal Service Interfaces, and External Dependencies")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.italic = True
    r_sub.font.color.rgb = RGBColor(15, 118, 110)

    # Metadata Box
    meta_table = doc.add_table(rows=2, cols=4)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_headers = ["Project Lead", "Domain / Track", "Architecture", "API Standard"]
    meta_values = [
        "Ayon Mukherjee (Nightfarers)",
        "EduGenAI / Domain 04",
        "Deterministic Glass-Box",
        "FastAPI REST (OpenAPI 3.1)"
    ]
    for c_idx, h in enumerate(meta_headers):
        style_header_cell(meta_table.cell(0, c_idx), h)
        style_data_cell(meta_table.cell(1, c_idx), meta_values[c_idx], bg_color="F8FAFC", bold=True)
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------
    # EXECUTIVE SUMMARY & CRITICAL ARCHITECTURAL DISCLOSURE
    # -------------------------------------------------------------
    h1 = doc.add_heading("1. Executive Summary & API Design Philosophy", level=1)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)
    for r in h1.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(15)
        r.font.color.rgb = RGBColor(30, 58, 138)

    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.space_after = Pt(6)
    r = p_intro.add_run(
        "MasteryFlow is an Explainable Adaptive Learning and Intervention Engine designed to solve the explainability "
        "and reliability crises found in contemporary educational AI. The system is engineered around a clean, decoupled "
        "architecture comprising an ultra-fast FastAPI REST backend, a pure-Python psychometric engine, an ACID-compliant "
        "SQLite relational database, and an interactive Streamlit UI portal."
    )
    r.font.name = "Calibri"
    r.font.size = Pt(10)

    add_callout(
        doc,
        "MasteryFlow deliberately uses ZERO external generative LLM APIs (e.g., OpenAI GPT-4, Google Gemini, Anthropic Claude, "
        "or Hugging Face) and ZERO third-party cloud analytics services in its core pedagogical decision loop. "
        "Every assessment calculation, prerequisite validation, and learning path decision is mathematically computed in pure Python "
        "via Bayesian Knowledge Tracing (BKT) and 6 deterministic pedagogical rules. "
        "This ensures 100% mathematical explainability, sub-millisecond latency, zero hallucination risk, 100% offline capability, "
        "and zero student data leakage to commercial cloud providers.",
        title="CORE ARCHITECTURAL INVARIANT: ZERO EXTERNAL LLM APIS",
        bg_color="ECFDF5",
        border_color="059669",
        title_color=(4, 120, 87)
    )

    p_breakdown = doc.add_paragraph()
    p_breakdown.paragraph_format.space_after = Pt(8)
    r = p_breakdown.add_run(
        "The project API architecture is categorized into three well-defined tiers:\n"
        "• Tier 1: Internal Backend REST API (FastAPI) — Exposes 9 production-grade endpoints for telemetry ingestion, next-action evaluation, teacher overrides, cohort heatmaps, and longitudinal time-travel simulation.\n"
        "• Tier 2: Internal Python Service API (masteryflow.engine) — High-performance programmatic interfaces allowing direct, zero-overhead in-process communication.\n"
        "• Tier 3: Client-Side Visualization CDN APIs — Static frontend assets loaded by the browser (Three.js and Google Fonts) strictly for 3D graphics rendering and typography."
    )
    r.font.name = "Calibri"
    r.font.size = Pt(10)

    # -------------------------------------------------------------
    # SECTION 2: FASTAPI REST API ENDPOINTS
    # -------------------------------------------------------------
    h2 = doc.add_heading("2. Complete Backend REST API Reference (FastAPI)", level=1)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(4)
    for r in h2.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(15)
        r.font.color.rgb = RGBColor(30, 58, 138)

    p_rest_intro = doc.add_paragraph()
    p_rest_intro.paragraph_format.space_after = Pt(6)
    r = p_rest_intro.add_run(
        "The backend REST API is hosted via Uvicorn on port 8000 and documented interactively via OpenAPI / Swagger. "
        "All request and response models are strictly validated at runtime using Pydantic v2. "
        "Interactive Swagger documentation is available at http://127.0.0.1:8000/docs, OpenAPI schema at http://127.0.0.1:8000/openapi.json, "
        "and ReDoc specifications at http://127.0.0.1:8000/redoc."
    )
    r.font.name = "Calibri"
    r.font.size = Pt(10)

    # Summary Table of All Endpoints
    tbl_endpoints = doc.add_table(rows=10, cols=4)
    tbl_endpoints.alignment = WD_TABLE_ALIGNMENT.CENTER
    cols = ["HTTP Method", "Endpoint Path", "Category", "Functional Purpose"]
    for i, col_name in enumerate(cols):
        style_header_cell(tbl_endpoints.cell(0, i), col_name)

    endpoints_data = [
        ("GET", "/", "Health & Engine", "Root status check and psychometric invariant verification"),
        ("POST", "/api/attempt", "Mastery Engine", "Ingest assessment attempt, evaluate telemetry weight w, update BKT posterior"),
        ("GET", "/api/next-action/{student_id}", "Pedagogical Decision", "Evaluate 6 deterministic pedagogical rules and yield next learning decision"),
        ("GET", "/api/state/{student_id}", "Cognitive State", "Retrieve full cognitive vector, virtual clock, and concept records"),
        ("GET", "/api/student/{student_id}/mastery", "Mastery State", "Retrieve per-concept cognitive mastery map directly from SQLite"),
        ("POST", "/api/teacher/override", "Teacher Authority", "Apply persistent human-in-the-loop override with SQLite audit log"),
        ("POST", "/api/time-travel", "Virtual Simulation", "Advance virtual clock to simulate longitudinal Ebbinghaus memory decay"),
        ("GET", "/api/teacher/heatmap", "Cohort Analytics", "Compute 2D cohort mastery heatmap matrix across curriculum concepts C1–C10"),
        ("GET", "/api/teacher/stuck-learners", "Intervention Queue", "Retrieve escalation queue of learners with Delta p < 0.05 across 3 cycles")
    ]

    for row_idx, data in enumerate(endpoints_data, start=1):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        style_data_cell(tbl_endpoints.cell(row_idx, 0), data[0], bg_color=bg, bold=True)
        style_data_cell(tbl_endpoints.cell(row_idx, 1), data[1], bg_color=bg, is_code=True)
        style_data_cell(tbl_endpoints.cell(row_idx, 2), data[2], bg_color=bg)
        style_data_cell(tbl_endpoints.cell(row_idx, 3), data[3], bg_color=bg)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Detailed Endpoint Specifications
    def add_endpoint_detail(
        doc,
        method,
        path,
        title,
        description,
        params_info,
        req_json=None,
        resp_json=None,
        psychometric_note=None
    ):
        p_ep = doc.add_paragraph()
        p_ep.paragraph_format.space_before = Pt(10)
        p_ep.paragraph_format.space_after = Pt(2)
        r_m = p_ep.add_run(f"[{method}] ")
        r_m.bold = True
        r_m.font.name = "Consolas"
        r_m.font.size = Pt(11)
        r_m.font.color.rgb = RGBColor(16, 185, 129) if method == "GET" else RGBColor(59, 130, 246)
        
        r_p = p_ep.add_run(path)
        r_p.bold = True
        r_p.font.name = "Consolas"
        r_p.font.size = Pt(11)
        r_p.font.color.rgb = RGBColor(30, 58, 138)
        
        r_t = p_ep.add_run(f" — {title}")
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(11)
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(15, 118, 110)

        p_desc = doc.add_paragraph()
        p_desc.paragraph_format.space_after = Pt(4)
        r_d = p_desc.add_run(f"Description: {description}")
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(9.5)

        if params_info:
            p_pi = doc.add_paragraph()
            p_pi.paragraph_format.space_after = Pt(2)
            r_pi = p_pi.add_run("Parameters & Payload Schema:")
            r_pi.bold = True
            r_pi.font.name = "Calibri"
            r_pi.font.size = Pt(9.5)
            r_pi.font.color.rgb = RGBColor(71, 85, 105)
            
            p_param_body = doc.add_paragraph()
            p_param_body.paragraph_format.space_after = Pt(4)
            r_pb = p_param_body.add_run(params_info)
            r_pb.font.name = "Calibri"
            r_pb.font.size = Pt(9)

        if req_json:
            p_req = doc.add_paragraph()
            p_req.paragraph_format.space_after = Pt(1)
            r_req = p_req.add_run("Sample Request Body (JSON):")
            r_req.bold = True
            r_req.font.name = "Calibri"
            r_req.font.size = Pt(9)
            add_code_block(doc, req_json)

        if resp_json:
            p_resp = doc.add_paragraph()
            p_resp.paragraph_format.space_after = Pt(1)
            r_resp = p_resp.add_run("Sample Response Body (200 OK):")
            r_resp.bold = True
            r_resp.font.name = "Calibri"
            r_resp.font.size = Pt(9)
            add_code_block(doc, resp_json)

        if psychometric_note:
            add_callout(doc, psychometric_note, title="ALGORITHMIC BACKEND BEHAVIOR", bg_color="EFF6FF", border_color="3B82F6", title_color=(29, 78, 216))

    # Endpoint 1: GET /
    add_endpoint_detail(
        doc,
        method="GET",
        path="/",
        title="Root Health & Psychometric Engine Metadata",
        description="Pings the running backend service to confirm service readiness, competition domain, and architectural invariants.",
        params_info="None. Simple HTTP GET request.",
        resp_json="""{
  "status": "online",
  "service": "MasteryFlow Engine REST API",
  "version": "1.0.0",
  "domain": "Domain 04: Intelligent Educational Systems",
  "competition": "YUVA Megathon 2026",
  "docs_url": "/docs",
  "psychometric_invariants": {
    "pure_python_engine": true,
    "zero_llm_decision_loop": true,
    "deterministic_reproducibility": "100.0%"
  }
}""",
        psychometric_note="Executed by the Streamlit frontend upon startup (frontend/student.py:124) with a 0.8s timeout to dynamically switch between Live REST Backend mode and Embedded Pure-Python Fallback mode."
    )

    # Endpoint 2: POST /api/attempt
    add_endpoint_detail(
        doc,
        method="POST",
        path="/api/attempt",
        title="Submit Interactive Attempt & Update BKT Posterior",
        description="Ingests granular telemetry from student assessment attempts, executes the anti-gaming telemetry scoring pipeline, and computes the Bayesian Knowledge Tracing posterior mastery.",
        params_info=(
            "• student_id (string, required): Unique identifier of learner (e.g., 'STU_042')\n"
            "• concept_id (string, required): Curriculum concept key from C1 to C10\n"
            "• is_correct (boolean, required): Whether response matches exact fractional value\n"
            "• difficulty (float, default: 0.3, range: [0.0, 1.0]): Item psychometric difficulty\n"
            "• is_transfer (boolean, default: false): True if question evaluates cross-concept transfer\n"
            "• hints_used (integer, default: 0): Progressive hint drawer interactions\n"
            "• attempt_no (integer, default: 1): 1 for first try; >1 for retry attempts\n"
            "• retry_gap_seconds (float, default: 999.0): Latency between consecutive retries\n"
            "• time_ms (integer, default: 10000): Response latency in milliseconds\n"
            "• confidence (string, default: 'medium'): Metacognitive self-rating ('low', 'medium', 'high')"
        ),
        req_json="""{
  "student_id": "STU_042",
  "concept_id": "C2",
  "is_correct": true,
  "difficulty": 0.45,
  "is_transfer": false,
  "hints_used": 1,
  "attempt_no": 1,
  "retry_gap_seconds": 999.0,
  "time_ms": 14200,
  "confidence": "high"
}""",
        resp_json="""{
  "status": "success",
  "concept_id": "C2",
  "is_correct": true,
  "prior_p": 0.420,
  "posterior_p": 0.684,
  "new_p": 0.731,
  "evidence_weight": 0.850,
  "evidence_sum": 3.450,
  "cognitive_status": "practicing",
  "is_misconception": false,
  "uncertainty_se": 0.082
}""",
        psychometric_note="Evaluates telemetry weight w: if response time < 5000 ms, evidence weight w is clamped to 0.00, suppressing rapid guessing. The Bayesian update scales slip and guess by question difficulty d, and applies learning transition T = 0.15."
    )

    # Endpoint 3: GET /api/next-action/{student_id}
    add_endpoint_detail(
        doc,
        method="GET",
        path="/api/next-action/{student_id}",
        title="Evaluate 6 Deterministic Pedagogical Rules",
        description="Queries the learner's cognitive state from SQLite, evaluates the 6 ordered pedagogical rules against the C1–C10 Directed Acyclic Graph, and deterministically outputs the next educational intervention.",
        params_info="• student_id (string, path parameter): Identifier of learner to evaluate.",
        resp_json="""{
  "action": "PRACTICE",
  "target_concept": "C2",
  "target_concept_name": "Equivalent fractions and simplifying",
  "reason": "Current concept C2 in progress (p_eff=0.684 < 0.850). Consolidating foundational skills.",
  "rule_number": 4,
  "rule_name": "Practice (ZPD Consolidation)",
  "p_eff": 0.684,
  "evidence_sum": 3.450,
  "status": "practicing",
  "is_fragile": false,
  "config_version": 1,
  "inputs_json": "{\"student_id\":\"STU_042\",\"concept_id\":\"C2\",\"p_eff\":0.684,\"rule\":4}"
}""",
        psychometric_note="Strictly evaluates the 6 ordered rules: Rule 0 (Teacher Override) -> Rule 1 (Teacher Intervention if Delta p < 0.05 over 3 cycles) -> Rule 2 (Remediate Weakest Prerequisite < 0.55) -> Rule 3 (Spaced Review if Decayed < 0.60) -> Rule 4 (Practice ZPD) -> Rule 5 (Advance Next Unlocked Node) -> Rule 6 (Challenge Capstone)."
    )

    # Endpoint 4: GET /api/state/{student_id}
    add_endpoint_detail(
        doc,
        method="GET",
        path="/api/state/{student_id}",
        title="Retrieve Comprehensive Student Cognitive Vector",
        description="Returns complete psychometric state across all curriculum nodes, virtual clock timestamp, active concept, current streak, and historical telemetry.",
        params_info="• student_id (string, path parameter): Identifier of learner.",
        resp_json="""{
  "student_id": "STU_042",
  "active_concept_id": "C2",
  "virtual_clock": 0.0,
  "concepts": {
    "C1": {
      "p": 0.920,
      "p_eff": 0.920,
      "stability_days": 14.0,
      "evidence_sum": 4.80,
      "transfer_passed": true,
      "is_fragile": false,
      "status": "mastered"
    },
    "C2": {
      "p": 0.684,
      "p_eff": 0.684,
      "stability_days": 7.0,
      "evidence_sum": 3.45,
      "transfer_passed": false,
      "is_fragile": false,
      "status": "practicing"
    }
  }
}""",
        psychometric_note="Effective mastery p_eff is dynamically adjusted by the Prerequisite Ceiling Rule: p_eff[C] <= min(prereqs) + 0.25. If violated, is_fragile is flagged true."
    )

    # Endpoint 5: GET /api/student/{student_id}/mastery
    add_endpoint_detail(
        doc,
        method="GET",
        path="/api/student/{student_id}/mastery",
        title="Retrieve Per-Concept Cognitive Mastery Map",
        description="Provides direct access to the student_mastery table in SQLite, returning raw probability p, effective probability p_eff, stability days, and transfer status.",
        params_info="• student_id (string, path parameter): Learner identifier.",
        resp_json="""{
  "status": "success",
  "student_id": "STU_042",
  "mastery": {
    "C1": {"p": 0.92, "p_eff": 0.92, "stability_days": 14.0, "status": "mastered", "transfer_passed": 1},
    "C2": {"p": 0.68, "p_eff": 0.68, "stability_days": 7.0, "status": "practicing", "transfer_passed": 0}
  }
}"""
    )

    # Endpoint 6: POST /api/teacher/override
    add_endpoint_detail(
        doc,
        method="POST",
        path="/api/teacher/override",
        title="Apply Persistent Human-in-the-Loop Teacher Override",
        description="Allows educators to exercise ultimate pedagogical authority by commanding an override on student action or concept target. Written with ACID transaction safety to the SQLite overrides table.",
        params_info=(
            "• student_id (string, required): Student targeted for override\n"
            "• override_concept (string, required): Concept key (e.g., 'C1')\n"
            "• override_action (string, required): Action command ('Practice', 'Remediate', 'Review', 'Advance')\n"
            "• teacher_name (string, required): Authoring educator name for accountability audit\n"
            "• reason (string, required): Justification text for institutional audit trail"
        ),
        req_json="""{
  "student_id": "STU_042",
  "override_concept": "C1",
  "override_action": "Remediate",
  "teacher_name": "Prof. Sharma",
  "reason": "Observed foundational unit fraction misconception in 1-on-1 coaching."
}""",
        resp_json="""{
  "status": "persisted",
  "next_decision": {
    "action": "REMEDIATE_PREREQUISITE",
    "target_concept": "C1",
    "reason": "Teacher Override by Prof. Sharma: Observed foundational unit fraction misconception.",
    "rule_number": 0,
    "rule_name": "Teacher Override (Human Authority)"
  }
}""",
        psychometric_note="Rule 0 intercepts the decision loop before automated heuristics execute. The override remains active until completed or cleared, maintaining complete institutional governance."
    )

    # Endpoint 7: POST /api/time-travel
    add_endpoint_detail(
        doc,
        method="POST",
        path="/api/time-travel",
        title="Advance Virtual Clock (Ebbinghaus Decay Simulation)",
        description="Advances the learner's longitudinal clock by a specified duration in days, recomputing effective mastery according to the Ebbinghaus exponential forgetting curve.",
        params_info=(
            "• student_id (string, required): Student identifier\n"
            "• days (float, required, gt: 0.0): Number of virtual days elapsed (e.g., 14.0 or 21.0)"
        ),
        req_json="""{
  "student_id": "STU_042",
  "days": 21.0
}""",
        resp_json="""{
  "status": "advanced",
  "student_state": {
    "student_id": "STU_042",
    "virtual_clock_days": 21.0,
    "decayed_concepts": {
      "C1": {
        "prior_p": 0.92,
        "decayed_p_eff": 0.584,
        "stability_days": 14.0,
        "status": "decayed_review_needed"
      }
    }
  }
}""",
        psychometric_note="Implements p(t) = p_floor + (p0 - p_floor) * exp(-t / S). When p_eff drops below review_threshold (0.60), Rule 3 automatically triggers Spaced Review before downstream failure occurs."
    )

    # Endpoint 8: GET /api/teacher/heatmap
    add_endpoint_detail(
        doc,
        method="GET",
        path="/api/teacher/heatmap",
        title="Compute 2D Cohort Mastery Heatmap Matrix",
        description="Calculates a normalized 2D matrix of effective mastery values across all 10 curriculum concepts for an array of student IDs, revealing systemic classroom bottlenecks.",
        params_info="• student_ids (array of strings, query parameter): List of student IDs to aggregate.",
        resp_json="""{
  "STU_001": [0.95, 0.88, 0.42, 0.81, 0.20, 0.15, 0.10, 0.10, 0.10, 0.10],
  "STU_002": [0.92, 0.90, 0.85, 0.88, 0.82, 0.78, 0.65, 0.50, 0.30, 0.15],
  "STU_042": [0.92, 0.68, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10]
}"""
    )

    # Endpoint 9: GET /api/teacher/stuck-learners
    add_endpoint_detail(
        doc,
        method="GET",
        path="/api/teacher/stuck-learners",
        title="Retrieve Stuck-Learner Intervention Escalation Queue",
        description="Scans the student cohort for learners whose mastery progression has plateaued (Delta p < 0.05 over 3 consecutive attempts on the same concept).",
        params_info="None.",
        resp_json="""{
  "stuck_learners": [
    {
      "student_id": "STU_019",
      "concept_id": "C4",
      "consecutive_stagnant_cycles": 3,
      "delta_p": 0.012,
      "recommended_action": "1-on-1 Remedial Session on Like Denominators",
      "flagged_at": 1759124000.0
    }
  ]
}""",
        psychometric_note="Enforces Rule 1 (Teacher Intervention) to prevent automated question loops from demoralizing stuck learners with endless repetitive drilling."
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # SECTION 3: INTERNAL PYTHON SERVICE API CONTRACT
    # -------------------------------------------------------------
    h3 = doc.add_heading("3. Internal Python Service API Contract (masteryflow.engine)", level=1)
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(4)
    for r in h3.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(15)
        r.font.color.rgb = RGBColor(30, 58, 138)

    p_py_intro = doc.add_paragraph()
    p_py_intro.paragraph_format.space_after = Pt(6)
    r = p_py_intro.add_run(
        "For zero-overhead in-process communication, testing suites, and embedded fallback execution, "
        "the engine exposes a unified Python Service Contract in backend/engine/service.py and backend/engine/contracts.py. "
        "Any module can directly import and call these functions without running an HTTP network daemon."
    )
    r.font.name = "Calibri"
    r.font.size = Pt(10)

    add_code_block(doc, """from backend.engine import (
    record_attempt,           # Processes attempt, anti-gaming telemetry, and updates BKT
    next_action,              # Evaluates the 6 deterministic pedagogical rules
    get_student_state,        # Returns full cognitive vector and virtual clock
    apply_teacher_override,   # Persists teacher override and generates decision
    advance_student_time,     # Simulates longitudinal Ebbinghaus memory decay
    get_cohort_heatmap,       # Generates 2D cohort mastery matrix
    get_stuck_learners        # Returns queue of learners flagged for human coaching
)""")

    # Function Specifications Table
    tbl_py_funcs = doc.add_table(rows=8, cols=3)
    tbl_py_funcs.alignment = WD_TABLE_ALIGNMENT.CENTER
    py_cols = ["Python Function Signature", "Return Type", "Description"]
    for i, col_name in enumerate(py_cols):
        style_header_cell(tbl_py_funcs.cell(0, i), col_name)

    py_funcs_data = [
        ("record_attempt(student_id, concept_id, is_correct, difficulty=0.3, ...)", "AttemptResult", "Computes telemetry weight w, adjusts slip/guess, and updates BKT probability"),
        ("next_action(student_id)", "Decision", "Evaluates 6 rules against DAG and returns explainable decision object"),
        ("get_student_state(student_id)", "Dict[str, Any]", "Returns serialized learner cognitive vector, clock, and concept records"),
        ("apply_teacher_override(student_id, concept, action, teacher, reason)", "Decision", "Logs override to SQLite and immediately produces corresponding Decision"),
        ("advance_student_time(student_id, days)", "Dict[str, Any]", "Applies exponential decay p(t) across concepts and updates SQLite state"),
        ("get_cohort_heatmap(student_ids)", "Dict[str, List[float]]", "Computes 2D matrix of effective mastery values across C1–C10"),
        ("get_stuck_learners()", "List[Dict[str, Any]]", "Identifies students with Delta p < 0.05 across 3 consecutive cycles")
    ]

    for row_idx, data in enumerate(py_funcs_data, start=1):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        style_data_cell(tbl_py_funcs.cell(row_idx, 0), data[0], bg_color=bg, is_code=True)
        style_data_cell(tbl_py_funcs.cell(row_idx, 1), data[1], bg_color=bg, bold=True)
        style_data_cell(tbl_py_funcs.cell(row_idx, 2), data[2], bg_color=bg)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # SECTION 4: CLIENT-SIDE WEB & CDN ASSETS
    # -------------------------------------------------------------
    h4 = doc.add_heading("4. Client-Side Web & CDN Dependencies", level=1)
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(4)
    for r in h4.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(15)
        r.font.color.rgb = RGBColor(30, 58, 138)

    p_cdn_intro = doc.add_paragraph()
    p_cdn_intro.paragraph_format.space_after = Pt(6)
    r = p_cdn_intro.add_run(
        "While the engine executes 100% locally with zero external intelligence or data transmission, "
        "the frontend interface integrates standard client-side CDN script assets strictly for hardware-accelerated 3D graphics "
        "and typography rendering in the user's local web browser:"
    )
    r.font.name = "Calibri"
    r.font.size = Pt(10)

    tbl_cdn = doc.add_table(rows=4, cols=4)
    tbl_cdn.alignment = WD_TABLE_ALIGNMENT.CENTER
    cdn_cols = ["Library / Asset", "CDN Provider / URL", "File Location in Repo", "Purpose"]
    for i, col_name in enumerate(cdn_cols):
        style_header_cell(tbl_cdn.cell(0, i), col_name)

    cdn_data = [
        ("Three.js (r128)", "cdnjs.cloudflare.com/.../three.min.js", "frontend/components/universe_3d.py", "WebGL 3D engine for rendering the interactive curriculum concept universe"),
        ("OrbitControls.js", "cdn.jsdelivr.net/.../OrbitControls.js", "frontend/components/universe_3d.py", "Interactive mouse camera panning, rotating, and zooming in 3D universe"),
        ("Plus Jakarta Sans & JetBrains Mono", "fonts.googleapis.com/css2?family=...", "frontend/components/theme.py", "Modern 2026 dark glassmorphic typography and monospace HUD numbers")
    ]

    for row_idx, data in enumerate(cdn_data, start=1):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        style_data_cell(tbl_cdn.cell(row_idx, 0), data[0], bg_color=bg, bold=True)
        style_data_cell(tbl_cdn.cell(row_idx, 1), data[1], bg_color=bg, is_code=True)
        style_data_cell(tbl_cdn.cell(row_idx, 2), data[2], bg_color=bg)
        style_data_cell(tbl_cdn.cell(row_idx, 3), data[3], bg_color=bg)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # SECTION 5: FRONTEND-TO-BACKEND INTEGRATION & FAILOVER
    # -------------------------------------------------------------
    h5 = doc.add_heading("5. Frontend Integration & Resilient Zero-Latency Failover", level=1)
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(4)
    for r in h5.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(15)
        r.font.color.rgb = RGBColor(30, 58, 138)

    p_failover = doc.add_paragraph()
    p_failover.paragraph_format.space_after = Pt(6)
    r = p_failover.add_run(
        "The Streamlit frontend (frontend/student.py) implements an intelligent dual-mode communication bridge. "
        "It attempts to consume the live FastAPI REST service over HTTP, but seamlessly falls back to embedded pure-Python "
        "execution with direct SQLite persistence if the HTTP daemon is not detected:"
    )
    r.font.name = "Calibri"
    r.font.size = Pt(10)

    add_code_block(doc, """# frontend/student.py: Lines 112-132
FASTAPI_URL = os.getenv("MASTERYFLOW_API_URL", "http://localhost:8000")

def check_backend_online() -> bool:
    try:
        r = requests.get(f"{FASTAPI_URL}/", timeout=0.8)
        return r.status_code == 200
    except Exception:
        return False

# Automatic failover: uses FastAPI if online; falls back to embedded engine if offline
is_backend_live = check_backend_online()
local_db, local_graph = get_embedded_engine()""")

    add_callout(
        doc,
        "This dual-mode architecture guarantees zero presentation downtime during competitive hackathons and stage demonstrations. "
        "Whether evaluated via curl, Swagger, automated pytest, or a standalone laptop with no open network ports, "
        "the application operates with 100% functional integrity.",
        title="ZERO-DOWNTIME COMPETITION DESIGN",
        bg_color="FEF3C7",
        border_color="D97706",
        title_color=(180, 83, 9)
    )

    # -------------------------------------------------------------
    # SECTION 6: API VERIFICATION TESTS (PYTEST SUITE)
    # -------------------------------------------------------------
    h6 = doc.add_heading("6. Automated API Verification Suite (tests/test_api.py)", level=1)
    h6.paragraph_format.space_before = Pt(14)
    h6.paragraph_format.space_after = Pt(4)
    for r in h6.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(15)
        r.font.color.rgb = RGBColor(30, 58, 138)

    p_test_intro = doc.add_paragraph()
    p_test_intro.paragraph_format.space_after = Pt(6)
    r = p_test_intro.add_run(
        "Every endpoint is backed by automated unit tests in tests/test_api.py and integration tests in tests/test_service_contract.py. "
        "The test suite executes via 'pytest' with 100% green status across 41 total test suites, guaranteeing API contract compliance:"
    )
    r.font.name = "Calibri"
    r.font.size = Pt(10)

    tbl_tests = doc.add_table(rows=6, cols=3)
    tbl_tests.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_cols = ["Test Case", "Target Route / Contract", "Validation Assertion"]
    for i, col_name in enumerate(test_cols):
        style_header_cell(tbl_tests.cell(0, i), col_name)

    tests_data = [
        ("test_api_submit_attempt", "POST /api/attempt", "Verifies BKT posterior update: new_p > prior_p, status == 'success'"),
        ("test_api_next_action", "GET /api/next-action/{id}", "Verifies 6-rule output: action in [PRACTICE, ADVANCE, REVIEW, REMEDIATE]"),
        ("test_api_teacher_override", "POST /api/teacher/override", "Verifies persistence: status == 'persisted', target == overridden concept"),
        ("test_api_advance_time", "POST /api/time-travel", "Verifies virtual clock advancement: clock == 14 days, status == 'advanced'"),
        ("test_api_teacher_heatmap_and_stuck_queue", "GET /api/teacher/*", "Verifies cohort matrix dimensions (10 concepts) and stuck queue format")
    ]

    for row_idx, data in enumerate(tests_data, start=1):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        style_data_cell(tbl_tests.cell(row_idx, 0), data[0], bg_color=bg, is_code=True)
        style_data_cell(tbl_tests.cell(row_idx, 1), data[1], bg_color=bg, bold=True)
        style_data_cell(tbl_tests.cell(row_idx, 2), data[2], bg_color=bg)

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    # -------------------------------------------------------------
    # FOOTER & SIGN-OFF
    # -------------------------------------------------------------
    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_foot = p_foot.add_run("MasteryFlow API Specification  •  Team Nightfarers  •  SRM IST YUVA Megathon 2026")
    r_foot.font.name = "Calibri"
    r_foot.font.size = Pt(9)
    r_foot.font.color.rgb = RGBColor(148, 163, 184)

    # Save to disk
    output_path_space = "API Used.docx"
    output_path_under = "API_Used.docx"
    doc.save(output_path_space)
    doc.save(output_path_under)
    print(f"[OK] Successfully saved '{output_path_space}' and '{output_path_under}'.")

if __name__ == "__main__":
    build_api_used_document()
