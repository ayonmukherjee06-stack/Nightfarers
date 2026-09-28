# MasteryFlow: 12-Slide Pitch Deck Architecture

**YUVA Megathon 2026 | SRMIST Trichy | EduGenAI Track (Domain 4)**  
**Project:** MasteryFlow: Explainable Adaptive Learning and Intervention Engine  
**Team Name:** Nightfarers | **Team Leader:** Ayon Mukherjee (+91 8102429090)  
**Team Members:** Yash (ML Lead), Shreyash Jha (Backend Lead), Soham Choudhury (Frontend Co-Lead), Ayon Mukherjee (Lead & Orchestrator)

---

## Slide 1: Title & Hook
- **Title:** MasteryFlow: Explainable Adaptive Learning & Intervention Engine
- **Subtitle:** Moving from Black-Box AI to Deterministic, Psychometrically Auditable EdTech
- **Visuals:** Dual-view screenshot: Student Glass-Box "Why This Next?" card alongside Teacher Cohort Heatmap.
- **Presenter:** Ayon Mukherjee (Lead)
- **Key Talking Point:** "EdTech AI has an explainability crisis. When an algorithm pushes a student backward or forward without proof, students disengage and teachers lose trust. MasteryFlow replaces black-box guessing with transparent, deterministic mathematics."

---

## Slide 2: The Problem: The High Cost of Black-Box EdTech
- **Pain Point 1 (Student):** Arbitrary recommendations with no rationale ("Why am I practicing this again?").
- **Pain Point 2 (Teacher):** Zero visibility into root misconceptions; teachers cannot override black-box models.
- **Pain Point 3 (Pedagogical):** Disconnected problem lists ignore foundational prerequisite chains.
- **Hard Data:** 68% of adaptive learning dropouts cite frustration with unexplainable difficulty jumps.

---

## Slide 3: The Solution: Glass-Box Adaptive Architecture
- **Three Core Pillars:**
  1. **Algorithmic Transparency:** 100% deterministic Python decision loop. Zero LLM hallucinations.
  2. **Psychometric Rigor:** Bayesian Knowledge Tracing (BKT) with difficulty scaling, multi-signal telemetry weight ($w$), and Ebbinghaus memory decay.
  3. **Human-in-the-Loop Authority:** Institutional Teacher Command Center with 1-click persistent SQLite overrides.

---

## Slide 4: Structural Knowledge Graph (C1–C10 Fractions & Ratios)
- **Visual:** Validated NetworkX Directed Acyclic Graph (DAG) starting at C1 (Fraction basics) and culminating in C10 (Proportion word problems).
- **Graph Invariant:** Recursive upstream prerequisite edge traversal. A student cannot comprehend child node $C$ if ancestral node $P$ has $p_{\text{eff}}[P] < 0.55$.
- **Prerequisite Ceiling Rule:** $p_{\text{eff}}[C] \le \min(p_{\text{eff}}[\text{prereqs}]) + 0.25$. Any violation flags the node as `fragile`.

---

## Slide 5: The Cognitive Engine: Yash's BKT & Decay Formulation
- **Difficulty-Scaled Slip & Guess:** $s(d) = s_0 + 0.10 \cdot d$, $g(d) = g_0 \cdot (1 - 0.5 \cdot d)$.
- **Multi-Signal Telemetry Weight ($w \in [0, 1]$):** Penalizes rapid guessing (<5s latency $\rightarrow w=0$) and hints used ($w = \max(0, 1 - 0.25 \cdot \text{hints})$).
- **Ebbinghaus Memory Decay:** $p(t) = p_{\text{floor}} + (p_0 - p_{\text{floor}}) \cdot e^{-\lambda \cdot t}$. Automatically decays past mastery over elapsed calendar days.

---

## Slide 6: The 6 Deterministic Pedagogical Rules
- **Rule Hierarchy (Priority Order):**
  1. *Teacher Intervention:* Stagnation ($\Delta p < 0.05$ across 3 cycles) $\rightarrow$ halts automated loop; alerts teacher.
  2. *Remediate Prerequisite:* Recursive walk finds weakest unmastered ancestor ($p_{\text{eff}} < 0.55$).
  3. *Spaced Review:* Previously mastered concept decayed to $p_{\text{eff}} < 0.60$ (most decayed first).
  4. *Practice:* Current concept not mastered ($< 0.85$), fragile, or transfer unverified.
  5. *Advance:* Mastered ($\ge 0.85$ with transfer verified) and next concept prereqs $\ge 0.55$.
  6. *Challenge:* Curriculum mastered or challenge mode active.

---

## Slide 7: Glass-Box Explainability in Action
- **Dual Perspectives:**
  - **Student View:** "You are practicing C7, but your mastery of prerequisite C2 is currently 42%. Strengthening C2 first guarantees success!"
  - **Teacher Snapshot:** Serialized `inputs_json` capturing $p_{\text{eff}}$, recent errors, hint count, latency, and rule ID.

---

## Slide 8: Teacher Command Center & Systemic Bottlenecks
- **Visual:** Cohort Matrix (Students $\times$ Concepts C1–C10) with color-coded heat cells.
- **Systemic Bottleneck Detector:** Flags when $\ge 25\%$ of cohort has $p < 0.55$ on a foundational concept (e.g., C2), advising teacher to conduct a targeted mini-lecture before downstream assignments.
- **Stuck-Learner Queue:** Direct escalation card with 1-click persistent override modal.

---

## Slide 9: Technical Innovations
- **Innovation (a): Information-Gain Adaptive Item Selection:** Shannon entropy reduction and Fisher Item Information selects questions matching student ZPD ($d \approx p$).
- **Innovation (b): Student Self-Regulated Agency:** "Request Different Action" modal allowing students to express learning preferences, logged to SQLite.
- **Innovation (c): Virtual Clock Time Travel:** Slider advancing calendar days live to demonstrate Ebbinghaus forgetting triggering spaced retrieval.

---

## Slide 10: System Architecture & Persistence
- **Visual:** 3-Tier Architecture Diagram (Streamlit Frontend $\leftrightarrow$ FastAPI REST Service $\leftrightarrow$ SQLite 9-Table Database $\leftrightarrow$ Pure Python Decision Core).
- **Reproducibility Invariant (Test 8):** Every decision is recomputed from stored `inputs_json` with zero variance.

---

## Slide 11: Verification: 25 Automated Tests & Judge Stress Proofs
- **Test Suite Proofs:**
  - Test 1: Easy Streak vs. Failed Transfer (stays in Practice).
  - Test 2: Rapid Guessing Telemetry Suppression ($w = 0$).
  - Test 3: Prerequisite Inconsistency & Fragile Flag.
  - Test 4: Long-Gap Memory Forgetting (Triggers Review, not Remediate).
  - Test 5: Persistent Teacher Override in SQLite.
  - Test 6: Twin Histories Divergence.
  - Test 7: Cold Start Diagnostic Divergence.
  - Test 8: Decision Snapshot Reproducibility (100% Identical).
- **Execution Speed:** 25/25 Tests Pass in < 0.6 seconds under `pytest`.

---

## Slide 12: Business Impact, Scalability & Roadmap
- **Institutional Market:** Deployable to K-12 schools, higher-ed STEM departments, and competitive exam test prep.
- **Offline & Low-Bandwidth Resilience:** Pure Python decision engine requires zero external API tokens or GPU infrastructure.
- **Summary:** MasteryFlow transforms adaptive learning into a trustworthy, explainable partnership between student, teacher, and psychometric science.
