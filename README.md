# Mealy <-> Moore Machine Conversion Simulator
**CSET302 - Automata Theory & Computability Project**

A lightweight Python simulator that converts between Mealy and Moore machines while preserving and displaying output behaviour.

---

## Features
- **Bi-directional Conversion**:
  - **Mealy $\to$ Moore**: Computes incoming output sets, performs state splitting $(q, y)$, maps transitions, and designates the Moore initial state.
  - **Moore $\to$ Mealy**: Retains state structure and associates transition outputs with destination state outputs ($\lambda(s, a) = \lambda'(s')$).
- **Dynamic User Input**: Enter custom states, alphabet, transitions, and outputs interactively.
- **Built-in Benchmark Demos**:
  - Demo 1: Mealy $\to$ Moore conversion on a `'01'` sequence detector.
  - Demo 2: Moore $\to$ Mealy conversion on a `'10'` substring detector.
- **Visualizations**: Formatted ASCII transition tables and state traversal logs.
- **Output Preservation Validation**: Simulates input strings side-by-side on both machines to formally verify:
  $$\text{Output}_{Moore} = \lambda'(s_0) + \text{Output}_{Mealy}$$

---

## How to Run

### 1. Run Interactive CLI
```bash
python simulator.py
```

### 2. Run Automated Demo
```bash
python simulator.py --demo
```

### 3. Run Unit Tests
```bash
python -m unittest test_simulator.py
```

---

## Project Structure
- [simulator.py](file:///d:/Bennett/Sem%205/Automata/Project/simulator.py): Core conversion algorithms, transition tables, simulation engine, and interactive CLI.
- [test_simulator.py](file:///d:/Bennett/Sem%205/Automata/Project/test_simulator.py): Automated unit test suite verifying mathematical correctness.
- [M1_Simulator_Design_Report.docx](file:///d:/Bennett/Sem%205/Automata/Project/M1_Simulator_Design_Report.docx): Formal Word Document submission report mapped to the 5-mark M1 evaluation rubric (Problem Analysis, Existing Tools, System Design, Algorithms & Manual Validation).
- [PROJECT_STUDY_GUIDE_AND_VIVA.md](file:///d:/Bennett/Sem%205/Automata/Project/PROJECT_STUDY_GUIDE_AND_VIVA.md): Comprehensive revision and viva study guide covering theory, state-splitting rationale, manually solved example, and top 15 viva Q&As.
- [PROJECT_STUDY_GUIDE_AND_VIVA.docx](file:///d:/Bennett/Sem%205/Automata/Project/PROJECT_STUDY_GUIDE_AND_VIVA.docx): Printable Word version of the study guide.
- [M1_DESIGN_REPORT.md](file:///d:/Bennett/Sem%205/Automata/Project/M1_DESIGN_REPORT.md): Markdown version of the design report.
