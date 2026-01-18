import streamlit as st

def render_left_recursion():
    st.title("🚫 4.1 Left Recursion (Elimination)")
    
    st.markdown("""
    ### 🧬 Definition
    **Left recursion** occurs when a non-terminal symbol directly (or indirectly) calls itself on the leftmost side of its own production rule.
    """)

    st.info(r"""
    **General Form:** $A \to A \alpha \mid \beta$
    - **$A$**: The Non-terminal.
    - **$\alpha$**: Any sequence of grammar symbols (terminals or non-terminals).
    - **$\beta$**: A sequence that **does not start with $A$**.
    """)

    st.divider()

    st.header("🛠️ The Rule for Elimination")
    st.markdown(r"""
    To prevent infinite loops in Top-Down parsing, the left-recursive production $A \to A \alpha \mid \beta$ is replaced with two new rules using a new non-terminal $A'$:
    """)

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("**Original Rule**")
        st.latex(r"A \to A \alpha \mid \beta")
    
    with col_r2:
        st.markdown("**Eliminated Rules**")
        st.latex(r"A \to \beta A'")
        st.latex(r"A' \to \alpha A' \mid \varepsilon")

    st.divider()

    st.subheader("📝 Example: Step-by-Step Elimination")
    st.markdown("**Given Grammar:**")
    st.code("""
E -> E + T | T
T -> T * F | F
F -> (E) | id
    """, language="text")

    # Step 1
    with st.expander(r"1️⃣ Processing $E \to E + T \mid T$", expanded=True):
        st.markdown(r"""
        - **Compare:** $A = E, \alpha = + T, \beta = T$.
        - **Resulting Productions:**
        """)
        st.latex(r"E \to T E'")
        st.latex(r"E' \to + T E' \mid \varepsilon")

    # Step 2
    with st.expander(r"2️⃣ Processing $T \to T * F \mid F$", expanded=True):
        st.markdown(r"""
        - **Compare:** $A = T, \alpha = * F, \beta = F$.
        - **Resulting Productions:**
        """)
        st.latex(r"T \to F T'")
        st.latex(r"T' \to * F T' \mid \varepsilon")

    # Step 3
    with st.expander(r"3️⃣ Processing $F \to (E) \mid id$", expanded=True):
        st.markdown(r"""
        - **Observation:** Left recursion is **not** applied here because the right-hand side does not begin with $F$.
        - **Resulting Production:**
        """)
        st.latex(r"F \to (E) \mid id")

    st.divider()

    st.header("🧪 Step-by-Step Elimination Lab")
    st.markdown("Enter your grammar rules below to see the step-by-step elimination process.")

    col_l1, col_l2 = st.columns([2, 1])
    with col_l1:
        user_grammar = st.text_area("Enter Grammar (e.g., E -> E+T | T):", 
                                    value="A -> A + B | B * C | d", 
                                    height=120, key="lr_lab_input")
    with col_l2:
        st.info("""
        **Format:**
        - Use `->` for rules.
        - Use `|` for options.
        - One non-terminal per line.
        """)

    if st.button("🚀 Eliminated Step-by-Step", use_container_width=True):
        lines = [line.strip() for line in user_grammar.split("\n") if "->" in line]
        if not lines:
            st.error("Invalid grammar format. Please use 'LHS -> RHS | RHS'.")
        else:
            all_converted = []
            for line in lines:
                lhs, rhs_blob = line.split("->")
                lhs = lhs.strip()
                options = [opt.strip() for opt in rhs_blob.split("|") if opt.strip()]
                
                # Identify alpha and beta
                alphas = []
                betas = []
                for opt in options:
                    tokens = opt.split() if " " in opt else list(opt)
                    if tokens and tokens[0] == lhs:
                        # Left recursive
                        alphas.append(" ".join(tokens[1:]))
                    else:
                        betas.append(opt)

                with st.expander(f"🔍 Analyzing Non-Terminal: **{lhs}**", expanded=True):
                    if alphas:
                        st.write(f"✅ **Left Recursion Detected!**")
                        st.markdown(r"- **$\alpha$ segments:** " + ", ".join([f"`{a}`" for a in alphas]))
                        st.markdown(r"- **$\beta$ segments:** " + ", ".join([f"`{b}`" for b in betas]))
                        
                        new_nt = f"{lhs}'"
                        rule1 = f"{lhs} -> " + " | ".join([f"{b} {new_nt}" for b in betas])
                        rule2 = f"{new_nt} -> " + " | ".join([f"{a} {new_nt}" for a in alphas]) + " | ε"
                        
                        st.success("**Resulting Rules:**")
                        st.latex(rule1.replace("->", r"\to"))
                        st.latex(rule2.replace("->", r"\to"))
                        all_converted.append(rule1)
                        all_converted.append(rule2)
                    else:
                        st.write("❌ **No Direct Left Recursion.**")
                        st.info("Rule remains unchanged.")
                        all_converted.append(f"{lhs} -> {' | '.join(betas)}")

            st.divider()
            st.markdown("### ✅ Final Converted Grammar")
            st.code("\n".join(all_converted), language="text")

    # Navigation
    c_nav1, c_nav2 = st.columns(2)
    with c_nav1:
        if st.button("⬅️ Previous: Introduction to Parsers"):
            st.session_state.unit1_topic = "4.1 Introduction to Parsers"
            st.rerun()
    
    with c_nav2:
        if st.button("Next: Left Factoring ➡️", use_container_width=True):
            st.session_state.unit1_topic = "4.3 Left Factoring"
            st.rerun()
