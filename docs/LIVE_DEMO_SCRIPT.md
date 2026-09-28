# MasteryFlow: 5-Minute Live Presentation Script & Speaker Cues

**YUVA Megathon 2026 | SRMIST Trichy | EduGenAI Track (Domain 4)**  
**Target Duration:** Exactly 5 Minutes (300 Seconds) + 2 Minutes Judge Q&A  
**Team Name:** Nightfarers | **Team Leader:** Ayon Mukherjee

---

## ⏱️ Minute 0:00 – 1:00 | The Hook, Problem & Mission
**Speaker:** **Ayon Mukherjee (Team Lead)**  
**Visual on Screen:** Slide 1 & 2 (The Black-Box Crisis in EdTech)

> *"Respected judges and faculty, when an adaptive learning platform tells a struggling 8th grader to 'try question 47 next', do you know why it picked that question? In 95% of platforms today, the answer is: nobody knows. It's either an opaque neural recommender or a generative LLM that hallucinates difficulty.*
>
> *This black-box design causes students to disengage and leaves teachers completely in the dark. We built **MasteryFlow: Explainable Adaptive Learning and Intervention Engine**.*
>
> *MasteryFlow is founded on a strict engineering principle: **Zero LLM hallucinations in the decision path, 100% deterministic psychometrics, and complete Glass-Box explainability.** Let's show you how it works mathematically."*  
> *(Handoff: "I'll turn to Yash to explain our cognitive modeling engine.")*

---

## ⏱️ Minute 1:00 – 2:00 | Mathematical Rigor & Psychometrics
**Speaker:** **Yash (ML & Knowledge Tracing Lead)**  
**Visual on Screen:** Slide 4 & 5 (BKT Math, Telemetry Weighting & Ebbinghaus Decay)

> *"Thank you, Ayon. Traditional systems treat every student attempt equally. MasteryFlow implements difficulty-scaled Bayesian Knowledge Tracing across our 10-concept Fractions and Ratios DAG.*
>
> *We scale slip and guess parameters by question difficulty: harder questions carry low guess probability, while foundational questions carry low slip. Next, our telemetry weight $w$ actively combats guessing: if a student spams an answer in under 5 seconds, $w$ drops to zero, yielding zero mastery gain.*
>
> *Finally, human memory is not permanent. We integrate an Ebbinghaus retention decay curve: after 15 to 21 days of inactivity, effective belief decays exponentially, allowing the engine to schedule spaced retrieval before foundational forgetting causes downstream failure."*  
> *(Handoff: "Now Shreyash and Soham will present our persistence and student interface.")*

---

## ⏱️ Minute 2:00 – 3:00 | Backend Persistence & Student Experience
**Speakers:** **Shreyash Jha (Backend Lead) & Soham Choudhury (Frontend Co-Lead)**  
**Visual on Screen:** Slide 7 & 10 (System Architecture & Question Runner)

> **Shreyash:** *"To guarantee institutional compliance, our backend runs a FastAPI REST architecture backed by an ACID-compliant 9-table SQLite schema. Crucially, we enforce **Decision Snapshotting**: every recommendation serializes an immutable `inputs_json` payload capturing the exact state vector and config version, guaranteeing 100% deterministic reproducibility under audit."*
>
> **Soham:** *"On the student interface, questions are strictly evaluated using Python's exact `fractions.Fraction` arithmetic—zero rounding errors. If a student solves 5 consecutive questions correctly, our Streak Challenge mode triggers, serving higher-difficulty transfer problems for acceleration."*  
> *(Handoff: "Ayon will now demonstrate the live system running in real time.")*

---

## ⏱️ Minute 3:00 – 4:00 | Live System Demonstration
**Speaker:** **Ayon Mukherjee (Team Lead)**  
**Visual on Screen:** Live Streamlit Application running on `localhost:8501`

> *"Let's look at the live application. Here is our student **Diya Sharma**. Diya is currently practicing Concept C7 (Unit Rates). Watch our 'Why This Next?' Glass-Box card:*  
> *It explicitly explains to Diya: 'Your mastery of prerequisite C2 (Equivalent fractions) is 42%. You recorded 2 errors and used 2 hints. Strengthening C2 first guarantees success!'*  
> *Notice: the engine halted failure on C7 and automatically routed Diya to heal C2.*
>
> *Now let's switch to the **Teacher Command Center**. Here is our live cohort heatmap. Notice this urgent alert: our **Systemic Bottleneck Detector** found that 50% of the cohort is weak on C2, directly advising the instructor to hold a 10-minute workshop.*
>
> *And if a teacher disagrees with the algorithm? We provide **1-Click Persistent Override**: I can select any student, enforce an action and target concept, enter a pedagogical reason, and click Apply. It writes immediately to our SQLite audit log and takes absolute precedence!"*

---

## ⏱️ Minute 4:00 – 5:00 | Verification & Technical Defense
**Speaker:** **Ayon Mukherjee & Team**  
**Visual on Screen:** Live Terminal running `pytest` & Slide 11 (25 Green Tests)

> *"To prove that this is not a mock UI or hardcoded prototype, here is our automated test suite under `pytest`:*  
> *(Ayon runs `pytest masteryflow/tests/ -v`)*  
> *All **25 automated tests pass 100% green in half a second**.*
>
> *We have proven: Test 1 transfer locking, Test 2 anti-guessing suppression, Test 3 prerequisite capping, Test 4 memory decay, Test 5 persistent SQLite override, Test 6 twin history divergence, Test 7 cold start divergence, and Test 8 snapshot reproducibility.*
>
> *MasteryFlow delivers the transparency students deserve and the governance teachers require. Thank you, and we are ready for your questions!"*
