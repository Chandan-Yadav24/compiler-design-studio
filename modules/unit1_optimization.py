import streamlit as st
import pandas as pd
import re

def analyze_dead_code(code_str):
    """
    Analyzes code for dead code (unreachable or unused assignments).
    Returns a list of steps and the final optimized code.
    """
    lines = [line.strip() for line in code_str.split('\n') if line.strip()]
    steps = []
    
    # 1. Reachability Analysis
    reachable_lines = []
    is_reachable = True
    for i, line in enumerate(lines):
        if is_reachable:
            reachable_lines.append(line)
        else:
            steps.append(f"**Step {len(steps)+1}:** Remove unreachable line `{line}` (Follows `return` or `exit`)")
        
        # Heuristic for end of block
        if "return" in line or "exit" in line:
            is_reachable = False
            
    # 2. Unused Assignment Analysis (Reverse Scan)
    # We keep track of variables used. If a variable is assigned but never used later, it's dead.
    current_code = list(reachable_lines)
    
    changed = True
    while changed:
        changed = False
        used_vars = set()
        to_remove = []
        
        # Find all used variables (on RHS)
        for line in current_code:
            # Match assignments like x = y + z
            if "=" in line:
                rhs = line.split("=", 1)[1]
                used_vars.update(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', rhs))
            else:
                # Other statements like return x
                used_vars.update(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', line))
        
        # Check assignments from bottom up
        for i in range(len(current_code) - 1, -1, -1):
            line = current_code[i]
            if "=" in line:
                lhs = line.split("=", 1)[0].strip()
                # If the variable is NOT used anywhere else (heuristic)
                # and it's an assignment (LHS is just a variable)
                if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', lhs):
                    if lhs not in used_vars:
                        steps.append(f"**Step {len(steps)+1}:** Remove unused assignment `{line}` (Variable `{lhs}` is never utilized)")
                        to_remove.append(i)
                        changed = True
        
        # Remove identified dead lines
        for idx in sorted(to_remove, reverse=True):
            current_code.pop(idx)
            
    return steps, "\n".join(current_code)

def render_dead_code():
    st.title("✂️ 5.4 Dead Code Elimination")
    
    st.markdown(r"""
    **Dead Code Elimination (DCE)** is an optimization technique that removes code that does not affect the program's results. This makes the program smaller and faster.
    """)

    st.divider()

    # --- SECTION 1: THEORY ---
    st.header("📘 1. What is Dead Code?")
    st.markdown("""
    There are two main types of dead code:
    1.  **Unreachable Code:** Code that can never be executed (e.g., code following a `return` statement).
    2.  **Unused Assignments:** Code that performs a calculation and stores it in a variable, but that variable is never read again.
    """)

    # Visual Comparison
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("❌ Before Optimization")
        st.code("""
int main() {
    int x = 5;
    int y = 10; // DEAD: Never used
    int z = x * 2;
    return z;
    printf("Done"); // DEAD: Unreachable
}
        """, language="cpp")
    with c2:
        st.subheader("✅ After Optimization")
        st.code("""
int main() {
    int x = 5;
    int z = x * 2;
    return z;
}
        """, language="cpp")

    st.divider()

    # --- SECTION 2: VISUALIZATION ---
    st.header("🖼️ 2. Control Flow Visualization")
    st.markdown("Optimization simplifies the program's flow graph by pruning dead branches.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Original Flow**")
        st.graphviz_chart('''
        digraph {
            rankdir=TB;
            node [shape=box, style=filled, fillcolor="white", fontcolor="black"];
            Start -> Assign_X -> Assign_Y -> Return_X -> Dead_Print;
            Dead_Print [label="Print (REMOVED)", fillcolor="#ffe6e6", style=dashed];
            Assign_Y [label="y = 10 (REMOVED)", fillcolor="#ffe6e6", style=dashed];
        }
        ''')
    with col2:
        st.markdown("**Optimized Flow**")
        st.graphviz_chart('''
        digraph {
            rankdir=TB;
            node [shape=box, style=filled, fillcolor="#e6ffed", fontcolor="black"];
            Start -> Assign_X -> Return_X -> End;
        }
        ''')

    st.divider()

    # --- SECTION 3: INTERACTIVE LAB ---
    st.header("🧪 3. Interactive Step-by-Step Lab")
    st.markdown("Enter a simple TAC-like code snippet to see how the compiler removes dead lines.")

    default_code = "x = 5\ny = 10\nz = x + 1\nreturn z\nw = 20"
    u_code = st.text_area("Input Code (one statement per line):", value=default_code, height=150)

    if st.button("🚀 Optimize Code"):
        steps, optimized = analyze_dead_code(u_code)
        
        if not steps:
            st.info("No dead code found! The code is already optimal.")
            st.code(u_code)
        else:
            st.success("✨ Optimization Complete!")
            
            st.subheader("🚶‍♂️ Optimization Walkthrough")
            for step in steps:
                st.write(step)
            
            st.subheader("🎯 Final Optimized Code")
            st.code(optimized)

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: Three-Address Code"):
            st.session_state.unit1_topic = "5.3 Three-Address Code (TAC)"
            st.rerun()
    with nav2:
        if st.button("🎉 Unit 1 Complete!", use_container_width=True):
            st.success("Module I - Unit 1 - Front End of Compiler - Completed!")
            st.balloons()
