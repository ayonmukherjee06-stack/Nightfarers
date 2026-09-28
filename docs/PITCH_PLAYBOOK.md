# 🏆 MasteryFlow: Hackathon Pitch & Judge Defense Playbook
**YUVA Megathon 2026 | Domain 4: Intelligent Educational Systems**  
**Team Nightfarers:** Ayon Mukherjee (Lead), Yash (ML Lead), Soham Choudhury (Frontend Lead), Shreyash Jha (Backend Lead)

---

## ⏱️ Part 1: The 30-Second Elevator Pitch (The Hook)

> *"Good afternoon, judges. Today, most adaptive learning platforms fail students in two ways:*  
> *1. They use **black-box LLMs** that hallucinate difficulty and can't explain why a question was picked.*  
> *2. They fall victim to **brute-force guessing** and ignore **longitudinal human forgetting**.*  
> 
> *We built **MasteryFlow**: a 100% deterministic, explainable adaptive learning engine for middle-school mathematics. Powered by difficulty-scaled Bayesian Knowledge Tracing, Ebbinghaus forgetting curves, and anti-gaming telemetry, MasteryFlow guarantees that every pedagogical decision is mathematically reproducible with zero variance, zero hallucination, and full teacher-in-the-loop governance."*

---

## 🎬 Part 2: The 3-Minute Live Demo Sequence (Step-by-Step Clicks)

When presenting at your table or stage, follow this exact sequence:

### Step 1: Open `http://localhost:8501` (Student Experience - 45s)
1. **Highlight the UI:** Point to the 2026 Dark Glass interface, the Active Streak flame, and the **"Why This Next?"** transparent explainability card.
2. **Key Talking Point:**  
   *"Notice that the student sees the exact mathematical reason why Concept C1 was chosen under Rule 4. No black boxes."*
3. **Trigger Anti-Gaming Defense:** Click sidebar `⚡ 1-Click Jury Demo Presets` $\to$ **Preset 1 (Anti-Gaming Defense)**.
4. **Point to Telemetry Card:**  
   *"Look at the telemetry HUD: When an adversarial student guesses in under 1.5 seconds, evidence weight $w$ drops to exactly 0.0. The lucky guess earns zero unearned mastery."*

### Step 2: Longitudinal Ebbinghaus Time Travel (45s)
1. **Trigger Time Travel:** Click sidebar $\to$ **Preset 3 (Memory Time Travel +21d Decay)**.
2. **Observe the Engine Pivot:**  
   *"Diya mastered this concept 3 weeks ago. Watch how the engine does not treat mastery as a permanent badge. Over 21 days of inactivity, her effective mastery $p_{\text{eff}}$ decayed below 60%. The engine immediately pivoted from Practice to **Rule 3: Spaced Review** to arrest forgetting before she fails downstream."*

### Step 3: Prerequisite Inconsistency & Ceiling Capping (45s)
1. **Trigger Prerequisite Collapse:** Click sidebar $\to$ **Preset 2 (Prereq Collapse)**.
2. **Observe Concept Knowledge Tree (DAG):**  
   Switch to tab **"Concept Knowledge Tree (DAG)"**.
   *"Alex attempted advanced fraction addition (C4) with raw score 0.88. But his foundational equivalence (C2) collapsed to 0.35. Our mathematical invariant caps C4 at $\min(\text{prereqs}) + 0.25 = 0.60$, flags it as Fragile, and immediately forces upstream remediation on C2."*

### Step 4: Teacher Command Center & Human Override (45s)
1. Switch sidebar to **"👩‍🏫 Teacher Command Center & Cohort Deck"**.
2. **Show Systemic Bottlenecks:**  
   *"The educator gets an aggregate cohort heatmap across all 10 canonical concepts. Notice the Red Alert: C2 is a systemic bottleneck blocking 3 downstream topics for 33% of the class. Instead of 30 individual interventions, the teacher conducts a 10-minute mini-lecture."*
3. **Show 1-Click Persistent Override:**  
   *"If the teacher knows better from an in-person quiz, they apply a 1-click override. It writes to SQLite and immediately supersedes the algorithm, recorded in an immutable audit log."*

---

## 🛡️ Part 3: The 5 Hardest Judge Questions & Winning Defenses

### Q1: *"Why didn't you just use GPT-4 or Claude to recommend the next problem?"*
> **Winning Answer:**  
> *"In safety-critical domains like education, LLMs are fundamentally unsuitable for the decision loop for three reasons:*  
> *1. **Non-deterministic drift:** The same student profile can get different recommendations on different days.*  
> *2. **Hallucinated prerequisites:** LLMs cannot enforce mathematical DAG ceiling bounds.*  
> *3. **Cost and latency:** MasteryFlow runs in under 10 milliseconds purely in Python with zero API costs, zero internet requirements, and 100% reproducible test proofs (Test 8)."*

### Q2: *"How do you prevent students from gaming the system by trial-and-error?"*
> **Winning Answer:**  
> *"We track multi-signal telemetry through four signals: response latency, retry gap, hint access count, and metacognitive confidence. If a student retries in $<5$ seconds, evidence weight $w$ clamps to 0.0. Hints attenuate evidence exponentially by $0.5^{\text{hints}}$. A student cannot brute-force their way to a mastery badge without verified deliberate practice."*

### Q3: *"What is the 'Transfer Failure Barrier'?"*
> **Winning Answer:**  
> *"Many students learn to solve simple procedural items by pattern matching (e.g. difficulty $d=0.2$). In MasteryFlow, high accuracy on easy items only grants **Provisional Mastery**. To achieve Certified Mastery, the student must pass a novel transfer problem ($d \ge 0.70$). If they fail, Rule 4 locks them in practice until deep conceptual understanding is verified."*

### Q4: *"How do you prove Test 8 (Reproducibility)?"*
> **Winning Answer:**  
> *"Every single decision logs an immutable `inputs_snapshot` JSON blob into SQLite containing the student's exact concept vector, config hyperparameters, and DAG state. We have an automated test (`test_decision_reproducibility_from_snapshot`) that re-runs the decision from the snapshot and asserts with 0.00% variance that the exact same action, target concept, and explanation string are generated."*

### Q5: *"Can your system work offline without internet?"*
> **Winning Answer:**  
> *"Yes, 100%. Both our FastAPI backend and Streamlit UI run entirely on localhost using SQLite and pure Python standard math libraries (`fractions.Fraction`, `math`, `networkx`). You can pull the ethernet cord right now and the entire system operates with zero latency."*

---

## 📊 Part 4: Automated Test Suite Summary (Show this table to Judges!)

Run in terminal: `pytest masteryflow/tests/ -v`

| Test Category | Test Count | Key Invariant Verified |
| :--- | :---: | :--- |
| **Engine Decision Rules** | 14 Tests | Strict priority hierarchy: Override $\to$ Stagnation $\to$ Prereq Gap $\to$ Spaced Review $\to$ Practice $\to$ Advance $\to$ Challenge. |
| **Anti-Gaming Telemetry** | 5 Tests | Rapid retrying clamp ($w=0.0$), speed attenuation, and hint penalties. |
| **Prerequisite Invariants** | 6 Tests | DAG acyclicity, recursive ancestor walk, and fragile ceiling capping ($\min + 0.25$). |
| **Longitudinal Decay** | 4 Tests | Exponential Ebbinghaus decay curve, asymptotic retention floor (0.25), stability growth. |
| **FastAPI REST API** | 5 Tests | Endpoints `/api/next-action`, `/api/submit-attempt`, `/api/override`, `/api/teacher/heatmap`. |
| **Persistence & Snapshotting** | 4 Tests | 12-table SQLite schema, foreign keys, and Test 8 zero-variance reproduction. |
| **Question Bank Exactness** | 3 Tests | Zero float rounding errors via strict `fractions.Fraction` rational arithmetic. |
| **TOTAL** | **41 Tests** | **100% PASSING in 2.6s** |

---

## 🎯 Final Team Role Credit Breakdown
- **Ayon Mukherjee:** Team Lead, System Architecture, 6 Decision Rules (`decide.py`), Teacher Command Center (`teacher.py`), 2026 UI Design System (`theme.py`), Pitch & Judge Defense.
- **Yash:** ML Lead, Bayesian Knowledge Tracing formulation, Anti-Gaming Telemetry Weight ($w$), Ebbinghaus Retention Decay, Persona Bench (`ml_inspector.py`).
- **Soham Choudhury:** Frontend Co-Lead, Question Bank Lead, 50 Fractional Question Generators (`bank.py`), Interactive Question Player (`question_runner.py`), DAG Visualizer (`dag_visualizer.py`).
- **Shreyash Jha:** Backend Lead, FastAPI REST microservices (`server.py`, `routes.py`), 12-table ACID SQLite persistence (`db.py`), Turnkey Orchestrator (`run_demo.py`).
