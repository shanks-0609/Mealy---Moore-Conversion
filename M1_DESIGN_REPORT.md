# M1 Design Report: Mealy <-> Moore Machine Conversion Simulator
**Course:** CSET302 - Automata Theory and Computability  
**Evaluation:** Milestone 1 (M1) - Problem Analysis & Project Design (5 Marks)  
**Topic:** Mealy <-> Moore Conversion: Convert between machines while preserving and displaying output behaviour.

---

## 1. Problem Definition & Automata Specification (1 Mark)

### 1.1 Problem Statement & Objectives
Finite State Machines with outputs are foundational models in computer science, digital circuit design, and lexical analysis:
- In a **Mealy Machine**, output depends on both the **current state and the current input symbol**.
- In a **Moore Machine**, output depends **solely on the current state**.

**Primary Objective:**  
Design and implement a simulator that converts:
1. An arbitrary Mealy machine into an equivalent Moore machine.
2. An arbitrary Moore machine into an equivalent Mealy machine.
3. Rigorously verifies and demonstrates **output behaviour preservation** across both representations for any input string $w \in \Sigma^*$.

### 1.2 Formal Automata Specifications (Tuples)

#### A. Mealy Machine Formal 6-Tuple:
$$M_1 = (Q, \Sigma, \Delta, \delta, \lambda, q_0)$$
- $Q$: Finite set of states $\{q_0, q_1, \dots, q_{n-1}\}$
- $\Sigma$: Finite set of input symbols (input alphabet)
- $\Delta$: Finite set of output symbols (output alphabet)
- $\delta: Q \times \Sigma \to Q$: State transition function
- $\lambda: Q \times \Sigma \to \Delta$: Transition output function
- $q_0 \in Q$: Initial state

#### B. Moore Machine Formal 6-Tuple:
$$M_2 = (S, \Sigma, \Delta, \delta', \lambda', s_0)$$
- $S$: Finite set of states $\{s_0, s_1, \dots, s_{m-1}\}$
- $\Sigma$: Finite set of input symbols
- $\Delta$: Finite set of output symbols
- $\delta': S \times \Sigma \to S$: State transition function
- $\lambda': S \to \Delta$: State output function
- $s_0 \in S$: Initial state

### 1.3 Equivalence & Output Behaviour Criterion
For an input string $w = a_1 a_2 \dots a_k$ of length $k$:
- **Mealy Machine Output:** Produces $k$ output symbols: $y_1 y_2 \dots y_k$.
- **Moore Machine Output:** Produces $k+1$ output symbols: $y_0 y_1 y_2 \dots y_k$, where $y_0 = \lambda'(s_0)$ is the output associated with the initial state before reading any input.
- **Preservation Condition:**
  $$\text{Output}_{Moore}(w) = \lambda'(s_0) \circ \text{Output}_{Mealy}(w)$$
  The subsequent $k$ symbols of Moore output must be identical to the Mealy output.

---

## 2. Existing Tools & Feasibility Analysis (1 Mark)

| Tool / Platform | Strengths | Limitations | Feasibility of Proposed Simulator |
| :--- | :--- | :--- | :--- |
| **JFLAP** | Widely used educational GUI tool for automata and grammars. | Heavy Java desktop dependency; does not provide direct automated bi-directional Mealy $\leftrightarrow$ Moore conversion with step-by-step state splitting logs or side-by-side string validation. | High. A lightweight, standalone Python CLI/module requires zero third-party installation and executes seamlessly on any platform. |
| **Automata (Python Lib)** | Good library for DFAs and NFAs. | Primarily focuses on language acceptors (DFA/NFA/PDA/Turing); lacks native, detailed Mealy/Moore conversion visualization and step-by-step trace breakdown. | High. Tailored specifically for CSET302 curriculum requirements with clean ASCII table displays and verification routines. |
| **Online Web Simulators** | Browser accessible. | Often black-box converters without granular state-splitting tracking, manual test verification, or exportable traces. | High. Standalone Python code provides direct command-line automation, testability, and clear pedagogical logging. |

---

## 3. Simulator Design & Methodology (2 Marks)

### 3.1 Modular Architecture
The simulator is organized into four distinct modules:
1. **Core Models (`MealyMachine`, `MooreMachine`)**: Dataclasses holding formal tuples, transition tables, and step simulation engines.
2. **Conversion Engine (`mealy_to_moore`, `moore_to_mealy`)**: Implements mathematical state splitting and transition mapping algorithms with step logs.
3. **Table & Trace Visualizer**: Clean, formatted ASCII transition tables and state traversal traces.
4. **Validation & Verification Harness**: Executes test strings through both original and converted machines, automatically verifying $\text{Output}_{Moore}[1:] == \text{Output}_{Mealy}$.

### 3.2 Input-Processing-Output (IPO) Workflow
```
[User Input]
  ├── Dynamic Input (states, alphabet, transitions, outputs, initial state)
  └── Or Predefined Benchmarks (1's complement, Sequence Detectors)
         │
         ▼
[Processing Engine]
  ├── Mealy -> Moore: Identify incoming outputs -> Split states (q, y) -> Map transitions
  └── Moore -> Mealy: Retain states -> Map transition outputs to dest state output lambda'(s')
         │
         ▼
[Visualization & Output]
  ├── Display Original Transition Table
  ├── Display Step-by-Step Conversion Log
  └── Display Converted Transition Table
         │
         ▼
[Validation Engine]
  ├── Simulate input string w on both machines
  ├── Trace state sequence & generated output
  └── Assert: Output_Moore = lambda'(s0) + Output_Mealy -> PASS/FAIL
```

### 3.3 UI / CLI Layout
```
+--------------------------------------------------------------------+
|             MEALY <-> MOORE CONVERSION SIMULATOR                   |
+--------------------------------------------------------------------+
| 1. Demo Mealy -> Moore (Sequence '01' Detector)                    |
| 2. Demo Moore -> Mealy (Substring '10' Detector)                   |
| 3. Dynamic Input: Enter Custom Mealy Machine -> Convert to Moore   |
| 4. Dynamic Input: Enter Custom Moore Machine -> Convert to Mealy   |
| 5. Exit                                                            |
+--------------------------------------------------------------------+
```

---

## 4. Algorithm Selection & Correctness (1 Mark)

### 4.1 Mealy to Moore Conversion Algorithm
**Algorithm Steps:**
1. Given Mealy machine $M = (Q, \Sigma, \Delta, \delta, \lambda, q_0)$.
2. For each state $q \in Q$, find the set of all incoming transition outputs:
   $$IncomingOutputs(q) = \{ \lambda(p, a) \mid p \in Q, a \in \Sigma, \delta(p, a) = q \}$$
3. For each state $q$ and each output $y \in IncomingOutputs(q)$, create a new Moore state $(q, y)$ with state output $\lambda'((q, y)) = y$.
4. For initial state $q_0$: If $q_0$ requires an initial output (or has no incoming transitions), create $(q_0, y_{init})$ where $y_{init}$ is the designated initial output.
5. Define transitions for all created Moore states:
   $$\delta'((q, y), a) = (\delta(q, a), \lambda(q, a))$$
6. Moore initial state is set to $(q_0, y_{init})$.

### 4.2 Moore to Mealy Conversion Algorithm
**Algorithm Steps:**
1. Given Moore machine $M' = (S, \Sigma, \Delta, \delta', \lambda', s_0)$.
2. Set Mealy states $Q = S$ and initial state $q_0 = s_0$.
3. For each state $s \in S$ and input symbol $a \in \Sigma$:
   - Set next state $\delta(s, a) = \delta'(s, a) = s'$.
   - Set transition output $\lambda(s, a) = \lambda'(s')$.

---

### 4.3 Manually Solved Validation Example

#### Problem: Convert Mealy Machine detecting sequence `'01'` to Moore Machine

**Given Mealy Machine:**
- States: $\{q_0, q_1\}$, Initial State: $q_0$
- Inputs: $\Sigma = \{0, 1\}$, Outputs: $\Delta = \{0, 1\}$
- Transition Table:
  - $\delta(q_0, 0) = q_1, \lambda(q_0, 0) = 0$
  - $\delta(q_0, 1) = q_0, \lambda(q_0, 1) = 0$
  - $\delta(q_1, 0) = q_1, \lambda(q_1, 0) = 0$
  - $\delta(q_1, 1) = q_0, \lambda(q_1, 1) = 1$ (Sequence '01' detected!)

**Manual Conversion Steps:**
1. **Analyze Incoming Outputs:**
   - Incoming to $q_0$: from $(q_0, 1) \to$ output `0`; from $(q_1, 1) \to$ output `1`.  
     $\implies IncomingOutputs(q_0) = \{0, 1\}$.
   - Incoming to $q_1$: from $(q_0, 0) \to$ output `0`; from $(q_1, 0) \to$ output `0`.  
     $\implies IncomingOutputs(q_1) = \{0\}$.
2. **State Splitting:**
   - Split $q_0$ into $q_{0\_0}$ (output `0`) and $q_{0\_1}$ (output `1`).
   - Split $q_1$ into $q_{1\_0}$ (output `0`).
   - Initial state: $q_{0\_0}$ (initial output `0`).
3. **Moore Transition Table:**
   - On input `0`, all $q_0$ states go to $(q_1, 0) = q_{1\_0}$.
   - On input `1`, all $q_0$ states go to $(q_0, 0) = q_{0\_0}$.
   - On input `0`, $q_{1\_0}$ goes to $(q_1, 0) = q_{1\_0}$.
   - On input `1`, $q_{1\_0}$ goes to $(q_0, 1) = q_{0\_1}$.

**Resultant Moore Table:**

| State | Input 0 | Input 1 | State Output |
| :---: | :---: | :---: | :---: |
| $\to q_{0\_0}$ | $q_{1\_0}$ | $q_{0\_0}$ | `0` |
| $q_{0\_1}$ | $q_{1\_0}$ | $q_{0\_0}$ | `1` |
| $q_{1\_0}$ | $q_{1\_0}$ | $q_{0\_1}$ | `0` |

**Validation on String $w = 0101$:**
- **Mealy Trace:**
  - Start $q_0 \xrightarrow{0/0} q_1 \xrightarrow{1/1} q_0 \xrightarrow{0/0} q_1 \xrightarrow{1/1} q_0$
  - Output = `0101`
- **Moore Trace:**
  - Start $q_{0\_0} \xrightarrow{0} q_{1\_0} \xrightarrow{1} q_{0\_1} \xrightarrow{0} q_{1\_0} \xrightarrow{1} q_{0\_1}$
  - Outputs visited: $\lambda'(q_{0\_0}) \lambda'(q_{1\_0}) \lambda'(q_{0\_1}) \lambda'(q_{1\_0}) \lambda'(q_{0\_1})$ = `00101`
- **Verification:**
  - $\text{Moore Output}[1:] = \text{0101} == \text{Mealy Output}$ (**VERIFIED** $\checkmark$)
