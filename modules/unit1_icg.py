import streamlit as st
import pandas as pd
import re

def generate_postfix_steps(expression):
    """
    Generates a textual step-by-step walkthrough of infix to postfix conversion.
    Uses a precedence-based replacement strategy.
    """
    prec = {'^': 4, '*': 3, '/': 3, '%': 3, '+': 2, '-': 2}
    
    # Clean expression
    expr = expression.replace(" ", "")
    steps = []
    
    # Helper to find inner-most parenthesis
    def get_inner_paren(s):
        start = -1
        for i, char in enumerate(s):
            if char == '(':
                start = i
            elif char == ')':
                if start != -1:
                    return start, i
        return -1, -1

    current = expr
    step_count = 1

    # 1. Handle Parentheses first
    while True:
        s, e = get_inner_paren(current)
        if s == -1: break
        
        inner = current[s+1:e]
        inner_postfix = infix_to_postfix_simple(inner)
        new_expr = current[:s] + f"[{inner_postfix}]" + current[e+1:]
        steps.append(f"**Step {step_count}:** Resolve parenthesis `({inner})` ➜ `{inner_postfix}`")
        current = new_expr
        step_count += 1

    # 2. Handle operators by precedence
    def walk_logic(e_str, count):
        tokens = re.findall(r"\[.*?\]|[a-zA-Z0-9]+|\^|\*|/|%|\+|-", e_str)
        groups = [['^'], ['*', '/', '%'], ['+', '-']]
        temp_expr = list(tokens)
        
        for group in groups:
            i = 0
            while i < len(temp_expr):
                if temp_expr[i] in group:
                    op = temp_expr[i]
                    left = temp_expr[i-1]
                    right = temp_expr[i+1]
                    l_disp = left.replace("[", "").replace("]", "")
                    r_disp = right.replace("[", "").replace("]", "")
                    new_val = f"{l_disp} {r_disp} {op}"
                    steps.append(f"**Step {count}:** Convert `{l_disp} {op} {r_disp}` ➜ `{new_val}`")
                    count += 1
                    temp_expr[i-1:i+2] = [f"[{new_val}]"]
                    i -= 1
                i += 1
        return count

    walk_logic(current, step_count)
    final = steps[-1].split("➜")[-1].strip().replace("`", "") if steps else expression
    return steps, final

def infix_to_postfix_simple(expression):
    prec = {'^': 4, '*': 3, '/': 3, '%': 3, '+': 2, '-': 2, '(': 1}
    op_stack = []
    postfix = []
    tokens = re.findall(r'[a-zA-Z0-9]+|\(|\)|\^|\*|/|%|\+|-', expression)
    for t in tokens:
        if re.match(r'[a-zA-Z0-9]+', t): postfix.append(t)
        elif t == '(': op_stack.append(t)
        elif t == ')':
            while op_stack and op_stack[-1] != '(': postfix.append(op_stack.pop())
            if op_stack: op_stack.pop()
        else:
            while op_stack and prec.get(op_stack[-1], 0) >= prec.get(t, 0): postfix.append(op_stack.pop())
            op_stack.append(t)
    while op_stack: postfix.append(op_stack.pop())
    return " ".join(postfix)

def render_icg():
    st.title("⚙️ 5.2 Intermediate Code Generation")
    
    st.markdown(r"""
    **Intermediate Code (IC)** is an machine-independent representation that serves as a bridge within the compiler.
    """)

    # --- SECTION 1: INTRODUCTION ---
    st.header("📘 1. Intermediate Code (IC)")
    st.markdown(r"""
    *   **Generation:** Created during parsing or semantic analysis.
    *   **Property:** Simple, machine-independent, and optimization-friendly.
    
    **Common Forms:**
    1.  **Postfix Notation**
    2.  **Syntax Trees**
    3.  **Three-Address Code (TAC)**
    """)

    st.divider()

    # --- SECTION 2: POSTFIX NOTATION ---
    st.header("🧮 2. Postfix Notation")
    st.markdown(r"""
    In **Postfix notation**, the operator follows its operands (Reverse Polish Notation).
    
    **The e₁ e₂ θ Rule:**
    Applying operator $\theta$ to expressions $e_1$ and $e_2$:
    """)
    st.latex(r"e_1 \ e_2 \ \theta")

    st.subheader("⚖️ Operator Precedence")
    precedence_data = [
        {"Priority": "1", "Operator": "( )", "Description": "Parentheses", "Associativity": "Highest"},
        {"Priority": "2", "Operator": "^", "Description": "Exponentiation", "Associativity": "R to L"},
        {"Priority": "3", "Operator": "*, /, %", "Description": "Mult, Div, Mod", "Associativity": "L to R"},
        {"Priority": "4", "Operator": "+, -", "Description": "Add, Sub", "Associativity": "L to R"}
    ]
    st.table(pd.DataFrame(precedence_data))

    st.divider()

    # --- INTERACTIVE LAB ---
    st.header("🧪 3. Interactive Postfix Lab")
    st.markdown("Enter an Infix expression to see the **Expression Form** step-by-step logic.")

    u_infix = st.text_input("Enter Infix Expression:", value="2*y-(a+4*c)+y", key="postfix_icg_lab_v3")
    
    if u_infix:
        try:
            steps, final_res = generate_postfix_steps(u_infix)
            st.success(f"🎯 **Final Postfix Result:** `{final_res}`")
            st.subheader("🚶‍♂️ Step-by-Step Conversion")
            for step in steps:
                st.write(step)
            if not steps:
                st.info("The expression is already in its simplest form.")
        except Exception as e:
            st.error(f"Error in processing logic: {str(e)}")

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: Semantic Analysis"):
            st.session_state.unit1_topic = "5.1 Semantic Analysis (SDT & SDD)"
            st.rerun()
    with nav2:
        if st.button("Next: Three-Address Code (TAC) ➡️", use_container_width=True):
            st.session_state.unit1_topic = "5.3 Three-Address Code (TAC)"
            st.rerun()
