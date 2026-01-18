import streamlit as st
import pandas as pd
import re

def generate_tac_logic(expression):
    """
    Parses expression and generates Three-Address Instructions list.
    """
    prec = {'^': 4, '*': 3, '/': 3, '%': 3, '+': 2, '-': 2, '(': 1}
    op_stack = []
    val_stack = []
    instructions = []
    temp_count = 1

    def create_instruction(op, arg1, arg2):
        nonlocal temp_count
        res = f"t{temp_count}"
        temp_count += 1
        instructions.append({"op": op, "arg1": arg1, "arg2": arg2, "result": res})
        return res

    # Tokenize
    tokens = re.findall(r'[a-zA-Z0-9]+|\(|\)|\^|\*|/|%|\+|-', expression)
    
    try:
        for t in tokens:
            if re.match(r'[a-zA-Z0-9]+', t):
                val_stack.append(t)
            elif t == '(':
                op_stack.append(t)
            elif t == ')':
                while op_stack and op_stack[-1] != '(':
                    op = op_stack.pop()
                    arg2 = val_stack.pop()
                    arg1 = val_stack.pop()
                    val_stack.append(create_instruction(op, arg1, arg2))
                if op_stack: op_stack.pop()
            else:
                while op_stack and prec.get(op_stack[-1], 0) >= prec.get(t, 0):
                    op = op_stack.pop()
                    arg2 = val_stack.pop()
                    arg1 = val_stack.pop()
                    val_stack.append(create_instruction(op, arg1, arg2))
                op_stack.append(t)
                
        while op_stack:
            op = op_stack.pop()
            arg2 = val_stack.pop()
            arg1 = val_stack.pop()
            val_stack.append(create_instruction(op, arg1, arg2))
        
        return instructions, None
    except Exception as e:
        return None, f"Invalid Expression Syntax: {str(e)}"

def render_tac():
    st.title("📜 5.3 Three-Address Code (TAC)")
    
    st.markdown(r"""
    **Three-Address Code (TAC)** is an intermediate representation where each instruction has at most three operands. There are three primary ways to implement this in memory:
    """)

    st.divider()

    # --- SECTION A: THEORY ---
    st.header("📘 1. Implementation Methods")
    
    t1, t2, t3 = st.tabs(["Quadruples", "Triples", "Indirect Triples"])
    
    with t1:
        st.subheader("1. Quadruples")
        st.markdown(r"""
        *   **Structure:** `(op, arg1, arg2, Result)`
        *   **How it works:** Explicitly stores the result in a temporary variable (e.g., $t_1, t_2$).
        *   **Benefit:** Easy to move code during optimization because results are named, not position-dependent.
        """)
    
    with t2:
        st.subheader("2. Triples")
        st.markdown(r"""
        *   **Structure:** `(op, arg1, arg2)`
        *   **How it works:** No "Result" field. The result is referred to by the **index** (e.g., `(0)` refers to instruction at line 0).
        *   **Benefit:** Space-efficient; avoids cluttering the symbol table with temporary names.
        """)
        
    with t3:
        st.subheader("3. Indirect Triples")
        st.markdown(r"""
        *   **Structure:** Two tables — **Triple Table** and **Pointer Table**.
        *   **How it works:** Pointer table lists execution order. Reordering code only requires changing the pointer table.
        *   **Benefit:** Best of both worlds — space-efficient and optimization-friendly.
        """)

    st.divider()

    # --- SECTION B: INTERACTIVE SOLVER ---
    st.header("🧪 2. Interactive TAC Solver")
    st.markdown("Enter an expression (e.g., `a + b * c / d`) to generate the corresponding TAC, Quadruples, and Triples.")

    col_in, col_btn = st.columns([3, 1])
    with col_in:
        u_input = st.text_input("Input Expression:", value="a + b * c", key="tac_input_main")
    with col_btn:
        st.write("") # padding
        solve_btn = st.button("🚀 Generate TAC", use_container_width=True)

    if solve_btn:
        instructions, error = generate_tac_logic(u_input)
        
        if error:
            st.error(error)
        elif not instructions:
            st.info("Expression is already minimal.")
        else:
            st.success("✅ Intermediate Code Generated Successfully!")
            
            # --- 1. Three-Address Code ---
            st.subheader("📋 A. Three-Address Code")
            for i, inst in enumerate(instructions):
                st.code(f"{inst['result']} = {inst['arg1']} {inst['op']} {inst['arg2']}")
            
            # --- 2. Quadruples & Triples ---
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("🗓️ B. Quadruples Table")
                quad_data = []
                for inst in instructions:
                    quad_data.append([inst['op'], inst['arg1'], inst['arg2'], inst['result']])
                st.table(pd.DataFrame(quad_data, columns=["op", "arg1", "arg2", "Result"]))
                
            with c2:
                st.subheader("🔗 C. Triples Table")
                trip_data = []
                # Map results to indices for referencing
                res_to_idx = {inst['result']: f"({i})" for i, inst in enumerate(instructions)}
                
                for i, inst in enumerate(instructions):
                    a1 = res_to_idx.get(inst['arg1'], inst['arg1'])
                    a2 = res_to_idx.get(inst['arg2'], inst['arg2'])
                    trip_data.append([i, inst['op'], a1, a2])
                st.table(pd.DataFrame(trip_data, columns=["#", "op", "arg1", "arg2"]))

            st.info("💡 **Insight:** Notice how 'Result' in Quadruples becomes an index reference `(n)` in Triples!")

    st.divider()

    # --- SECTION C: COMPARISON ---
    st.header("📊 3. Comparison Summary")
    summary_data = [
        {"Feature": "Space", "Quadruples": "Uses more space (4 fields)", "Triples": "Most space-efficient", "Indirect Triples": "Slightly more than Triples"},
        {"Feature": "Temporary Names", "Quadruples": "Explicitly used (t1, t2)", "Triples": "Not used (uses indices)", "Indirect Triples": "Not used"},
        {"Feature": "Ease of Moving Code", "Quadruples": "Very Easy", "Triples": "Difficult (refs break)", "Indirect Triples": "Easy (change pointers)"},
        {"Feature": "Symbol Table", "Quadruples": "Larger (stores temps)", "Triples": "Smaller", "Indirect Triples": "Smaller"}
    ]
    st.table(pd.DataFrame(summary_data))

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: Intermediate Code Generation"):
            st.session_state.unit1_topic = "5.2 Intermediate Code Generation"
            st.rerun()
    with nav2:
        if st.button("🎉 Unit 1 Complete!", use_container_width=True):
            st.success("Module I - Unit 1 - Front End of Compiler - Completed!")
            st.balloons()
