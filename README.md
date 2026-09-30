# MasteryFlow: Explainable Adaptive Learning & Intervention Engine

**Team Name:** Nightfarers | **Team Leader:** Ayon Mukherjee (+91 8102429090), Email ID - ayonmukherjee06@gmail.com
**Team Members** : Ayon Mukherjee, Shreyash Jha, Shubham Mallick, Soham Choudhury.
**GitHub Link** : 


**YUVA Megathon 2026 | SRM Institute of Science and Technology, Tiruchirappalli**  
**Track:** EduGenAI | **Domain 04:** Intelligent Educational Systems  
**Challenge:** MasteryFlow: Explainable Adaptive Learning and Intervention Engine  

---

##  Clean & Modular Project Architecture

The codebase is organized into cleanly decoupled directories:

```text
YUVA/
├── backend/                #  Algorithmic Core, FastAPI REST API, and SQLite Database Layer
│   ├── api/                # FastAPI routes, models, database layer (db.py), and seeder (seed_data.py)
│   ├── engine/             # Pure-Python BKT, DAG graph, 6 pedagogical rules (decide.py), decay, overrides
│   ├── sim/                # CLI demo and student archetype replay harness
│   ├── demo_ml_engine.py   # Machine Learning live proof runner (Profiles A, B, C, D)
│   ├── run_api.py          # FastAPI REST backend launcher (port 8000)
│   └── __init__.py
│
├── frontend/               #  Modern 2026 Dark Glassmorphic User Interface
│   ├── components/         # Modular UI cards: Glass-box HUD, DAG visualizer, heatmap, telemetry
│   ├── app.py              # Main unified Streamlit portal (Student, Teacher, Live Demo, ML Bench)
│   ├── student.py          # Student Adaptive Learning & Question Runner
│   ├── teacher.py          # Teacher Command Center, Heatmap & Override Console
│   ├── live_demo.py        # Live presentation interactive judge demo
│   ├── ml_inspector.py     # Live psychometric inspector & interactive formula bench
│   ├── run_ui.py           # Streamlit portal launcher (auto-port detection)
│   └── __init__.py
│
├── data/                   #  Curriculum Graph, Parameterized Questions, Personas & Configs
│   ├── concepts.json       # Canonical 10-concept curriculum DAG (C1 to C10)
│   ├── questions.json      # 50 verified math questions verified via fractions.Fraction
│   ├── personas.json       # 4 student archetypes (False Master, Prereq Gap, Rapid Guesser, Twin)
│   ├── config.yaml         # Deterministic threshold configurations
│   └── sim_profiles/       # JSON execution traces for automated replay
│
├── docs/                   #  Presentations, Pitch Deck, Handbooks & Official Proposals
│   ├── presentation.html   # Standalone interactive slide deck for presentation
│   ├── PITCH_PLAYBOOK.md   # Complete judge defense playbook & scoring rubric alignment
│   ├── PITCH_DECK.md       # Slide-by-slide script and talking points
│   ├── JUDGE_QA_DEFENSE.md # Technical defense for hard judge questions
│   ├── LIVE_DEMO_SCRIPT.md # 3-minute stage demo relay choreography
│   ├── COLLEAGUE_HANDOFF.md# Technical specification and API contract handoff
│   ├── YUVA PPT.pptx       # Official competition slide deck
│   └── *.docx, *.pdf       # Official proposals and problem statements
│
├── scripts/                #  Utility, Catalog Generation & Verification Scripts
│   ├── generate_api_used_docx.py
│   ├── generate_chapters_docx.py
│   ├── generate_guide_docx.py
│   ├── generate_infographic_ppt.py
│   ├── generate_latest_ppt.py
│   ├── generate_ml_qa_docx.py
│   ├── generate_presentation_docx.py
│   ├── populate_megathon_template.py
│   ├── test_direct_mail.py
│   └── verify_all_42.py
│
├── tests/                  #  Comprehensive Automated Pytest Suite (55 Tests, 100% Green)
│   ├── conftest.py         # Test environment and path resolution setup
│   ├── test_api.py         # FastAPI route verification
│   ├── test_bank.py        # Question bank exactness verification
│   ├── test_coldstart.py   # Cold-start cognitive divergence proof
│   ├── test_decide.py      # The 6 deterministic ordered pedagogical rules
│   ├── test_email_otp.py   # Email OTP authentication and reset flows
│   ├── test_engine_core.py # BKT update, uncertainty SE, Ebbinghaus decay formulas
│   ├── test_export.py      # Multi-format CSV and Excel data export service
│   ├── test_heatmap.py     # Cohort heatmap & bottleneck detection
│   ├── test_innovations.py # Information gain item ranking & student agency
│   ├── test_multi_subject_video.py # Multi-subject curriculum & YouTube catalog tests
│   ├── test_override.py    # Persistent teacher override & audit log
│   ├── test_persistence.py # SQLite state persistence & recovery
│   ├── test_replay.py      # Archetype multi-step simulation replay
│   ├── test_service_contract.py # Engine export contract verification
│   └── test_time_travel.py # Longitudinal virtual clock forgetting curves
│
├── masteryflow.db          #  Active SQLite database with seeded students, concepts & attempts
├── requirements.txt        #  Pinned Python dependencies
├── .gitignore              #  Clean git ignore for caches, venvs, and artifacts
├── run_demo.py             #  Unified Full-Stack Launcher (boots Backend + Frontend)
├── run_api.py              #  Root shortcut to launch Backend
└── run_ui.py               #  Root shortcut to launch Frontend
```

---

##  The 4-Member Engineering Team & Role Ownership

| Member | Primary Role | Core Deliverables & Workstream |
| :--- | :--- | :--- |
| **Ayon Mukherjee** | **Team Lead, Frontend Co-Lead & Orchestrator** | 6 deterministic decision rules (`decide.py`), Teacher Command Center (`teacher.py`), Glass-Box explainability card, time-travel clock slider, 25 automated tests, live pitch & judge defense. |
| **Yash** | **ML Model & Knowledge Tracing Lead** | Bayesian Knowledge Tracing (BKT) formulation, difficulty-scaled slip/guess, multi-signal telemetry weight ($w$), Ebbinghaus exponential decay curves, and prerequisite ceiling capping. |
| **Shreyash Jha** | **Backend & Persistence Lead** | FastAPI REST service, ACID-compliant 12-table SQLite schema (`db.py`), configuration versioning, decision snapshotting (`inputs_json`), and single-command clean-boot script (`run_demo.py`). |
| **Soham Choudhury** | **Frontend Co-Lead & Question Bank Lead** | Student Experience portal, interactive DAG concept visualizer, 50 parameterized fraction questions across C1–C10 with exact `fractions.Fraction` verification, progressive hint drawer, and Streak Challenge mode. |

---

##  The Core Innovation: Moving Beyond Black-Box AI

Most existing adaptive learning systems suffer from an **explainability crisis**: they rely either on opaque deep-learning recommenders or non-deterministic LLMs that hallucinate difficulty and give unexplainable recommendations.

**MasteryFlow** introduces a **Glass-Box Psychometric Architecture**:
1. **100% Deterministic Python:** The core pedagogical decision loop runs in pure Python with **zero LLM calls** and **zero network calls**. Every recommendation is mathematically computed from stored telemetry and DAG invariants.
2. **Difficulty-Scaled Bayesian Knowledge Tracing:** Scales slip and guess parameters by question difficulty ($d \in [0, 1]$) and integrates a multi-signal evidence weight ($w$) that completely suppresses rapid guessing (<5s response time $\rightarrow w=0$).
3. **Ebbinghaus Memory Retention Decay:** Models human forgetting via $p(t) = p_{\text{floor}} + (p_0 - p_{\text{floor}}) \cdot e^{-\lambda \cdot t}$, automatically scheduling spaced retrieval review before downstream failure occurs.
4. **Institutional Human-in-the-Loop Governance:** Educators maintain ultimate authority through an interactive Teacher Command Center with 1-click persistent SQLite overrides and systemic bottleneck detection.

---

##  The Structural Curriculum Graph (C1–C10 Fractions & Ratios)

```text
[C1: Fraction Basics]
       │
       ▼
[C2: Equivalent Fractions & Simplifying]
  ┌────┼───────────────┬────────────────┐
  ▼    ▼               ▼                ▼
[C3] [C4: Add/Sub]   [C5: Mult/Div]   [C6: Ratio Basics]
  │                    │                │      │
  │                    └───────┬────────┘      │
  │                            ▼               │
  │                   [C7: Equivalent Ratios]  │
  │                            │               │
  │                            ▼               │
  └──────────────┐    [C8: Proportions]        │
                 ▼             │               │
        [C9: Percentages]      │               │
                 │             │               │
                 └──────┬──────┘               │
                        ▼                      ▼
               [C10: Capstone Multi-Step Word Problems]
```

### Structural DAG Invariants:
- **Acyclic Enforcement:** Validated with depth-first cycle detection upon initialization.
- **Recursive Prerequisite Remediation:** Traverses all upstream ancestors; if any unmastered prerequisite has $p_{\text{eff}} < 0.55$, downstream work is halted to heal the root bottleneck.
- **Prerequisite Ceiling Rule:** Effective mastery is strictly bounded by $p_{\text{eff}}[C] \le \min_{P \in \text{prereqs}}(p_{\text{eff}}[P]) + 0.25$. Any violation tags the concept as `is_fragile = True`.

---

##  The 6 Deterministic Pedagogical Rules (`backend/engine/decide.py`)

At each interaction, the decision engine evaluates six ordered rules in strict priority:
1. **Rule 0: Persistent Teacher Override (Human Authority):** Human-in-the-loop override logged in SQLite takes absolute precedence over automated algorithms.
2. **Rule 1: Teacher Intervention (Stagnation):** If $\Delta p < 0.05$ across 3 consecutive cycles on the same concept, automated loops halt and alert the teacher for 1-on-1 coaching.
3. **Rule 2: Remediate Prerequisite (Foundational Gap):** Recursive ancestor walk selects the weakest unmastered ancestor ($p_{\text{eff}} < 0.55$) to heal root gaps.
4. **Rule 3: Spaced Review (Retention Decay):** Any previously mastered concept decayed to $p_{\text{eff}} < 0.60$ triggers spaced retrieval practice (most decayed first).
5. **Rule 4: Practice (ZPD Consolidation):** Current concept not mastered ($< 0.85$), marked fragile, or transfer unverified operates within the Zone of Proximal Development.
6. **Rule 5: Advance (Next Unlocked Node):** Current concept mastered ($\ge 0.85$ with verified transfer proof) and next concept prereqs $\ge 0.55$.
7. **Rule 6: Challenge (Capstone & Acceleration):** Entire curriculum mastered or challenge mode active; serves multi-step word problems.

---

##  Quickstart & Reproduction

### Prerequisites:
- Python 3.10+
- Install dependencies:
```powershell
pip install -r requirements.txt
```

### 1. Run the Full Automated Test Suite (41 Tests 100% Green):
```powershell
pytest
```

### 2. Launch the Unified Full-Stack Application:
```powershell
python run_demo.py
```
*Automatically boots the FastAPI REST backend on port 8000 and opens the Streamlit frontend portal on **[http://localhost:8501](http://localhost:8501)**.*

### 3. Launch Frontend Only:
```powershell
python run_ui.py
# or
streamlit run frontend/app.py
```

### 4. Launch Backend API Only:
```powershell
python run_api.py
# or
python backend/run_api.py
```
*Interactive Swagger Documentation available at **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.*

### 5. Run the ML Engine Persona Simulation Runner (Yash):
```powershell
python backend/demo_ml_engine.py
```

### 6. View Pitch Playbook & Presentation Slides:
- **Presentation Deck (HTML):** Open [`docs/presentation.html`](./docs/presentation.html) in your browser.
- **Judge Defense Playbook:** [`docs/PITCH_PLAYBOOK.md`](./docs/PITCH_PLAYBOOK.md)
- **Live Demo Relay Script:** [`docs/LIVE_DEMO_SCRIPT.md`](./docs/LIVE_DEMO_SCRIPT.md)
- **Official Slide Deck:** [`docs/YUVA PPT.pptx`](./docs/YUVA%20PPT.pptx)

---

##  Summary of Automated Test Suite (Judge Defense Proofs)

| Test ID | Stress Scenario | Expected Deterministic Engine Behavior | Status |
| :--- | :--- | :--- | :---: |
| **Test 1** | Easy Streak vs. Failed Transfer | Several easy items correct ($d=0.2$), but transfer failed ($d=0.8$). Stays in Practice; transfer remains provisional. | **PASSED** |
| **Test 2** | Rapid Guessing / Spamming | Response latency $< 5$s sets evidence weight $w=0$. Mastery gain is suppressed ($< 0.01$). | **PASSED** |
| **Test 3** | Prerequisite Inconsistency | High score on C4 while C2 is 0.35. C4 capped at 0.60 and marked fragile; queues Remediate C2. | **PASSED** |
| **Test 4** | Long-Gap Memory Forgetting | Mastered C1, clock advances 21 days; retention decays $< 0.60$. Action is Spaced Review, NOT Remediate. | **PASSED** |
| **Test 5** | Persistent Teacher Override | Teacher overrides Practice C3 to Remediate C1. Written to SQLite; engine obeys; audit trail intact. | **PASSED** |
| **Test 6** | Twin Histories Divergence | Two students with identical current C3 scores receive opposite next actions due to historical decay. | **PASSED** |
| **Test 7** | Cold Start Divergence | Opposite diagnostic patterns produce divergent cognitive vectors and distinct entry points. | **PASSED** |
| **Test 8** | Decision Reproducibility | Recomputing from stored `inputs_json` snapshot produces 100% identical action, concept, and reason string. | **PASSED** |
| **Test 9** | Question Bank Exactness | All 50 fraction questions programmatically validated via `fractions.Fraction`. Zero rounding errors. | **PASSED** |
| **Test 10** | Colleague API Contract | Validates engine export contract for FastAPI REST routes, SQLite persistence, and CLI runners. | **PASSED** |

---

##  Mandatory Competition Disclosures & Limitations

### 1. Honest Disclosure of AI Tools Used:
In compliance with YUVA Megathon rules:
- **Antigravity AI Assistant** was utilized during the sprint for boilerplate generation, initial test structure authoring, and markdown documentation formatting.
- **All core algorithmic formulations**, including difficulty-scaled BKT, anti-gaming telemetry weight $w$, Ebbinghaus decay formulas, the 6 ordered rules, DAG invariants, and software architecture, were authored, designed, and verified by the **Nightfarers team**.
- The core decision engine contains **zero external generative LLM dependencies** in its execution loop.

### 2. Known Limitations & Production Roadmap:
- **Curriculum Scope:** Bounded to Fractions, Ratios, and Proportions (Concepts C1 through C10). Expanding to Algebra and Geometry is on our post-hackathon roadmap.
- **Database Engine:** Currently uses SQLite for local zero-configuration demonstration; production institutional scale requires migration to PostgreSQL.
- **Diagnostic Cold-Start:** Uses a 6-item linear diagnostic sample rather than full multi-dimensional Computerized Adaptive Testing.
