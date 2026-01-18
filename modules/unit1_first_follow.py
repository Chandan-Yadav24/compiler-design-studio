import streamlit as st
import re

def tokenize(text):
    return re.findall(r"[a-zA-Z0-9]+'|[a-zA-Z0-9]+|[^a-zA-Z0-9\s]", text)

def compute_first_follow(grammar_rules):
    # 1. Parse rules
    rules = {} # LHS -> List of RHS lists
    non_terminals = [] # Use list to preserve order for start symbol
    all_symbols = set()
    
    for line in grammar_rules.split("\n"):
        if "->" in line:
            lhs, rhs_blob = line.split("->")
            lhs = lhs.strip()
            if lhs not in rules: 
                rules[lhs] = []
                non_terminals.append(lhs)
            all_symbols.add(lhs)
            options = rhs_blob.split("|")
            for opt in options:
                tokens = tokenize(opt)
                rules[lhs].append(tokens)
                for t in tokens: all_symbols.add(t)
                
    nt_set = set(non_terminals)
    terminals = all_symbols - nt_set
    if "ε" in terminals: terminals.remove("ε")
    if "e" in terminals: terminals.remove("e") 
    
    # 2. Compute FIRST
    first = {nt: set() for nt in nt_set}
    changed = True
    while changed:
        changed = False
        for lhs in nt_set:
            for rhs in rules[lhs]:
                old_len = len(first[lhs])
                if not rhs or rhs[0] in ["ε", "e"]:
                    first[lhs].add("ε")
                else:
                    for i, sym in enumerate(rhs):
                        if sym in terminals:
                            first[lhs].add(sym)
                            break
                        elif sym in nt_set:
                            first[lhs].update(first[sym] - {"ε"})
                            if "ε" not in first[sym]:
                                break
                        if i == len(rhs) - 1: # All symbols had ε
                            first[lhs].add("ε")
                if len(first[lhs]) > old_len: changed = True

    # 3. Compute FOLLOW
    follow = {nt: set() for nt in nt_set}
    if non_terminals:
        follow[non_terminals[0]].add("$")
    
    changed = True
    while changed:
        changed = False
        for lhs in nt_set:
            for rhs in rules[lhs]:
                for i, sym in enumerate(rhs):
                    if sym in nt_set:
                        old_len = len(follow[sym])
                        if i + 1 < len(rhs):
                            # Add FIRST(rest of rhs)
                            rest_tokens = rhs[i+1:]
                            all_nullable = True
                            for r_sym in rest_tokens:
                                if r_sym in terminals:
                                    follow[sym].add(r_sym)
                                    all_nullable = False
                                    break
                                elif r_sym in nt_set:
                                    follow[sym].update(first[r_sym] - {"ε"})
                                    if "ε" not in first[r_sym]:
                                        all_nullable = False
                                        break
                            if all_nullable:
                                follow[sym].update(follow[lhs])
                        else: # Last symbol
                            follow[sym].update(follow[lhs])
                            
                        if len(follow[sym]) > old_len: changed = True
                        
    return first, follow, nt_set

def render_first_follow():
    st.title("🎯 4.4 FIRST and FOLLOW Sets")
    
    st.markdown(r"""
    **FIRST** and **FOLLOW** sets are the foundational tools required to construct a **Parsing Table** for Top-Down (LL) parsing. They help the parser decide which production rule to apply for a given input symbol.
    """)

    st.divider()

    # --- FIRST SETS ---
    st.header("🏁 I) FIRST Sets")
    st.markdown(r"""
    The **FIRST set** of a grammar symbol is the set of **terminals** that can appear as the first symbol in any string derived from that symbol.
    """)

    with st.expander("🛠️ Rules to Compute FIRST", expanded=True):
        st.markdown(r"""
        1. **Terminals:** If $X$ is a terminal, then $\text{FIRST}(X) = \{X\}$.
        2. **Non-terminals:** If $X \to Y_1 Y_2 \dots Y_n$ is a production:
           - Add everything in $\text{FIRST}(Y_1)$ to $\text{FIRST}(X)$ (except $\varepsilon$).
           - If $Y_1 \Rightarrow \varepsilon$, then add $\text{FIRST}(Y_2)$ to $\text{FIRST}(X)$, and so on.
           - If all $Y_1, Y_2, \dots, Y_n \Rightarrow \varepsilon$, then add $\varepsilon$ to $\text{FIRST}(X)$.
        3. **Epsilon:** If $X \to \varepsilon$, then add $\varepsilon$ to $\text{FIRST}(X)$.
        """)

    st.divider()

    # --- FOLLOW SETS ---
    st.header("👣 II) FOLLOW Sets")
    st.markdown(r"""
    The **FOLLOW set** of a non-terminal $A$ is the set of **terminals** that can appear immediately to the right of $A$ in some sentential form (derivation).
    """)

    with st.expander("🛠️ Rules to Compute FOLLOW", expanded=True):
        st.markdown(r"""
        1. **Start Symbol:** If $S$ is the start symbol, add the end-marker **$** to $\text{FOLLOW}(S)$.
        2. **Production $B \to \alpha A \beta$:** 
           Everything in $\text{FIRST}(\beta)$ (except $\varepsilon$) is added to $\text{FOLLOW}(A)$.
        3. **Production $B \to \alpha A$** OR **$B \to \alpha A \beta$** (where $\beta \Rightarrow \varepsilon$):
           Everything in $\text{FOLLOW}(B)$ is added to $\text{FOLLOW}(A)$.
        """)

    st.divider()

    # --- EXAMPLE ---
    st.header("📝 Example: Computing FIRST & FOLLOW")
    st.markdown(r"""
    **Given Factored Grammar:**
    - $E \to T E'$
    - $E' \to + T E' \mid \varepsilon$
    - $T \to F T'$
    - $T' \to * F T' \mid \varepsilon$
    - $F \to (E) \mid id$
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏁 1. FIRST Sets Results")
        st.latex(r"\text{FIRST}(F) = \{ (, id \}")
        st.latex(r"\text{FIRST}(T') = \{ *, \varepsilon \}")
        
        st.latex(r"\text{FIRST}(T) = \{ (, id \}")
        st.caption("Same as FIRST(F)")
        
        st.latex(r"\text{FIRST}(E') = \{ +, \varepsilon \}")
        
        st.latex(r"\text{FIRST}(E) = \{ (, id \}")
        st.caption("Same as FIRST(T)")

    with col2:
        st.subheader("👣 2. FOLLOW Sets Results")
        st.latex(r"\text{FOLLOW}(E) = \{ \$, ) \}")
        st.caption("Starts with $ (Start symbol) + ')' from F → (E)")
        
        st.latex(r"\text{FOLLOW}(E') = \{ \$, ) \}")
        st.caption("Same as FOLLOW(E)")
        
        st.latex(r"\text{FOLLOW}(T) = \{ +, \$, ) \}")
        st.caption("FIRST(E') without ε + FOLLOW(E')")
        
        st.latex(r"\text{FOLLOW}(T') = \{ +, \$, ) \}")
        st.caption("Same as FOLLOW(T)")
        
        st.latex(r"\text{FOLLOW}(F) = \{ *, +, \$, ) \}")
        st.caption("FIRST(T') without ε + FOLLOW(T')")

    st.divider()

    # --- INTERACTIVE LAB ---
    st.header("🧪 FIRST & FOLLOW Interactive Lab")
    st.markdown("Enter your grammar rules below to compute the sets automatically.")

    col_l1, col_l2 = st.columns([2, 1])
    with col_l1:
        u_grammar = st.text_area("Enter Grammar (e.g., E -> T E' | e):", 
                                 value="E -> T E'\nE' -> + T E' | e\nT -> F T'\nT' -> * F T' | e\nF -> ( E ) | id", 
                                 height=150, key="ff_lab_input")
    with col_l2:
        st.info("""
        **Format:**
        - Use `->` for rules.
        - Use `|` for options.
        - Use `e` or `ε` for epsilon.
        - One non-terminal per line.
        """)

    if st.button("🚀 Compute FIRST & FOLLOW", use_container_width=True):
        if not u_grammar.strip():
            st.error("Please enter a grammar.")
        else:
            try:
                first_sets, follow_sets, nts = compute_first_follow(u_grammar)
                
                if not nts:
                    st.warning("No non-terminals found. Check your `->` symbols.")
                else:
                    st.success("✅ Sets Computed Successfully!")
                    
                    res_col1, res_col2 = st.columns(2)
                    
                    with res_col1:
                        st.subheader("🏁 FIRST Sets")
                        for nt in sorted(list(nts)):
                            s_vals = ", ".join(sorted(list(first_sets[nt])))
                            st.latex(r"\text{FIRST}(" + nt + r") = \{ " + s_vals + r" \}")
                            
                    with res_col2:
                        st.subheader("👣 FOLLOW Sets")
                        for nt in sorted(list(nts)):
                            symbols = sorted(list(follow_sets[nt]))
                            # Escape $ for LaTeX
                            s_vals = ", ".join([s.replace("$", r"\$") for s in symbols])
                            st.latex(r"\text{FOLLOW}(" + nt + r") = \{ " + s_vals + r" \}")
            except Exception as e:
                st.error(f"Error in computation: {str(e)}")

    st.divider()

    # Navigation
    c_nav1, c_nav2 = st.columns(2)
    with c_nav1:
        if st.button("⬅️ Previous: Left Factoring"):
            st.session_state.unit1_topic = "4.3 Left Factoring"
            st.rerun()
    
    with c_nav2:
        if st.button("Next: LL(1) Predictive Parsing Table ➡️", use_container_width=True):
            st.session_state.unit1_topic = "4.5 LL(1) Predictive Parsing Table"
            st.rerun()
