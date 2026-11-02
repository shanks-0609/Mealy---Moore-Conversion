"""
Mealy <-> Moore Machine Conversion and Simulation System
Automata Theory & Computability (CSET302) Project Simulator

Converts between Mealy and Moore machines while preserving and verifying output behaviour.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Set, Optional


@dataclass
class MealyMachine:
    states: List[str]
    inputs: List[str]
    outputs: List[str]
    initial_state: str
    transitions: Dict[Tuple[str, str], str]  # (state, input) -> next_state
    output_table: Dict[Tuple[str, str], str]  # (state, input) -> output_symbol

    def simulate(self, input_string: str) -> Tuple[List[str], str, List[Tuple[str, str, str, str]]]:
        """
        Simulate Mealy machine on input string.
        Returns:
            - state_sequence: list of states traversed [q0, q1, ...]
            - output_string: concatenation of outputs produced
            - trace: list of (current_state, input_sym, next_state, output_sym)
        """
        curr = self.initial_state
        state_seq = [curr]
        out_symbols = []
        trace = []

        for ch in input_string:
            if (curr, ch) not in self.transitions:
                raise ValueError(f"Transition undefined for state '{curr}' on input '{ch}'")
            next_st = self.transitions[(curr, ch)]
            out_sym = self.output_table[(curr, ch)]
            trace.append((curr, ch, next_st, out_sym))
            out_symbols.append(out_sym)
            curr = next_st
            state_seq.append(curr)

        return state_seq, "".join(out_symbols), trace

    def print_table(self):
        """Prints Mealy transition and output table in clean ASCII format."""
        header_line = f"+{'-'*14}+" + "+".join(f"{'-'*18}" for _ in self.inputs) + "+"
        col_headers = " | ".join(f"{'Input: ' + sym:^16}" for sym in self.inputs)
        print(header_line)
        print(f"| {'State':^12} | {col_headers} |")
        sub_headers = " | ".join(f"{'Next St / Out':^16}" for _ in self.inputs)
        print(f"| {'':^12} | {sub_headers} |")
        print(header_line)

        for q in self.states:
            prefix = "-> " if q == self.initial_state else "   "
            row_items = []
            for a in self.inputs:
                nxt = self.transitions.get((q, a), "-")
                out = self.output_table.get((q, a), "-")
                entry = f"{nxt} / {out}" if nxt != "-" else "-"
                row_items.append(f"{entry:^16}")
            print(f"| {prefix + q:<12} | " + " | ".join(row_items) + " |")
        print(header_line)


@dataclass
class MooreMachine:
    states: List[str]
    inputs: List[str]
    outputs: List[str]
    initial_state: str
    transitions: Dict[Tuple[str, str], str]  # (state, input) -> next_state
    state_outputs: Dict[str, str]            # state -> output_symbol

    def simulate(self, input_string: str) -> Tuple[List[str], str, List[Tuple[str, str, str, str]]]:
        """
        Simulate Moore machine on input string.
        Returns:
            - state_sequence: list of states traversed [s0, s1, ...]
            - output_string: concatenation of outputs (including initial state output)
            - trace: list of (current_state, input_sym, next_state, next_state_output)
        """
        curr = self.initial_state
        state_seq = [curr]
        out_symbols = [self.state_outputs[curr]]
        trace = []

        for ch in input_string:
            if (curr, ch) not in self.transitions:
                raise ValueError(f"Transition undefined for state '{curr}' on input '{ch}'")
            next_st = self.transitions[(curr, ch)]
            nxt_out = self.state_outputs[next_st]
            trace.append((curr, ch, next_st, nxt_out))
            out_symbols.append(nxt_out)
            curr = next_st
            state_seq.append(curr)

        return state_seq, "".join(out_symbols), trace

    def print_table(self):
        """Prints Moore transition and state output table."""
        header_line = f"+{'-'*14}+" + "+".join(f"{'-'*14}" for _ in self.inputs) + f"+{'-'*14}+"
        col_headers = " | ".join(f"{'Input ' + sym:^12}" for sym in self.inputs)
        print(header_line)
        print(f"| {'State':^12} | {col_headers} | {'Output':^12} |")
        print(header_line)

        for s in self.states:
            prefix = "-> " if s == self.initial_state else "   "
            row_items = []
            for a in self.inputs:
                nxt = self.transitions.get((s, a), "-")
                row_items.append(f"{nxt:^12}")
            out = self.state_outputs.get(s, "-")
            print(f"| {prefix + s:<12} | " + " | ".join(row_items) + f" | {out:^12} |")
        print(header_line)


# ==============================================================================
# CONVERSION ALGORITHMS
# ==============================================================================

def mealy_to_moore(mealy: MealyMachine, default_initial_output: Optional[str] = None) -> Tuple[MooreMachine, List[str]]:
    """
    Converts a Mealy machine to an equivalent Moore machine.
    
    Algorithm:
      1. For each Mealy state q, identify all output symbols associated with incoming transitions.
      2. If incoming outputs for state q are {y1, y2, ...}, split q into states (q, y1), (q, y2)...
      3. For the start state q0:
         - If q0 has incoming transitions, assign Moore initial state according to default_initial_output
           or incoming output; if multiple incoming outputs exist, initial state is (q0, default_initial_output).
         - If q0 has no incoming transitions, Moore state is (q0, default_initial_output).
      4. For each Moore state (q, y), on input 'a':
         - Next Mealy state is nxt = delta(q, a), with output o = lambda(q, a).
         - Next Moore state is (nxt, o).
      5. State output of (q, y) is y.
    """
    steps_log = []
    steps_log.append("Step 1: Identifying distinct incoming outputs for each Mealy state...")

    # Map each state to the set of outputs associated with incoming transitions
    incoming_outputs: Dict[str, Set[str]] = {q: set() for q in mealy.states}
    for (src, inp), dst in mealy.transitions.items():
        out = mealy.output_table[(src, inp)]
        incoming_outputs[dst].add(out)

    for q, outs in incoming_outputs.items():
        steps_log.append(f"  - State '{q}' incoming outputs: {sorted(list(outs)) if outs else 'None (unentered)'}")

    # Determine default initial output for q0
    if default_initial_output is None:
        if incoming_outputs[mealy.initial_state]:
            default_initial_output = sorted(list(incoming_outputs[mealy.initial_state]))[0]
        else:
            default_initial_output = mealy.outputs[0] if mealy.outputs else "0"

    steps_log.append(f"Step 2: Assigning initial output for start state '{mealy.initial_state}' -> '{default_initial_output}'")

    # Generate Moore states
    steps_log.append("Step 3: State splitting based on incoming outputs...")
    moore_states_map: Dict[Tuple[str, str], str] = {}  # (mealy_state, output) -> moore_state_name
    moore_state_outputs: Dict[str, str] = {}

    for q in mealy.states:
        outs = incoming_outputs[q].copy()
        if q == mealy.initial_state:
            outs.add(default_initial_output)
        
        # If state has no incoming transitions and isn't initial state
        if not outs:
            outs.add(mealy.outputs[0] if mealy.outputs else "0")

        for o in sorted(list(outs)):
            state_name = f"{q}_{o}"
            moore_states_map[(q, o)] = state_name
            moore_state_outputs[state_name] = o
            steps_log.append(f"  - Created Moore state '{state_name}' with state output '{o}'")

    moore_initial = moore_states_map[(mealy.initial_state, default_initial_output)]
    steps_log.append(f"  -> Moore Initial State designated as: '{moore_initial}'")

    # Build transitions
    steps_log.append("Step 4: Mapping transitions: delta_Moore((q, y), a) = (delta_Mealy(q, a), lambda_Mealy(q, a))")
    moore_transitions: Dict[Tuple[str, str], str] = {}

    for (q, o), s_name in moore_states_map.items():
        for a in mealy.inputs:
            if (q, a) in mealy.transitions:
                nxt_mealy = mealy.transitions[(q, a)]
                nxt_out = mealy.output_table[(q, a)]
                nxt_moore = moore_states_map[(nxt_mealy, nxt_out)]
                moore_transitions[(s_name, a)] = nxt_moore

    moore_all_states = list(moore_state_outputs.keys())
    moore_machine = MooreMachine(
        states=moore_all_states,
        inputs=mealy.inputs.copy(),
        outputs=mealy.outputs.copy(),
        initial_state=moore_initial,
        transitions=moore_transitions,
        state_outputs=moore_state_outputs
    )

    return moore_machine, steps_log


def moore_to_mealy(moore: MooreMachine) -> Tuple[MealyMachine, List[str]]:
    """
    Converts a Moore machine to an equivalent Mealy machine.
    
    Algorithm:
      1. Mealy states Q = Moore states S.
      2. Initial state q0 = s0.
      3. For each state s in S and input symbol 'a':
         - Next state delta_Mealy(s, a) = delta_Moore(s, a) = s'.
         - Transition output lambda_Mealy(s, a) = lambda_Moore(s') (the output of the destination state).
    """
    steps_log = []
    steps_log.append("Step 1: Retaining original states and initial state...")
    steps_log.append(f"  - States: {moore.states}")
    steps_log.append(f"  - Initial State: {moore.initial_state}")

    mealy_transitions: Dict[Tuple[str, str], str] = {}
    mealy_outputs: Dict[Tuple[str, str], str] = {}

    steps_log.append("Step 2: Associating transition output with the destination state's Moore output...")
    for s in moore.states:
        for a in moore.inputs:
            if (s, a) in moore.transitions:
                nxt_st = moore.transitions[(s, a)]
                nxt_out = moore.state_outputs[nxt_st]
                mealy_transitions[(s, a)] = nxt_st
                mealy_outputs[(s, a)] = nxt_out
                steps_log.append(f"  - Transition ({s}, '{a}') -> Next State: '{nxt_st}', Output: '{nxt_out}'")

    mealy_machine = MealyMachine(
        states=moore.states.copy(),
        inputs=moore.inputs.copy(),
        outputs=moore.outputs.copy(),
        initial_state=moore.initial_state,
        transitions=mealy_transitions,
        output_table=mealy_outputs
    )

    return mealy_machine, steps_log


# ==============================================================================
# VALIDATION & VERIFICATION
# ==============================================================================

def verify_equivalence(mealy: MealyMachine, moore: MooreMachine, test_strings: List[str]):
    """
    Executes test strings on both machines and validates output behaviour preservation.
    Formal criterion:
      Output_Moore(w) = lambda_Moore(s0) + Output_Mealy(w)
      Length(Output_Moore) = Length(w) + 1
      Length(Output_Mealy) = Length(w)
    """
    print("\n" + "="*70)
    print("OUTPUT BEHAVIOUR PRESERVATION & VALIDATION")
    print("="*70)
    print("Theoretical Condition: Moore Output = (Initial State Output) + Mealy Output\n")

    all_passed = True

    for w in test_strings:
        print(f"--- Testing String: '{w}' (length = {len(w)}) ---")
        try:
            m_seq, m_out, m_trace = mealy.simulate(w)
            mo_seq, mo_out, mo_trace = moore.simulate(w)

            print(f"  Mealy Simulation:")
            print(f"    States Traversed : {' -> '.join(m_seq)}")
            print(f"    Mealy Output     : '{m_out}' (Length: {len(m_out)})")

            print(f"  Moore Simulation:")
            print(f"    States Traversed : {' -> '.join(mo_seq)}")
            print(f"    Moore Output     : '{mo_out}' (Length: {len(mo_out)})")
            print(f"    Initial Output   : '{mo_out[0]}', Subsequent: '{mo_out[1:]}'")

            # Verification check
            is_valid = (mo_out[1:] == m_out)
            status = "PASS" if is_valid else "FAIL"
            if not is_valid:
                all_passed = False

            print(f"  Validation Result: [{status}] (mo_out[1:] == m_out: '{mo_out[1:]}' == '{m_out}')\n")

        except Exception as e:
            print(f"  Error during simulation: {e}\n")
            all_passed = False

    return all_passed


# ==============================================================================
# PRESET BENCHMARK MACHINES (FOR INSTANT DEMO & EVALUATION)
# ==============================================================================

def get_preset_mealy_1s_complement() -> MealyMachine:
    """Mealy machine computing 1's complement of a binary string."""
    return MealyMachine(
        states=["q0"],
        inputs=["0", "1"],
        outputs=["0", "1"],
        initial_state="q0",
        transitions={
            ("q0", "0"): "q0",
            ("q0", "1"): "q0"
        },
        output_table={
            ("q0", "0"): "1",
            ("q0", "1"): "0"
        }
    )


def get_preset_mealy_sequence_detector() -> MealyMachine:
    """Mealy machine detecting sequence '01' (outputs 1 on completion)."""
    return MealyMachine(
        states=["q0", "q1"],
        inputs=["0", "1"],
        outputs=["0", "1"],
        initial_state="q0",
        transitions={
            ("q0", "0"): "q1",
            ("q0", "1"): "q0",
            ("q1", "0"): "q1",
            ("q1", "1"): "q0"
        },
        output_table={
            ("q0", "0"): "0",
            ("q0", "1"): "0",
            ("q1", "0"): "0",
            ("q1", "1"): "1"  # '01' detected
        }
    )


def get_preset_moore_sequence_detector() -> MooreMachine:
    """Moore machine detecting substring '10' (outputs 'Y' when in detect state)."""
    return MooreMachine(
        states=["q0", "q1", "q2"],
        inputs=["0", "1"],
        outputs=["N", "Y"],
        initial_state="q0",
        transitions={
            ("q0", "0"): "q0",
            ("q0", "1"): "q1",
            ("q1", "0"): "q2",
            ("q1", "1"): "q1",
            ("q2", "0"): "q0",
            ("q2", "1"): "q1"
        },
        state_outputs={
            "q0": "N",
            "q1": "N",
            "q2": "Y"
        }
    )


# ==============================================================================
# DYNAMIC USER INPUT PARSER
# ==============================================================================

def input_custom_mealy() -> MealyMachine:
    print("\n--- Enter Mealy Machine Specification ---")
    states = input("Enter states separated by spaces (e.g. q0 q1): ").strip().split()
    inputs = input("Enter input alphabet symbols separated by spaces (e.g. 0 1): ").strip().split()
    outputs = input("Enter output alphabet symbols separated by spaces (e.g. 0 1): ").strip().split()
    initial = input(f"Enter initial state [{states[0]}]: ").strip() or states[0]

    transitions = {}
    output_table = {}

    print("\nDefine transitions and outputs for each (State, Input):")
    for q in states:
        for a in inputs:
            nxt = input(f"  Next state for ({q}, '{a}'): ").strip()
            out = input(f"  Output for ({q}, '{a}'): ").strip()
            transitions[(q, a)] = nxt
            output_table[(q, a)] = out

    return MealyMachine(states, inputs, outputs, initial, transitions, output_table)


def input_custom_moore() -> MooreMachine:
    print("\n--- Enter Moore Machine Specification ---")
    states = input("Enter states separated by spaces (e.g. q0 q1 q2): ").strip().split()
    inputs = input("Enter input alphabet symbols separated by spaces (e.g. 0 1): ").strip().split()
    outputs = input("Enter output alphabet symbols separated by spaces (e.g. N Y): ").strip().split()
    initial = input(f"Enter initial state [{states[0]}]: ").strip() or states[0]

    state_outputs = {}
    print("\nDefine state outputs:")
    for s in states:
        out = input(f"  Output for state '{s}': ").strip()
        state_outputs[s] = out

    transitions = {}
    print("\nDefine transitions for each (State, Input):")
    for s in states:
        for a in inputs:
            nxt = input(f"  Next state for ({s}, '{a}'): ").strip()
            transitions[(s, a)] = nxt

    return MooreMachine(states, inputs, outputs, initial, transitions, state_outputs)


# ==============================================================================
# MAIN INTERACTIVE CLI
# ==============================================================================

def run_mealy_to_moore_pipeline(mealy: MealyMachine, test_strings: Optional[List[str]] = None):
    print("\n" + "="*70)
    print("1. ORIGINAL MEALY MACHINE")
    print("="*70)
    mealy.print_table()

    print("\n" + "="*70)
    print("2. STEP-BY-STEP CONVERSION (MEALY -> MOORE)")
    print("="*70)
    moore, steps = mealy_to_moore(mealy)
    for s in steps:
        print(s)

    print("\n" + "="*70)
    print("3. RESULTANT MOORE MACHINE")
    print("="*70)
    moore.print_table()

    if test_strings is None:
        raw_tests = input("\nEnter test input strings separated by space (or press Enter for defaults '0', '01', '101'): ").strip()
        test_strings = raw_tests.split() if raw_tests else ["0", "01", "101", "0110"]

    verify_equivalence(mealy, moore, test_strings)


def run_moore_to_mealy_pipeline(moore: MooreMachine, test_strings: Optional[List[str]] = None):
    print("\n" + "="*70)
    print("1. ORIGINAL MOORE MACHINE")
    print("="*70)
    moore.print_table()

    print("\n" + "="*70)
    print("2. STEP-BY-STEP CONVERSION (MOORE -> MEALY)")
    print("="*70)
    mealy, steps = moore_to_mealy(moore)
    for s in steps:
        print(s)

    print("\n" + "="*70)
    print("3. RESULTANT MEALY MACHINE")
    print("="*70)
    mealy.print_table()

    if test_strings is None:
        raw_tests = input("\nEnter test input strings separated by space (or press Enter for defaults '0', '10', '1010'): ").strip()
        test_strings = raw_tests.split() if raw_tests else ["0", "10", "1010", "1100"]

    verify_equivalence(mealy, moore, test_strings)


def main():
    import sys

    # Quick demo / automated test flag
    if "--demo" in sys.argv:
        print("Running Automated Benchmark Demo...\n")
        print(">>> DEMO 1: Mealy to Moore (Sequence Detector '01') <<<")
        mealy_demo = get_preset_mealy_sequence_detector()
        run_mealy_to_moore_pipeline(mealy_demo, ["0", "01", "001", "0101"])

        print("\n" + "#"*70 + "\n")
        print(">>> DEMO 2: Moore to Mealy (Substring '10' Detector) <<<")
        moore_demo = get_preset_moore_sequence_detector()
        run_moore_to_mealy_pipeline(moore_demo, ["0", "10", "1010", "1100"])
        return

    while True:
        print("\n" + "="*60)
        print("    MEALY <-> MOORE CONVERSION & SIMULATOR (M1)")
        print("="*60)
        print("1. Demo Mealy -> Moore (Sequence '01' Detector)")
        print("2. Demo Moore -> Mealy (Substring '10' Detector)")
        print("3. Dynamic Input: Enter Custom Mealy Machine -> Convert to Moore")
        print("4. Dynamic Input: Enter Custom Moore Machine -> Convert to Mealy")
        print("5. Exit")
        choice = input("\nSelect an option [1-5]: ").strip()

        if choice == "1":
            mealy = get_preset_mealy_sequence_detector()
            run_mealy_to_moore_pipeline(mealy)
        elif choice == "2":
            moore = get_preset_moore_sequence_detector()
            run_moore_to_mealy_pipeline(moore)
        elif choice == "3":
            mealy = input_custom_mealy()
            run_mealy_to_moore_pipeline(mealy)
        elif choice == "4":
            moore = input_custom_moore()
            run_moore_to_mealy_pipeline(moore)
        elif choice == "5":
            print("Exiting simulator. Good luck with your M1 evaluation!")
            break
        else:
            print("Invalid option. Please choose between 1 and 5.")


if __name__ == "__main__":
    main()
