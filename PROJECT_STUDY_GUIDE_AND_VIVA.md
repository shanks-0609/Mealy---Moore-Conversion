# Complete Project Study & Viva Preparation Guide
## Mealy <-> Moore Machine Conversion Simulator
**Course:** CSET302 - Automata Theory and Computability (Sem 5)  
**Evaluation:** Milestone 1 (M1) - Problem Analysis & Project Design (5 Marks)  
**Evaluation Dates:** 2 - 6 November 2026  

---

## Table of Contents
1. [Project Elevator Pitch (30-Second Summary)](#1-project-elevator-pitch)
2. [Evaluation Rubric & What Examiners Look For](#2-evaluation-rubric--what-examiners-look-for)
3. [Core Theory: Mealy vs. Moore Machines](#3-core-theory-mealy-vs-moore-machines)
4. [Formal Mathematical Specifications (The 6-Tuples)](#4-formal-mathematical-specifications)
5. [The Output Timing Difference: Length $k$ vs. $k+1$](#5-the-output-timing-difference)
6. [Conversion Algorithms Deep Dive](#6-conversion-algorithms-deep-dive)
   - [Mealy to Moore Algorithm & State Splitting](#61-mealy-to-moore-algorithm--state-splitting)
   - [Moore to Mealy Algorithm](#62-moore-to-mealy-algorithm)
7. [The Manually Solved Benchmark ('01' Sequence Detector)](#7-the-manually-solved-benchmark)
8. [Existing Tools & Feasibility Analysis](#8-existing-tools--feasibility-analysis)
9. [Simulator Architecture & Code Walkthrough](#9-simulator-architecture--code-walkthrough)
10. [Top 15 Viva / Oral Exam Questions & Model Answers](#10-top-15-viva-questions--model-answers)
11. [How to Demo the Project in the Evaluation](#11-how-to-demo-the-project-in-the-evaluation)

---

<a name="1-project-elevator-pitch"></a>
## 1. Project Elevator Pitch (30-Second Summary)

> *"Good morning / afternoon sir/ma'am. Our project is a **Mealy $\leftrightarrow$ Moore Machine Conversion Simulator** designed for CSET302. In automata theory, Mealy machines associate outputs with state transitions, while Moore machines associate outputs strictly with states. While both models have equivalent computational power, converting between them requires handling **state splitting** and the **1-symbol output timing difference** ($k$ vs $k+1$ outputs). Our simulator automates bi-directional conversion, provides an audit log of why states split, visualizes formatted ASCII transition tables, and formally verifies that $\text{Output}_{Moore}[1:] == \text{Output}_{Mealy}$ across all test strings. It is completely implemented in pure Python with zero external dependencies and validated with automated unit tests."*

---

<a name="2-evaluation-rubric--what-examiners-look-for"></a>
## 2. Evaluation Rubric & What Examiners Look For

| Criterion | Marks | What You Must Show & Explain |
| :--- | :---: | :--- |
| **1. Problem Definition & Automata Specification** | **1** | - Define Mealy and Moore machines clearly.<br>- State formal 6-tuples for both ($Q, \Sigma, \Delta, \delta, \lambda, q_0$ vs $S, \Sigma, \Delta, \delta', \lambda', s_0$).<br>- State inputs, outputs, transition functions.<br>- Explain why Moore output has length $|w| + 1$ while Mealy has length $|w|$.<br>- State the formal preservation condition: $\text{Output}_{Moore}(w) = \lambda'(s_0) \circ \text{Output}_{Mealy}(w)$. |
| **2. Existing Tools & Feasibility** | **1** | - Review existing tools: **JFLAP**, **Automata-lib**, and **Web Simulators**.<br>- Explain limitations: JFLAP requires Java JRE and lacks step-by-step conversion logs; Automata-lib focuses only on language acceptors (DFAs/NFAs), not transducers; Web tools are black boxes.<br>- Explain feasibility: Technical (pure Python, cross-platform), Pedagogical (detailed step logs), Operational (< 1 ms runtime). |
| **3. Simulator Design & Methodology** | **2** | - Explain the 5 modules: Core Models, Conversion Engine, Table Visualizer, Verification Harness, CLI Interface.<br>- Draw/explain the **Input-Processing-Output (IPO) workflow**.<br>- Show the UI / CLI wireframe.<br>- Explain data structures used (Python dataclasses, dictionaries for $\delta$ and $\lambda$). |
| **4. Algorithm Selection & Correctness** | **1** | - Present step-by-step pseudocode for both conversions.<br>- Explain state splitting logic: why a state $q$ splits into $(q, y)$ based on incoming outputs.<br>- Walk through the **manually solved '01' sequence detector example**.<br>- Show the manual table and trace on string `"0101"` matching the simulator output. |
| **TOTAL** | **5 Marks** | **All 4 criteria are fully addressed in our report, code, and tests.** |

---

<a name="3-core-theory-mealy-vs-moore-machines"></a>
## 3. Core Theory: Mealy vs. Moore Machines

### Key Differences at a Glance:

| Property | Mealy Machine | Moore Machine |
| :--- | :--- | :--- |
| **Output Dependency** | Current State **AND** Current Input: $\lambda(q, a)$ | Current State **ONLY**: $\lambda'(s)$ |
| **Output Placement** | Placed on the **transitions / edges** ($a / y$) | Placed inside or next to the **states** ($s / y$) |
| **Output Timing** | Changes **immediately** when input arrives (asynchronous with state arrival) | Changes **only after** transition into the state occurs (synchronous with clock edge) |
| **Output String Length** | For input of length $k$, output length is **$k$** | For input of length $k$, output length is **$k + 1$** (includes initial state output) |
| **Number of States** | Generally **fewer states** for the same logic | Often requires **more states** due to state splitting |
| **Hardware Implication** | Faster response; but susceptible to input glitches/hazards | 1 clock cycle delay; immune to input glitches (outputs are registered) |

---

<a name="4-formal-mathematical-specifications"></a>
## 4. Formal Mathematical Specifications (The 6-Tuples)

### A. Mealy Machine Formal 6-Tuple
A Mealy Machine is mathematically defined as:
$$M_1 = (Q, \Sigma, \Delta, \delta, \lambda, q_0)$$
1. **$Q$**: Finite non-empty set of states: $\{q_0, q_1, \dots, q_{n-1}\}$.
2. **$\Sigma$**: Finite non-empty set of input symbols (input alphabet), e.g., $\{0, 1\}$.
3. **$\Delta$**: Finite non-empty set of output symbols (output alphabet), e.g., $\{0, 1\}$.
4. **$\delta$**: Transition function mapping a state and an input symbol to the next state:
   $$\delta: Q \times \Sigma \to Q$$
5. **$\lambda$**: Transition output function mapping a state and an input symbol to an output symbol:
   $$\lambda: Q \times \Sigma \to \Delta$$
6. **$q_0$**: Initial / start state, where $q_0 \in Q$.

### B. Moore Machine Formal 6-Tuple
A Moore Machine is mathematically defined as:
$$M_2 = (S, \Sigma, \Delta, \delta', \lambda', s_0)$$
1. **$S$**: Finite non-empty set of states: $\{s_0, s_1, \dots, s_{m-1}\}$.
2. **$\Sigma$**: Finite non-empty set of input symbols (identical to Mealy).
3. **$\Delta$**: Finite non-empty set of output symbols (identical to Mealy).
4. **$\delta'$**: Transition function mapping a state and an input symbol to the next state:
   $$\delta': S \times \Sigma \to S$$
5. **$\lambda'$**: State output function mapping a state to an output symbol:
   $$\lambda': S \to \Delta$$
6. **$s_0$**: Initial / start state, where $s_0 \in S$.

---

<a name="5-the-output-timing-difference"></a>
## 5. The Output Timing Difference: Length $k$ vs. $k+1$

This is the **#1 question professors ask in vivas**:
> *"Why is Moore output length $k+1$ when Mealy output is $k$ for an input string of length $k$?"*

### The Reason:
- When a Moore machine powers on or resets, it is in its initial state $s_0$.
- Because **every state in a Moore machine has an output associated with it**, $s_0$ immediately emits its output symbol $\lambda'(s_0)$ **before any input character is read!**
- When the first input symbol $a_1$ arrives, the machine transitions to state $s_1$, which emits $\lambda'(s_1)$.
- After reading $k$ input symbols $a_1 a_2 \dots a_k$, the machine has visited states $s_0, s_1, s_2, \dots, s_k$.
- Total outputs emitted = $k + 1$ symbols:
  $$\text{Output}_{Moore}(w) = \lambda'(s_0) \lambda'(s_1) \dots \lambda'(s_k)$$
- In contrast, a Mealy machine produces an output **only when traversing a transition**. Before reading an input symbol, no transition occurs, so no output is produced. After reading $k$ symbols, it produces exactly $k$ outputs:
  $$\text{Output}_{Mealy}(w) = \lambda(q_0, a_1) \lambda(q_1, a_2) \dots \lambda(q_{k-1}, a_k)$$

### The Equivalence Criterion:
$$\text{Output}_{Moore}(w) = \lambda'(s_0) \circ \text{Output}_{Mealy}(w)$$
If you discard or slice off the first symbol of the Moore machine's output (`Output_Moore[1:]`), the remaining $k$ characters are **strictly identical** to the Mealy output!

---

<a name="6-conversion-algorithms-deep-dive"></a>
## 6. Conversion Algorithms Deep Dive

<a name="61-mealy-to-moore-algorithm--state-splitting"></a>
### 6.1 Mealy to Moore Algorithm & State Splitting

#### Why do states split?
In a Mealy machine, state $q$ might be entered from state $A$ with output `0`, and from state $B$ with output `1`.
In a Moore machine, a state can have **only one output**.
Therefore, we cannot keep state $q$ as a single state. We must split $q$ into:
- $q_0$: for all incoming transitions that produced output `0`.
- $q_1$: for all incoming transitions that produced output `1`.

#### Step-by-Step Algorithm:
1. **Find Incoming Outputs:** For each state $q \in Q$, find the set of outputs on all incoming transitions:
   $$\text{IncomingOutputs}(q) = \{ \lambda(p, a) \mid p \in Q, a \in \Sigma, \delta(p, a) = q \}$$
2. **Handle Initial State:** The start state $q_0$ must have an initial output $y_{init}$ assigned (from its incoming transitions, or default `0`). Add $y_{init}$ to $\text{IncomingOutputs}(q_0)$.
3. **Generate Moore States:** For each $q \in Q$ and each output $y \in \text{IncomingOutputs}(q)$, create Moore state $(q, y)$ with $\lambda'((q, y)) = y$.
4. **Designate Start State:** Moore initial state is $s_0 = (q_0, y_{init})$.
5. **Map Transitions:** For every Moore state $(q, y)$ and input $a \in \Sigma$:
   - Look up the Mealy transition: $next\_state = \delta(q, a)$ and $out = \lambda(q, a)$.
   - The destination Moore state is $(next\_state, out)$.
   - Therefore:
     $$\delta'((q, y), a) = (\delta(q, a), \lambda(q, a))$$
6. **Maximum State Bound:**
   $$\text{Max Moore States} = |Q| \times |\Delta|$$
   Where $|Q|$ is number of Mealy states, and $|\Delta|$ is number of output symbols.

---

<a name="62-moore-to-mealy-algorithm"></a>
### 6.2 Moore to Mealy Algorithm

Converting Moore to Mealy is much simpler and **never increases state count**.

#### Why does state count stay the same?
In a Moore machine, the output is tied to the state itself. When moving to state $s'$, that state's output is $\lambda'(s')$.
In a Mealy machine, we can simply place that output onto the transition entering $s'$.

#### Step-by-Step Algorithm:
1. **Retain States:** Mealy states $Q = S$ and initial state $q_0 = s_0$.
2. **Map Transitions and Outputs:** For every state $s \in S$ and input $a \in \Sigma$:
   - Next state remains the same: $\delta(s, a) = \delta'(s, a) = s'$.
   - The transition output is set to the destination state's output:
     $$\lambda(s, a) = \lambda'(s') = \lambda'(\delta'(s, a))$$
3. **State Count:**
   $$|Q_{Mealy}| = |S_{Moore}|$$

---

<a name="7-the-manually-solved-benchmark"></a>
## 7. The Manually Solved Benchmark ('01' Sequence Detector)

*Study this example thoroughly — you can draw it on the whiteboard or explain it step-by-step during your presentation.*

### The Problem:
Design a Mealy machine that detects the pattern `'01'` in a binary stream, emitting `1` when `'01'` is detected and `0` otherwise. Then manually convert it to an equivalent Moore machine and validate it on string $w = \text{"0101"}$.

### Step 1: Given Mealy Machine
- States: $Q = \{q_0, q_1\}$ (where $q_0 = \text{start / no '0' seen}$, $q_1 = \text{saw '0'}$)
- Alphabets: $\Sigma = \{0, 1\}$, $\Delta = \{0, 1\}$, Start state = $q_0$.

**Mealy Transition Table:**
| Current State | Input 0 (Next / Out) | Input 1 (Next / Out) | Explanation |
| :---: | :---: | :---: | :--- |
| $\to q_0$ | $q_1 \ / \ 0$ | $q_0 \ / \ 0$ | On '0', go to $q_1$ (saw '0'). On '1', stay in $q_0$. |
| $q_1$ | $q_1 \ / \ 0$ | $q_0 \ / \ 1$ | On '0', stay in $q_1$. On '1', pattern '01' detected! Output `1`, return to $q_0$. |

---

### Step 2: Calculate Incoming Outputs & Split States
1. **Examine state $q_0$:**
   - From $(q_0, 1) \to$ arrives at $q_0$ with output **`0`**.
   - From $(q_1, 1) \to$ arrives at $q_0$ with output **`1`**.
   - Incoming outputs for $q_0$ = $\{0, 1\}$.
   - **Conclusion:** $q_0$ MUST be split into **2 Moore states**:
     - $q_{0\_0}$ (with state output `0`)
     - $q_{0\_1}$ (with state output `1`)

2. **Examine state $q_1$:**
   - From $(q_0, 0) \to$ arrives at $q_1$ with output **`0`**.
   - From $(q_1, 0) \to$ arrives at $q_1$ with output **`0`**.
   - Incoming outputs for $q_1$ = $\{0\}$.
   - **Conclusion:** $q_1$ requires only **1 Moore state**:
     - $q_{1\_0}$ (with state output `0`)

3. **Start State:**
   - Mealy start state was $q_0$. With default initial output `0`, the Moore start state is **$q_{0\_0}$**.

---

### Step 3: Resultant Moore Machine Transition Table

| Moore State | On Input 0 | On Input 1 | State Output ($\lambda'$) |
| :---: | :---: | :---: | :---: |
| $\to q_{0\_0}$ | $q_{1\_0}$ | $q_{0\_0}$ | **0** |
| $q_{0\_1}$ | $q_{1\_0}$ | $q_{0\_0}$ | **1** |
| $q_{1\_0}$ | $q_{1\_0}$ | $q_{0\_1}$ | **0** |

*Notice:* Both $q_{0\_0}$ and $q_{0\_1}$ have identical next states on input 0 ($q_{1\_0}$) and input 1 ($q_{0\_0}$) because in the original Mealy machine, state $q_0$ transitioned to $q_1$ (output 0) and $q_0$ (output 0). But their state outputs are different (`0` vs `1`).

---

### Step 4: Trace and Validation on String $w = \text{"0101"}$

Let's trace input string $w = 0101$ symbol by symbol:

#### Mealy Machine Trace:
- Start at $q_0$ (no initial output)
- Read `0`: transition $q_0 \xrightarrow{0 / 0} q_1$. Output: `0`
- Read `1`: transition $q_1 \xrightarrow{1 / 1} q_0$. Output: `1` (First `'01'` detected)
- Read `0`: transition $q_0 \xrightarrow{0 / 0} q_1$. Output: `0`
- Read `1`: transition $q_1 \xrightarrow{1 / 1} q_0$. Output: `1` (Second `'01'` detected)
- **Mealy Output:** `"0101"` (Length = 4)

#### Moore Machine Trace:
- Start at state $q_{0\_0}$. Emits initial output: **`0`**
- Read `0`: transition $q_{0\_0} \to q_{1\_0}$. State $q_{1\_0}$ emits: **`0`**
- Read `1`: transition $q_{1\_0} \to q_{0\_1}$. State $q_{0\_1}$ emits: **`1`** (Detected!)
- Read `0`: transition $q_{0\_1} \to q_{1\_0}$. State $q_{1\_0}$ emits: **`0`**
- Read `1`: transition $q_{1\_0} \to q_{0\_1}$. State $q_{0\_1}$ emits: **`1`** (Detected!)
- **Moore Output:** `"00101"` (Length = 5)

#### Formal Equivalence Check:
$$\text{Moore Output} = \text{"00101"}$$
$$\text{Moore Output}[1:] = \text{"0101"} == \text{Mealy Output ("0101")}$$
**Verification: PASS $\checkmark$**

---

<a name="8-existing-tools--feasibility-analysis"></a>
## 8. Existing Tools & Feasibility Analysis

When asked: *"Why build a new simulator when tools like JFLAP exist?"*

### Tool Review:
1. **JFLAP:**
   - *Strengths:* Popular educational GUI for Turing machines, grammars, and DFAs.
   - *Weaknesses:* Requires Java JRE; no automated step-by-step state splitting logs; no automated bi-directional conversion with batch string validation; cannot be run as a lightweight CLI or Python script.
2. **Automata-lib (Python Library):**
   - *Strengths:* Excellent for DFAs, NFAs, and regular expressions.
   - *Weaknesses:* Focuses on language acceptors (accept/reject), not transducers (output generators); Mealy/Moore conversions are not natively supported with step logs.
3. **Web Simulators:**
   - *Strengths:* Accessible in a web browser without installation.
   - *Weaknesses:* Black-box implementations (only shows final answer, not the intermediate state-splitting steps); cannot be automated in unit tests; requires internet access.

### Feasibility Justification:
- **Technical Feasibility:** Written in 100% pure Python 3 using standard libraries (`dataclasses`, `typing`). Runs on any OS without extra packages.
- **Pedagogical Feasibility:** Explicitly prints educational step-by-step logs explaining every split state and verifies the formal condition $\text{Output}_{Moore}[1:] == \text{Output}_{Mealy}$.
- **Operational Feasibility:** Ultra-fast (< 1 ms per conversion), zero configuration, reproducible with unit tests.

---

<a name="9-simulator-architecture--code-walkthrough"></a>
## 9. Simulator Architecture & Code Walkthrough

The codebase consists of two primary Python files:

### 1. `simulator.py` (Core Engine)
- **`MealyMachine` (dataclass):**
  - Fields: `states`, `inputs`, `outputs`, `initial_state`, `transitions`, `output_table`.
  - Methods: `simulate(input_string)` returns state sequence, output string, and trace; `print_table()` prints formatted ASCII table.
- **`MooreMachine` (dataclass):**
  - Fields: `states`, `inputs`, `outputs`, `initial_state`, `transitions`, `state_outputs`.
  - Methods: `simulate(input_string)` (includes start state output); `print_table()`.
- **`mealy_to_moore(mealy, default_initial_output)`:**
  - Implements the 5-step conversion algorithm and logs every step.
- **`moore_to_mealy(moore)`:**
  - Implements the 3-step conversion algorithm.
- **`verify_equivalence(mealy, moore, test_strings)`:**
  - Asserts $\text{Output}_{Moore}[1:] == \text{Output}_{Mealy}$ across all test inputs.
- **Interactive CLI Menu:**
  - Allows entering custom machines or running built-in benchmark demos.

### 2. `test_simulator.py` (Unit Tests)
- `test_mealy_to_moore_1s_complement`: Tests inverter logic across various binary strings.
- `test_mealy_to_moore_sequence_detector`: Tests the `'01'` detector.
- `test_moore_to_mealy_substring_detector`: Tests Moore-to-Mealy on `'10'` detector.
- `test_state_count_split`: Formally tests that $q_0$ splits into $q_{0\_0}$ and $q_{0\_1}$ (total 3 Moore states).

---

<a name="10-top-15-viva-questions--model-answers"></a>
## 10. Top 15 Viva / Oral Exam Questions & Model Answers

### Q1: What is the primary difference between a Mealy and a Moore machine?
**Answer:** In a Mealy machine, output depends on both the current state and the current input symbol ($\lambda: Q \times \Sigma \to \Delta$). In a Moore machine, output depends exclusively on the current state ($\lambda': S \to \Delta$).

### Q2: For an input string of length $k$, how many output symbols do Mealy and Moore machines generate?
**Answer:** A Mealy machine generates $k$ output symbols because an output is produced only upon transitioning on an input symbol. A Moore machine generates $k+1$ output symbols because the initial state emits an output symbol before any input symbol is processed.

### Q3: When are a Mealy machine and a Moore machine said to be equivalent?
**Answer:** They are equivalent if for every input string $w \in \Sigma^*$, the output of the Moore machine matches the output of the Mealy machine except for the initial state output symbol $\lambda'(s_0)$:
$$\text{Output}_{Moore}(w) = \lambda'(s_0) \circ \text{Output}_{Mealy}(w)$$
Or programmatically: `Output_Moore[1:] == Output_Mealy`.

### Q4: Why do states split when converting from Mealy to Moore?
**Answer:** In a Mealy machine, transitions arriving at a single state $q$ from different source states or inputs can have different output symbols (e.g., one enters with output `0`, another with output `1`). In a Moore machine, every state must have exactly one fixed output. Therefore, state $q$ must be split into distinct states $(q, y)$ for each distinct incoming output $y$.

### Q5: If a Mealy machine has $n$ states and the output alphabet has $m$ symbols, what is the theoretical maximum number of states in the equivalent Moore machine?
**Answer:** The theoretical maximum is $n \times m$ states. Each Mealy state can split into at most $m$ Moore states (one for each possible output symbol).

### Q6: Can a state split during Moore to Mealy conversion?
**Answer:** No. In Moore to Mealy conversion, state count never increases because each state in a Moore machine already has a single output. The transition output in the Mealy machine is simply assigned the destination state's output ($\lambda(s, a) = \lambda'(\delta'(s, a))$). Thus, $|Q_{Mealy}| \le |S_{Moore}|$.

### Q7: Why does Moore machine have better glitch resistance in digital hardware?
**Answer:** In Mealy machines, because output is directly tied to the input wire, any combinatorial noise or glitch on the input line immediately ripples through to the output. In Moore machines, the output depends only on the current state (stored in flip-flops), making outputs synchronized with the clock and immune to input glitches.

### Q8: What happens if a start state in a Mealy machine has no incoming transitions?
**Answer:** If $q_0$ has no incoming transitions, it does not acquire an output from any transition. In the equivalent Moore machine, we assign it a designated initial output $y_{init}$ (or the default first symbol of $\Delta$).

### Q9: What are the 6 tuples of a Mealy machine?
**Answer:** $M = (Q, \Sigma, \Delta, \delta, \lambda, q_0)$, where $Q$ is the set of states, $\Sigma$ is the input alphabet, $\Delta$ is the output alphabet, $\delta: Q \times \Sigma \to Q$ is the state transition function, $\lambda: Q \times \Sigma \to \Delta$ is the transition output function, and $q_0 \in Q$ is the initial state.

### Q10: What are the 6 tuples of a Moore machine?
**Answer:** $M = (S, \Sigma, \Delta, \delta', \lambda', s_0)$, where $S$ is the set of states, $\Sigma$ is the input alphabet, $\Delta$ is the output alphabet, $\delta': S \times \Sigma \to S$ is the state transition function, $\lambda': S \to \Delta$ is the state output function, and $s_0 \in S$ is the initial state.

### Q11: In your sequence detector example, why did $q_0$ split into 2 states while $q_1$ remained 1 state?
**Answer:** $q_0$ was entered from transition $(q_0, 1)$ with output `0` and from $(q_1, 1)$ with output `1`. Because it had two incoming outputs (`0` and `1`), it had to split into $q_{0\_0}$ and $q_{0\_1}$. In contrast, $q_1$ was only entered with output `0` (from both $(q_0, 0)$ and $(q_1, 0)$), so it only required $q_{1\_0}$.

### Q12: How does your code verify that the conversion was correct?
**Answer:** In `test_simulator.py` and `simulator.py`, the function `verify_equivalence()` simulates a set of candidate input strings on both machines. For each string $w$, it asserts that `mo_out[1:] == m_out` and that `len(mo_out) == len(m_out) + 1`. If all strings match, the test passes.

### Q13: What data structures did you use in `simulator.py`?
**Answer:** We used Python `dataclass` to represent `MealyMachine` and `MooreMachine`. Transitions are stored in a dictionary mapping `(current_state, input_symbol) -> next_state`. Mealy outputs are stored in `(current_state, input_symbol) -> output_symbol`, and Moore outputs are stored in `state -> output_symbol`.

### Q14: What is the time complexity of the Mealy to Moore conversion algorithm?
**Answer:** The time complexity is $O(|Q| \cdot |\Sigma| + |S| \cdot |\Sigma|)$, which is $O(|Q| \cdot |\Sigma| \cdot |\Delta|)$ in the worst case, where $|Q|$ is states, $|\Sigma|$ is alphabet size, and $|\Delta|$ is output alphabet size. Since FSMs typically have small alphabets (e.g. binary $\{0, 1\}$), the algorithm runs in sub-millisecond time.

### Q15: What are your planned deliverables for Milestone 2 (M2)?
**Answer:** For M2, we plan to implement a Graphical User Interface (GUI) to visually draw state diagrams with animated node traversals, add state minimization algorithms (Hopcroft's algorithm) to reduce redundant states post-conversion, and provide export options to Graphviz and LaTeX.

---

<a name="11-how-to-demo-the-project-in-the-evaluation"></a>
## 11. How to Demo the Project in the Evaluation

When asked to present or demo your project, follow this exact sequence:

### Step 1: Run Unit Tests (Shows robustness & 0 errors)
```bash
python -m unittest test_simulator.py
```
**Say:** *"Sir/Ma'am, first we run our automated test suite. All 4 unit tests execute in 0.000s and pass, validating 1's complement generation, sequence detection, and state count splitting."*

### Step 2: Run Built-in Automated Benchmark Demo
```bash
python simulator.py --demo
```
**Say:** *"Next, we run our automated benchmark demo. Here you can see the original Mealy machine for the '01' sequence detector. Our algorithm computes the incoming outputs: state $q_0$ receives both 0 and 1, so it splits into $q_{0\_0}$ and $q_{0\_1}$. Then it builds the Moore table and verifies the string '0101' side-by-side, confirming that Moore output '00101' sliced from index 1 equals Mealy output '0101'."*

### Step 3: Run Interactive CLI (If they want custom input)
```bash
python simulator.py
```
**Say:** *"Our simulator also supports dynamic keyboard input (Option 3 and 4) where any custom Mealy or Moore machine can be entered interactively."*

### Step 4: Show the M1 Design Report Document
Open `M1_Simulator_Design_Report.docx` and show:
1. Cover page with Student Details and M1 Evaluation window.
2. Rubric alignment table (addressing all 5 marks).
3. Formal 6-tuple specifications.
4. Tool comparative matrix.
5. IPO workflow and UI wireframe.
6. Manually solved example with step-by-step trace table.
