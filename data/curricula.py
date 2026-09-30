"""MasteryFlow Multi-Subject Curriculum Registry & YouTube Remediation Catalog (curricula.py).

Comprehensive multi-disciplinary knowledge graphs, concept DAGs, practice items,
and curated YouTube video lessons for:
1. Mathematics (Fractions, Ratios & Proportions) [C1-C10]
2. Computer Networks (OSI, Framing, IP Subnetting, Routing, TCP/UDP, Security) [CN1-CN8]
3. Artificial Intelligence (Search, Game Trees, ML, Deep Learning, CNNs, Transformers, RL) [AI1-AI8]
4. Formal Languages & Automata (DFA, NFA, Pumping Lemma, CFG, PDA, Turing Machines) [FLA1-FLA8]
5. Biochemistry (Biomolecules, Enzymes, Glycolysis, Krebs Cycle, ATP Synthase, Central Dogma) [BIO1-BIO8]
"""

from typing import Any, Dict, List, Optional


SUBJECTS_REGISTRY: Dict[str, Dict[str, Any]] = {
    "Mathematics": {
        "id": "MATH",
        "name": "Mathematics",
        "display_name": "Mathematics (Fractions & Proportions)",
        "icon": "",
        "description": "Foundational rational arithmetic, ratio comparisons, cross-multiplication, and proportional modeling.",
        "concept_prefix": "C",
        "default_active_concept": "C1",
    },
    "Computer Networks": {
        "id": "CN",
        "name": "Computer Networks",
        "display_name": "Computer Networks & Protocols",
        "icon": "",
        "description": "Layered architectures (OSI & TCP/IP), framing, CIDR subnetting, dynamic routing, transport reliability, and security.",
        "concept_prefix": "CN",
        "default_active_concept": "CN1",
    },
    "Artificial Intelligence": {
        "id": "AI",
        "name": "Artificial Intelligence",
        "display_name": "Artificial Intelligence & Deep Learning",
        "icon": "",
        "description": "Heuristic search, adversarial trees, gradient descent, deep neural networks, CNNs, transformers, and reinforcement learning.",
        "concept_prefix": "AI",
        "default_active_concept": "AI1",
    },
    "Formal Languages & Automata": {
        "id": "FLA",
        "name": "Formal Languages & Automata",
        "display_name": "Formal Languages & Automata Theory (FLA)",
        "icon": "",
        "description": "Regular languages, DFAs, NFAs, Pumping Lemma, Context-Free Grammars, Pushdown Automata, and Turing computability.",
        "concept_prefix": "FLA",
        "default_active_concept": "FLA1",
    },
    "Biochemistry": {
        "id": "BIO",
        "name": "Biochemistry",
        "display_name": "Biochemistry & Cellular Bioenergetics",
        "icon": "",
        "description": "Macromolecular structures, enzyme kinetics, glycolysis, Krebs cycle, chemiosmosis, membranes, and the central dogma.",
        "concept_prefix": "BIO",
        "default_active_concept": "BIO1",
    },
}


# ==============================================================================
# 1. MATHEMATICS (C1 - C10)
# ==============================================================================
MATH_CONCEPTS: Dict[str, Dict[str, Any]] = {
    "C1": {
        "id": "C1",
        "name": "Fraction basics (part-whole, number line)",
        "short_name": "Fraction Basics",
        "prerequisites": [],
        "category": "Foundations",
        "order": 1,
        "icon": "",
        "description": "Baseline foundation: visual unit fractions and fractional values on a 0-to-1 number line.",
    },
    "C2": {
        "id": "C2",
        "name": "Equivalent fractions and simplifying",
        "short_name": "Equivalent Fractions",
        "prerequisites": ["C1"],
        "category": "Foundations",
        "order": 2,
        "icon": "",
        "description": "Equivalence property via common divisors; reducing fractions to lowest terms.",
    },
    "C3": {
        "id": "C3",
        "name": "Comparing and ordering fractions",
        "short_name": "Comparing Fractions",
        "prerequisites": ["C2"],
        "category": "Comparison",
        "order": 3,
        "icon": "",
        "description": "Cross-multiplication and least common denominator comparisons.",
    },
    "C4": {
        "id": "C4",
        "name": "Adding and subtracting fractions",
        "short_name": "Fraction Addition & Subtraction",
        "prerequisites": ["C2"],
        "category": "Operations",
        "order": 4,
        "icon": "",
        "description": "Addition and subtraction with like and unlike denominators using LCD.",
    },
    "C5": {
        "id": "C5",
        "name": "Multiplying and dividing fractions",
        "short_name": "Fraction Multiplication & Division",
        "prerequisites": ["C2"],
        "category": "Operations",
        "order": 5,
        "icon": "",
        "description": "Area model multiplication and reciprocal division algorithms.",
    },
    "C6": {
        "id": "C6",
        "name": "Ratio basics (part:part, part:whole)",
        "short_name": "Ratio Basics",
        "prerequisites": ["C1", "C2"],
        "category": "Ratios",
        "order": 6,
        "icon": "",
        "description": "Representing relational quantities as colon ratios and simplified fraction ratios.",
    },
    "C7": {
        "id": "C7",
        "name": "Equivalent ratios and unit rate",
        "short_name": "Equivalent Ratios & Unit Rate",
        "prerequisites": ["C6", "C5"],
        "category": "Ratios",
        "order": 7,
        "icon": "",
        "description": "Scaling ratios up/down and computing per-unit benchmark rates.",
    },
    "C8": {
        "id": "C8",
        "name": "Proportion (solve a/b = c/d)",
        "short_name": "Solving Proportions",
        "prerequisites": ["C7"],
        "category": "Proportions",
        "order": 8,
        "icon": "",
        "description": "Algebraic cross-multiplication to solve missing variable proportions.",
    },
    "C9": {
        "id": "C9",
        "name": "Percentages as ratios",
        "short_name": "Percentages as Ratios",
        "prerequisites": ["C3", "C6"],
        "category": "Percentages",
        "order": 9,
        "icon": "",
        "description": "Relating parts per hundred to simplified fractions and decimal equivalents.",
    },
    "C10": {
        "id": "C10",
        "name": "Proportion word problems & scaling",
        "short_name": "Applied Word Problems",
        "prerequisites": ["C8", "C9"],
        "category": "Applications",
        "order": 10,
        "icon": "",
        "description": "Capstone multi-step real-world modeling: recipe scaling, map distances, and rate problems.",
    },
}


# ==============================================================================
# 2. COMPUTER NETWORKS (CN1 - CN8)
# ==============================================================================
NETWORKS_CONCEPTS: Dict[str, Dict[str, Any]] = {
    "CN1": {
        "id": "CN1",
        "name": "OSI & TCP/IP Reference Models",
        "short_name": "Layered Architectures",
        "prerequisites": [],
        "category": "Architecture",
        "order": 1,
        "icon": "",
        "description": "7-layer OSI model vs 4-layer TCP/IP stack; data encapsulation, headers, and protocol data units (PDUs).",
    },
    "CN2": {
        "id": "CN2",
        "name": "Data Link Layer, Framing & Error Detection",
        "short_name": "Framing & MAC",
        "prerequisites": ["CN1"],
        "category": "Data Link Layer",
        "order": 2,
        "icon": "",
        "description": "48-bit MAC addresses, frame delimiters, bit-stuffing, and Cyclic Redundancy Checks (CRC).",
    },
    "CN3": {
        "id": "CN3",
        "name": "IP Addressing, Subnetting & CIDR",
        "short_name": "IP Subnetting",
        "prerequisites": ["CN2"],
        "category": "Network Layer",
        "order": 3,
        "icon": "",
        "description": "IPv4/IPv6 address hierarchies, subnet masks, CIDR prefix calculations (/24, /27), and network/broadcast IDs.",
    },
    "CN4": {
        "id": "CN4",
        "name": "Routing Protocols (OSPF & BGP)",
        "short_name": "Routing Protocols",
        "prerequisites": ["CN3"],
        "category": "Network Layer",
        "order": 4,
        "icon": "",
        "description": "Intra-domain link-state routing (Dijkstra algorithm in OSPF) vs inter-domain path-vector routing (BGP).",
    },
    "CN5": {
        "id": "CN5",
        "name": "Transport Layer (TCP vs UDP & 3-Way Handshake)",
        "short_name": "TCP vs UDP",
        "prerequisites": ["CN2"],
        "category": "Transport Layer",
        "order": 5,
        "icon": "",
        "description": "Connection-oriented reliable stream (TCP SYN-SYN/ACK-ACK) vs lightweight best-effort datagrams (UDP).",
    },
    "CN6": {
        "id": "CN6",
        "name": "TCP Flow & Congestion Control",
        "short_name": "Congestion Control",
        "prerequisites": ["CN5"],
        "category": "Transport Layer",
        "order": 6,
        "icon": "",
        "description": "Sliding window flow control, slow start, congestion avoidance, additive increase multiplicative decrease (AIMD).",
    },
    "CN7": {
        "id": "CN7",
        "name": "Application Layer Protocols (DNS & HTTP/HTTPS)",
        "short_name": "DNS & Web Protocols",
        "prerequisites": ["CN5"],
        "category": "Application Layer",
        "order": 7,
        "icon": "",
        "description": "Hierarchical DNS namespace resolution, HTTP/1.1 vs HTTP/2 multiplexing, and TLS session handshakes.",
    },
    "CN8": {
        "id": "CN8",
        "name": "Network Security & Cryptography",
        "short_name": "Network Security",
        "prerequisites": ["CN3", "CN7"],
        "category": "Security",
        "order": 8,
        "icon": "",
        "description": "Symmetric vs asymmetric public key cryptography, digital signatures, packet-filtering firewalls, and NAT.",
    },
}


# ==============================================================================
# 3. ARTIFICIAL INTELLIGENCE (AI1 - AI8)
# ==============================================================================
AI_CONCEPTS: Dict[str, Dict[str, Any]] = {
    "AI1": {
        "id": "AI1",
        "name": "State-Space Search & Graph Traversal",
        "short_name": "Heuristic Search",
        "prerequisites": [],
        "category": "Search & Planning",
        "order": 1,
        "icon": "",
        "description": "Uninformed search (BFS, DFS) and informed heuristic search (A*, Greedy Best-First, admissible heuristics).",
    },
    "AI2": {
        "id": "AI2",
        "name": "Adversarial Search & Game Trees",
        "short_name": "Minimax & Pruning",
        "prerequisites": ["AI1"],
        "category": "Search & Planning",
        "order": 2,
        "icon": "",
        "description": "Minimax algorithm for two-player zero-sum games, evaluation functions, and Alpha-Beta branch pruning.",
    },
    "AI3": {
        "id": "AI3",
        "name": "Supervised Learning & Regression",
        "short_name": "Supervised Learning",
        "prerequisites": ["AI1"],
        "category": "Machine Learning",
        "order": 3,
        "icon": "",
        "description": "Linear and logistic regression, Mean Squared Error (MSE), cost function surfaces, and gradient descent updates.",
    },
    "AI4": {
        "id": "AI4",
        "name": "Artificial Neurons & Activation Functions",
        "short_name": "Perceptrons & Activations",
        "prerequisites": ["AI3"],
        "category": "Deep Learning",
        "order": 4,
        "icon": "",
        "description": "McCulloch-Pitts perceptron, linear separability, non-linear activations (ReLU, Sigmoid, GELU, Softmax).",
    },
    "AI5": {
        "id": "AI5",
        "name": "Deep Neural Networks & Backpropagation",
        "short_name": "Backpropagation",
        "prerequisites": ["AI4"],
        "category": "Deep Learning",
        "order": 5,
        "icon": "",
        "description": "Multi-layer perceptrons, computational graphs, matrix calculus chain rule, and backward gradient propagation.",
    },
    "AI6": {
        "id": "AI6",
        "name": "Convolutional Neural Networks (CNNs)",
        "short_name": "CNNs & Computer Vision",
        "prerequisites": ["AI5"],
        "category": "Computer Vision",
        "order": 6,
        "icon": "",
        "description": "Kernels/filters, 2D convolution operations, max-pooling, feature hierarchies, and translational invariance.",
    },
    "AI7": {
        "id": "AI7",
        "name": "Transformers & Self-Attention Mechanisms",
        "short_name": "Transformers & LLMs",
        "prerequisites": ["AI5"],
        "category": "Modern Architectures",
        "order": 7,
        "icon": "",
        "description": "Query-Key-Value scaled dot-product attention, multi-head attention, positional encodings, and encoder-decoder stacks.",
    },
    "AI8": {
        "id": "AI8",
        "name": "Reinforcement Learning & Bellman Optimality",
        "short_name": "Reinforcement Learning",
        "prerequisites": ["AI3", "AI5"],
        "category": "Reinforcement Learning",
        "order": 8,
        "icon": "",
        "description": "Markov Decision Processes (MDPs), policy vs value iteration, discount factor gamma, and Q-learning updates.",
    },
}


# ==============================================================================
# 4. FORMAL LANGUAGES & AUTOMATA (FLA1 - FLA8)
# ==============================================================================
FLA_CONCEPTS: Dict[str, Dict[str, Any]] = {
    "FLA1": {
        "id": "FLA1",
        "name": "Alphabets, Languages & Regular Expressions",
        "short_name": "Regular Expressions",
        "prerequisites": [],
        "category": "Regular Languages",
        "order": 1,
        "icon": "",
        "description": "Formal definitions of symbols, alphabets (Sigma), strings, Kleene star closure, union, and regular expressions.",
    },
    "FLA2": {
        "id": "FLA2",
        "name": "Deterministic Finite Automata (DFA)",
        "short_name": "DFA Design",
        "prerequisites": ["FLA1"],
        "category": "Regular Languages",
        "order": 2,
        "icon": "",
        "description": "5-tuple DFA formal structure (Q, Sigma, delta, q0, F), state transition diagrams, and regular language recognition.",
    },
    "FLA3": {
        "id": "FLA3",
        "name": "Nondeterministic Automata (NFA) & Subset Construction",
        "short_name": "NFA to DFA",
        "prerequisites": ["FLA2"],
        "category": "Regular Languages",
        "order": 3,
        "icon": "",
        "description": "NFA with epsilon-transitions, equivalent expressive power, and powerset subset construction algorithm.",
    },
    "FLA4": {
        "id": "FLA4",
        "name": "Pumping Lemma for Regular Languages",
        "short_name": "Pumping Lemma",
        "prerequisites": ["FLA2", "FLA3"],
        "category": "Regular Languages",
        "order": 4,
        "icon": "",
        "description": "Adversarial pumping lemma proofs by contradiction demonstrating non-regularity of counting languages like a^n b^n.",
    },
    "FLA5": {
        "id": "FLA5",
        "name": "Context-Free Grammars (CFG) & Derivations",
        "short_name": "Context-Free Grammars",
        "prerequisites": ["FLA1"],
        "category": "Context-Free Languages",
        "order": 5,
        "icon": "",
        "description": "Non-terminals, production rules, leftmost/rightmost derivations, parse trees, and grammar ambiguity.",
    },
    "FLA6": {
        "id": "FLA6",
        "name": "Pushdown Automata (PDA) & Stack Memory",
        "short_name": "Pushdown Automata",
        "prerequisites": ["FLA5"],
        "category": "Context-Free Languages",
        "order": 6,
        "icon": "",
        "description": "Automata augmented with last-in-first-out (LIFO) stack memory; acceptance by empty stack and final state.",
    },
    "FLA7": {
        "id": "FLA7",
        "name": "Turing Machines & Computability",
        "short_name": "Turing Machines",
        "prerequisites": ["FLA6"],
        "category": "Turing Computability",
        "order": 7,
        "icon": "",
        "description": "Infinite tape model, read/write head transitions, Church-Turing thesis, and recursively enumerable languages.",
    },
    "FLA8": {
        "id": "FLA8",
        "name": "Decidability, Halting Problem & P vs NP",
        "short_name": "Decidability & Complexity",
        "prerequisites": ["FLA7"],
        "category": "Complexity & Decidability",
        "order": 8,
        "icon": "",
        "description": "Turing undecidability of the Halting Problem via diagonalization, polynomial reductions, and P vs NP complexity.",
    },
}


# ==============================================================================
# 5. BIOCHEMISTRY (BIO1 - BIO8)
# ==============================================================================
BIOCHEM_CONCEPTS: Dict[str, Dict[str, Any]] = {
    "BIO1": {
        "id": "BIO1",
        "name": "Water, Hydrogen Bonds & pH Buffers",
        "short_name": "Aqueous Foundations",
        "prerequisites": [],
        "category": "Foundations",
        "order": 1,
        "icon": "",
        "description": "Polar water molecules, hydrogen bond networks, weak acids/bases, Henderson-Hasselbalch equation, and bicarbonate buffer.",
    },
    "BIO2": {
        "id": "BIO2",
        "name": "Amino Acids & Protein Hierarchies",
        "short_name": "Protein Structure",
        "prerequisites": ["BIO1"],
        "category": "Structural Biology",
        "order": 2,
        "icon": "",
        "description": "20 amino acid side-chain properties, peptide bonds, alpha-helices, beta-sheets, and tertiary folding energetics.",
    },
    "BIO3": {
        "id": "BIO3",
        "name": "Enzyme Kinetics & Catalysis (Michaelis-Menten)",
        "short_name": "Enzyme Kinetics",
        "prerequisites": ["BIO2"],
        "category": "Enzymology",
        "order": 3,
        "icon": "",
        "description": "Transition state lowering, Michaelis constant (Km), Vmax, Lineweaver-Burk plots, and competitive/allosteric inhibition.",
    },
    "BIO4": {
        "id": "BIO4",
        "name": "Carbohydrate Metabolism & Glycolysis",
        "short_name": "Glycolysis Pathway",
        "prerequisites": ["BIO3"],
        "category": "Metabolism",
        "order": 4,
        "icon": "",
        "description": "Glucose phosphorylation, 10-step glycolytic pathway, net 2 ATP and 2 NADH generation, and phosphofructokinase-1 control.",
    },
    "BIO5": {
        "id": "BIO5",
        "name": "Citric Acid Cycle (Krebs Cycle)",
        "short_name": "Citric Acid Cycle",
        "prerequisites": ["BIO4"],
        "category": "Metabolism",
        "order": 5,
        "icon": "",
        "description": "Mitochondrial pyruvate dehydrogenase, acetyl-CoA condensation with oxaloacetate, GTP synthesis, and electron carriers.",
    },
    "BIO6": {
        "id": "BIO6",
        "name": "Oxidative Phosphorylation & ATP Synthase",
        "short_name": "Oxidative Phosphorylation",
        "prerequisites": ["BIO5"],
        "category": "Bioenergetics",
        "order": 6,
        "icon": "",
        "description": "Electron transport chain Complexes I-IV, chemiosmotic proton-motive force, and rotary catalysis of F0-F1 ATP synthase.",
    },
    "BIO7": {
        "id": "BIO7",
        "name": "Lipid Metabolism & Fluid Mosaic Membranes",
        "short_name": "Lipids & Membranes",
        "prerequisites": ["BIO1", "BIO5"],
        "category": "Membranes & Lipids",
        "order": 7,
        "icon": "",
        "description": "Phospholipid bilayers, cholesterol fluidity regulation, triacylglycerol storage, and mitochondrial beta-oxidation of fatty acids.",
    },
    "BIO8": {
        "id": "BIO8",
        "name": "Nucleic Acids, Replication & Central Dogma",
        "short_name": "Central Dogma",
        "prerequisites": ["BIO2", "BIO6"],
        "category": "Molecular Genetics",
        "order": 8,
        "icon": "",
        "description": "DNA double-helix structure, DNA polymerase fidelity, RNA transcription, and ribosomal mRNA-to-protein translation.",
    },
}


SUBJECTS_CONCEPTS_MAP: Dict[str, Dict[str, Dict[str, Any]]] = {
    "Mathematics": MATH_CONCEPTS,
    "Computer Networks": NETWORKS_CONCEPTS,
    "Artificial Intelligence": AI_CONCEPTS,
    "Formal Languages & Automata": FLA_CONCEPTS,
    "Biochemistry": BIOCHEM_CONCEPTS,
}


# ==============================================================================
# CURATED YOUTUBE VIDEO LESSON CATALOG FOR EVERY CONCEPT
# ==============================================================================
YOUTUBE_VIDEOS_CATALOG: Dict[str, Dict[str, Any]] = {
    # --- Mathematics ---
    "C1": {
        "concept_id": "C1",
        "subject": "Mathematics",
        "video_id": "CA9XLJpQp3c",
        "title": 'Math Antics - Fractions Are Parts',
        "channel": 'Math Antics',
        "duration": "11:42",
        "url": "https://www.youtube.com/watch?v=CA9XLJpQp3c",
        "thumbnail_url": "https://img.youtube.com/vi/CA9XLJpQp3c/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/CA9XLJpQp3c",
        "description": 'Baseline foundation: visual unit fractions and fractional values on a 0-to-1 number line.',
        "takeaways": [
            'Denominator = total number of equal parts partitioned.',
            'Numerator = count of parts selected or accumulated.',
            'On a number line, unit fractions divide the interval between 0 and 1.',
        ]
    },
    "C2": {
        "concept_id": "C2",
        "subject": "Mathematics",
        "video_id": "qcHHhd6HizI",
        "title": 'Equivalent Fractions - What Are They and How to Find Them',
        "channel": "Let's Do Math",
        "duration": "5:45",
        "url": "https://www.youtube.com/watch?v=qcHHhd6HizI",
        "thumbnail_url": "https://img.youtube.com/vi/qcHHhd6HizI/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/qcHHhd6HizI",
        "description": 'Equivalence property via common divisors; reducing fractions to lowest terms.',
        "takeaways": [
            'Multiplying by n/n is mathematically equivalent to multiplying by 1.',
            'Simplifying requires dividing by the Greatest Common Divisor (GCD).',
            'A fraction is in lowest terms when numerator and denominator are coprime.',
        ]
    },
    "C3": {
        "concept_id": "C3",
        "subject": "Mathematics",
        "video_id": "KNdUJQ_qd4U",
        "title": 'Math Antics - Comparing Fractions',
        "channel": 'Math Antics',
        "duration": "10:28",
        "url": "https://www.youtube.com/watch?v=KNdUJQ_qd4U",
        "thumbnail_url": "https://img.youtube.com/vi/KNdUJQ_qd4U/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/KNdUJQ_qd4U",
        "description": 'Cross-multiplication and least common denominator comparisons.',
        "takeaways": [
            'Convert to a common denominator to compare numerators directly.',
            'Cross-multiplication shortcut: compare a*d with b*c.',
            'Benchmark testing against 1/2 resolves quick comparisons.',
        ]
    },
    "C4": {
        "concept_id": "C4",
        "subject": "Mathematics",
        "video_id": "52ZlXsFJULI",
        "title": 'Adding and Subtracting Fractions with Like & Unlike Denominators',
        "channel": 'Khan Academy',
        "duration": "10:20",
        "url": "https://www.youtube.com/watch?v=52ZlXsFJULI",
        "thumbnail_url": "https://img.youtube.com/vi/52ZlXsFJULI/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/52ZlXsFJULI",
        "description": 'Addition and subtraction with like and unlike denominators using LCD.',
        "takeaways": [
            'Never add denominators together!',
            'Find the Least Common Multiple (LCM) of denominators.',
            'Scale numerators accordingly before adding or subtracting.',
        ]
    },
    "C5": {
        "concept_id": "C5",
        "subject": "Mathematics",
        "video_id": "qmfXyR7Z6Lk",
        "title": 'Math Antics - Multiplying Fractions',
        "channel": 'Math Antics',
        "duration": "11:34",
        "url": "https://www.youtube.com/watch?v=qmfXyR7Z6Lk",
        "thumbnail_url": "https://img.youtube.com/vi/qmfXyR7Z6Lk/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/qmfXyR7Z6Lk",
        "description": 'Area model multiplication and reciprocal division algorithms.',
        "takeaways": [
            'Multiply straight across: (a/b) * (c/d) = (a*c) / (b*d).',
            'Cross-cancel common factors early to simplify arithmetic.',
            'Division rule: Keep, Change, Flip (multiply by reciprocal).',
        ]
    },
    "C6": {
        "concept_id": "C6",
        "subject": "Mathematics",
        "video_id": "RQ2nYUBVvqI",
        "title": 'Math Antics - Ratios And Rates',
        "channel": 'Math Antics',
        "duration": "10:49",
        "url": "https://www.youtube.com/watch?v=RQ2nYUBVvqI",
        "thumbnail_url": "https://img.youtube.com/vi/RQ2nYUBVvqI/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/RQ2nYUBVvqI",
        "description": 'Representing relational quantities as colon ratios and simplified fraction ratios.',
        "takeaways": [
            'A ratio compares quantities: 3 blue to 4 red is 3:4.',
            'Part-to-whole ratio compares a subset to the combined sum.',
            'Ratios can be simplified just like fractions.',
        ]
    },
    "C7": {
        "concept_id": "C7",
        "subject": "Mathematics",
        "video_id": "s0RBRkehzwo",
        "title": 'Unit Rates, Ratios & Proportions - Word Problems',
        "channel": 'The Organic Chemistry Tutor',
        "duration": "14:15",
        "url": "https://www.youtube.com/watch?v=s0RBRkehzwo",
        "thumbnail_url": "https://img.youtube.com/vi/s0RBRkehzwo/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/s0RBRkehzwo",
        "description": 'Scaling ratios up/down and computing per-unit benchmark rates.',
        "takeaways": [
            'A unit rate has a denominator equal to 1.',
            'Divide the numerator by the denominator to find the unit value.',
            'Scale unit rates by multiplication to solve any quantity.',
        ]
    },
    "C8": {
        "concept_id": "C8",
        "subject": "Mathematics",
        "video_id": "USmit5zUGas",
        "title": 'Math Antics - Proportions',
        "channel": 'Math Antics',
        "duration": "10:35",
        "url": "https://www.youtube.com/watch?v=USmit5zUGas",
        "thumbnail_url": "https://img.youtube.com/vi/USmit5zUGas/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/USmit5zUGas",
        "description": 'Algebraic cross-multiplication to solve missing variable proportions.',
        "takeaways": [
            'In proportion a/b = c/d, cross products a*d and b*c are identical.',
            'Isolate the unknown variable with basic division.',
            'Check work by verifying equal cross-product products.',
        ]
    },
    "C9": {
        "concept_id": "C9",
        "subject": "Mathematics",
        "video_id": "JeVSmq1Nrpw",
        "title": 'Math Antics - What Are Percentages?',
        "channel": 'Math Antics',
        "duration": "8:52",
        "url": "https://www.youtube.com/watch?v=JeVSmq1Nrpw",
        "thumbnail_url": "https://img.youtube.com/vi/JeVSmq1Nrpw/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/JeVSmq1Nrpw",
        "description": 'Relating parts per hundred to simplified fractions and decimal equivalents.',
        "takeaways": [
            "Percent means 'parts per 100': 45% = 45/100.",
            'Convert fraction to percentage: divide, then multiply by 100.',
            'Use benchmark percentages (10%, 25%, 50%) for fast mental checks.',
        ]
    },
    "C10": {
        "concept_id": "C10",
        "subject": "Mathematics",
        "video_id": "JOZSFwuyqok",
        "title": 'Ratio and Proportion Word Problems - Math',
        "channel": 'The Organic Chemistry Tutor',
        "duration": "12:40",
        "url": "https://www.youtube.com/watch?v=JOZSFwuyqok",
        "thumbnail_url": "https://img.youtube.com/vi/JOZSFwuyqok/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/JOZSFwuyqok",
        "description": 'Capstone multi-step real-world modeling: recipe scaling, map distances, and rate problems.',
        "takeaways": [
            'Assign consistent units to numerator and denominator.',
            'Write the ratio equation before plugging in variables.',
            'Check that answer makes practical physical sense.',
        ]
    },
    # --- Computer Networks ---
    "CN1": {
        "concept_id": "CN1",
        "subject": "Computer Networks",
        "video_id": "vv4y_uOneC0",
        "title": 'OSI Model Explained | OSI Animation | 7 Layers',
        "channel": 'TechTerms',
        "duration": "14:23",
        "url": "https://www.youtube.com/watch?v=vv4y_uOneC0",
        "thumbnail_url": "https://img.youtube.com/vi/vv4y_uOneC0/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/vv4y_uOneC0",
        "description": '7-layer OSI model vs 4-layer TCP/IP stack; data encapsulation, headers, and protocol data units (PDUs).',
        "takeaways": [
            'Physical -> Data Link -> Network -> Transport -> Session -> Presentation -> Application.',
            'Encapsulation appends headers at each descending layer.',
            'PDUs: Bits -> Frames -> Packets -> Segments -> Application Data.',
        ]
    },
    "CN2": {
        "concept_id": "CN2",
        "subject": "Computer Networks",
        "video_id": "NhpzBldHOYo",
        "title": 'Data Link Layer Framing & Error Detection',
        "channel": 'Neso Academy',
        "duration": "11:15",
        "url": "https://www.youtube.com/watch?v=NhpzBldHOYo",
        "thumbnail_url": "https://img.youtube.com/vi/NhpzBldHOYo/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/NhpzBldHOYo",
        "description": '48-bit MAC addresses, frame delimiters, bit-stuffing, and Cyclic Redundancy Checks (CRC).',
        "takeaways": [
            'MAC addresses are 48-bit globally unique hardware identifiers.',
            'Bit stuffing prevents delimiter mimicry in payload data.',
            'CRC uses polynomial binary division to detect burst bit errors.',
        ]
    },
    "CN3": {
        "concept_id": "CN3",
        "subject": "Computer Networks",
        "video_id": "5WfiTHiU4x8",
        "title": 'What is an IP Address? IP Addressing & Subnetting Explained',
        "channel": 'NetworkChuck',
        "duration": "18:45",
        "url": "https://www.youtube.com/watch?v=5WfiTHiU4x8",
        "thumbnail_url": "https://img.youtube.com/vi/5WfiTHiU4x8/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/5WfiTHiU4x8",
        "description": 'IPv4/IPv6 address hierarchies, subnet masks, CIDR prefix calculations (/24, /27), and network/broadcast IDs.',
        "takeaways": [
            'IP addresses consist of 32 bits divided into 4 octets.',
            'CIDR notation /24 reserves 24 bits for network and 8 bits for hosts.',
            'Usable hosts = 2^(host_bits) - 2 (subtracting network and broadcast IDs).',
        ]
    },
    "CN4": {
        "concept_id": "CN4",
        "subject": "Computer Networks",
        "video_id": "kfvJ8QVJscc",
        "title": 'OSPF Routing Protocol Explained Step by Step',
        "channel": 'CertBros',
        "duration": "12:18",
        "url": "https://www.youtube.com/watch?v=kfvJ8QVJscc",
        "thumbnail_url": "https://img.youtube.com/vi/kfvJ8QVJscc/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/kfvJ8QVJscc",
        "description": 'Intra-domain link-state routing (Dijkstra algorithm in OSPF) vs inter-domain path-vector routing (BGP).',
        "takeaways": [
            'Routers operate at OSI Layer 3 using IP forwarding tables.',
            'OSPF floods Link State Advertisements and computes shortest paths via Dijkstra.',
            'BGP coordinates routing policies between independent Autonomous Systems (AS).',
        ]
    },
    "CN5": {
        "concept_id": "CN5",
        "subject": "Computer Networks",
        "video_id": "uwoD5YsGACg",
        "title": 'TCP vs UDP Comparison & 3-Way Handshake',
        "channel": 'PowerCert Animated Videos',
        "duration": "8:36",
        "url": "https://www.youtube.com/watch?v=uwoD5YsGACg",
        "thumbnail_url": "https://img.youtube.com/vi/uwoD5YsGACg/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/uwoD5YsGACg",
        "description": 'Connection-oriented reliable stream (TCP SYN-SYN/ACK-ACK) vs lightweight best-effort datagrams (UDP).',
        "takeaways": [
            'TCP provides ordered, reliable, acknowledged delivery of byte streams.',
            'UDP has lower latency with zero connection overhead (ideal for DNS, gaming).',
            'The 3-way handshake synchronizes sequence numbers before data transfer.',
        ]
    },
    "CN6": {
        "concept_id": "CN6",
        "subject": "Computer Networks",
        "video_id": "ReQiSK8W3Ag",
        "title": 'TCP Flow Control & Sliding Window Protocol',
        "channel": 'Neso Academy',
        "duration": "13:42",
        "url": "https://www.youtube.com/watch?v=ReQiSK8W3Ag",
        "thumbnail_url": "https://img.youtube.com/vi/ReQiSK8W3Ag/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/ReQiSK8W3Ag",
        "description": 'Sliding window flow control, slow start, congestion avoidance, additive increase multiplicative decrease (AIMD).',
        "takeaways": [
            'Flow control protects the receiver buffer; congestion control protects the transit network.',
            'Slow Start doubles cwnd every RTT until ssthresh is reached.',
            'AIMD provides distributed fairness and stability across shared bottlenecks.',
        ]
    },
    "CN7": {
        "concept_id": "CN7",
        "subject": "Computer Networks",
        "video_id": "mpQZVYPuDGU",
        "title": 'How a DNS Server (Domain Name System) Works',
        "channel": 'PowerCert Animated Videos',
        "duration": "10:11",
        "url": "https://www.youtube.com/watch?v=mpQZVYPuDGU",
        "thumbnail_url": "https://img.youtube.com/vi/mpQZVYPuDGU/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/mpQZVYPuDGU",
        "description": 'Hierarchical DNS namespace resolution, HTTP/1.1 vs HTTP/2 multiplexing, and TLS session handshakes.',
        "takeaways": [
            'DNS translates human domain names into machine IP addresses via recursive resolution.',
            'Recursive queries traverse Root -> TLD -> Authoritative Nameservers.',
            'HTTP/2 and HTTP/3 introduce stream multiplexing over TCP/QUIC.',
        ]
    },
    "CN8": {
        "concept_id": "CN8",
        "subject": "Computer Networks",
        "video_id": "inWWhr5tnEA",
        "title": 'What Is Cyber Security & Cryptography | How It Works',
        "channel": 'Simplilearn',
        "duration": "23:15",
        "url": "https://www.youtube.com/watch?v=inWWhr5tnEA",
        "thumbnail_url": "https://img.youtube.com/vi/inWWhr5tnEA/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/inWWhr5tnEA",
        "description": 'Symmetric vs asymmetric public key cryptography, digital signatures, packet-filtering firewalls, and NAT.',
        "takeaways": [
            'Asymmetric crypto uses public key for encryption, private key for decryption.',
            'TLS handshake authenticates the server via Certificate Authorities (CAs).',
            'Bulk data transfer uses fast symmetric encryption (e.g. AES-GCM).',
        ]
    },
    # --- Artificial Intelligence ---
    "AI1": {
        "concept_id": "AI1",
        "subject": "Artificial Intelligence",
        "video_id": "ySN5Wnu88nE",
        "title": 'A* (A Star) Search Algorithm - Computerphile',
        "channel": 'Computerphile',
        "duration": "12:44",
        "url": "https://www.youtube.com/watch?v=ySN5Wnu88nE",
        "thumbnail_url": "https://img.youtube.com/vi/ySN5Wnu88nE/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/ySN5Wnu88nE",
        "description": 'Uninformed search (BFS, DFS) and informed heuristic search (A*, Greedy Best-First, admissible heuristics).',
        "takeaways": [
            'g(n) is the exact cost from start to node n; h(n) is the estimated heuristic cost.',
            'f(n) = g(n) + h(n) guides the priority queue toward the optimal goal.',
            'An admissible heuristic never overestimates the true remaining cost.',
        ]
    },
    "AI2": {
        "concept_id": "AI2",
        "subject": "Artificial Intelligence",
        "video_id": "l-hh51ncgDI",
        "title": 'Algorithms Explained: Minimax and Alpha-Beta Pruning',
        "channel": 'Sebastian Lague',
        "duration": "17:35",
        "url": "https://www.youtube.com/watch?v=l-hh51ncgDI",
        "thumbnail_url": "https://img.youtube.com/vi/l-hh51ncgDI/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/l-hh51ncgDI",
        "description": 'Minimax algorithm for two-player zero-sum games, evaluation functions, and Alpha-Beta branch pruning.',
        "takeaways": [
            'Maximizing player seeks highest score; Minimizing player seeks lowest score.',
            'Alpha is the best value Max can guarantee; Beta is best for Min.',
            'Branches where beta <= alpha can be safely pruned without loss of optimality.',
        ]
    },
    "AI3": {
        "concept_id": "AI3",
        "subject": "Artificial Intelligence",
        "video_id": "sDv4f4s2SB8",
        "title": 'Gradient Descent, Step-by-Step',
        "channel": 'StatQuest with Josh Starmer',
        "duration": "8:30",
        "url": "https://www.youtube.com/watch?v=sDv4f4s2SB8",
        "thumbnail_url": "https://img.youtube.com/vi/sDv4f4s2SB8/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/sDv4f4s2SB8",
        "description": 'Linear and logistic regression, Mean Squared Error (MSE), cost function surfaces, and gradient descent updates.',
        "takeaways": [
            'Logistic regression predicts probabilities between 0 and 1 via the Sigmoid curve.',
            'Cost function measures divergence between predicted values and ground truth.',
            'Gradient descent updates weights opposite to the gradient: w = w - lr * grad.',
        ]
    },
    "AI4": {
        "concept_id": "AI4",
        "subject": "Artificial Intelligence",
        "video_id": "aircAruvnKk",
        "title": 'But what is a neural network? | Deep learning chapter 1',
        "channel": '3Blue1Brown',
        "duration": "19:13",
        "url": "https://www.youtube.com/watch?v=aircAruvnKk",
        "thumbnail_url": "https://img.youtube.com/vi/aircAruvnKk/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/aircAruvnKk",
        "description": 'McCulloch-Pitts perceptron, linear separability, non-linear activations (ReLU, Sigmoid, GELU, Softmax).',
        "takeaways": [
            'A neuron computes an affine combination of inputs: z = sum(w_i * x_i) + b.',
            'Non-linear activations allow networks to learn non-linear decision boundaries.',
            'Softmax normalizes multi-class output vectors into valid probability distributions.',
        ]
    },
    "AI5": {
        "concept_id": "AI5",
        "subject": "Artificial Intelligence",
        "video_id": "Ilg3gGewQ5U",
        "title": 'Backpropagation, intuitively | Deep Learning Chapter 3',
        "channel": '3Blue1Brown',
        "duration": "13:53",
        "url": "https://www.youtube.com/watch?v=Ilg3gGewQ5U",
        "thumbnail_url": "https://img.youtube.com/vi/Ilg3gGewQ5U/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/Ilg3gGewQ5U",
        "description": 'Multi-layer perceptrons, computational graphs, matrix calculus chain rule, and backward gradient propagation.',
        "takeaways": [
            'Backprop computes partial derivatives of the cost with respect to every weight.',
            'The chain rule multiplies local derivatives across consecutive layers.',
            'Enables efficient end-to-end training of deep multi-layer architectures.',
        ]
    },
    "AI6": {
        "concept_id": "AI6",
        "subject": "Artificial Intelligence",
        "video_id": "YRhxdVk_sIs",
        "title": 'Convolutional Neural Networks (CNNs) Explained',
        "channel": 'deeplizard',
        "duration": "21:38",
        "url": "https://www.youtube.com/watch?v=YRhxdVk_sIs",
        "thumbnail_url": "https://img.youtube.com/vi/YRhxdVk_sIs/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/YRhxdVk_sIs",
        "description": 'Kernels/filters, 2D convolution operations, max-pooling, feature hierarchies, and translational invariance.',
        "takeaways": [
            'Convolutions slide small weight filters across input pixels to detect local patterns.',
            'Early layers detect edges/textures; deep layers compose semantic shapes.',
            'Pooling layers reduce spatial dimensionality and provide translation invariance.',
        ]
    },
    "AI7": {
        "concept_id": "AI7",
        "subject": "Artificial Intelligence",
        "video_id": "zxQyTK8quyY",
        "title": "Transformer Neural Networks, ChatGPT's foundation, Clearly Explained!",
        "channel": 'StatQuest with Josh Starmer',
        "duration": "15:52",
        "url": "https://www.youtube.com/watch?v=zxQyTK8quyY",
        "thumbnail_url": "https://img.youtube.com/vi/zxQyTK8quyY/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/zxQyTK8quyY",
        "description": 'Query-Key-Value scaled dot-product attention, multi-head attention, positional encodings, and encoder-decoder stacks.',
        "takeaways": [
            'Self-attention computes dynamic weights: Softmax((Q*K^T) / sqrt(d_k)) * V.',
            'Multi-head attention lets models attend to syntax, semantics, and reference simultaneously.',
            'Transformers eliminate recurrence, enabling massive parallel pretraining on GPUs.',
        ]
    },
    "AI8": {
        "concept_id": "AI8",
        "subject": "Artificial Intelligence",
        "video_id": "JgvyzIkgxF0",
        "title": 'An Introduction to Reinforcement Learning',
        "channel": 'Arxiv Insights',
        "duration": "11:20",
        "url": "https://www.youtube.com/watch?v=JgvyzIkgxF0",
        "thumbnail_url": "https://img.youtube.com/vi/JgvyzIkgxF0/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/JgvyzIkgxF0",
        "description": 'Markov Decision Processes (MDPs), policy vs value iteration, discount factor gamma, and Q-learning updates.',
        "takeaways": [
            'The Bellman equation decomposes expected future return into immediate reward + discounted continuation.',
            'Exploration vs exploitation dilemma balanced via epsilon-greedy policies.',
            'Q-learning iteratively approximates the optimal action-value function Q*(s, a).',
        ]
    },
    # --- Formal Languages & Automata ---
    "FLA1": {
        "concept_id": "FLA1",
        "subject": "Formal Languages & Automata",
        "video_id": "58N2N7zJGrQ",
        "title": 'Introduction to Theory of Computation: Alphabets & Languages',
        "channel": 'Neso Academy',
        "duration": "9:45",
        "url": "https://www.youtube.com/watch?v=58N2N7zJGrQ",
        "thumbnail_url": "https://img.youtube.com/vi/58N2N7zJGrQ/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/58N2N7zJGrQ",
        "description": 'Formal definitions of symbols, alphabets (Sigma), strings, Kleene star closure, union, and regular expressions.',
        "takeaways": [
            'An alphabet is a finite non-empty set of symbols.',
            'Kleene star Sigma* is the set of all finite strings over Sigma including epsilon.',
            'A language is any subset of Sigma*.',
        ]
    },
    "FLA2": {
        "concept_id": "FLA2",
        "subject": "Formal Languages & Automata",
        "video_id": "40i4PKpM0cI",
        "title": 'Deterministic Finite Automata (DFA) State Diagrams & Design',
        "channel": 'Neso Academy',
        "duration": "12:10",
        "url": "https://www.youtube.com/watch?v=40i4PKpM0cI",
        "thumbnail_url": "https://img.youtube.com/vi/40i4PKpM0cI/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/40i4PKpM0cI",
        "description": '5-tuple DFA formal structure (Q, Sigma, delta, q0, F), state transition diagrams, and regular language recognition.',
        "takeaways": [
            'In a DFA, every state has exactly one transition for each alphabet symbol.',
            'A string is accepted if the terminal state belongs to the set of accepting states F.',
            'DFAs have strictly finite memory (no stack or unbounded tape).',
        ]
    },
    "FLA3": {
        "concept_id": "FLA3",
        "subject": "Formal Languages & Automata",
        "video_id": "--CSVsFIDng",
        "title": 'Conversion of NFA to DFA (Subset Construction Algorithm)',
        "channel": 'Neso Academy',
        "duration": "14:05",
        "url": "https://www.youtube.com/watch?v=--CSVsFIDng",
        "thumbnail_url": "https://img.youtube.com/vi/--CSVsFIDng/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/--CSVsFIDng",
        "description": 'NFA with epsilon-transitions, equivalent expressive power, and powerset subset construction algorithm.',
        "takeaways": [
            'NFAs can transition to multiple states or epsilon-transition without consuming input.',
            'Subset construction represents DFA states as subsets of NFA states (power set 2^Q).',
            'NFAs and DFAs recognize the exact same class of regular languages.',
        ]
    },
    "FLA4": {
        "concept_id": "FLA4",
        "subject": "Formal Languages & Automata",
        "video_id": "dikEDuepOtI",
        "title": 'Pumping Lemma for Regular Languages: Proofs & Contradictions',
        "channel": 'Neso Academy',
        "duration": "15:30",
        "url": "https://www.youtube.com/watch?v=dikEDuepOtI",
        "thumbnail_url": "https://img.youtube.com/vi/dikEDuepOtI/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/dikEDuepOtI",
        "description": 'Adversarial pumping lemma proofs by contradiction demonstrating non-regularity of counting languages like a^n b^n.',
        "takeaways": [
            'Pumping Lemma conditions: string s = xyz with |y| > 0, |xy| <= p, and xy^i z in L for all i >= 0.',
            'Choose a target string s of length >= pumping length p.',
            'Show that pumping y produces a string outside the language, establishing contradiction.',
        ]
    },
    "FLA5": {
        "concept_id": "FLA5",
        "subject": "Formal Languages & Automata",
        "video_id": "3rzTRtjUM_I",
        "title": 'Context-Free Grammars (CFG) & Derivations',
        "channel": 'Neso Academy',
        "duration": "11:50",
        "url": "https://www.youtube.com/watch?v=3rzTRtjUM_I",
        "thumbnail_url": "https://img.youtube.com/vi/3rzTRtjUM_I/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/3rzTRtjUM_I",
        "description": 'Non-terminals, production rules, leftmost/rightmost derivations, parse trees, and grammar ambiguity.',
        "takeaways": [
            'Production rules replace a single variable on LHS with a string of variables and terminals.',
            'A grammar is ambiguous if a string admits two distinct leftmost derivation parse trees.',
            'CFGs capture hierarchical syntactic nesting such as balanced expressions.',
        ]
    },
    "FLA6": {
        "concept_id": "FLA6",
        "subject": "Formal Languages & Automata",
        "video_id": "4ejIAmp_Atw",
        "title": 'Introduction to Pushdown Automata (PDA) & Stack Memory',
        "channel": 'Neso Academy',
        "duration": "13:15",
        "url": "https://www.youtube.com/watch?v=4ejIAmp_Atw",
        "thumbnail_url": "https://img.youtube.com/vi/4ejIAmp_Atw/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/4ejIAmp_Atw",
        "description": 'Automata augmented with last-in-first-out (LIFO) stack memory; acceptance by empty stack and final state.',
        "takeaways": [
            'PDA transitions specify (input symbol read, top of stack popped -> symbol pushed).',
            'Deterministic PDAs (DPDA) are strictly less powerful than Nondeterministic PDAs (NPDA).',
            'A language is context-free if and only if some PDA recognizes it.',
        ]
    },
    "FLA7": {
        "concept_id": "FLA7",
        "subject": "Formal Languages & Automata",
        "video_id": "gJQTFhkhwPA",
        "title": 'Turing Machines: Infinite Tape & Computability',
        "channel": 'EngMicroLectures',
        "duration": "9:18",
        "url": "https://www.youtube.com/watch?v=gJQTFhkhwPA",
        "thumbnail_url": "https://img.youtube.com/vi/gJQTFhkhwPA/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/gJQTFhkhwPA",
        "description": 'Infinite tape model, read/write head transitions, Church-Turing thesis, and recursively enumerable languages.',
        "takeaways": [
            'A Turing machine can read, overwrite symbols, and shift its head Left or Right.',
            'The Church-Turing thesis asserts any algorithmic computation can be simulated by a Turing machine.',
            'Languages recognized are Turing-recognizable; those where machines always halt are Turing-decidable.',
        ]
    },
    "FLA8": {
        "concept_id": "FLA8",
        "subject": "Formal Languages & Automata",
        "video_id": "macM_MtS_w4",
        "title": 'Turing & The Halting Problem - Computerphile',
        "channel": 'Computerphile',
        "duration": "12:04",
        "url": "https://www.youtube.com/watch?v=macM_MtS_w4",
        "thumbnail_url": "https://img.youtube.com/vi/macM_MtS_w4/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/macM_MtS_w4",
        "description": 'Turing undecidability of the Halting Problem via diagonalization, polynomial reductions, and P vs NP complexity.',
        "takeaways": [
            'The Halting Problem asks if program P halts on input w.',
            "Proof uses Cantor's diagonalization: construct a machine that halts if and only if it doesn't halt.",
            'P vs NP asks if problems with polynomial verifiable answers have polynomial solutions.',
        ]
    },
    # --- Biochemistry ---
    "BIO1": {
        "concept_id": "BIO1",
        "subject": "Biochemistry",
        "video_id": "ASLUY2U1M-8",
        "title": 'How Polarity Makes Water Behave Strangely',
        "channel": 'TED-Ed',
        "duration": "11:02",
        "url": "https://www.youtube.com/watch?v=ASLUY2U1M-8",
        "thumbnail_url": "https://img.youtube.com/vi/ASLUY2U1M-8/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/ASLUY2U1M-8",
        "description": 'Polar water molecules, hydrogen bond networks, weak acids/bases, Henderson-Hasselbalch equation, and bicarbonate buffer.',
        "takeaways": [
            "Oxygen's high electronegativity creates a permanent dipole in H2O.",
            'Hydrogen bonds drive hydrophobic collapse and macromolecular folding.',
            'Henderson-Hasselbalch equation computes buffer capacity: pH = pKa + log([A-]/[HA]).',
        ]
    },
    "BIO2": {
        "concept_id": "BIO2",
        "subject": "Biochemistry",
        "video_id": "2Jgb_DpaQhM",
        "title": 'Proteins & Amino Acid Hierarchies (Primary to Quaternary)',
        "channel": 'Bozeman Science',
        "duration": "8:58",
        "url": "https://www.youtube.com/watch?v=2Jgb_DpaQhM",
        "thumbnail_url": "https://img.youtube.com/vi/2Jgb_DpaQhM/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/2Jgb_DpaQhM",
        "description": '20 amino acid side-chain properties, peptide bonds, alpha-helices, beta-sheets, and tertiary folding energetics.',
        "takeaways": [
            'Peptide bonds form via condensation between carboxyl and amino termini.',
            'Secondary structures are stabilized by backbone hydrogen bonds.',
            'Tertiary folding is driven by hydrophobic side chain burial and disulfide bridges.',
        ]
    },
    "BIO3": {
        "concept_id": "BIO3",
        "subject": "Biochemistry",
        "video_id": "X_YXTWU2maY",
        "title": 'An Introduction to Enzyme Kinetics (Michaelis-Menten: Km & Vmax)',
        "channel": 'Khan Academy',
        "duration": "14:12",
        "url": "https://www.youtube.com/watch?v=X_YXTWU2maY",
        "thumbnail_url": "https://img.youtube.com/vi/X_YXTWU2maY/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/X_YXTWU2maY",
        "description": 'Transition state lowering, Michaelis constant (Km), Vmax, Lineweaver-Burk plots, and competitive/allosteric inhibition.',
        "takeaways": [
            'Enzymes accelerate reaction rates by lowering activation energy (Delta G++).',
            'Km is the substrate concentration at which reaction rate is exactly half of Vmax.',
            'Competitive inhibitors increase apparent Km without altering Vmax.',
        ]
    },
    "BIO4": {
        "concept_id": "BIO4",
        "subject": "Biochemistry",
        "video_id": "gggC9vctvBQ",
        "title": 'Metabolism | Glycolysis (10 Enzymatic Steps)',
        "channel": 'Ninja Nerd',
        "duration": "32:15",
        "url": "https://www.youtube.com/watch?v=gggC9vctvBQ",
        "thumbnail_url": "https://img.youtube.com/vi/gggC9vctvBQ/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/gggC9vctvBQ",
        "description": 'Glucose phosphorylation, 10-step glycolytic pathway, net 2 ATP and 2 NADH generation, and phosphofructokinase-1 control.',
        "takeaways": [
            'Hexokinase and PFK-1 consume 2 ATP in the preparatory investment phase.',
            'Substrate-level phosphorylation by phosphoglycerate kinase and pyruvate kinase produces 4 ATP (net +2).',
            'PFK-1 is the primary committed allosteric rate-limiting checkpoint.',
        ]
    },
    "BIO5": {
        "concept_id": "BIO5",
        "subject": "Biochemistry",
        "video_id": "rr7IRYLqleg",
        "title": 'Metabolism | The Krebs Cycle (Citric Acid Cycle: 8 Steps)',
        "channel": 'Ninja Nerd',
        "duration": "28:40",
        "url": "https://www.youtube.com/watch?v=rr7IRYLqleg",
        "thumbnail_url": "https://img.youtube.com/vi/rr7IRYLqleg/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/rr7IRYLqleg",
        "description": 'Mitochondrial pyruvate dehydrogenase, acetyl-CoA condensation with oxaloacetate, GTP synthesis, and electron carriers.',
        "takeaways": [
            'Oxaloacetate (4C) combines with Acetyl-CoA (2C) to form Citrate (6C).',
            'Two oxidative decarboxylation steps release 2 CO2 molecules.',
            'Each turn yields 3 NADH, 1 FADH2, and 1 GTP/ATP.',
        ]
    },
    "BIO6": {
        "concept_id": "BIO6",
        "subject": "Biochemistry",
        "video_id": "mfgCcFXUZRk",
        "title": 'Electron Transport Chain & ATP Synthase Chemiosmosis',
        "channel": 'Khan Academy',
        "duration": "30:10",
        "url": "https://www.youtube.com/watch?v=mfgCcFXUZRk",
        "thumbnail_url": "https://img.youtube.com/vi/mfgCcFXUZRk/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/mfgCcFXUZRk",
        "description": 'Electron transport chain Complexes I-IV, chemiosmotic proton-motive force, and rotary catalysis of F0-F1 ATP synthase.',
        "takeaways": [
            'Complexes I, III, and IV pump protons into the intermembrane space to generate a proton-motive force.',
            'Oxygen serves as the terminal electron acceptor, being reduced to H2O.',
            'Proton backflow drives the mechanical rotation of F0-F1 ATP synthase to phosphorylate ADP to ATP.',
        ]
    },
    "BIO7": {
        "concept_id": "BIO7",
        "subject": "Biochemistry",
        "video_id": "qBCVVszQQNs",
        "title": 'Inside the Cell Membrane & Fluid Mosaic Model',
        "channel": 'Amoeba Sisters',
        "duration": "8:22",
        "url": "https://www.youtube.com/watch?v=qBCVVszQQNs",
        "thumbnail_url": "https://img.youtube.com/vi/qBCVVszQQNs/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/qBCVVszQQNs",
        "description": 'Phospholipid bilayers, cholesterol fluidity regulation, triacylglycerol storage, and mitochondrial beta-oxidation of fatty acids.',
        "takeaways": [
            'Phospholipids spontaneously form bilayers with hydrophobic cores and hydrophilic surfaces.',
            'Cholesterol buffers membrane fluidity across high and low temperature fluctuations.',
            'Beta-oxidation systematically breaks fatty acids into 2-carbon Acetyl-CoA units in the mitochondria.',
        ]
    },
    "BIO8": {
        "concept_id": "BIO8",
        "subject": "Biochemistry",
        "video_id": "gG7uCskUOrA",
        "title": 'From DNA to Protein - 3D (Replication, Transcription & Translation)',
        "channel": 'yourgenome',
        "duration": "13:28",
        "url": "https://www.youtube.com/watch?v=gG7uCskUOrA",
        "thumbnail_url": "https://img.youtube.com/vi/gG7uCskUOrA/hqdefault.jpg",
        "embed_url": "https://www.youtube.com/embed/gG7uCskUOrA",
        "description": 'DNA double-helix structure, DNA polymerase fidelity, RNA transcription, and ribosomal mRNA-to-protein translation.',
        "takeaways": [
            "DNA replication is semi-conservative and catalyzed 5' -> 3' by DNA Polymerase.",
            'RNA Polymerase synthesizes complementary pre-mRNA from template DNA.',
            'Ribosomes decode mRNA triplets using aminoacyl-tRNAs in the A, P, and E sites.',
        ]
    },
}


# ==============================================================================
# PRACTICE QUESTIONS FOR ALL NEW SUBJECTS
# ==============================================================================
MULTI_SUBJECT_QUESTIONS: List[Dict[str, Any]] = [
    # --- Computer Networks Questions ---
    {
        "id": "Q_CN1_01",
        "concept_id": "CN1",
        "subject": "Computer Networks",
        "type": "medium",
        "difficulty": 0.40,
        "is_transfer": False,
        "prompt": "Which OSI layer is directly responsible for converting raw bitstreams into discrete logical data frames and performing physical MAC addressing?",
        "options": [
            "A) Physical Layer (Layer 1)",
            "B) Data Link Layer (Layer 2)",
            "C) Network Layer (Layer 3)",
            "D) Transport Layer (Layer 4)"
        ],
        "correct_answer": "B) Data Link Layer (Layer 2)",
        "hints": [
            "The Physical layer transmits raw electrical or optical bits without frame delimiters.",
            "Layer 2 handles local network framing and MAC hardware addressing."
        ],
        "explanation": "The Data Link Layer (OSI Layer 2) packages raw physical bit streams into structured frames and applies 48-bit MAC addresses."
    },
    {
        "id": "Q_CN1_02",
        "concept_id": "CN1",
        "subject": "Computer Networks",
        "type": "hard",
        "difficulty": 0.75,
        "is_transfer": True,
        "prompt": "During outbound network transmission, data passes through layers. At which layer does a packet become encapsulated with both a header AND a trailing Frame Check Sequence (FCS) trailer?",
        "options": [
            "A) Transport Layer",
            "B) Network Layer",
            "C) Data Link Layer",
            "D) Physical Layer"
        ],
        "correct_answer": "C) Data Link Layer",
        "hints": [
            "Most layers only append a header at the front of the payload.",
            "This layer appends both a frame header and an error-checking CRC trailer at the end."
        ],
        "explanation": "The Data Link Layer is the unique OSI layer that appends both a header (source/dest MAC) and a trailer (CRC/FCS checksum)."
    },
    {
        "id": "Q_CN2_01",
        "concept_id": "CN2",
        "subject": "Computer Networks",
        "type": "easy",
        "difficulty": 0.30,
        "is_transfer": False,
        "prompt": "What is the standard length in bits of an Ethernet IEEE 802 Media Access Control (MAC) address?",
        "options": [
            "A) 32 bits",
            "B) 48 bits",
            "C) 64 bits",
            "D) 128 bits"
        ],
        "correct_answer": "B) 48 bits",
        "hints": [
            "IPv4 addresses are 32 bits, while IPv6 addresses are 128 bits.",
            "MAC addresses are represented as 12 hexadecimal characters (6 bytes)."
        ],
        "explanation": "An Ethernet MAC address is 48 bits long (6 octets, e.g. 00:1A:2B:3C:4D:5E)."
    },
    {
        "id": "Q_CN3_01",
        "concept_id": "CN3",
        "subject": "Computer Networks",
        "type": "medium",
        "difficulty": 0.50,
        "is_transfer": False,
        "prompt": "For an IPv4 subnet configured with prefix /27, how many assignable host IP addresses are available on that single subnet?",
        "options": [
            "A) 62",
            "B) 30",
            "C) 32",
            "D) 14"
        ],
        "correct_answer": "B) 30",
        "hints": [
            "An IPv4 address has 32 bits. If 27 bits are masked for network, how many host bits remain?",
            "Formula: Usable hosts = 2^(host_bits) - 2."
        ],
        "explanation": "32 - 27 = 5 host bits. Total addresses = 2^5 = 32. Subtracting network ID and broadcast ID yields 30 usable host IPs."
    },
    {
        "id": "Q_CN4_01",
        "concept_id": "CN4",
        "subject": "Computer Networks",
        "type": "medium",
        "difficulty": 0.55,
        "is_transfer": False,
        "prompt": "Which shortest-path graph algorithm does Open Shortest Path First (OSPF) execute on its link-state database to compute the optimal routing topology?",
        "options": [
            "A) Bellman-Ford Algorithm",
            "B) Floyd-Warshall Algorithm",
            "C) Dijkstra's Shortest Path Algorithm",
            "D) Kruskal's Minimum Spanning Tree"
        ],
        "correct_answer": "C) Dijkstra's Shortest Path Algorithm",
        "hints": [
            "Distance-vector protocols like RIP use Bellman-Ford.",
            "Link-state protocols build a full topological graph and run Dijkstra's algorithm."
        ],
        "explanation": "OSPF routers flood link-state packets and each independently runs Dijkstra's algorithm to compute the shortest-path tree."
    },
    {
        "id": "Q_CN5_01",
        "concept_id": "CN5",
        "subject": "Computer Networks",
        "type": "easy",
        "difficulty": 0.25,
        "is_transfer": False,
        "prompt": "What is the correct 3-step packet flag sequence exchanged by client and server during a standard TCP connection handshake?",
        "options": [
            "A) ACK -> SYN -> ACK",
            "B) SYN -> SYN-ACK -> ACK",
            "C) FIN -> ACK -> FIN-ACK",
            "D) PUSH -> ACK -> SYN"
        ],
        "correct_answer": "B) SYN -> SYN-ACK -> ACK",
        "hints": [
            "The client initiates by sending a synchronize flag (SYN).",
            "The server acknowledges and synchronizes (SYN-ACK), then client finalizes with ACK."
        ],
        "explanation": "TCP establishes reliable connection state through the canonical SYN -> SYN-ACK -> ACK 3-way handshake."
    },
    {
        "id": "Q_CN6_01",
        "concept_id": "CN6",
        "subject": "Computer Networks",
        "type": "hard",
        "difficulty": 0.70,
        "is_transfer": True,
        "prompt": "In TCP Congestion Control, what mathematical adjustment does the congestion window (cwnd) undergo upon detecting packet loss via triple duplicate ACKs under AIMD?",
        "options": [
            "A) cwnd resets to 1 Maximum Segment Size (MSS)",
            "B) cwnd halves: cwnd = cwnd / 2 (Multiplicative Decrease)",
            "C) cwnd remains unchanged while window timer expires",
            "D) cwnd increases linearly by +1 MSS"
        ],
        "correct_answer": "B) cwnd halves: cwnd = cwnd / 2 (Multiplicative Decrease)",
        "hints": [
            "AIMD stands for Additive Increase Multiplicative Decrease.",
            "Triple duplicate ACKs trigger Fast Retransmit and Fast Recovery, cutting cwnd in half rather than crashing to 1 MSS."
        ],
        "explanation": "Under AIMD Fast Recovery, cwnd is halved (cwnd/2) and ssthresh is set to the new cwnd, maintaining throughput without full restart."
    },
    {
        "id": "Q_CN7_01",
        "concept_id": "CN7",
        "subject": "Computer Networks",
        "type": "easy",
        "difficulty": 0.30,
        "is_transfer": False,
        "prompt": "Which DNS record type is queried to resolve a human-readable domain name (e.g. google.com) directly into an IPv4 address?",
        "options": [
            "A) A Record",
            "B) AAAA Record",
            "C) MX Record",
            "D) CNAME Record"
        ],
        "correct_answer": "A) A Record",
        "hints": [
            "AAAA maps to IPv6 addresses.",
            "A single 'A' record maps domain names to standard 32-bit IPv4 addresses."
        ],
        "explanation": "An 'A' (Address) record maps a hostname to its IPv4 address. 'AAAA' is used for 128-bit IPv6 addresses."
    },
    {
        "id": "Q_CN8_01",
        "concept_id": "CN8",
        "subject": "Computer Networks",
        "type": "hard",
        "difficulty": 0.65,
        "is_transfer": False,
        "prompt": "In Transport Layer Security (TLS 1.3), why is asymmetric public key cryptography used primarily during the initial handshake rather than for encrypting the entire web session payload?",
        "options": [
            "A) Asymmetric encryption is mathematically vulnerable to replay attacks",
            "B) Asymmetric encryption is computationally hundreds of times slower than symmetric ciphers (e.g. AES)",
            "C) Asymmetric keys cannot encrypt payloads larger than 256 bytes",
            "D) Web browsers only support symmetric algorithms"
        ],
        "correct_answer": "B) Asymmetric encryption is computationally hundreds of times slower than symmetric ciphers (e.g. AES)",
        "hints": [
            "Public key math involves modular exponentiation of very large prime numbers.",
            "Symmetric ciphers like AES-GCM use simple bit-shifts and substitution-permutation networks."
        ],
        "explanation": "Asymmetric cryptography is computationally expensive. It is used during the handshake to establish a shared secret, after which fast symmetric ciphers (AES) encrypt bulk traffic."
    },

    # --- Artificial Intelligence Questions ---
    {
        "id": "Q_AI1_01",
        "concept_id": "AI1",
        "subject": "Artificial Intelligence",
        "type": "medium",
        "difficulty": 0.45,
        "is_transfer": False,
        "prompt": "In the A* Search algorithm with evaluation function f(n) = g(n) + h(n), what property must the heuristic function h(n) satisfy to guarantee finding the mathematically optimal shortest path?",
        "options": [
            "A) Monotonicity with h(goal) > 0",
            "B) Admissibility (h(n) never overestimates true cost to goal)",
            "C) Strict proportionality to Euclidean distance",
            "D) Completeness under depth-first ordering"
        ],
        "correct_answer": "B) Admissibility (h(n) never overestimates true cost to goal)",
        "hints": [
            "If a heuristic exaggerates the cost, A* might ignore the true optimal path.",
            "Admissibility means h(n) <= h*(n) for all nodes n."
        ],
        "explanation": "An admissible heuristic never overestimates the true remaining cost to the goal, ensuring A* tree search never misses the optimal shortest path."
    },
    {
        "id": "Q_AI2_01",
        "concept_id": "AI2",
        "subject": "Artificial Intelligence",
        "type": "hard",
        "difficulty": 0.65,
        "is_transfer": False,
        "prompt": "In a Minimax game tree with Alpha-Beta pruning, when can a subtree search beneath a Minimizing node be immediately pruned?",
        "options": [
            "A) When beta <= alpha",
            "B) When alpha reaches zero",
            "C) When beta > alpha",
            "D) When all terminal leaves are evaluated"
        ],
        "correct_answer": "A) When beta <= alpha",
        "hints": [
            "Alpha is the best value Max can guarantee so far.",
            "If Min can force a value smaller than or equal to Alpha, Max will never choose this branch."
        ],
        "explanation": "When beta <= alpha, the maximizing parent already has a guaranteed move better than what this minimizing branch offers, allowing instant pruning."
    },
    {
        "id": "Q_AI3_01",
        "concept_id": "AI3",
        "subject": "Artificial Intelligence",
        "type": "easy",
        "difficulty": 0.35,
        "is_transfer": False,
        "prompt": "What activation function is applied to the linear combination z = w^T * x + b in Logistic Regression to bound the output within valid probability range [0, 1]?",
        "options": [
            "A) Rectified Linear Unit (ReLU)",
            "B) Sigmoid Function 1 / (1 + e^(-z))",
            "C) Hyperbolic Tangent (tanh)",
            "D) Softplus Function"
        ],
        "correct_answer": "B) Sigmoid Function 1 / (1 + e^(-z))",
        "hints": [
            "It forms a smooth S-curve mapped between 0 and 1.",
            "Sigmoid sigma(z) = 1 / (1 + exp(-z))."
        ],
        "explanation": "The Sigmoid function squashes any real-valued number into the range (0, 1), representing valid posterior probabilities in binary classification."
    },
    {
        "id": "Q_AI4_01",
        "concept_id": "AI4",
        "subject": "Artificial Intelligence",
        "type": "medium",
        "difficulty": 0.50,
        "is_transfer": False,
        "prompt": "Why has the Rectified Linear Unit (ReLU: f(x) = max(0, x)) largely superseded the Sigmoid function as default activation in hidden layers of deep neural networks?",
        "options": [
            "A) ReLU prevents the vanishing gradient problem for positive activations",
            "B) ReLU restricts activations to between -1 and +1",
            "C) ReLU is continuously differentiable at exactly zero",
            "D) ReLU requires calculating costly exponential powers"
        ],
        "correct_answer": "A) ReLU prevents the vanishing gradient problem for positive activations",
        "hints": [
            "Sigmoid gradients saturate near 0 when inputs are large positive or negative values.",
            "ReLU derivative is constant 1 for any positive input x > 0."
        ],
        "explanation": "ReLU maintains a constant derivative of 1 for all positive inputs, allowing gradients to flow back through dozens of layers without vanishing."
    },
    {
        "id": "Q_AI5_01",
        "concept_id": "AI5",
        "subject": "Artificial Intelligence",
        "type": "hard",
        "difficulty": 0.80,
        "is_transfer": True,
        "prompt": "Mathematically, the Backpropagation algorithm is an efficient implementation of which rule of multivariate calculus applied across computational graphs?",
        "options": [
            "A) Integration by Parts",
            "B) The Multivariate Chain Rule",
            "C) Taylor Series Expansion",
            "D) L'Hopital's Rule"
        ],
        "correct_answer": "B) The Multivariate Chain Rule",
        "hints": [
            "It decomposes the derivative of composite functions dL/dw = (dL/da) * (da/dz) * (dz/dw).",
            "Calculus chain rule multiplies partial derivatives backwards."
        ],
        "explanation": "Backpropagation recursively applies the multivariate chain rule from the scalar loss backward through intermediate node tensors."
    },
    {
        "id": "Q_AI6_01",
        "concept_id": "AI6",
        "subject": "Artificial Intelligence",
        "type": "medium",
        "difficulty": 0.55,
        "is_transfer": False,
        "prompt": "In Convolutional Neural Networks, what is the primary structural benefit of using parameter sharing (sliding identical kernel weights across the image)?",
        "options": [
            "A) Eliminates the need for training labels",
            "B) Enforces translational invariance and drastically reduces parameter count",
            "C) Prevents the network from learning spatial patterns",
            "D) Guarantees convex loss landscapes"
        ],
        "correct_answer": "B) Enforces translational invariance and drastically reduces parameter count",
        "hints": [
            "A feature detector (like an edge detector) should detect an edge regardless of where it appears.",
            "Sharing weights across all positions prevents millions of redundant weights."
        ],
        "explanation": "Parameter sharing allows a kernel to detect features anywhere in an image while reducing parameters compared to fully connected layers."
    },
    {
        "id": "Q_AI7_01",
        "concept_id": "AI7",
        "subject": "Artificial Intelligence",
        "type": "hard",
        "difficulty": 0.75,
        "is_transfer": True,
        "prompt": "In the Transformer Self-Attention formula Attention(Q, K, V) = softmax((Q * K^T) / sqrt(d_k)) * V, why is the dot product divided by the scaling factor sqrt(d_k)?",
        "options": [
            "A) To ensure Query and Key matrices have equal dimensions",
            "B) To prevent large dot products from pushing softmax into regions with vanishingly small gradients",
            "C) To convert the attention matrix into a lower-triangular causal mask",
            "D) To enforce orthogonality between Query and Value vectors"
        ],
        "correct_answer": "B) To prevent large dot products from pushing softmax into regions with vanishingly small gradients",
        "hints": [
            "For large vector dimensions d_k, dot products grow large in magnitude.",
            "Large inputs cause softmax outputs to become extreme (0 or 1), where derivatives approach zero."
        ],
        "explanation": "For large d_k, dot products grow proportionally to d_k, pushing softmax into saturation with tiny gradients. Scaling by 1/sqrt(d_k) stabilizes variance."
    },
    {
        "id": "Q_AI8_01",
        "concept_id": "AI8",
        "subject": "Artificial Intelligence",
        "type": "hard",
        "difficulty": 0.70,
        "is_transfer": False,
        "prompt": "In Reinforcement Learning, what fundamental relation expresses the value of a state V(s) as the immediate expected reward plus the discounted value of successor states?",
        "options": [
            "A) The Bellman Equation",
            "B) Bayes' Theorem",
            "C) The Markov Chain Stationary Theorem",
            "D) The Central Limit Theorem"
        ],
        "correct_answer": "A) The Bellman Equation",
        "hints": [
            "V(s) = max_a [ R(s, a) + gamma * sum_s' P(s'|s,a) * V(s') ].",
            "Named after Richard Bellman, the founder of dynamic programming."
        ],
        "explanation": "The Bellman Equation recursively defines the value of a state or state-action pair in Markov Decision Processes."
    },

    # --- Formal Languages & Automata Questions ---
    {
        "id": "Q_FLA1_01",
        "concept_id": "FLA1",
        "subject": "Formal Languages & Automata",
        "type": "easy",
        "difficulty": 0.25,
        "is_transfer": False,
        "prompt": "Given alphabet Sigma = {0, 1}, does the Kleene star set Sigma* contain the empty string epsilon?",
        "options": [
            "A) Yes, Sigma* always includes epsilon because Sigma^0 = {epsilon}",
            "B) No, only positive closure Sigma+ includes epsilon",
            "C) Only if explicitly defined in Sigma",
            "D) No, epsilon is not a valid formal string"
        ],
        "correct_answer": "A) Yes, Sigma* always includes epsilon because Sigma^0 = {epsilon}",
        "hints": [
            "Sigma* is defined as the union of Sigma^0, Sigma^1, Sigma^2, ...",
            "Any set raised to the 0th power equals {epsilon}."
        ],
        "explanation": "By definition, Sigma* = Union_{k=0..infinity} Sigma^k. Since Sigma^0 = {epsilon}, epsilon is always an element of Sigma*."
    },
    {
        "id": "Q_FLA2_01",
        "concept_id": "FLA2",
        "subject": "Formal Languages & Automata",
        "type": "medium",
        "difficulty": 0.45,
        "is_transfer": False,
        "prompt": "What is the minimum number of states required in a Deterministic Finite Automaton (DFA) over alphabet {0, 1} to accept strings ending with '01'?",
        "options": [
            "A) 2 states",
            "B) 3 states",
            "C) 4 states",
            "D) 5 states"
        ],
        "correct_answer": "B) 3 states",
        "hints": [
            "State 0: Start / reset (no match).",
            "State 1: Saw '0'.",
            "State 2: Saw '01' (Accepting state)."
        ],
        "explanation": "Exactly 3 states are required: q0 (start), q1 (last saw 0), and q2 (accepting, last saw 01). Seeing 0 in q2 transitions to q1; seeing 1 transitions to q0."
    },
    {
        "id": "Q_FLA3_01",
        "concept_id": "FLA3",
        "subject": "Formal Languages & Automata",
        "type": "medium",
        "difficulty": 0.60,
        "is_transfer": False,
        "prompt": "If an NFA has n states, what is the theoretical maximum number of states in the equivalent minimal DFA generated via the Subset Construction algorithm?",
        "options": [
            "A) n^2",
            "B) 2^n",
            "C) 2n",
            "D) n!"
        ],
        "correct_answer": "B) 2^n",
        "hints": [
            "Each state in the converted DFA represents a subset of states from the NFA.",
            "The power set of a set with n elements has 2^n subsets."
        ],
        "explanation": "Subset construction pairs each DFA state with a subset of NFA states. For n states, the power set size is 2^n."
    },
    {
        "id": "Q_FLA4_01",
        "concept_id": "FLA4",
        "subject": "Formal Languages & Automata",
        "type": "hard",
        "difficulty": 0.75,
        "is_transfer": True,
        "prompt": "Why does the Pumping Lemma prove that the language L = {0^n 1^n | n >= 0} is NOT regular?",
        "options": [
            "A) Because 0^n 1^n contains an infinite alphabet",
            "B) Because any pumping segment y in string s = 0^p 1^p consists entirely of 0s, altering the count equality when pumped",
            "C) Because regular languages cannot contain the character 1",
            "D) Because finite automata cannot have accepting states"
        ],
        "correct_answer": "B) Because any pumping segment y in string s = 0^p 1^p consists entirely of 0s, altering the count equality when pumped",
        "hints": [
            "Pumping Lemma specifies |xy| <= p, so y must reside entirely within the leading 0s.",
            "Pumping y to i=2 yields 0^(p+|y|) 1^p, which has more 0s than 1s, violating language membership."
        ],
        "explanation": "Since |xy| <= p, the substring y consists solely of 0s. Pumping y creates strings with unequal numbers of 0s and 1s, proving L is not regular."
    },
    {
        "id": "Q_FLA5_01",
        "concept_id": "FLA5",
        "subject": "Formal Languages & Automata",
        "type": "medium",
        "difficulty": 0.50,
        "is_transfer": False,
        "prompt": "A Context-Free Grammar is formally classified as 'ambiguous' if and only if:",
        "options": [
            "A) It generates an infinite number of strings",
            "B) Some string in its language has two or more distinct leftmost derivations (or parse trees)",
            "C) It contains epsilon production rules",
            "D) It cannot be parsed in polynomial time"
        ],
        "correct_answer": "B) Some string in its language has two or more distinct leftmost derivations (or parse trees)",
        "hints": [
            "Ambiguity relates to parse tree uniqueness.",
            "If a grammar allows multiple interpretations for the exact same statement, it is ambiguous."
        ],
        "explanation": "Grammar ambiguity means at least one string admits multiple valid syntax parse trees or leftmost derivations."
    },
    {
        "id": "Q_FLA6_01",
        "concept_id": "FLA6",
        "subject": "Formal Languages & Automata",
        "type": "medium",
        "difficulty": 0.55,
        "is_transfer": False,
        "prompt": "What memory structure distinguishes a Pushdown Automaton (PDA) from a standard Finite State Automaton (DFA/NFA)?",
        "options": [
            "A) Random Access Memory (RAM) address registers",
            "B) An unbounded Last-In-First-Out (LIFO) stack",
            "C) A bidirectional read/write tape",
            "D) A FIFO priority queue"
        ],
        "correct_answer": "B) An unbounded Last-In-First-Out (LIFO) stack",
        "hints": [
            "PDAs can push symbols onto and pop symbols off of this structure.",
            "LIFO stack memory enables matching opening and closing delimiters."
        ],
        "explanation": "A Pushdown Automaton is a finite automaton equipped with an unbounded LIFO stack, enabling recognition of context-free languages."
    },
    {
        "id": "Q_FLA7_01",
        "concept_id": "FLA7",
        "subject": "Formal Languages & Automata",
        "type": "hard",
        "difficulty": 0.70,
        "is_transfer": False,
        "prompt": "Which theoretical thesis states that every physically realizable algorithmic computation can be simulated by a Universal Turing Machine?",
        "options": [
            "A) The Church-Turing Thesis",
            "B) Cook's Theorem",
            "C) Godel's Incompleteness Theorem",
            "D) Moore's Law"
        ],
        "correct_answer": "A) The Church-Turing Thesis",
        "hints": [
            "Jointly named after Alonzo Church (lambda calculus) and Alan Turing (Turing machines).",
            "It defines the universal baseline of effective computability."
        ],
        "explanation": "The Church-Turing thesis posits that any function computable by an intuitive algorithm can be computed by a Turing machine."
    },
    {
        "id": "Q_FLA8_01",
        "concept_id": "FLA8",
        "subject": "Formal Languages & Automata",
        "type": "hard",
        "difficulty": 0.85,
        "is_transfer": True,
        "prompt": "Alan Turing's proof that the Halting Problem is undecidable relies upon which fundamental mathematical proof technique first introduced by Georg Cantor?",
        "options": [
            "A) Mathematical Induction",
            "B) Diagonalization Proof by Contradiction",
            "C) Squeeze Theorem",
            "D) Dynamic Programming"
        ],
        "correct_answer": "B) Diagonalization Proof by Contradiction",
        "hints": [
            "Cantor used it to prove the uncountability of real numbers.",
            "Turing constructed a hypothetical machine D that halts if and only if it does not halt."
        ],
        "explanation": "Turing employed Cantor's diagonalization argument to construct a contradiction: a machine designed to do the opposite of what the hypothetical halting decider predicts."
    },

    # --- Biochemistry Questions ---
    {
        "id": "Q_BIO1_01",
        "concept_id": "BIO1",
        "subject": "Biochemistry",
        "type": "medium",
        "difficulty": 0.40,
        "is_transfer": False,
        "prompt": "According to the Henderson-Hasselbalch equation (pH = pKa + log([A-]/[HA])), what is the resulting pH of a buffer solution when the conjugate base concentration [A-] equals the weak acid concentration [HA]?",
        "options": [
            "A) pH = 7.00",
            "B) pH = pKa",
            "C) pH = pKa + 1.0",
            "D) pH = 0.00"
        ],
        "correct_answer": "B) pH = pKa",
        "hints": [
            "When [A-] = [HA], the ratio [A-]/[HA] = 1.",
            "log10(1) = 0."
        ],
        "explanation": "When conjugate base and acid concentrations are equal, log(1) = 0, so pH = pKa. This represents maximum buffering capacity."
    },
    {
        "id": "Q_BIO2_01",
        "concept_id": "BIO2",
        "subject": "Biochemistry",
        "type": "easy",
        "difficulty": 0.30,
        "is_transfer": False,
        "prompt": "What chemical bond links the alpha-carboxyl group of one amino acid to the alpha-amino group of an adjacent amino acid in a polypeptide backbone?",
        "options": [
            "A) Phosphodiester bond",
            "B) Peptide (amide) bond",
            "C) Glycosidic bond",
            "D) Ester linkage"
        ],
        "correct_answer": "B) Peptide (amide) bond",
        "hints": [
            "Formed via a condensation (dehydration) reaction releasing H2O.",
            "It has partial double-bond character due to resonance."
        ],
        "explanation": "A peptide bond is a planar covalent amide linkage formed between the carboxyl carbon and amino nitrogen of adjacent amino acids."
    },
    {
        "id": "Q_BIO3_01",
        "concept_id": "BIO3",
        "subject": "Biochemistry",
        "type": "hard",
        "difficulty": 0.70,
        "is_transfer": False,
        "prompt": "In Michaelis-Menten enzyme kinetics, how does the presence of a classic Competitive Inhibitor affect the apparent Km and Vmax values of the enzyme?",
        "options": [
            "A) Apparent Km increases while Vmax remains unchanged",
            "B) Both apparent Km and Vmax decrease proportionally",
            "C) Vmax decreases while Km remains unchanged",
            "D) Apparent Km decreases while Vmax increases"
        ],
        "correct_answer": "A) Apparent Km increases while Vmax remains unchanged",
        "hints": [
            "A competitive inhibitor binds to the same active site as the substrate.",
            "High substrate concentration can outcompete the inhibitor to reach full Vmax."
        ],
        "explanation": "Competitive inhibitors compete for the active site, requiring higher substrate concentration to reach half-maximal velocity (higher Km), while Vmax remains achievable."
    },
    {
        "id": "Q_BIO4_01",
        "concept_id": "BIO4",
        "subject": "Biochemistry",
        "type": "medium",
        "difficulty": 0.50,
        "is_transfer": False,
        "prompt": "What is the net yield of ATP and NADH molecules produced per single molecule of glucose entering the complete 10-step Glycolysis pathway?",
        "options": [
            "A) 4 ATP and 4 NADH",
            "B) Net 2 ATP and 2 NADH",
            "C) Net 2 ATP and 0 NADH",
            "D) 32 ATP and 6 NADH"
        ],
        "correct_answer": "B) Net 2 ATP and 2 NADH",
        "hints": [
            "Glycolysis invests 2 ATP in the preparatory phase.",
            "It produces 4 ATP in the payoff phase: 4 - 2 = 2 net ATP."
        ],
        "explanation": "Glycolysis consumes 2 ATP and generates 4 ATP by substrate-level phosphorylation, yielding net 2 ATP and 2 NADH per glucose."
    },
    {
        "id": "Q_BIO5_01",
        "concept_id": "BIO5",
        "subject": "Biochemistry",
        "type": "medium",
        "difficulty": 0.55,
        "is_transfer": False,
        "prompt": "In the initial step of the Citric Acid Cycle (Krebs Cycle), what 4-carbon intermediate condenses with 2-carbon Acetyl-CoA to synthesize 6-carbon Citrate?",
        "options": [
            "A) Malate",
            "B) Oxaloacetate",
            "C) Alpha-ketoglutarate",
            "D) Succinate"
        ],
        "correct_answer": "B) Oxaloacetate",
        "hints": [
            "The reaction is catalyzed by citrate synthase.",
            "Oxaloacetate (4C) + Acetyl-CoA (2C) -> Citrate (6C) + CoA-SH."
        ],
        "explanation": "Citrate synthase condenses 4-carbon Oxaloacetate with 2-carbon Acetyl-CoA to form 6-carbon Citrate."
    },
    {
        "id": "Q_BIO6_01",
        "concept_id": "BIO6",
        "subject": "Biochemistry",
        "type": "hard",
        "difficulty": 0.75,
        "is_transfer": True,
        "prompt": "During Oxidative Phosphorylation in mitochondria, what physical mechanism powers the catalytic synthesis of ATP from ADP and inorganic phosphate by ATP Synthase?",
        "options": [
            "A) Direct substrate phosphorylation by cytochrome c",
            "B) Chemiosmotic proton-motive force driving rotation of the F0 subunit",
            "C) Passive diffusion of glucose across the outer membrane",
            "D) Thermal cleavage of GTP high-energy bonds"
        ],
        "correct_answer": "B) Chemiosmotic proton-motive force driving rotation of the F0 subunit",
        "hints": [
            "Peter Mitchell's chemiosmotic hypothesis.",
            "Protons pumped into the intermembrane space flow through the F0 stalk, causing mechanical rotation."
        ],
        "explanation": "Protons flow down their electrochemical gradient through the membrane-embedded F0 rotor of ATP Synthase, driving mechanical rotation that catalyzes ATP synthesis in F1."
    },
    {
        "id": "Q_BIO7_01",
        "concept_id": "BIO7",
        "subject": "Biochemistry",
        "type": "medium",
        "difficulty": 0.45,
        "is_transfer": False,
        "prompt": "Why do phospholipid bilayer membranes with a higher percentage of cis-unsaturated fatty acid tails exhibit greater fluid permeability at lower temperatures?",
        "options": [
            "A) Unsaturated tails have rigid linear shapes that pack tightly together",
            "B) Cis double bonds introduce permanent kinks that prevent tight crystalline hydrocarbon packing",
            "C) Cis double bonds form ionic bonds with extracellular sodium",
            "D) Unsaturated fatty acids dissolve cholesterol completely"
        ],
        "correct_answer": "B) Cis double bonds introduce permanent kinks that prevent tight crystalline hydrocarbon packing",
        "hints": [
            "Saturated fats pack closely into solid fats (like butter).",
            "Cis double bonds create bent kinks, keeping oils liquid at room temperature."
        ],
        "explanation": "Cis double bonds introduce structural kinks into hydrocarbon chains, inhibiting tight van der Waals packing and preserving membrane fluidity at cold temperatures."
    },
    {
        "id": "Q_BIO8_01",
        "concept_id": "BIO8",
        "subject": "Biochemistry",
        "type": "easy",
        "difficulty": 0.35,
        "is_transfer": False,
        "prompt": "In the Watson-Crick DNA double helix model, how many hydrogen bonds stabilize the pairing between Guanine (G) and Cytosine (C)?",
        "options": [
            "A) 1 hydrogen bond",
            "B) 2 hydrogen bonds",
            "C) 3 hydrogen bonds",
            "D) 4 hydrogen bonds"
        ],
        "correct_answer": "C) 3 hydrogen bonds",
        "hints": [
            "Adenine (A) and Thymine (T) are held together by 2 hydrogen bonds.",
            "Guanine and Cytosine form a stronger 3-hydrogen-bond interaction."
        ],
        "explanation": "Guanine and Cytosine pair via 3 specific hydrogen bonds, giving G-C rich DNA regions higher thermal denaturation melting temperatures (Tm)."
    },
]


def get_subject_concepts(subject_name: str = "Mathematics") -> Dict[str, Dict[str, Any]]:
    """Returns the concept dictionary for a requested subject."""
    return SUBJECTS_CONCEPTS_MAP.get(subject_name, MATH_CONCEPTS)


def get_video_for_concept(concept_id: str) -> Optional[Dict[str, Any]]:
    """Fetches the curated YouTube video metadata for a given concept ID."""
    return YOUTUBE_VIDEOS_CATALOG.get(concept_id)


def get_concept_video(concept_id: str) -> Optional[Dict[str, Any]]:
    """Alias for get_video_for_concept."""
    return get_video_for_concept(concept_id)


def get_videos_for_subject(subject_name: str) -> List[Dict[str, Any]]:
    """Returns all curated YouTube video metadata objects for a given subject."""
    concepts = get_subject_concepts(subject_name)
    videos = []
    for cid in concepts:
        v = YOUTUBE_VIDEOS_CATALOG.get(cid)
        if v:
            videos.append(v)
    return videos


def get_questions_for_subject_and_concept(subject_name: str, concept_id: str) -> List[Dict[str, Any]]:
    """Returns practice questions for a concept in a given subject."""
    return [q for q in MULTI_SUBJECT_QUESTIONS if q.get("concept_id") == concept_id]

TOPIC_BRIEF_EXPLANATIONS: Dict[str, Dict[str, Any]] = {
    "C1": {
        "concept_id": "C1",
        "title": 'Fraction Basics: Part-Whole & The Number Line',
        "summary": 'Represents a part of a whole quantity or an exact coordinate on a continuous number line between 0 and 1.',
        "core_principles": [
            'Denominator (b != 0): Represents the total number of equal partitioned segments comprising one whole.',
            'Numerator (a): Counts how many of those equal partitioned segments are selected or accumulated.',
            'Number Line Placement: On a 0-to-1 interval, unit fraction 1/b divides the segment into b equal lengths.',
        ],
        "key_formula": 'Fraction = a / b (b != 0). On a number line: Coordinate = a * (1 / b).',
        "example": 'A 1-meter ribbon divided into 4 equal pieces has segments of length 1/4 m. Selecting 3 pieces yields 3/4 m.',
        "common_pitfall": 'Viewing numerator and denominator as two independent numbers rather than a single unified relational value.',
    },
    "C2": {
        "concept_id": "C2",
        "title": 'Equivalent Fractions & Simplifying to Lowest Terms',
        "summary": 'Two fractions represent the identical mathematical value if both terms are multiplied or divided by the same non-zero integer (multiplying by 1).',
        "core_principles": [
            'Identity Property of Multiplication: Multiplying by k/k (where k != 0) equals multiplying by 1, leaving numerical value unchanged.',
            'Simplification: Dividing numerator and denominator by their Greatest Common Divisor (GCD) yields irreducible lowest terms.',
            'Coprimality: A fraction a/b is fully simplified when gcd(a, b) = 1.',
        ],
        "key_formula": 'a / b = (a * k) / (b * k); Simplified = (a / gcd(a, b)) / (b / gcd(a, b)).',
        "example": 'To simplify 18/24: gcd(18, 24) = 6. Dividing gives (18 / 6) / (24 / 6) = 3/4.',
        "common_pitfall": 'Subtracting or adding the same number to both terms (e.g. 3/5 != (3-1)/(5-1) = 2/4).',
    },
    "C3": {
        "concept_id": "C3",
        "title": 'Comparing and Ordering Fractions with Unlike Denominators',
        "summary": 'Determines the relative magnitude of rational fractions using common denominators, benchmark testing, or algebraic cross-multiplication.',
        "core_principles": [
            'Common Denominator Rule: Convert fractions to share a common denominator (LCM of denominators) to compare numerators directly.',
            'Cross-Multiplication Shortcut: To compare a/b and c/d (with b, d > 0), compare cross-products a*d and b*c.',
            'Benchmark Strategy: Compare fractions against intuitive anchors like 1/2, 0, or 1 for fast mental checks.',
        ],
        "key_formula": 'If a*d > b*c, then a/b > c/d. If a*d < b*c, then a/b < c/d.',
        "example": 'Compare 3/5 vs 4/7: Cross-multiply 3*7 = 21 and 5*4 = 20. Since 21 > 20, 3/5 > 4/7.',
        "common_pitfall": 'Assuming a fraction with larger numbers is always greater (e.g. mistakenly believing 5/12 > 1/2).',
    },
    "C4": {
        "concept_id": "C4",
        "title": 'Adding & Subtracting Fractions with Like and Unlike Denominators',
        "summary": 'Fractions cannot be added or subtracted until they represent identical partition sizes by scaling to a Least Common Denominator (LCD).',
        "core_principles": [
            'Like Denominators: Add or subtract numerators directly while keeping the common denominator unchanged.',
            'Unlike Denominators: Find the Least Common Multiple (LCM) of the denominators and scale each fraction before combining.',
            'Post-Operation Reduction: Always simplify the resulting sum or difference to lowest terms.',
        ],
        "key_formula": 'a/b +- c/d = (a*d +- b*c) / (b*d) = (a*(LCD/b) +- c*(LCD/d)) / LCD.',
        "example": '1/4 + 1/6: LCD(4, 6) = 12. Convert: 3/12 + 2/12 = 5/12.',
        "common_pitfall": 'Adding denominators together: 1/2 + 1/2 != (1+1)/(2+2) = 2/4 = 1/2!',
    },
    "C5": {
        "concept_id": "C5",
        "title": 'Multiplying and Dividing Fractions Step-by-Step',
        "summary": 'Multiplying fractions computes the area of overlapping partitioned dimensions. Dividing multiplies by the multiplicative inverse (reciprocal).',
        "core_principles": [
            'Multiplication Algorithm: Multiply numerators straight across and denominators straight across: (a/b) * (c/d) = (a*c)/(b*d).',
            'Early Cross-Cancellation: Cancel common factors between any numerator and denominator prior to multiplication.',
            'Division Algorithm (Keep-Change-Flip): Dividing by c/d is mathematically identical to multiplying by its reciprocal d/c.',
        ],
        "key_formula": '(a/b) * (c/d) = (a*c) / (b*d); (a/b) / (c/d) = (a/b) * (d/c) = (a*d) / (b*c).',
        "example": '(2/3) / (4/5) = (2/3) * (5/4) = 10/12 = 5/6.',
        "common_pitfall": 'Inverting the first fraction instead of the second divisor fraction during division.',
    },
    "C6": {
        "concept_id": "C6",
        "title": 'Ratio Basics: Part-to-Part & Part-to-Whole Comparisons',
        "summary": "Quantifies the relative scale between two quantities, formatted as colon notation (a:b), words ('a to b'), or simplified fractions.",
        "core_principles": [
            'Part-to-Part Comparison: Relates one distinct subset to another subset (e.g. 3 blue to 4 red).',
            'Part-to-Whole Comparison: Relates one subset to the total sum of all parts: a / (a + b).',
            'Scale Independence: Multiplying or dividing both parts by the same positive factor preserves the ratio.',
        ],
        "key_formula": 'Part-to-Part: a : b. Part-to-Whole Fraction: a / (a + b) and b / (a + b).',
        "example": 'In a class with 12 boys and 16 girls, the boy:girl ratio is 12:16 = 3:4. The boy:total ratio is 12:28 = 3:7.',
        "common_pitfall": 'Confusing a part-to-part ratio (3:4) with a fraction of the whole (which is 3/7, not 3/4).',
    },
    "C7": {
        "concept_id": "C7",
        "title": 'Equivalent Ratios and Unit Rate Calculation',
        "summary": 'A unit rate normalizes a ratio so that its denominator equals exactly 1 unit, enabling direct price, speed, and efficiency comparisons.',
        "core_principles": [
            'Unit Rate Definition: A rate in which the second quantity is 1 unit (e.g., miles per 1 hour, dollars per 1 pound).',
            'Computation: Divide the first quantity by the second quantity.',
            'Proportional Scaling: Multiply the unit rate by any target count to solve for any proportional quantity.',
        ],
        "key_formula": 'Unit Rate k = Quantity A / Quantity B. Linear scaling equation: y = k * x.',
        "example": 'Driving 180 miles on 6 gallons of gas gives 180 / 6 = 30 miles per gallon. To drive 300 miles requires 300 / 30 = 10 gallons.',
        "common_pitfall": 'Inverting the division when calculating unit cost (e.g., dividing ounces by dollars instead of dollars by ounces).',
    },
    "C8": {
        "concept_id": "C8",
        "title": 'Proportion: Solving a/b = c/d with Cross-Multiplication',
        "summary": 'An equation stating that two rational ratios are equal, resolved algebraically by equating diagonal cross-products.',
        "core_principles": [
            'Cross-Product Equality: In any true proportion a/b = c/d, the cross-products a*d and b*c are strictly equal.',
            'Single Variable Isolation: When one term is unknown (e.g. a/b = x/d), isolate x: x = (a*d) / b.',
            'Geometric & Physical Applications: Foundation of similar figures, map scale drawings, and recipe adjustments.',
        ],
        "key_formula": 'a / b = c / d  <=>  a * d = b * c  =>  x = (b * c) / a.',
        "example": 'Solve 5/8 = x/56: 8 * x = 5 * 56 = 280 => x = 280 / 8 = 35.',
        "common_pitfall": 'Cross-multiplying when adding or multiplying fractions instead of when solving an equality between two ratios.',
    },
    "C9": {
        "concept_id": "C9",
        "title": 'Percentages as Ratios and Decimal Conversions',
        "summary": 'A percentage is a standardized rational ratio with a fixed denominator of 100, providing universal comparison across disparate scales.',
        "core_principles": [
            "Etymology: 'Per cent' literally translates to 'per one hundred' (parts out of 100).",
            'Decimal Conversion: Shift the decimal point two places left to convert percent to decimal (45% = 0.45).',
            'Fraction to Percent: Divide numerator by denominator, then multiply by 100%.',
        ],
        "key_formula": 'P% = P / 100. Percentage of value X = (P / 100) * X.',
        "example": 'Convert 3/8 to a percentage: 3 / 8 = 0.375. 0.375 * 100% = 37.5%.',
        "common_pitfall": 'Failing to shift the decimal point two places when multiplying (e.g., treating 6% as 0.6 instead of 0.06).',
    },
    "C10": {
        "concept_id": "C10",
        "title": 'Proportion Word Problems, Real-World Modeling & Scaling',
        "summary": 'Translates multi-sentence verbal descriptions into mathematical proportional equations, maintaining consistent unit orientation throughout.',
        "core_principles": [
            'Unit Alignment: Ensure the same physical units occupy corresponding positions on both sides of the equals sign.',
            'Rate-Time-Distance Modeling: Distance = Rate * Time; scaling recipes and currency conversions follow identical linear structures.',
            'Reasonableness Check: Verify that the computed answer aligns with intuitive physical expectations.',
        ],
        "key_formula": 'Unit_A1 / Unit_B1 = Unit_A2 / Unit_B2  =>  Cross-multiply and isolate unknown.',
        "example": 'A recipe for 4 people requires 6 cups of flour. For 10 people: 4 / 6 = 10 / x => 4x = 60 => x = 15 cups.',
        "common_pitfall": 'Flipping the unit positions across the equals sign (e.g. people/flour = flour/people).',
    },
    "CN1": {
        "concept_id": "CN1",
        "title": 'OSI & TCP/IP Reference Models Architecture Explained',
        "summary": 'Layered protocol stacks that standardize communication between heterogeneous computing systems across physical media to application software.',
        "core_principles": [
            'OSI 7 Layers: Physical -> Data Link -> Network -> Transport -> Session -> Presentation -> Application.',
            'TCP/IP 4 Layers: Network Access (Link) -> Internet -> Transport -> Application.',
            'Encapsulation & PDU: Bits (L1) -> Frames (L2) -> Packets (L3) -> Segments (L4) -> Data (L5-7).',
        ],
        "key_formula": 'Encapsulated Frame = L2 Header + L3 IP Header + L4 TCP/UDP Header + Payload + L2 CRC Trailer.',
        "example": 'A web browser request generates HTTP payload, wrapped in TCP header with port 443, wrapped in IP packet with target IP, wrapped in Ethernet frame with MAC address.',
        "common_pitfall": 'Confusing Layer 2 MAC addresses (local physical hop) with Layer 3 IP addresses (global logical routing).',
    },
    "CN2": {
        "concept_id": "CN2",
        "title": 'Data Link Layer, Framing & Error Detection (CRC)',
        "summary": 'Transforms raw bitstreams into discrete logical frames, manages local MAC physical addressing, and detects bit errors via polynomial division.',
        "core_principles": [
            'Framing & Delimiters: Bit-stuffing and byte-stuffing prevent payload data from mimicking frame boundary flags.',
            'Hardware Addressing: 48-bit MAC addresses uniquely identify Network Interface Cards (NICs) within a broadcast domain.',
            'Cyclic Redundancy Check (CRC): Modulo-2 polynomial division detects burst transmission errors with high mathematical certainty.',
        ],
        "key_formula": 'Transmitted Frame T(x) = D(x)*2^r + R(x), where R(x) = [D(x)*2^r] mod G(x) using XOR polynomial division.',
        "example": 'If the receiver computes [Received Frame] mod G(x) and obtains a non-zero remainder, a bit error occurred and the frame is discarded.',
        "common_pitfall": 'Believing standard CRC corrects errors; CRC is strictly an error-detection code, not forward error correction (FEC).',
    },
    "CN3": {
        "concept_id": "CN3",
        "title": 'IP Addressing, Subnetting & CIDR Calculations',
        "summary": 'Hierarchical 32-bit IPv4 logical addressing with Classless Inter-Domain Routing (CIDR) to segment networks and conserve address spaces.',
        "core_principles": [
            'IP Structure: 32 bits divided into 4 octets. Subnet mask delineates network bits vs host bits.',
            'CIDR Notation: /N specifies that the first N bits are reserved for network identification.',
            'Reserved Addresses: The all-zeros host address is the Network ID; the all-ones host address is the Directed Broadcast address.',
        ],
        "key_formula": 'Total Addresses = 2^(32 - N); Usable Host Addresses = 2^(32 - N) - 2.',
        "example": 'A /27 subnet mask has 32 - 27 = 5 host bits. Total addresses = 2^5 = 32. Usable hosts = 32 - 2 = 30.',
        "common_pitfall": 'Forgetting to subtract 2 for the network ID and broadcast address when sizing host capacities.',
    },
    "CN4": {
        "concept_id": "CN4",
        "title": 'Routing Protocols: Link-State (OSPF) vs Path-Vector (BGP)',
        "summary": 'Mechanisms routers use to dynamically discover topologies and determine optimal packet forwarding paths across interior networks and global internet backbones.',
        "core_principles": [
            "Link-State (OSPF): Routers flood Link-State Advertisements (LSAs) so every node maintains an identical map, executing Dijkstra's algorithm.",
            'Path-Vector (BGP): Coordinates routing policies between autonomous systems (AS), preventing loops by inspecting the AS-Path attribute list.',
            'Convergence: Fast dynamic reaction to physical link failures without forwarding loops.',
        ],
        "key_formula": 'OSPF Cost = Reference Bandwidth (100 Mbps) / Interface Bandwidth. BGP evaluates: Weight -> Local-Pref -> AS-Path -> Multi-Exit Discriminator.',
        "example": 'In OSPF, a 1 Gbps fiber link has a lower metric than a 100 Mbps link, prompting Dijkstra to route traffic across the fiber.',
        "common_pitfall": 'Assuming BGP always selects the route with the fewest hops or highest bandwidth; BGP routes are determined by business peering policies.',
    },
    "CN5": {
        "concept_id": "CN5",
        "title": 'Transport Layer: TCP vs UDP & The 3-Way Handshake',
        "summary": 'End-to-end transport communication. TCP provides reliable, ordered byte-streams; UDP offers lightweight, zero-overhead connectionless datagrams.',
        "core_principles": [
            'TCP 3-Way Handshake: SYN -> SYN-ACK -> ACK establishes sequence numbers and socket state before data transfer.',
            'Reliability Mechanisms: Sequence numbers, cumulative ACKs, checksums, and timeout retransmissions.',
            'UDP Use-Case: Unconnected best-effort delivery ideal for real-time low-latency voice, gaming, and DNS.',
        ],
        "key_formula": 'Handshake: Client sends SYN(Seq=x) -> Server replies SYN-ACK(Seq=y, Ack=x+1) -> Client sends ACK(Seq=x+1, Ack=y+1).',
        "example": "Web browsers use TCP port 443 for web pages so no text is lost; Discord voice and Zoom use UDP so dropped audio packets don't cause lag.",
        "common_pitfall": 'Believing UDP guarantees in-order arrival; UDP packets can arrive out of order, duplicated, or dropped.',
    },
    "CN6": {
        "concept_id": "CN6",
        "title": 'TCP Flow & Congestion Control (Sliding Window & AIMD)',
        "summary": 'Feedback loops that prevent fast senders from overflowing slow receivers (flow control) or congesting shared network routers (congestion control).',
        "core_principles": [
            'Flow Control: Receiver advertises available buffer space via the Receive Window (rwnd) in every TCP header.',
            'Congestion Control: Sender maintains a dynamic Congestion Window (cwnd) based on estimated network capacity.',
            'AIMD Algorithm: Additive Increase on successful RTT (+1 MSS), Multiplicative Decrease on packet loss (halve cwnd).',
        ],
        "key_formula": 'Effective Transmission Window W = min(cwnd, rwnd). In AIMD: cwnd_new = cwnd + 1 (no loss), cwnd_new = cwnd / 2 (on drop).',
        "example": 'During Slow Start, cwnd starts at 1-10 MSS and doubles every RTT until ssthresh, transitioning to linear AIMD growth.',
        "common_pitfall": 'Confusing flow control (protecting the endpoint receiver) with congestion control (protecting intermediate network links).',
    },
    "CN7": {
        "concept_id": "CN7",
        "title": 'Application Layer Protocols: DNS & HTTP/HTTPS',
        "summary": 'Core internet application services. DNS translates human domain names into IP addresses; HTTP/HTTPS delivers encrypted hypermedia web traffic.',
        "core_principles": [
            "Hierarchical DNS: Resolves queries through Recursive Resolver -> Root Server ('.') -> TLD Server ('.com') -> Authoritative Server.",
            'HTTP Evolution: HTTP/1.1 (persistent TCP), HTTP/2 (multiplexed streams over single connection), HTTP/3 (QUIC/UDP transport).',
            'HTTPS & TLS: Asymmetric key exchange authenticates server certificate, establishing ephemeral symmetric session keys.',
        ],
        "key_formula": 'HTTPS = HTTP + TLS (Transport Layer Security over TCP port 443).',
        "example": "Typing 'wikipedia.org' triggers a recursive DNS query returning an IP address, followed by a TLS handshake and encrypted HTTP GET request.",
        "common_pitfall": 'Assuming DNS always uses TCP; standard DNS lookups use UDP port 53 for speed, falling back to TCP only for payloads > 512 bytes.',
    },
    "CN8": {
        "concept_id": "CN8",
        "title": 'Network Security & Cryptography (Encryption, Firewalls & NAT)',
        "summary": 'Defending network availability, data confidentiality, and integrity through cryptographic ciphers, digital signatures, and stateful packet filtering.',
        "core_principles": [
            'Symmetric vs Asymmetric: Symmetric (AES) is fast and shares one secret key; Asymmetric (RSA/ECC) uses public/private key pairs.',
            'Hashing & Integrity: Cryptographic hashes (SHA-256) generate irreversible fingerprints; digital signatures verify origin authentication.',
            'Firewalls & NAT: Stateful inspection monitors connection state; Network Address Translation maps multiple private IPs to one public IP.',
        ],
        "key_formula": 'Digital Signature = Encrypt_PrivateKey(Hash(Message)). Verified by Decrypt_PublicKey(Signature) == Hash(Message).',
        "example": "During TLS session setup, the server sends its certificate signed by a CA. The browser verifies the signature using the CA's built-in public key.",
        "common_pitfall": 'Reusing an initialization vector (IV) or nonce with stream ciphers like AES-GCM, which fatally compromises confidentiality.',
    },
    "AI1": {
        "concept_id": "AI1",
        "title": 'State-Space Search & Graph Traversal (BFS, DFS & A*)',
        "summary": 'Systematic exploration of problem configurations from an initial state to a goal state using uninformed search or informed heuristic guidance.',
        "core_principles": [
            'Uninformed Search: BFS uses a FIFO queue to guarantee shortest path on unweighted graphs; DFS uses a LIFO stack.',
            'A* Search: Evaluates nodes using f(n) = g(n) + h(n), where g(n) is actual cost from start and h(n) is heuristic estimate to goal.',
            'Admissibility & Consistency: An admissible heuristic never overestimates true remaining cost, guaranteeing optimal paths.',
        ],
        "key_formula": 'f(n) = g(n) + h(n), where h(n) <= h*(n) (Admissibility condition).',
        "example": 'In GPS route planning, straight-line Euclidean distance h(n) to the destination is an admissible heuristic that guides A* directly toward the goal.',
        "common_pitfall": 'Using an inadmissible heuristic (overestimating true remaining distance), which causes A* to lose its mathematical guarantee of optimality.',
    },
    "AI2": {
        "concept_id": "AI2",
        "title": 'Adversarial Search & Game Trees (Minimax & Alpha-Beta)',
        "summary": 'Optimal decision-making algorithms for two-player, zero-sum, perfect-information competitive games (such as Chess and Tic-Tac-Toe).',
        "core_principles": [
            "Minimax Rule: Maximizing player selects moves maximizing their utility; minimizing opponent chooses moves minimizing Max's utility.",
            'Game Tree Recursion: Terminal states return payoff utilities; values propagate upward through alternate max and min plies.',
            'Alpha-Beta Pruning: Prunes branches that cannot influence the final decision whenever beta <= alpha, reducing branching factor from b to sqrt(b).',
        ],
        "key_formula": 'Alpha = max guaranteed for Max; Beta = min guaranteed for Min. Prune branch if beta <= alpha.',
        "example": 'If Min already has an option evaluating to 2 (beta=2), and another branch for Max already guarantees at least 4 (alpha=4), the remaining branch is pruned.',
        "common_pitfall": 'Believing Alpha-Beta pruning changes the chosen move; it returns the exact same move as full Minimax while expanding far fewer nodes.',
    },
    "AI3": {
        "concept_id": "AI3",
        "title": 'Supervised Learning: Linear/Logistic Regression & Gradients',
        "summary": 'Parameter estimation algorithms that learn mappings from feature inputs to target labels by iteratively minimizing a mathematical loss function.',
        "core_principles": [
            'Model Classes: Linear regression predicts continuous real values; logistic regression outputs probabilities via the Sigmoid function.',
            'Loss Functions: Mean Squared Error (MSE) for regression; Binary Cross-Entropy (Log-Loss) for classification.',
            'Gradient Descent: Updates model parameters in the direction of steepest loss descent opposite to the gradient vector.',
        ],
        "key_formula": 'Gradient Update: theta_{t+1} = theta_t - lr * grad_theta(Loss). Sigmoid: sigma(z) = 1 / (1 + e^-z).',
        "example": 'Predicting house prices: fitting weights w and bias b to minimize sum of squared prediction errors across training samples.',
        "common_pitfall": 'Setting the learning rate too high (causing divergence and oscillating loss) or too low (causing exceedingly slow convergence).',
    },
    "AI4": {
        "concept_id": "AI4",
        "title": 'Artificial Neurons & Non-Linear Activation Functions',
        "summary": 'The computational unit of deep learning: combines weighted inputs linearly and applies non-linear activation functions to approximate complex functions.',
        "core_principles": [
            'Perceptron Computation: Computes affine sum z = sum(w_i * x_i) + b, followed by non-linear activation a = sigma(z).',
            'Universal Approximation: Non-linear activations allow networks to learn non-linear decision boundaries and solve non-linearly separable problems like XOR.',
            'Common Activations: ReLU (max(0, z)), Leaky ReLU, Sigmoid (1/(1+e^-z)), GELU, and Softmax (multi-class probability distribution).',
        ],
        "key_formula": 'z = W^T * x + b; a = activation(z). Softmax: p_i = exp(z_i) / sum_j exp(z_j).',
        "example": 'A single linear neuron cannot solve the XOR problem; adding a hidden layer with ReLU activation solves XOR effortlessly.',
        "common_pitfall": 'Using Sigmoid or Tanh activations across deep networks, which saturates gradients near 0 and prevents early layers from learning.',
    },
    "AI5": {
        "concept_id": "AI5",
        "title": 'Deep Neural Networks & Backpropagation (Calculus Chain Rule)',
        "summary": 'Efficient algorithm to compute the exact gradient of the loss function with respect to every weight in a multi-layer network via the multivariable chain rule.',
        "core_principles": [
            'Forward Pass: Inputs propagate through layers to compute intermediate activations and final loss.',
            'Backward Pass: Error signals delta propagate backwards from output layer to input layer.',
            'Chain Rule Application: The partial derivative d(Loss)/dw equals the local activation times the incoming backpropagated error signal.',
        ],
        "key_formula": "d(Loss)/dw^(l) = delta^(l) * (a^(l-1))^T; delta^(l) = [(W^(l+1))^T * delta^(l+1)] (element-wise product) sigma'(z^(l)).",
        "example": 'Computing weight gradients across 100 layers takes O(N) operations with backpropagation instead of O(N^2) with numerical differentiation.',
        "common_pitfall": 'Initializing all weights to identical constants (e.g. zeros), which causes hidden neurons to compute identical gradients and fail to specialize.',
    },
    "AI6": {
        "concept_id": "AI6",
        "title": 'Convolutional Neural Networks (CNNs): Kernels & Pooling',
        "summary": 'Specialized neural network architectures for grid-structured spatial data (images, audio) utilizing weight sharing and translational invariance.',
        "core_principles": [
            'Convolution Operation: Slides small parameterized weight matrices (kernels/filters) across inputs to compute feature activation maps.',
            'Hierarchical Representation: Early layers detect edges and textures; deeper layers compose complex semantic object shapes.',
            'Pooling & Subsampling: Max-pooling reduces spatial dimensions, controls overfitting, and grants translation invariance.',
        ],
        "key_formula": 'Output Dimension O = floor((W - K + 2P) / S) + 1, where W=input size, K=kernel size, P=padding, S=stride.',
        "example": 'A 3x3 Sobel kernel detects sharp vertical brightness transitions (edges) regardless of where the edge appears in the image.',
        "common_pitfall": 'Connecting raw high-resolution image pixels directly into fully-connected dense layers, creating millions of parameters that overfit.',
    },
    "AI7": {
        "concept_id": "AI7",
        "title": 'Transformers & Self-Attention Mechanisms (Q, K, V Vectors)',
        "summary": 'Sequence modeling architecture that eliminates recurrence in favor of parallelized multi-head self-attention, dynamically weighting relationships between all token pairs.',
        "core_principles": [
            'Query, Key, Value Projections: Every token embedding is projected into Query (Q), Key (K), and Value (V) vector representations.',
            'Scaled Dot-Product Attention: Computes attention weights by taking the dot product of Q and K, scaled by sqrt(d_k) and normalized via Softmax.',
            'Multi-Head Parallelism: Multiple attention heads capture diverse semantic, syntactic, and relational context simultaneously.',
        ],
        "key_formula": 'Attention(Q, K, V) = Softmax((Q * K^T) / sqrt(d_k)) * V.',
        "example": "In the sentence 'The animal didn't cross the street because it was too tired', self-attention assigns high weight between 'it' and 'animal'.",
        "common_pitfall": 'Omitting positional encodings; since self-attention is permutation-invariant, positional embeddings must be added to preserve token order.',
    },
    "AI8": {
        "concept_id": "AI8",
        "title": 'Reinforcement Learning & Bellman Optimality Equation',
        "summary": 'Goal-oriented framework where an autonomous agent learns optimal behaviors through environmental trial-and-error interactions to maximize cumulative discounted rewards.',
        "core_principles": [
            "Markov Decision Process (MDP): Defined by states S, actions A, transition probabilities P(s'|s,a), rewards R(s,a), and discount factor gamma.",
            'Bellman Optimality: Decomposes optimal state-action value Q*(s, a) into immediate reward plus discounted maximum expected future reward.',
            'Exploration vs Exploitation: Balancing discovering new potential strategies (epsilon-random exploration) with exploiting known high-reward actions.',
        ],
        "key_formula": "Bellman Optimality: Q*(s, a) = R(s, a) + gamma * max_{a'} Q*(s', a'). Q-learning update: Q(s,a) <- Q(s,a) + alpha*[r + gamma*max_a' Q(s',a') - Q(s,a)].",
        "example": 'A grid-world agent receives +10 for reaching the goal and -1 for every step; a discount factor gamma=0.95 motivates finding the shortest route.',
        "common_pitfall": 'Using pure greedy exploitation (epsilon=0), which causes the agent to get stuck in local sub-optimal policies without discovering the global optimum.',
    },
    "FLA1": {
        "concept_id": "FLA1",
        "title": 'Alphabets, Languages & Regular Expressions',
        "summary": 'The mathematical foundation of theoretical computer science: formal definitions of symbols, alphabets, finite strings, and regular language operators.',
        "core_principles": [
            'Alphabet (Sigma): A finite, non-empty set of symbols. Strings are finite sequences of symbols from Sigma; epsilon is the empty string.',
            'Language (L): Any subset of Sigma* (the set of all finite strings over Sigma including epsilon).',
            'Regular Operations: Union (L1 U L2), Concatenation (L1 L2), and Kleene Star Closure (L* = union of all powers L^i for i >= 0).',
        ],
        "key_formula": 'Sigma* = {epsilon} U Sigma U Sigma^2 U Sigma^3 ...; Regular Expression generates the class of Regular Languages.',
        "example": "Over Sigma = {0, 1}, regex (0|1)* 00 represents the regular language of all binary strings that terminate with suffix '00'.",
        "common_pitfall": 'Conflating the empty string epsilon (a valid string of length 0) with the empty language emptyset (a set containing zero strings).',
    },
    "FLA2": {
        "concept_id": "FLA2",
        "title": 'Deterministic Finite Automata (DFA) State Diagrams',
        "summary": 'A 5-tuple abstract machine with strictly finite internal memory that deterministically accepts or rejects input strings.',
        "core_principles": [
            'Formal 5-Tuple: (Q, Sigma, delta, q0, F) where Q=states, Sigma=alphabet, delta=transition function, q0=initial state, F=accept states.',
            'Deterministic Transition: delta: Q x Sigma -> Q requires exactly one unique outbound transition from every state for each alphabet symbol.',
            'Language Acceptance: A string w is accepted if the unique state path traversed from q0 terminates in an accept state f in F.',
        ],
        "key_formula": 'delta: Q x Sigma -> Q. Extended transition: delta_hat(q, wa) = delta(delta_hat(q, w), a). Accept if delta_hat(q0, w) in F.',
        "example": "An automaton with 2 states (q_even, q_odd) where each '1' toggles state recognizes binary strings with an even number of 1s (F = {q_even}).",
        "common_pitfall": 'Leaving undefined transitions in a DFA; every state must have an explicit transition for every symbol in Sigma.',
    },
    "FLA3": {
        "concept_id": "FLA3",
        "title": 'Nondeterministic Automata (NFA) & Subset Construction',
        "summary": 'Automata permitting zero, one, or multiple transitions per symbol and spontaneous epsilon-moves, equivalent in expressive power to DFAs.',
        "core_principles": [
            'Non-Determinism: The transition function delta: Q x (Sigma U {epsilon}) -> 2^Q maps to a set of possible next states.',
            'Epsilon Transitions: Transitions between states without consuming any input symbol.',
            'Rabin-Scott Subset Construction: Proves NFAs and DFAs are computationally equivalent; an n-state NFA can be converted into a DFA with <= 2^n states.',
        ],
        "key_formula": 'Q_DFA = 2^(Q_NFA). For DFA state S subseteq Q_NFA: delta_DFA(S, a) = epsilon_closure( union_{q in S} delta_NFA(q, a) ).',
        "example": "An NFA guessing if a string ends with '01' needs only 3 states, whereas powerset construction converts it into an equivalent deterministic DFA.",
        "common_pitfall": 'Assuming NFAs can recognize languages that DFAs cannot; both recognize the exact same class of Regular Languages.',
    },
    "FLA4": {
        "concept_id": "FLA4",
        "title": 'Pumping Lemma for Regular Languages: Proofs & Contradictions',
        "summary": 'A fundamental property of all regular languages, used as a proof by contradiction to prove that a given language is NOT regular.',
        "core_principles": [
            'Pigeonhole Principle Basis: Any DFA with p states processing a string of length >= p must repeat a state, creating a loop.',
            'Partitioning Conditions: String s = xyz with |y| > 0, |xy| <= p, and xy^i z in L for all integers i >= 0.',
            'Adversarial Contradiction: Choose a string s in L of length >= p and show that pumping y outside (i=0 or i=2) yields a string not in L.',
        ],
        "key_formula": 's = xyz with |y| >= 1 and |xy| <= p => For all i >= 0, xy^i z must belong to L.',
        "example": 'Proving L = {0^n 1^n | n >= 0} is non-regular: Choose s = 0^p 1^p. Since |xy| <= p, y consists entirely of 0s. Pumping i=2 yields 0^(p+|y|) 1^p not in L.',
        "common_pitfall": 'Attempting to use the Pumping Lemma to prove a language IS regular; the lemma is a necessary condition, not a sufficient test.',
    },
    "FLA5": {
        "concept_id": "FLA5",
        "title": 'Context-Free Grammars (CFG) & Derivations',
        "summary": 'A 4-tuple generative syntactic system (V, Sigma, R, S) capable of expressing recursive hierarchical nesting (such as programming language syntax).',
        "core_principles": [
            'Components: Variables (V), Terminals (Sigma), Production Rules (R: A -> alpha where A in V), and Start Symbol (S in V).',
            'Derivations & Parse Trees: Leftmost and rightmost derivations systematically replace non-terminals, yielding hierarchical parse trees.',
            'Chomsky Hierarchy: Context-Free Languages strictly encompass Regular Languages and are recognized by Pushdown Automata.',
        ],
        "key_formula": 'Production Rule format: A -> alpha, where A in V and alpha in (V U Sigma)*.',
        "example": 'The grammar S -> 0S1 | epsilon generates the non-regular context-free language {0^n 1^n | n >= 0}.',
        "common_pitfall": 'Grammar ambiguity: a CFG is ambiguous if a string admits two distinct leftmost derivation parse trees (e.g. arithmetic order of operations).',
    },
    "FLA6": {
        "concept_id": "FLA6",
        "title": 'Pushdown Automata (PDA) & Stack Memory',
        "summary": 'Finite state automata augmented with an unbounded Last-In-First-Out (LIFO) stack memory, recognizing the full class of Context-Free Languages.',
        "core_principles": [
            'Stack Operations: Transitions read an input symbol, pop the top stack symbol, and push a replacement stack symbol (a, b -> c).',
            'Acceptance Modes: Acceptance by entering a final state (F) or acceptance by emptying the stack (Null Stack).',
            'Determinism Difference: Deterministic PDAs (DPDAs) are strictly less powerful than Non-deterministic PDAs (NPDAs).',
        ],
        "key_formula": 'delta: Q x (Sigma U {epsilon}) x (Gamma U {epsilon}) -> 2^(Q x (Gamma U {epsilon})), where Gamma is the stack alphabet.',
        "example": "To recognize {0^n 1^n}: Push 'X' for each '0' read; pop 'X' for each '1' read. Accept if stack is empty when input finishes.",
        "common_pitfall": 'Assuming DPDAs can recognize all CFLs; languages like even-length palindromes {w w^R} require non-deterministic branching (NPDAs).',
    },
    "FLA7": {
        "concept_id": "FLA7",
        "title": 'Turing Machines: Infinite Tape & Computability',
        "summary": 'The foundational mathematical model of general-purpose computation: a finite state controller manipulating symbols on an infinite two-way tape.',
        "core_principles": [
            'Formal Definition: (Q, Sigma, Gamma, delta, q0, q_accept, q_reject) where Gamma is tape alphabet (Sigma subset Gamma, blank in Gamma).',
            'Tape Head Action: delta: Q x Gamma -> Q x Gamma x {L, R} reads a cell, overwrites a symbol, and moves head Left or Right.',
            'Church-Turing Thesis: Any algorithmic process physically computable in our universe can be simulated by a Turing Machine.',
        ],
        "key_formula": "delta(q, a) = (q', b, D), where q'=next state, b=symbol written, D in {L, R}.",
        "example": 'A Turing Machine recognizes non-context-free language {a^n b^n c^n} by zig-zagging across the tape, marking off matching triples.',
        "common_pitfall": "Confusing Turing-Recognizable (TM halts on 'yes' but may loop forever on 'no') with Turing-Decidable (TM halts on all inputs with yes or no).",
    },
    "FLA8": {
        "concept_id": "FLA8",
        "title": 'Decidability, Halting Problem & P vs NP',
        "summary": 'The absolute theoretical boundaries of computation: undecidability of the Halting Problem and computational complexity class classifications.',
        "core_principles": [
            'Halting Problem (H): Proves that no general algorithm can determine whether an arbitrary program will finish running or loop forever.',
            'Diagonalization Proof: Alan Turing constructed a paradox machine D that runs program M on its own source code and halts iff M loops.',
            'Complexity Classes: P contains problems solvable in polynomial time O(n^k); NP contains problems verifiable in polynomial time.',
        ],
        "key_formula": 'A_TM = { <M, w> | M is a TM that accepts string w } is undecidable. P subseteq NP.',
        "example": "If a universal halting decider H existed, constructing D(<D>) would invert H's prediction, causing a mathematical contradiction: D halts iff D loops.",
        "common_pitfall": "Assuming undecidable means 'we haven't figured out the algorithm yet'; Turing proved mathematically that no such algorithm can ever exist.",
    },
    "BIO1": {
        "concept_id": "BIO1",
        "title": 'Water, Hydrogen Bonds & pH Buffers (Henderson-Hasselbalch)',
        "summary": "Water's dipolar geometry and hydrogen bonding drive macromolecular folding, while physiological buffer systems maintain strict pH homeostasis.",
        "core_principles": [
            "Dipole Nature: Oxygen's high electronegativity creates a permanent dipole in H2O, enabling up to 4 hydrogen bonds per molecule.",
            'Hydrophobic Effect: Water molecules exclude non-polar molecules, increasing solvent entropy and driving protein/lipid self-assembly.',
            'Buffering Action: Weak acid/conjugate base pairs resist pH changes near their pKa.',
        ],
        "key_formula": 'Henderson-Hasselbalch: pH = pKa + log([A-] / [HA]). Maximum buffering capacity occurs when pH = pKa.',
        "example": 'Blood plasma buffer: CO2 + H2O <=> H2CO3 <=> H+ + HCO3-. Bicarbonate maintains arterial blood pH at 7.40 +- 0.05.',
        "common_pitfall": 'Believing a buffer maintains a neutral pH of 7.0; buffers stabilize pH near their specific pKa value, which varies by acid.',
    },
    "BIO2": {
        "concept_id": "BIO2",
        "title": 'Amino Acids & Protein Hierarchies (Primary to Quaternary)',
        "summary": 'Proteins are polymers of 20 alpha-amino acids connected by peptide bonds, folding into 4 hierarchical structural tiers essential for biochemical activity.',
        "core_principles": [
            'Primary Structure: Linear covalent peptide sequence (N-terminus to C-terminus) formed by condensation reactions.',
            'Secondary Structure: Local regular geometries (alpha-helices and beta-sheets) stabilized exclusively by backbone hydrogen bonds.',
            'Tertiary & Quaternary: 3D folding driven by hydrophobic burial, salt bridges, hydrogen bonds, and covalent disulfide crosslinks.',
        ],
        "key_formula": 'Peptide bond formation: -COOH + H2N- -> -CO-NH- + H2O. Primary -> Secondary -> Tertiary -> Quaternary.',
        "example": 'Hemoglobin consists of a quaternary tetramer (two alpha and two beta globin subunits) with four oxygen-binding heme prosthetic groups.',
        "common_pitfall": 'Assuming secondary structures involve side-chain R-group bonds; secondary structures are formed solely by backbone amide-carbonyl hydrogen bonds.',
    },
    "BIO3": {
        "concept_id": "BIO3",
        "title": 'Enzyme Kinetics & Catalysis (Michaelis-Menten: Km & Vmax)',
        "summary": 'Enzymes act as biological catalysts, accelerating reaction rates by stabilizing transition states and lowering activation energy without altering delta G.',
        "core_principles": [
            'Catalytic Acceleration: Lowers activation energy (Delta G++) without altering initial or final Gibbs free energy equilibria (Delta G).',
            'Michaelis Constant (Km): Substrate concentration at which reaction velocity v0 is exactly half of Vmax; inversely related to substrate affinity.',
            'Inhibition Mechanisms: Competitive inhibitors increase apparent Km with no effect on Vmax; non-competitive inhibitors decrease Vmax.',
        ],
        "key_formula": 'Michaelis-Menten: v0 = (Vmax * [S]) / (Km + [S]). Lineweaver-Burk: 1/v0 = (Km / Vmax) * (1/[S]) + (1/Vmax).',
        "example": 'A competitive inhibitor competes with substrate for the active site; adding excess substrate outcompetes the inhibitor, achieving normal Vmax.',
        "common_pitfall": 'Interpreting a high Km as high enzyme affinity; a higher Km means more substrate is required, indicating lower binding affinity.',
    },
    "BIO4": {
        "concept_id": "BIO4",
        "title": 'Carbohydrate Metabolism & Glycolysis (10 Enzymatic Steps)',
        "summary": 'The universal 10-step anaerobic cytosolic pathway that breaks down one 6-carbon glucose into two 3-carbon pyruvates, netting 2 ATP and 2 NADH.',
        "core_principles": [
            'Energy Investment Phase: Steps 1-3 consume 2 ATP (Hexokinase and Phosphofructokinase-1) to phosphorylate hexose intermediates.',
            'Cleavage Phase: Fructose-1,6-bisphosphate is cleaved by Aldolase into DHAP and G3P.',
            'Payoff Phase: Steps 6-10 produce 4 ATP via substrate-level phosphorylation and 2 NADH, netting +2 ATP and +2 NADH.',
        ],
        "key_formula": 'Net Reaction: Glucose + 2 NAD+ + 2 ADP + 2 Pi -> 2 Pyruvate + 2 NADH + 2 H+ + 2 ATP + 2 H2O.',
        "example": 'PFK-1 is the committed rate-limiting checkpoint; high ATP allosterically inhibits PFK-1, slowing glycolysis when cellular energy is abundant.',
        "common_pitfall": 'Forgetting that 2 ATP molecules are invested up front, mistakenly believing glycolysis produces a gross of only 2 ATP.',
    },
    "BIO5": {
        "concept_id": "BIO5",
        "title": 'Citric Acid Cycle (Krebs Cycle): 8 Steps & Electron Carriers',
        "summary": 'Mitochondrial matrix metabolic engine that oxidizes acetyl-CoA into CO2, transferring high-energy electrons to reduce NAD+ and FAD cofactors.',
        "core_principles": [
            'Entry Condensation: 2-carbon Acetyl-CoA combines with 4-carbon Oxaloacetate to form 6-carbon Citrate.',
            'Decarboxylations: Two oxidative decarboxylation steps release 2 molecules of CO2 and generate 2 NADH.',
            'Yield per Turn: Each turn produces 3 NADH, 1 FADH2, 1 GTP (ATP), and regenerates Oxaloacetate.',
        ],
        "key_formula": 'Per Acetyl-CoA: Acetyl-CoA + 3 NAD+ + FAD + GDP + Pi + 2 H2O -> 2 CO2 + 3 NADH + FADH2 + GTP + CoA-SH.',
        "example": 'Because 1 glucose yields 2 pyruvates, 1 glucose drives two full turns of the Krebs cycle, yielding 6 NADH, 2 FADH2, 2 GTP, and 4 CO2.',
        "common_pitfall": 'Thinking oxygen is directly consumed in the Krebs cycle; while oxygen is not a direct reactant, the cycle halts anaerobically due to lack of NAD+ regeneration.',
    },
    "BIO6": {
        "concept_id": "BIO6",
        "title": 'Oxidative Phosphorylation & ATP Synthase Chemiosmosis',
        "summary": 'Inner mitochondrial membrane complexes transfer electrons from NADH/FADH2 to oxygen, establishing a proton gradient that drives rotary ATP synthesis.',
        "core_principles": [
            'Electron Transport Chain: Complexes I, III, and IV pump protons into the intermembrane space as electrons flow toward terminal acceptor O2.',
            'Proton-Motive Force: Combined electrical potential Delta-psi and chemical pH gradient Delta-pH across the inner membrane.',
            'Chemiosmosis & F0-F1 ATP Synthase: Proton flux through the F0 rotor drives mechanical rotation of F1 subunits, phosphorylating ADP + Pi -> ATP.',
        ],
        "key_formula": 'Proton-Motive Force Delta-p = Delta-psi - (2.3 * R * T / F) * Delta-pH. ~4 protons generate 1 ATP.',
        "example": 'Cyanide binds tightly to Cytochrome c Oxidase (Complex IV), blocking electron transfer to O2, collapsing the proton gradient, and causing rapid cellular arrest.',
        "common_pitfall": 'Thinking protons are pumped into the mitochondrial matrix; protons are pumped outward from the matrix into the intermembrane space.',
    },
    "BIO7": {
        "concept_id": "BIO7",
        "title": 'Lipid Metabolism & Fluid Mosaic Membranes Architecture',
        "summary": 'Amphipathic phospholipid bilayers regulating cellular boundaries and mitochondrial beta-oxidation breaking fatty acids into 2-carbon Acetyl-CoA units.',
        "core_principles": [
            'Fluid Mosaic Model: Phospholipid bilayer with integral proteins and cholesterol that buffer membrane fluidity against temperature extremes.',
            'Fatty Acid Degradation (Beta-Oxidation): Cyclic 4-step mitochondrial pathway cleaving 2-carbon Acetyl-CoA fragments from acyl chains.',
            'Energy Yield: Each round of beta-oxidation yields 1 FADH2, 1 NADH, and 1 Acetyl-CoA, yielding significantly higher ATP per gram than carbohydrates.',
        ],
        "key_formula": 'Rounds of Beta-Oxidation = (n / 2) - 1 for an n-carbon saturated fatty acid; yields (n / 2) Acetyl-CoA.',
        "example": 'Palmitic acid (16 carbons) undergoes 7 rounds of beta-oxidation, yielding 8 Acetyl-CoA, 7 FADH2, and 7 NADH, netting ~106 ATP.',
        "common_pitfall": 'Assuming saturated fatty acids increase membrane fluidity; saturated tails pack tightly, reducing fluidity, while cis-unsaturated kinks increase fluidity.',
    },
    "BIO8": {
        "concept_id": "BIO8",
        "title": 'Nucleic Acids, Replication & Central Dogma (DNA to Protein)',
        "summary": 'The molecular flow of genetic information: semi-conservative DNA replication, mRNA transcription, and ribosomal triplet translation into proteins.',
        "core_principles": [
            "DNA Double Helix: Antiparallel 5'->3' strands held by Watson-Crick base pairing: A=T (2 H-bonds) and G=C (3 H-bonds).",
            "Replication Fidelity: DNA Polymerase synthesizes 5'->3' with proofreading exonuclease activity on leading and lagging (Okazaki) strands.",
            'Central Dogma: DNA is transcribed into mRNA by RNA Polymerase, which is decoded into polypeptides by tRNAs at ribosomal A, P, and E sites.',
        ],
        "key_formula": 'Central Dogma: DNA -> (Transcription via RNA Pol) -> mRNA -> (Translation via Ribosome) -> Polypeptide.',
        "example": 'Codon AUG codes for Methionine and establishes the reading frame; stop codons (UAA, UAG, UGA) trigger release factor binding.',
        "common_pitfall": 'Believing RNA Polymerase requires an existing primer like DNA Polymerase; RNA Polymerase can initiate synthesis de novo.',
    },
}

def get_topic_brief_explanation(concept_id: str) -> Optional[Dict[str, Any]]:
    """Fetches the structured brief pedagogical explanation for a concept ID."""
    return TOPIC_BRIEF_EXPLANATIONS.get(concept_id)

