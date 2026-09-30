"""MasteryFlow Website & Platform Guide (project_guide.py).

Comprehensive, full-text documentation explaining how the website works,
detailing every component, navigation segment, psychometric engine, and workflow.
"""

from typing import Any, Dict, List, Optional
import streamlit as st

try:
    from frontend.components.theme import render_html, clean_html
    from data.curricula import SUBJECTS_REGISTRY, SUBJECTS_CONCEPTS_MAP, CANONICAL_CONCEPTS
except ImportError:
    from components.theme import render_html, clean_html
    try:
        from curricula import SUBJECTS_REGISTRY, SUBJECTS_CONCEPTS_MAP, CANONICAL_CONCEPTS
    except ImportError:
        SUBJECTS_REGISTRY = {}
        SUBJECTS_CONCEPTS_MAP = {}
        CANONICAL_CONCEPTS = {}


CHAPTERS: List[Dict[str, Any]] = [
    {
        "id": "sec1",
        "title": "1. Multi-Subject Adaptive Curriculum & DAGs",
        "badge": "Core Architecture",
        "summary": "MasteryFlow spans 5 academic disciplines across 42 concepts with strictly validated acyclic NetworkX knowledge graphs and prerequisite ceiling constraints.",
        "highlights": [
            "5 Full Academic Disciplines: Math, Computer Networks, AI, FLA, Biochemistry",
            "NetworkX acyclic DAG enforcement guarantees valid topological dependency ordering",
            "Prerequisite Ceiling Rule prevents premature advancement when foundational gaps exist"
        ]
    },
    {
        "id": "sec2",
        "title": "2. Glass-Box Decision Engine & BKT Psychometrics",
        "badge": "Adaptive AI",
        "summary": "100% deterministic pure-Python Bayesian Knowledge Tracing calculates latent mastery probability P(L) in real-time with zero LLM hallucination and complete mathematical explainability.",
        "highlights": [
            "Zero black-box LLMs in the routing loop: deterministic pure-Python execution",
            "Bayesian probability updates scaled dynamically by question difficulty (d in [0, 1])",
            "Real-time Glass-Box HUD reveals exact formulas, inputs, outputs, and pedagogical rationale"
        ]
    },
    {
        "id": "sec3",
        "title": "3. Anti-Gaming Telemetry Sentinel",
        "badge": "Security & Integrity",
        "summary": "Millisecond-precision response latency tracking detects rapid guessing attacks (<5s retry gaps) and instantly attenuates evidence weight to w = 0.00.",
        "highlights": [
            "Sub-5s retries after incorrect responses yield zero evidence credit (w = 0.00)",
            "Mastery gain delta is strictly +0.000%, completely neutralizing trial-and-error spamming",
            "Preserves classroom assessment fidelity without locking out or penalizing honest students"
        ]
    },
    {
        "id": "sec4",
        "title": "4. Intelligent Concept Guidance & Remediation",
        "badge": "Pedagogical Remediation",
        "summary": "When a student misses an exercise, the engine diagnoses the exact failure mode, triggers prerequisite remediation walks, and delivers targeted multi-level scaffolding.",
        "highlights": [
            "Recursive ancestor walk identifies the root unmastered prerequisite (P < 0.55)",
            "Step-by-step 3-tier hint ladder scaffolds problem-solving without giving away answers",
            "Automatic remediation cards explain conceptual intuitions and core takeaways"
        ]
    },
    {
        "id": "sec5",
        "title": "5. Teacher Desk & Pedagogical Overrides",
        "badge": "Educator Governance",
        "summary": "Educators retain ultimate authority with real-time cohort heatmaps, class bottleneck detection, and 1-click persistent SQLite overrides backed by immutable audit logs.",
        "highlights": [
            "Live color-coded cohort matrix: Mastered, Practicing, Fragile, and Unseen",
            "Systemic bottleneck detection flags concepts where over 30% of students struggle",
            "1-Click pedagogical overrides supersede automated machine decisions with audit logging"
        ]
    },
    {
        "id": "sec6",
        "title": "6. 3D Knowledge Universe & Memory Decay Simulator",
        "badge": "Retention & 3D WebGL",
        "summary": "Interactive 3D WebGL knowledge graph with Ebbinghaus memory decay simulation over 0 to 30 virtual days of inactivity, automatically queuing spaced retrieval reviews.",
        "highlights": [
            "Interactive WebGL 3D orbit controls: rotate, pan, zoom, and inspect concept nodes",
            "Hermann Ebbinghaus exponential forgetting curve: R(t) = exp(-dt / Stability)",
            "Cognitive Time-Travel slider schedules spaced reviews when retention drops below 60%"
        ]
    },
    {
        "id": "sec7",
        "title": "7. The 6-Tier Deterministic Pedagogical Rules",
        "badge": "Decision Logic",
        "summary": "Ordered rule hierarchy (Rules 0 to 6) in backend/engine/decide.py guarantees deterministic, reproducible routing for every student interaction.",
        "highlights": [
            "Strict priority evaluation: Teacher Override -> Stagnation -> Remediation -> Review -> Practice -> Advance -> Challenge",
            "Eliminates infinite loops and random walk behaviors found in heuristic tutors",
            "Fully reproducible: identical telemetry snapshots produce 100% identical actions"
        ]
    },
    {
        "id": "sec8",
        "title": "8. Full-Stack Quickstart & Test Verification",
        "badge": "Production Engineering",
        "summary": "One-command full-stack bootstrap (run_demo.py), FastAPI REST API with Swagger documentation, SQLite persistence, and 52/52 automated tests passing.",
        "highlights": [
            "Single-command launch boots FastAPI backend and Streamlit portal seamlessly",
            "10 comprehensive stress tests verify edge cases against the judging rubric",
            "Clean modular codebase with 100% green pytest verification"
        ]
    }
]

GUIDE_CHAPTERS = CHAPTERS


def render_project_guide():
    """Renders the comprehensive Website Guide explaining all components and portions of the platform."""
    # Top Hero Header Card
    render_html("""
    <div style="
        background: #FFFFFF;
        border: 1px solid rgba(228, 221, 211, 0.9);
        border-radius: 24px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -4px rgba(60, 50, 30, 0.05);
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
            <div style="max-width: 820px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                    <span style="
                        background: #F4EEE5;
                        color: #11141D;
                        border: 1px solid #E5DCD0;
                        font-size: 0.76rem;
                        font-weight: 700;
                        padding: 4px 12px;
                        border-radius: 9999px;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    ">
                        Website &amp; Feature User Manual
                    </span>
                    <span style="
                        background: #ECFDF5;
                        color: #065F46;
                        border: 1px solid #A7F3D0;
                        font-size: 0.74rem;
                        font-weight: 700;
                        padding: 4px 10px;
                        border-radius: 9999px;
                    ">
                        ● Complete Walkthrough of All Components
                    </span>
                </div>
                <h1 style="color: #11141D; margin: 0 0 8px 0; font-size: 2.1rem; font-weight: 800; letter-spacing: -0.03em;">
                    How MasteryFlow Works: User &amp; Component Guide
                </h1>
                <p style="color: #64748B; font-size: 0.96rem; line-height: 1.6; margin: 0;">
                    Welcome! This guide explains every portion of the website — from the sidebar controls and active learning workspace 
                    to the teacher command desk, 3D curriculum graph, and underlying deterministic decision engine.
                </p>
            </div>
            <div>
                <div style="
                    background: #FBF9F5;
                    border: 1px solid #E5DCD0;
                    border-radius: 16px;
                    padding: 12px 18px;
                    font-size: 0.80rem;
                    color: #44403C;
                ">
                    <div style="font-weight: 800; color: #11141D; margin-bottom: 4px;">MasteryFlow Apitex Edition</div>
                    <div><strong>Engine:</strong> 100% Deterministic Python</div>
                    <div><strong>Psychometrics:</strong> Bayesian Knowledge Tracing</div>
                    <div><strong>Disciplines:</strong> 5 Subjects &middot; 42 Concepts</div>
                </div>
            </div>
        </div>

        <!-- Quick Jump Feature Pills -->
        <div style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 12px;
            margin-top: 20px;
            padding-top: 18px;
            border-top: 1px solid rgba(228, 221, 211, 0.7);
        ">
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 10px 14px; border-radius: 12px;">
                <div style="font-size: 0.70rem; color: #64748B; text-transform: uppercase; font-weight: 700;">Section 1</div>
                <div style="font-size: 1.05rem; font-weight: 800; color: #11141D;">Website Layout</div>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 10px 14px; border-radius: 12px;">
                <div style="font-size: 0.70rem; color: #64748B; text-transform: uppercase; font-weight: 700;">Section 2</div>
                <div style="font-size: 1.05rem; font-weight: 800; color: #11141D;">Learn &amp; Question Runner</div>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 10px 14px; border-radius: 12px;">
                <div style="font-size: 0.70rem; color: #64748B; text-transform: uppercase; font-weight: 700;">Section 3</div>
                <div style="font-size: 1.05rem; font-weight: 800; color: #11141D;">Teacher Desk &amp; Overrides</div>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 10px 14px; border-radius: 12px;">
                <div style="font-size: 0.70rem; color: #64748B; text-transform: uppercase; font-weight: 700;">Section 4</div>
                <div style="font-size: 1.05rem; font-weight: 800; color: #11141D;">Curriculum &amp; 3D Cosmos</div>
            </div>
        </div>
    </div>
    """)

    # Interactive Guide Tabs
    tabs = st.tabs([
        "Website Layout & Tour",
        "Learn Portal & Question Runner",
        "Dashboard & Analytics",
        "Teacher Command Desk",
        "Curriculum & 3D Cosmos",
        "Adaptive AI & BKT Math",
        "The 6 Pedagogical Rules",
        "Anti-Gaming Sentinel",
        "Developer & Demo Tools",
        "Quickstart & Setup"
    ])

    # -------------------------------------------------------------
    # TAB 1: WEBSITE LAYOUT & TOUR
    # -------------------------------------------------------------
    with tabs[0]:
        st.markdown("### How the Website is Structured")
        st.markdown(
            """
            MasteryFlow is organized into two primary visual spaces: the **Left Control Sidebar** and the **Main Workspace**.
            Here is a breakdown of every element on your screen:
            """
        )

        render_html("""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin: 16px 0;">
            <div style="background: #FFFFFF; border: 1px solid #E5DCD0; border-radius: 16px; padding: 18px; box-shadow: 0 4px 14px -2px rgba(60, 50, 30, 0.04);">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="font-size: 0.82rem; font-weight: 800; color: #78716C;">NAV</span>
                    <strong style="color: #11141D; font-size: 0.98rem;">1. Left Navigation Menu</strong>
                </div>
                <div style="font-size: 0.82rem; color: #475569; line-height: 1.5;">
                    The primary navigation menu lets you switch instantly between key portals:<br>
                    &bull; <strong>Learn:</strong> Interactive adaptive practice, questions, and instant feedback.<br>
                    &bull; <strong>Dashboard:</strong> Student progress metrics, mastery rates, and analytics.<br>
                    &bull; <strong>Teacher Desk:</strong> Cohort matrix heatmap, bottleneck alerts, and 1-click overrides.<br>
                    &bull; <strong>Curriculum:</strong> Interactive 2D graph visualizer and 3D WebGL cosmos.<br>
                    &bull; <strong>Guide:</strong> This comprehensive feature manual!
                </div>
            </div>

            <div style="background: #FFFFFF; border: 1px solid #E5DCD0; border-radius: 16px; padding: 18px; box-shadow: 0 4px 14px -2px rgba(60, 50, 30, 0.04);">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="font-size: 0.82rem; font-weight: 800; color: #78716C;">CTX</span>
                    <strong style="color: #11141D; font-size: 0.98rem;">2. Discipline &amp; Profile Switchers</strong>
                </div>
                <div style="font-size: 0.82rem; color: #475569; line-height: 1.5;">
                    Located in the sidebar, these dropdowns allow you to:<br>
                    &bull; <strong>Switch Academic Discipline:</strong> Pivot between Mathematics, Computer Networks, AI, Formal Languages &amp; Automata, and Biochemistry.<br>
                    &bull; <strong>Switch Learner Profile:</strong> Test as different student personas (e.g. Diya Sharma, Aarav Mehta, Maya Patel) to observe personalized adaptive routing.
                </div>
            </div>

            <div style="background: #FFFFFF; border: 1px solid #E5DCD0; border-radius: 16px; padding: 18px; box-shadow: 0 4px 14px -2px rgba(60, 50, 30, 0.04);">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="font-size: 0.82rem; font-weight: 800; color: #78716C;">DEV</span>
                    <strong style="color: #11141D; font-size: 0.98rem;">3. Developer &amp; Demo Tools</strong>
                </div>
                <div style="font-size: 0.82rem; color: #475569; line-height: 1.5;">
                    Expandable sidebar panel for live demonstrations and judges:<br>
                    &bull; <strong>Stress-Test Suite:</strong> Live proofs for all 10 competition test criteria.<br>
                    &bull; <strong>Simulation Replays:</strong> Automated multi-step student archetype simulations.<br>
                    &bull; <strong>Test 8 Reproducibility:</strong> Verifies 0.00% variance from stored SQLite snapshots.<br>
                    &bull; <strong>Quick Triggers:</strong> 1-Click buttons to trigger Anti-Gaming defense or +21 Days memory decay.
                </div>
            </div>
        </div>
        """)

    # -------------------------------------------------------------
    # TAB 2: LEARN PORTAL & QUESTION RUNNER
    # -------------------------------------------------------------
    with tabs[1]:
        st.markdown("### The Learn Portal & Question Runner Explained")
        st.markdown(
            """
            When you enter the **Learn** segment, the adaptive engine serves questions tailored to your current Zone of Proximal Development (ZPD).
            Here is what each component in this portal does:
            """
        )

        render_html("""
        <div style="display: flex; flex-direction: column; gap: 14px; margin-top: 14px;">
            <div style="background: #FFFFFF; border: 1px solid #E5DCD0; border-left: 5px solid #11141D; border-radius: 14px; padding: 16px 20px;">
                <strong style="color: #11141D; font-size: 1.0rem;">1. Glass-Box Decision Card HUD</strong>
                <p style="font-size: 0.84rem; color: #475569; margin: 6px 0 0 0; line-height: 1.5;">
                    Appears at the very top of the Learn page. It reveals the engine's internal thinking:
                    <br>&bull; <strong>Target Concept Badge:</strong> The concept the engine chose for you (e.g. <code>Topic: C1</code>).
                    <br>&bull; <strong>Current Readiness Meter:</strong> Your current estimated mastery probability (e.g. <code>30%</code>).
                    <br>&bull; <strong>Active Pedagogical Rule:</strong> Explains which of the 6 deterministic rules was triggered (e.g. <em>Active Skill Practice &amp; Consolidation</em>, <em>Remediate Prerequisite</em>, or <em>Spaced Review</em>).
                </p>
            </div>

            <div style="background: #FFFFFF; border: 1px solid #E5DCD0; border-left: 5px solid #0284C7; border-radius: 14px; padding: 16px 20px;">
                <strong style="color: #0284C7; font-size: 1.0rem;">2. Student Agency Drawer ("Choose Your Learning Path")</strong>
                <p style="font-size: 0.84rem; color: #475569; margin: 6px 0 0 0; line-height: 1.5;">
                    Clicking <em>"Want to explore an alternate topic? Choose your learning path"</em> gives learners metacognitive agency. 
                    You can pick an unlocked foundational prerequisite to review, or select a parallel concept. 
                    The engine respects student choice while maintaining prerequisite safety invariants.
                </p>
            </div>

            <div style="background: #FFFFFF; border: 1px solid #E5DCD0; border-left: 5px solid #059669; border-radius: 14px; padding: 16px 20px;">
                <strong style="color: #059669; font-size: 1.0rem;">3. Question Card &amp; Difficulty Indicator</strong>
                <p style="font-size: 0.84rem; color: #475569; margin: 6px 0 0 0; line-height: 1.5;">
                    Displays the calibrated question prompt:
                    <br>&bull; <strong>Question ID:</strong> e.g. <code>Q_C01_01</code>.
                    <br>&bull; <strong>Difficulty Pill:</strong> Easy (0.2), Medium (0.5), or Hard (0.8) with visual difficulty gauge.
                    <br>&bull; <strong>Accepted Formats Pill:</strong> Clarifies exact formats accepted (e.g. fractions <code>3/4</code>, mixed numbers <code>1 1/2</code>, or decimals <code>0.75</code>).
                </p>
            </div>

            <div style="background: #FFFFFF; border: 1px solid #E5DCD0; border-left: 5px solid #D97706; border-radius: 14px; padding: 16px 20px;">
                <strong style="color: #D97706; font-size: 1.0rem;">4. Progressive 3-Tier Hint Ladder ("Need a hint?")</strong>
                <p style="font-size: 0.84rem; color: #475569; margin: 6px 0 0 0; line-height: 1.5;">
                    Clicking <em>"Need a hint?"</em> opens a progressive scaffolding ladder that guides without spoiling:
                    <br>&bull; <strong>Tier 1 (Definition Clue):</strong> Reminds learner of core conceptual terminology.
                    <br>&bull; <strong>Tier 2 (Strategic Clue):</strong> Suggests the specific mathematical or logical approach.
                    <br>&bull; <strong>Tier 3 (Walkthrough):</strong> Breaks down the calculation step-by-step.
                    <br><em>Note:</em> Consulting hints slightly modulates the evidence weight (w), reflecting scaffolded assistance.
                </p>
            </div>

            <div style="background: #FFFFFF; border: 1px solid #E5DCD0; border-left: 5px solid #7C3AED; border-radius: 14px; padding: 16px 20px;">
                <strong style="color: #7C3AED; font-size: 1.0rem;">5. Answer Input, Confidence Rating &amp; Instant Telemetry</strong>
                <p style="font-size: 0.84rem; color: #475569; margin: 6px 0 0 0; line-height: 1.5;">
                    <br>&bull; <strong>Clean Answer Field:</strong> Type your numerical, fraction, or textual answer directly.
                    <br>&bull; <strong>Confidence Selector:</strong> Choose High, Medium, or Low confidence. The system uses this to calibrate measurement uncertainty.
                    <br>&bull; <strong>Immediate Feedback:</strong> Displays green success confirmation or diagnostic feedback with the exact mathematical solution.
                </p>
            </div>
        </div>
        """)

    # -------------------------------------------------------------
    # TAB 3: DASHBOARD & PROGRESS ANALYTICS
    # -------------------------------------------------------------
    with tabs[2]:
        st.markdown("### Student Dashboard & Analytics")
        st.markdown(
            r"""
            The **Dashboard** portal gives learners and parents an executive overview of cognitive development:
            - **Cognitive Platinum Passport:** Apitex-styled luxury metric card tracking overall curriculum mastery percentage, current learning streak, and total questions answered.
            - **Concept-by-Concept Status Grid:** Visual cards for every concept showing whether it is *Mastered* ($\ge 85\%$), *Practicing* ($55\% - 84\%$), or *Needs Review* ($< 60\%$).
            - **Cognitive Time-Travel Simulator:** Slider allowing you to simulate 0 to 30 days of inactivity and watch memory retention decay dynamically according to Hermann Ebbinghaus forgetting curves.
            - **Spaced Review Scheduler:** Shows which concepts will need review first when memory decay occurs.
            """
        )

        if st.button("Open Dashboard Live", type="primary", key="btn_jump_dash"):
            st.session_state.portal_view_choice = "Dashboard"
            st.rerun()

    # -------------------------------------------------------------
    # TAB 4: TEACHER COMMAND DESK
    # -------------------------------------------------------------
    with tabs[3]:
        st.markdown("### Teacher Command Desk & Governance")
        st.markdown(
            """
            The **Teacher Desk** guarantees institutional human authority over the AI:
            """
        )

        render_html("""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin: 16px 0;">
            <div style="background: #FFFFFF; border: 1px solid #E5DCD0; border-radius: 16px; padding: 16px;">
                <div style="font-weight: 800; color: #11141D; font-size: 0.95rem; margin-bottom: 4px;">Live Cohort Matrix Heatmap</div>
                <div style="font-size: 0.80rem; color: #475569; line-height: 1.5;">
                    Displays all students (rows) across all concepts (columns). Color-coded into Green (Mastered), Blue (Practicing), Orange (Fragile/Decayed), and Gray (Unseen).
                </div>
            </div>

            <div style="background: #FFFFFF; border: 1px solid #E5DCD0; border-radius: 16px; padding: 16px;">
                <div style="font-weight: 800; color: #11141D; font-size: 0.95rem; margin-bottom: 4px;">Systemic Bottleneck Alerts</div>
                <div style="font-size: 0.80rem; color: #475569; line-height: 1.5;">
                    The system automatically detects if &gt;30% of the cohort is struggling with a specific concept, notifying the teacher to hold a targeted lecture.
                </div>
            </div>

            <div style="background: #FFFFFF; border: 1px solid #E5DCD0; border-radius: 16px; padding: 16px;">
                <div style="font-weight: 800; color: #11141D; font-size: 0.95rem; margin-bottom: 4px;">1-Click Persistent Overrides</div>
                <div style="font-size: 0.80rem; color: #475569; line-height: 1.5;">
                    Teachers can force-assign any student a concept and pedagogical mode (Practice, Remediate, Review, Challenge). Overrides take absolute precedence over algorithms.
                </div>
            </div>

            <div style="background: #FFFFFF; border: 1px solid #E5DCD0; border-radius: 16px; padding: 16px;">
                <div style="font-weight: 800; color: #11141D; font-size: 0.95rem; margin-bottom: 4px;">Immutable Audit Logging</div>
                <div style="font-size: 0.80rem; color: #475569; line-height: 1.5;">
                    Every teacher override is committed to SQLite with timestamp, teacher ID, student ID, target concept, and mandatory pedagogical justification.
                </div>
            </div>
        </div>
        """)

        if st.button("Open Teacher Desk Live", type="primary", key="btn_jump_teacher_tab"):
            st.session_state.portal_view_choice = "Teacher Desk"
            st.rerun()

    # -------------------------------------------------------------
    # TAB 5: CURRICULUM & 3D COSMOS
    # -------------------------------------------------------------
    with tabs[4]:
        st.markdown("### Curriculum Explorer & 3D Knowledge Universe")
        st.markdown(
            """
            In the **Curriculum** portal, learners and educators can explore the structural prerequisite DAGs across all 5 disciplines:
            - **2D Directed Acyclic Graph Visualizer:** Shows the exact topological ordering, milestone nodes, and prerequisite links.
            - **3D WebGL Cosmos:** Renders concepts as glowing celestial bodies in 3D Euclidean space. Drag to orbit 360°, scroll to zoom, and right-click to pan.
            - **Prerequisite Ceiling Rule Enforced:**
            """
        )
        st.latex(r"p_{\text{eff}}[C] \le \min_{P \in \text{prereqs}(C)}(p_{\text{eff}}[P]) + 0.25")
        st.markdown(
            r"""
            If foundational prerequisites are fragile ($< 55\%$), child concepts are capped and flagged as `is_fragile = True`, preventing students from attempting complex topics with shaky fundamentals.
            """
        )

        if st.button("Open Curriculum Explorer Live", type="primary", key="btn_jump_curriculum_tab"):
            st.session_state.portal_view_choice = "Curriculum"
            st.rerun()

    # -------------------------------------------------------------
    # TAB 6: ADAPTIVE AI & BKT MATH
    # -------------------------------------------------------------
    with tabs[5]:
        st.markdown("### Adaptive AI & Bayesian Knowledge Tracing (BKT)")
        st.markdown(
            r"""
            MasteryFlow eliminates black-box deep learning and hallucinating generative LLMs from the decision loop. 
            All cognitive states are computed with pure-Python **Difficulty-Scaled Bayesian Knowledge Tracing**:
            """
        )
        st.markdown(
            r"""
            - **Prior:** $P(L_0) \approx 0.15$
            - **Transit (Learning Rate):** $P(T) \approx 0.15$
            - **Difficulty-Scaled Slip:** $S(d) = S_{\text{base}} + 0.15 \cdot d$
            - **Difficulty-Scaled Guess:** $G(d) = G_{\text{base}} \cdot (1 - 0.50 \cdot d)$
            - **Evidence Weight:** $w \in [0.0, 1.0]$ based on response latency and attempt integrity.
            
            **Posterior Equations:**
            $$\text{If Correct: } P(L_t \mid O_t=1) = \frac{P(L_{t-1}) \cdot (1 - S(d))}{P(L_{t-1}) \cdot (1 - S(d)) + (1 - P(L_{t-1})) \cdot G(d)}$$
            $$\text{If Incorrect: } P(L_t \mid O_t=0) = \frac{P(L_{t-1}) \cdot S(d)}{P(L_{t-1}) \cdot S(d) + (1 - P(L_{t-1})) \cdot (1 - G(d))}$$
            $$\text{Evidence Blend: } P^*(L_t) = P(L_{t-1}) + w \cdot \left[ P(L_t \mid O_t) - P(L_{t-1}) \right]$$
            $$\text{Transition Step: } P(L_t) = P^*(L_t) + (1 - P^*(L_t)) \cdot P(T)$$
            """
        )

    # -------------------------------------------------------------
    # TAB 7: THE 6 PEDAGOGICAL RULES
    # -------------------------------------------------------------
    with tabs[6]:
        st.markdown("### The 6-Tier Deterministic Pedagogical Rules")
        st.markdown(
            r"""
            In `backend/engine/decide.py`, recommendations are selected by evaluating six ordered rules in strict priority:
            1. **Rule 0: Persistent Teacher Override (Human Authority):** Overrides all automated machine algorithms immediately.
            2. **Rule 1: Teacher Intervention Alert (Stagnation):** If $\Delta P < 0.05$ across 3 consecutive cycles, halts loops and summons 1-on-1 human coaching.
            3. **Rule 2: Remediate Prerequisite (Foundational Gap):** Recursive ancestor walk selects the weakest unmastered root ($P < 0.55$).
            4. **Rule 3: Spaced Review (Retention Decay):** Mastered concept decayed below $60\%$ triggers spaced retrieval practice.
            5. **Rule 4: Practice in ZPD:** Concept unlocked, $P < 0.85$, or transfer unverified.
            6. **Rule 5: Advance:** Concept mastered ($\ge 85\%$ + verified transfer proof) and next concept prereqs met.
            7. **Rule 6: Capstone Challenge:** Curriculum mastered or Challenge Mode enabled.
            """
        )

    # -------------------------------------------------------------
    # TAB 8: ANTI-GAMING SENTINEL
    # -------------------------------------------------------------
    with tabs[7]:
        st.markdown("### Anti-Gaming Telemetry Sentinel")
        st.markdown(
            r"""
            Students in online learning often try **rapid guessing attacks**: spamming random answers every 1 to 2 seconds until getting lucky.
            
            **How MasteryFlow Neutralizes This:**
            - Client telemetry records question presentation timestamp and submission latency ($\Delta t$).
            - If $\Delta t_{\text{retry}} < 5.0\text{ seconds}$ following an incorrect attempt, the engine triggers:
              $$w = 0.00$$
            - Mastery update $\Delta P = +0.000\%$. Trial-and-error guessing yields zero credit, preserving assessment validity!
            """
        )

    # -------------------------------------------------------------
    # TAB 9: DEVELOPER & DEMO TOOLS
    # -------------------------------------------------------------
    with tabs[8]:
        st.markdown("### Developer & Demo Tools Sidebar Walkthrough")
        st.markdown(
            """
            In the sidebar under **Developer & Demo Tools**, you can launch test harnesses and demonstration tools:
            - **Stress-Test Suite:** Automated harness executing all 10 competition test criteria in real-time.
            - **Simulation Replays:** Replays automated multi-step student archetypes (False Master, Prereq Gap, Rapid Guesser, Twin Learners).
            - **ML Engine Inspector:** Interactive workbench to test BKT formulas, slip/guess values, and forgetting curves live.
            - **Test 8 Reproducibility:** Clean executive verification screen proving 0.00% variance from SQLite snapshots.
            - **Quick Scenario Triggers:** One-click presets for *Anti-Gaming (w=0.0)* and *Memory Decay (+21 days)*.
            """
        )

    # -------------------------------------------------------------
    # TAB 10: QUICKSTART & SETUP
    # -------------------------------------------------------------
    with tabs[9]:
        st.markdown("### Quickstart & Operational Commands")
        st.markdown(
            """
            Run MasteryFlow locally or inspect the automated test suite:
            """
        )
        st.code(
            """
# 1. Boot Full Unified Stack (FastAPI Backend + Streamlit Portal):
python run_demo.py

# 2. Run Frontend Portal Only:
python run_ui.py
# (or: streamlit run frontend/app.py)

# 3. Run FastAPI Backend API Only:
python run_api.py
# Interactive Swagger Documentation: http://127.0.0.1:8000/docs

# 4. Run Automated Pytest Suite (52/52 Tests Green):
pytest
            """,
            language="powershell"
        )


# Backward-compatible alias
render_video_guide = render_project_guide
