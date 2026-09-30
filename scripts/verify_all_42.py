import json
import urllib.request

# Base curated videos that already passed oEmbed
BASE_PASSED = {
    "C1": {
        "video_id": "CA9XLJpQp3c",
        "title": "Math Antics - Fractions Are Parts",
        "channel": "Math Antics",
        "duration": "11:42",
        "description": "Baseline foundation: visual unit fractions and fractional values on a 0-to-1 number line.",
        "takeaways": [
            "Denominator = total number of equal parts partitioned.",
            "Numerator = count of parts selected or accumulated.",
            "On a number line, unit fractions divide the interval between 0 and 1."
        ]
    },
    "C2": {
        "video_id": "qcHHhd6HizI",
        "title": "Equivalent Fractions - What Are They and How to Find Them",
        "channel": "Let's Do Math",
        "duration": "5:45",
        "description": "Equivalence property via common divisors; reducing fractions to lowest terms.",
        "takeaways": [
            "Multiplying by n/n is mathematically equivalent to multiplying by 1.",
            "Simplifying requires dividing by the Greatest Common Divisor (GCD).",
            "A fraction is in lowest terms when numerator and denominator are coprime."
        ]
    },
    "C3": {
        "video_id": "KNdUJQ_qd4U",
        "title": "Math Antics - Comparing Fractions",
        "channel": "Math Antics",
        "duration": "10:28",
        "description": "Cross-multiplication and least common denominator comparisons.",
        "takeaways": [
            "Convert to a common denominator to compare numerators directly.",
            "Cross-multiplication shortcut: compare a*d with b*c.",
            "Benchmark testing against 1/2 resolves quick comparisons."
        ]
    },
    "C4": {
        "video_id": "52ZlXsFJULI",
        "title": "Adding and Subtracting Fractions with Like & Unlike Denominators",
        "channel": "Khan Academy",
        "duration": "10:20",
        "description": "Addition and subtraction with like and unlike denominators using LCD.",
        "takeaways": [
            "Never add denominators together!",
            "Find the Least Common Multiple (LCM) of denominators.",
            "Scale numerators accordingly before adding or subtracting."
        ]
    },
    "C5": {
        "video_id": "qmfXyR7Z6Lk",
        "title": "Math Antics - Multiplying Fractions",
        "channel": "Math Antics",
        "duration": "11:34",
        "description": "Area model multiplication and reciprocal division algorithms.",
        "takeaways": [
            "Multiply straight across: (a/b) * (c/d) = (a*c) / (b*d).",
            "Cross-cancel common factors early to simplify arithmetic.",
            "Division rule: Keep, Change, Flip (multiply by reciprocal)."
        ]
    },
    "C6": {
        "video_id": "RQ2nYUBVvqI",
        "title": "Math Antics - Ratios And Rates",
        "channel": "Math Antics",
        "duration": "10:49",
        "description": "Representing relational quantities as colon ratios and simplified fraction ratios.",
        "takeaways": [
            "A ratio compares quantities: 3 blue to 4 red is 3:4.",
            "Part-to-whole ratio compares a subset to the combined sum.",
            "Ratios can be simplified just like fractions."
        ]
    },
    "C7": {
        "video_id": "s0RBRkehzwo",
        "title": "Unit Rates, Ratios & Proportions - Word Problems",
        "channel": "The Organic Chemistry Tutor",
        "duration": "14:15",
        "description": "Scaling ratios up/down and computing per-unit benchmark rates.",
        "takeaways": [
            "A unit rate has a denominator equal to 1.",
            "Divide the numerator by the denominator to find the unit value.",
            "Scale unit rates by multiplication to solve any quantity."
        ]
    },
    "C8": {
        "video_id": "USmit5zUGas",
        "title": "Math Antics - Proportions",
        "channel": "Math Antics",
        "duration": "10:35",
        "description": "Algebraic cross-multiplication to solve missing variable proportions.",
        "takeaways": [
            "In proportion a/b = c/d, cross products a*d and b*c are identical.",
            "Isolate the unknown variable with basic division.",
            "Check work by verifying equal cross-product products."
        ]
    },
    "C9": {
        "video_id": "JeVSmq1Nrpw",
        "title": "Math Antics - What Are Percentages?",
        "channel": "Math Antics",
        "duration": "8:52",
        "description": "Relating parts per hundred to simplified fractions and decimal equivalents.",
        "takeaways": [
            "Percent means 'parts per 100': 45% = 45/100.",
            "Convert fraction to percentage: divide, then multiply by 100.",
            "Use benchmark percentages (10%, 25%, 50%) for fast mental checks."
        ]
    },
    "C10": {
        "video_id": "JOZSFwuyqok",
        "title": "Ratio and Proportion Word Problems - Math",
        "channel": "The Organic Chemistry Tutor",
        "duration": "12:40",
        "description": "Capstone multi-step real-world modeling: recipe scaling, map distances, and rate problems.",
        "takeaways": [
            "Assign consistent units to numerator and denominator.",
            "Write the ratio equation before plugging in variables.",
            "Check that answer makes practical physical sense."
        ]
    },
    "CN1": {
        "video_id": "vv4y_uOneC0",
        "title": "OSI Model Explained | OSI Animation | 7 Layers",
        "channel": "TechTerms",
        "duration": "14:23",
        "description": "7-layer OSI model vs 4-layer TCP/IP stack; data encapsulation, headers, and protocol data units (PDUs).",
        "takeaways": [
            "Physical -> Data Link -> Network -> Transport -> Session -> Presentation -> Application.",
            "Encapsulation appends headers at each descending layer.",
            "PDUs: Bits -> Frames -> Packets -> Segments -> Application Data."
        ]
    },
    "CN2": {
        "video_id": "NhpzBldHOYo",
        "title": "Data Link Layer Framing & Error Detection",
        "channel": "Neso Academy",
        "duration": "11:15",
        "description": "48-bit MAC addresses, frame delimiters, bit-stuffing, and Cyclic Redundancy Checks (CRC).",
        "takeaways": [
            "MAC addresses are 48-bit globally unique hardware identifiers.",
            "Bit stuffing prevents delimiter mimicry in payload data.",
            "CRC uses polynomial binary division to detect burst bit errors."
        ]
    },
    "CN3": {
        "video_id": "5WfiTHiU4x8",
        "title": "What is an IP Address? IP Addressing & Subnetting Explained",
        "channel": "NetworkChuck",
        "duration": "18:45",
        "description": "IPv4/IPv6 address hierarchies, subnet masks, CIDR prefix calculations (/24, /27), and network/broadcast IDs.",
        "takeaways": [
            "IP addresses consist of 32 bits divided into 4 octets.",
            "CIDR notation /24 reserves 24 bits for network and 8 bits for hosts.",
            "Usable hosts = 2^(host_bits) - 2 (subtracting network and broadcast IDs)."
        ]
    },
    "CN4": {
        "video_id": "kfvJ8QVJscc",
        "title": "OSPF Routing Protocol Explained Step by Step",
        "channel": "CertBros",
        "duration": "12:18",
        "description": "Intra-domain link-state routing (Dijkstra algorithm in OSPF) vs inter-domain path-vector routing (BGP).",
        "takeaways": [
            "Routers operate at OSI Layer 3 using IP forwarding tables.",
            "OSPF floods Link State Advertisements and computes shortest paths via Dijkstra.",
            "BGP coordinates routing policies between independent Autonomous Systems (AS)."
        ]
    },
    "CN5": {
        "video_id": "uwoD5YsGACg",
        "title": "TCP vs UDP Comparison & 3-Way Handshake",
        "channel": "PowerCert Animated Videos",
        "duration": "8:36",
        "description": "Connection-oriented reliable stream (TCP SYN-SYN/ACK-ACK) vs lightweight best-effort datagrams (UDP).",
        "takeaways": [
            "TCP provides ordered, reliable, acknowledged delivery of byte streams.",
            "UDP has lower latency with zero connection overhead (ideal for DNS, gaming).",
            "The 3-way handshake synchronizes sequence numbers before data transfer."
        ]
    },
    "CN6": {
        "video_id": "ReQiSK8W3Ag",
        "title": "TCP Flow Control & Sliding Window Protocol",
        "channel": "Neso Academy",
        "duration": "13:42",
        "description": "Sliding window flow control, slow start, congestion avoidance, additive increase multiplicative decrease (AIMD).",
        "takeaways": [
            "Flow control protects the receiver buffer; congestion control protects the transit network.",
            "Slow Start doubles cwnd every RTT until ssthresh is reached.",
            "AIMD provides distributed fairness and stability across shared bottlenecks."
        ]
    },
    "CN7": {
        "video_id": "mpQZVYPuDGU",
        "title": "How a DNS Server (Domain Name System) Works",
        "channel": "PowerCert Animated Videos",
        "duration": "10:11",
        "description": "Hierarchical DNS namespace resolution, HTTP/1.1 vs HTTP/2 multiplexing, and TLS session handshakes.",
        "takeaways": [
            "DNS translates human domain names into machine IP addresses via recursive resolution.",
            "Recursive queries traverse Root -> TLD -> Authoritative Nameservers.",
            "HTTP/2 and HTTP/3 introduce stream multiplexing over TCP/QUIC."
        ]
    },
    "CN8": {
        "video_id": "inWWhr5tnEA",
        "title": "What Is Cyber Security & Cryptography | How It Works",
        "channel": "Simplilearn",
        "duration": "23:15",
        "description": "Symmetric vs asymmetric public key cryptography, digital signatures, packet-filtering firewalls, and NAT.",
        "takeaways": [
            "Asymmetric crypto uses public key for encryption, private key for decryption.",
            "TLS handshake authenticates the server via Certificate Authorities (CAs).",
            "Bulk data transfer uses fast symmetric encryption (e.g. AES-GCM)."
        ]
    },
    "AI1": {
        "video_id": "ySN5Wnu88nE",
        "title": "A* (A Star) Search Algorithm - Computerphile",
        "channel": "Computerphile",
        "duration": "12:44",
        "description": "Uninformed search (BFS, DFS) and informed heuristic search (A*, Greedy Best-First, admissible heuristics).",
        "takeaways": [
            "g(n) is the exact cost from start to node n; h(n) is the estimated heuristic cost.",
            "f(n) = g(n) + h(n) guides the priority queue toward the optimal goal.",
            "An admissible heuristic never overestimates the true remaining cost."
        ]
    },
    "AI2": {
        "video_id": "l-hh51ncgDI",
        "title": "Algorithms Explained: Minimax and Alpha-Beta Pruning",
        "channel": "Sebastian Lague",
        "duration": "17:35",
        "description": "Minimax algorithm for two-player zero-sum games, evaluation functions, and Alpha-Beta branch pruning.",
        "takeaways": [
            "Maximizing player seeks highest score; Minimizing player seeks lowest score.",
            "Alpha is the best value Max can guarantee; Beta is best for Min.",
            "Branches where beta <= alpha can be safely pruned without loss of optimality."
        ]
    },
    "AI3": {
        "video_id": "sDv4f4s2SB8",
        "title": "Gradient Descent, Step-by-Step",
        "channel": "StatQuest with Josh Starmer",
        "duration": "8:30",
        "description": "Linear and logistic regression, Mean Squared Error (MSE), cost function surfaces, and gradient descent updates.",
        "takeaways": [
            "Logistic regression predicts probabilities between 0 and 1 via the Sigmoid curve.",
            "Cost function measures divergence between predicted values and ground truth.",
            "Gradient descent updates weights opposite to the gradient: w = w - lr * grad."
        ]
    },
    "AI4": {
        "video_id": "aircAruvnKk",
        "title": "But what is a neural network? | Deep learning chapter 1",
        "channel": "3Blue1Brown",
        "duration": "19:13",
        "description": "McCulloch-Pitts perceptron, linear separability, non-linear activations (ReLU, Sigmoid, GELU, Softmax).",
        "takeaways": [
            "A neuron computes an affine combination of inputs: z = sum(w_i * x_i) + b.",
            "Non-linear activations allow networks to learn non-linear decision boundaries.",
            "Softmax normalizes multi-class output vectors into valid probability distributions."
        ]
    },
    "AI5": {
        "video_id": "Ilg3gGewQ5U",
        "title": "Backpropagation, intuitively | Deep Learning Chapter 3",
        "channel": "3Blue1Brown",
        "duration": "13:53",
        "description": "Multi-layer perceptrons, computational graphs, matrix calculus chain rule, and backward gradient propagation.",
        "takeaways": [
            "Backprop computes partial derivatives of the cost with respect to every weight.",
            "The chain rule multiplies local derivatives across consecutive layers.",
            "Enables efficient end-to-end training of deep multi-layer architectures."
        ]
    },
    "AI6": {
        "video_id": "YRhxdVk_sIs",
        "title": "Convolutional Neural Networks (CNNs) Explained",
        "channel": "deeplizard",
        "duration": "21:38",
        "description": "Kernels/filters, 2D convolution operations, max-pooling, feature hierarchies, and translational invariance.",
        "takeaways": [
            "Convolutions slide small weight filters across input pixels to detect local patterns.",
            "Early layers detect edges/textures; deep layers compose semantic shapes.",
            "Pooling layers reduce spatial dimensionality and provide translation invariance."
        ]
    },
    "AI7": {
        "video_id": "zxQyTK8quyY",
        "title": "Transformer Neural Networks, ChatGPT's foundation, Clearly Explained!",
        "channel": "StatQuest with Josh Starmer",
        "duration": "15:52",
        "description": "Query-Key-Value scaled dot-product attention, multi-head attention, positional encodings, and encoder-decoder stacks.",
        "takeaways": [
            "Self-attention computes dynamic weights: Softmax((Q*K^T) / sqrt(d_k)) * V.",
            "Multi-head attention lets models attend to syntax, semantics, and reference simultaneously.",
            "Transformers eliminate recurrence, enabling massive parallel pretraining on GPUs."
        ]
    },
    "AI8": {
        "video_id": "JgvyzIkgxF0",
        "title": "An Introduction to Reinforcement Learning",
        "channel": "Arxiv Insights",
        "duration": "11:20",
        "description": "Markov Decision Processes (MDPs), policy vs value iteration, discount factor gamma, and Q-learning updates.",
        "takeaways": [
            "The Bellman equation decomposes expected future return into immediate reward + discounted continuation.",
            "Exploration vs exploitation dilemma balanced via epsilon-greedy policies.",
            "Q-learning iteratively approximates the optimal action-value function Q*(s, a)."
        ]
    },
    "FLA1": {
        "video_id": "58N2N7zJGrQ",
        "title": "Introduction to Theory of Computation: Alphabets & Languages",
        "channel": "Neso Academy",
        "duration": "9:45",
        "description": "Formal definitions of symbols, alphabets (Sigma), strings, Kleene star closure, union, and regular expressions.",
        "takeaways": [
            "An alphabet is a finite non-empty set of symbols.",
            "Kleene star Sigma* is the set of all finite strings over Sigma including epsilon.",
            "A language is any subset of Sigma*."
        ]
    },
    "FLA2": {
        "video_id": "40i4PKpM0cI",
        "title": "Deterministic Finite Automata (DFA) State Diagrams & Design",
        "channel": "Neso Academy",
        "duration": "12:10",
        "description": "5-tuple DFA formal structure (Q, Sigma, delta, q0, F), state transition diagrams, and regular language recognition.",
        "takeaways": [
            "In a DFA, every state has exactly one transition for each alphabet symbol.",
            "A string is accepted if the terminal state belongs to the set of accepting states F.",
            "DFAs have strictly finite memory (no stack or unbounded tape)."
        ]
    },
    "FLA3": {
        "video_id": "--CSVsFIDng",
        "title": "Conversion of NFA to DFA (Subset Construction Algorithm)",
        "channel": "Neso Academy",
        "duration": "14:05",
        "description": "NFA with epsilon-transitions, equivalent expressive power, and powerset subset construction algorithm.",
        "takeaways": [
            "NFAs can transition to multiple states or epsilon-transition without consuming input.",
            "Subset construction represents DFA states as subsets of NFA states (power set 2^Q).",
            "NFAs and DFAs recognize the exact same class of regular languages."
        ]
    },
    "FLA4": {
        "video_id": "dikEDuepOtI",
        "title": "Pumping Lemma for Regular Languages: Proofs & Contradictions",
        "channel": "Neso Academy",
        "duration": "15:30",
        "description": "Adversarial pumping lemma proofs by contradiction demonstrating non-regularity of counting languages like a^n b^n.",
        "takeaways": [
            "Pumping Lemma conditions: string s = xyz with |y| > 0, |xy| <= p, and xy^i z in L for all i >= 0.",
            "Choose a target string s of length >= pumping length p.",
            "Show that pumping y produces a string outside the language, establishing contradiction."
        ]
    },
    "FLA5": {
        "video_id": "3rzTRtjUM_I",
        "title": "Context-Free Grammars (CFG) & Derivations",
        "channel": "Neso Academy",
        "duration": "11:50",
        "description": "Non-terminals, production rules, leftmost/rightmost derivations, parse trees, and grammar ambiguity.",
        "takeaways": [
            "Production rules replace a single variable on LHS with a string of variables and terminals.",
            "A grammar is ambiguous if a string admits two distinct leftmost derivation parse trees.",
            "CFGs capture hierarchical syntactic nesting such as balanced expressions."
        ]
    },
    "FLA6": {
        "video_id": "4ejIAmp_Atw",
        "title": "Introduction to Pushdown Automata (PDA) & Stack Memory",
        "channel": "Neso Academy",
        "duration": "13:15",
        "description": "Automata augmented with last-in-first-out (LIFO) stack memory; acceptance by empty stack and final state.",
        "takeaways": [
            "PDA transitions specify (input symbol read, top of stack popped -> symbol pushed).",
            "Deterministic PDAs (DPDA) are strictly less powerful than Nondeterministic PDAs (NPDA).",
            "A language is context-free if and only if some PDA recognizes it."
        ]
    },
    "FLA7": {
        "video_id": "gJQTFhkhwPA",
        "title": "Turing Machines: Infinite Tape & Computability",
        "channel": "EngMicroLectures",
        "duration": "9:18",
        "description": "Infinite tape model, read/write head transitions, Church-Turing thesis, and recursively enumerable languages.",
        "takeaways": [
            "A Turing machine can read, overwrite symbols, and shift its head Left or Right.",
            "The Church-Turing thesis asserts any algorithmic computation can be simulated by a Turing machine.",
            "Languages recognized are Turing-recognizable; those where machines always halt are Turing-decidable."
        ]
    },
    "FLA8": {
        "video_id": "macM_MtS_w4",
        "title": "Turing & The Halting Problem - Computerphile",
        "channel": "Computerphile",
        "duration": "12:04",
        "description": "Turing undecidability of the Halting Problem via diagonalization, polynomial reductions, and P vs NP complexity.",
        "takeaways": [
            "The Halting Problem asks if program P halts on input w.",
            "Proof uses Cantor's diagonalization: construct a machine that halts if and only if it doesn't halt.",
            "P vs NP asks if problems with polynomial verifiable answers have polynomial solutions."
        ]
    },
    "BIO1": {
        "video_id": "ASLUY2U1M-8",
        "title": "How Polarity Makes Water Behave Strangely",
        "channel": "TED-Ed",
        "duration": "11:02",
        "description": "Polar water molecules, hydrogen bond networks, weak acids/bases, Henderson-Hasselbalch equation, and bicarbonate buffer.",
        "takeaways": [
            "Oxygen's high electronegativity creates a permanent dipole in H2O.",
            "Hydrogen bonds drive hydrophobic collapse and macromolecular folding.",
            "Henderson-Hasselbalch equation computes buffer capacity: pH = pKa + log([A-]/[HA])."
        ]
    },
    "BIO2": {
        "video_id": "2Jgb_DpaQhM",
        "title": "Proteins & Amino Acid Hierarchies (Primary to Quaternary)",
        "channel": "Bozeman Science",
        "duration": "8:58",
        "description": "20 amino acid side-chain properties, peptide bonds, alpha-helices, beta-sheets, and tertiary folding energetics.",
        "takeaways": [
            "Peptide bonds form via condensation between carboxyl and amino termini.",
            "Secondary structures are stabilized by backbone hydrogen bonds.",
            "Tertiary folding is driven by hydrophobic side chain burial and disulfide bridges."
        ]
    },
    "BIO3": {
        "video_id": "X_YXTWU2maY",
        "title": "An Introduction to Enzyme Kinetics (Michaelis-Menten: Km & Vmax)",
        "channel": "Khan Academy",
        "duration": "14:12",
        "description": "Transition state lowering, Michaelis constant (Km), Vmax, Lineweaver-Burk plots, and competitive/allosteric inhibition.",
        "takeaways": [
            "Enzymes accelerate reaction rates by lowering activation energy (Delta G++).",
            "Km is the substrate concentration at which reaction rate is exactly half of Vmax.",
            "Competitive inhibitors increase apparent Km without altering Vmax."
        ]
    },
    "BIO4": {
        "video_id": "gggC9vctvBQ",
        "title": "Metabolism | Glycolysis (10 Enzymatic Steps)",
        "channel": "Ninja Nerd",
        "duration": "32:15",
        "description": "Glucose phosphorylation, 10-step glycolytic pathway, net 2 ATP and 2 NADH generation, and phosphofructokinase-1 control.",
        "takeaways": [
            "Hexokinase and PFK-1 consume 2 ATP in the preparatory investment phase.",
            "Substrate-level phosphorylation by phosphoglycerate kinase and pyruvate kinase produces 4 ATP (net +2).",
            "PFK-1 is the primary committed allosteric rate-limiting checkpoint."
        ]
    },
    "BIO5": {
        "video_id": "rr7IRYLqleg",
        "title": "Metabolism | The Krebs Cycle (Citric Acid Cycle: 8 Steps)",
        "channel": "Ninja Nerd",
        "duration": "28:40",
        "description": "Mitochondrial pyruvate dehydrogenase, acetyl-CoA condensation with oxaloacetate, GTP synthesis, and electron carriers.",
        "takeaways": [
            "Oxaloacetate (4C) combines with Acetyl-CoA (2C) to form Citrate (6C).",
            "Two oxidative decarboxylation steps release 2 CO2 molecules.",
            "Each turn yields 3 NADH, 1 FADH2, and 1 GTP/ATP."
        ]
    },
    "BIO6": {
        "video_id": "mfgCcFXUZRk",
        "title": "Electron Transport Chain & ATP Synthase Chemiosmosis",
        "channel": "Khan Academy",
        "duration": "30:10",
        "description": "Electron transport chain Complexes I-IV, chemiosmotic proton-motive force, and rotary catalysis of F0-F1 ATP synthase.",
        "takeaways": [
            "Complexes I, III, and IV pump protons into the intermembrane space to generate a proton-motive force.",
            "Oxygen serves as the terminal electron acceptor, being reduced to H2O.",
            "Proton backflow drives the mechanical rotation of F0-F1 ATP synthase to phosphorylate ADP to ATP."
        ]
    },
    "BIO7": {
        "video_id": "qBCVVszQQNs",
        "title": "Inside the Cell Membrane & Fluid Mosaic Model",
        "channel": "Amoeba Sisters",
        "duration": "8:22",
        "description": "Phospholipid bilayers, cholesterol fluidity regulation, triacylglycerol storage, and mitochondrial beta-oxidation of fatty acids.",
        "takeaways": [
            "Phospholipids spontaneously form bilayers with hydrophobic cores and hydrophilic surfaces.",
            "Cholesterol buffers membrane fluidity across high and low temperature fluctuations.",
            "Beta-oxidation systematically breaks fatty acids into 2-carbon Acetyl-CoA units in the mitochondria."
        ]
    },
    "BIO8": {
        "video_id": "gG7uCskUOrA",
        "title": "From DNA to Protein - 3D (Replication, Transcription & Translation)",
        "channel": "yourgenome",
        "duration": "13:28",
        "description": "DNA double-helix structure, DNA polymerase fidelity, RNA transcription, and ribosomal mRNA-to-protein translation.",
        "takeaways": [
            "DNA replication is semi-conservative and catalyzed 5' -> 3' by DNA Polymerase.",
            "RNA Polymerase synthesizes complementary pre-mRNA from template DNA.",
            "Ribosomes decode mRNA triplets using aminoacyl-tRNAs in the A, P, and E sites."
        ]
    },
}

def verify_all():
    print(f"Total entries: {len(BASE_PASSED)}")
    assert len(BASE_PASSED) == 42, f"Expected 42 concepts, got {len(BASE_PASSED)}"
    
    passed_count = 0
    for cid, data in BASE_PASSED.items():
        vid = data["video_id"]
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                oembed_data = json.loads(resp.read().decode("utf-8"))
                passed_count += 1
                print(f"[OK 200] {cid:4} ({vid}) : {oembed_data.get('title')} [{oembed_data.get('author_name')}]")
        except Exception as e:
            print(f"[FAIL]   {cid:4} ({vid}) : {e}")

    print(f"\nFinal Result: {passed_count} / {len(BASE_PASSED)} verified active on YouTube!")
    return passed_count == len(BASE_PASSED)

if __name__ == "__main__":
    success = verify_all()
    if not success:
        exit(1)
