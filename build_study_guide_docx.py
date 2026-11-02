import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_study_guide_docx():
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    COLOR_PRIMARY = RGBColor(27, 54, 93)     # Navy
    COLOR_SECONDARY = RGBColor(70, 95, 130)  # Blue
    COLOR_TEXT = RGBColor(40, 40, 40)

    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = COLOR_TEXT
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(4)

    # Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("BENNETT UNIVERSITY\nCSET302: AUTOMATA THEORY & COMPUTABILITY\n")
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = COLOR_SECONDARY

    r2 = p.add_run("PROJECT STUDY & VIVA PREPARATION GUIDE\n")
    r2.font.size = Pt(18)
    r2.bold = True
    r2.font.color.rgb = COLOR_PRIMARY

    r3 = p.add_run("Mealy <-> Moore Machine Conversion Simulator | Milestone 1 (5 Marks)\n")
    r3.font.size = Pt(12)
    r3.italic = True
    r3.bold = True

    def h1(txt):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(txt)
        r.font.size = Pt(14)
        r.bold = True
        r.font.color.rgb = COLOR_PRIMARY
        return p

    def h2(txt):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(txt)
        r.font.size = Pt(12)
        r.bold = True
        r.font.color.rgb = COLOR_SECONDARY
        return p

    def code_box(txt):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl.rows[0].cells[0]
        set_cell_background(c, "F4F6F9")
        set_cell_margins(c, 80, 80, 120, 120)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(12)
        r = p.add_run(txt)
        r.font.name = 'Consolas'
        r.font.size = Pt(9.5)
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    h1("1. Project Elevator Pitch (What to Say at the Start)")
    p = doc.add_paragraph()
    r = p.add_run(
        "\"Good morning/afternoon. Our project is a Mealy <-> Moore Machine Conversion Simulator designed for CSET302. "
        "In automata theory, Mealy machines associate outputs with state transitions, while Moore machines associate outputs "
        "strictly with states. While both models have equivalent computational power, converting between them requires handling "
        "state splitting and the 1-symbol output timing difference (k vs k+1 outputs). Our simulator automates bi-directional conversion, "
        "provides an audit log of why states split, visualizes formatted ASCII transition tables, and formally verifies that "
        "Output_Moore[1:] == Output_Mealy across all test strings. It is implemented in pure Python with zero external dependencies and "
        "fully verified with unit tests.\""
    )
    r.italic = True

    h1("2. Evaluation Rubric & Marks Breakdown (5 Marks)")
    tbl = doc.add_table(rows=5, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(["Criterion", "Marks", "Key Focus to Present"]):
        c = tbl.rows[0].cells[i]
        set_cell_background(c, "1B365D")
        set_cell_margins(c, 80, 80, 90, 90)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    rdata = [
        ("Problem Definition & Automata Specification", "1", "Formal 6-tuples (Q, Σ, Δ, δ, λ, q0 vs S, Σ, Δ, δ', λ', s0), output timing difference (|w| vs |w|+1), and Output_Moore[1:] == Output_Mealy."),
        ("Existing Tools & Feasibility", "1", "JFLAP (heavy Java, lacks step logs), Automata-lib (acceptors only), Web tools (black-box). Our simulator is pure Python, pedagogical, <1ms runtime."),
        ("Simulator Design & Methodology", "2", "5 modules (Models, Engine, Visualizer, Harness, CLI), IPO workflow diagram, CLI wireframe, and dataclass transition structures."),
        ("Algorithm Selection & Correctness", "1", "State splitting logic based on incoming outputs, pseudocode, and manually solved '01' sequence detector step-by-step example on string '0101'.")
    ]
    for row_idx, d in enumerate(rdata, start=1):
        row = tbl.rows[row_idx]
        for col_idx, val in enumerate(d):
            c = row.cells[col_idx]
            set_cell_background(c, "FFFFFF" if row_idx % 2 != 0 else "F7FAFC")
            set_cell_margins(c, 60, 60, 80, 80)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if col_idx == 1:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    h1("3. Core Concepts & Mathematical Formalisms")
    h2("Mealy vs Moore Summary")
    doc.add_paragraph("• Mealy Machine: Output λ(q, a) depends on BOTH current state and current input. Output string length = |w|.")
    doc.add_paragraph("• Moore Machine: Output λ'(s) depends ONLY on current state. Output string length = |w| + 1 (emits initial state output before reading any input).")
    doc.add_paragraph("• Equivalence Condition: Output_Moore(w) = λ'(s0) ∘ Output_Mealy(w). Thus, Moore output sliced from index 1 equals Mealy output.")

    h2("State Splitting in Mealy -> Moore")
    doc.add_paragraph(
        "Why do states split? If incoming transitions to a Mealy state q produce different outputs (e.g. '0' and '1'), "
        "a single Moore state cannot satisfy both because a Moore state can have only one output. "
        "Hence, q splits into (q, 0) and (q, 1). Maximum Moore states possible = |Q| * |Δ|."
    )

    h2("Moore -> Mealy Conversion")
    doc.add_paragraph(
        "Does not increase state count. Mealy states Q = Moore states S. Each transition entering state s' simply inherits "
        "that state's output: λ(s, a) = λ'(s')."
    )

    h1("4. The Manually Solved '01' Sequence Detector Example")
    doc.add_paragraph("• Problem: Binary sequence detector detecting '01' pattern.")
    doc.add_paragraph("• Mealy States: q0 (start/no '0' seen), q1 (saw '0').")
    doc.add_paragraph("• Transitions: (q0, 0)->q1/0, (q0, 1)->q0/0, (q1, 0)->q1/0, (q1, 1)->q0/1 (Detected!).")
    doc.add_paragraph("• Incoming Outputs: q0 has {0, 1} -> splits into q0_0 and q0_1. q1 has {0} -> becomes q1_0.")
    doc.add_paragraph("• Validation String w = '0101':")
    code_box(
        "Input w:           '0'      '1'      '0'      '1'\n"
        "Mealy States:  q0 -----> q1 -----> q0 -----> q1 -----> q0\n"
        "Mealy Output:        '0'      '1'      '0'      '1'       => Output = '0101'\n"
        "\n"
        "Moore States:  q0_0 ---> q1_0 ---> q0_1 ---> q1_0 ---> q0_1\n"
        "Moore Output:   '0'      '0'      '1'      '0'      '1'   => Output = '00101'\n"
        "\n"
        "Verification: Moore[1:] = '0101' == Mealy ('0101')  [VERIFIED PASS]"
    )

    h1("5. Top 15 Viva Questions & Fast Answers")
    qa_list = [
        ("Q1: Why is Moore output length k+1 while Mealy is k?", 
         "A: A Moore machine outputs a symbol for its initial state before consuming any input symbol. Mealy produces an output only when traversing a transition upon reading an input."),
        ("Q2: What is the formal equivalence condition?", 
         "A: Output_Moore(w) = λ'(s0) ∘ Output_Mealy(w), or programmatically Output_Moore[1:] == Output_Mealy."),
        ("Q3: Why do states split in Mealy to Moore?", 
         "A: Because a single Mealy state may be reached with different outputs on different transitions, but a Moore state can only emit one fixed output."),
        ("Q4: What is the max states in Moore after conversion?", 
         "A: |Q| * |Δ|, where |Q| is the number of Mealy states and |Δ| is output alphabet size."),
        ("Q5: Can states split during Moore to Mealy?", 
         "A: No, state count never increases because each transition simply takes the output of its destination state."),
        ("Q6: Why are Moore machines preferred in some digital circuits?", 
         "A: Moore outputs are registered (clock-synchronized) and immune to glitches on the input lines."),
        ("Q7: What if the start state has no incoming transitions in Mealy?", 
         "A: We designate an initial output (e.g. first symbol of Δ or user choice) to form (q0, y_init)."),
        ("Q8: How does your code verify correctness?", 
         "A: Function verify_equivalence() simulates test strings on both machines and asserts that Moore[1:] == Mealy."),
        ("Q9: What libraries are required to run your simulator?", 
         "A: Zero external libraries; it uses pure Python 3 standard library (dataclasses, typing)."),
        ("Q10: What are your M2 milestone plans?", 
         "A: Interactive GUI visualizer with animated state traversal, Hopcroft state minimization, and export to Graphviz/LaTeX.")
    ]
    for q, a in qa_list:
        p = doc.add_paragraph()
        r_q = p.add_run(q + "\n")
        r_q.bold = True
        r_q.font.color.rgb = COLOR_PRIMARY
        r_a = p.add_run(a)
        r_a.font.size = Pt(10)

    h1("6. Evaluation Demo Commands Cheat Sheet")
    code_box(
        "# 1. Run Unit Tests (takes 0.000s, shows 4 passing tests):\n"
        "python -m unittest test_simulator.py\n\n"
        "# 2. Run Automated Benchmark Demo (displays Mealy, state splitting, Moore, and string validation):\n"
        "python simulator.py --demo\n\n"
        "# 3. Run Interactive CLI (allows entering custom machines):\n"
        "python simulator.py"
    )

    output_filename = "PROJECT_STUDY_GUIDE_AND_VIVA.docx"
    doc.save(output_filename)
    print(f"Study guide docx generated: {output_filename}")

if __name__ == "__main__":
    create_study_guide_docx()
