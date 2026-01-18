import streamlit as st
import pandas as pd
import re

def tokenize(text):
    return re.findall(r"[a-zA-Z0-9]+'|[a-zA-Z0-9]+|[^a-zA-Z0-9\s]", text)

def compute_first_follow_v2(grammar_rules):
    # 1. Parse rules
    rules = {} # LHS -> List of RHS lists
    non_terminals = [] 
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
    
    # terminals also include $
    term_set = list(terminals)
    term_set.append("$")
    
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
                        
    return first, follow, non_terminals, terminals, rules

def get_first_of_string(string_tokens, first_sets, terminals):
    res = set()
    if not string_tokens or string_tokens[0] in ["ε", "e"]:
        res.add("ε")
        return res
    
    for i, sym in enumerate(string_tokens):
        if sym in terminals:
            res.add(sym)
            return res
        elif sym in first_sets:
            res.update(first_sets[sym] - {"ε"})
            if "ε" not in first_sets[sym]:
                return res
        else: # Unknown symbol treatment as terminal
             res.add(sym)
             return res
             
    res.add("ε")
    return res

def simulate_ll1_logic(firsts, follows, nts, terms, rules, input_str):
    try:
        # Build Parsing Table for simulation
        parsing_table = {nt: {} for nt in nts}
        for lhs in nts:
            for rhs in rules[lhs]:
                alpha_first = get_first_of_string(rhs, firsts, terms)
                for a in alpha_first:
                    if a != "ε": parsing_table[lhs][a] = rhs
                if "ε" in alpha_first:
                    for b in follows[lhs]: parsing_table[lhs][b] = rhs
        
        start_nt = nts[0] if nts else None
        if not start_nt: return None, "Error: No grammar found."
        
        input_tokens = tokenize(input_str) + ["$"]
        stack = ["$", start_nt]
        
        history = []
        steps = 0
        limit = 100 
        
        while steps < limit:
            curr_stack = " ".join(reversed(stack))
            curr_input = " ".join(input_tokens)
            top = stack[-1]
            lookahead = input_tokens[0]
            
            step_data = {"Stack": curr_stack, "Input": curr_input}
            
            if top == "$" and lookahead == "$":
                step_data["Action"] = "Accept ✅"
                history.append(step_data)
                break
            
            if top == lookahead:
                step_data["Action"] = f"Match! Pop '{top}'"
                history.append(step_data)
                stack.pop()
                input_tokens.pop(0)
            elif top in parsing_table:
                if lookahead in parsing_table[top]:
                    rhs = parsing_table[top][lookahead]
                    rhs_str = " ".join(rhs) if rhs else "ε"
                    # Clean 'e' to ε for display
                    rhs_display = ["ε" if x == 'e' or x == 'ε' else x for x in rhs] if rhs else ["ε"]
                    step_data["Action"] = f"Predict: {top} → {' '.join(rhs_display)}"
                    history.append(step_data)
                    stack.pop()
                    if rhs and rhs[0] not in ["ε", "e"]:
                        for s in reversed(rhs):
                            stack.append(s)
                else:
                    step_data["Action"] = f"Error: No rule for ({top}, {lookahead})"
                    history.append(step_data)
                    return history, f"Runtime Error: Input '{lookahead}' unexpected for '{top}'."
            else:
                step_data["Action"] = f"Error: Terminal mismatch."
                history.append(step_data)
                return history, f"Mismatch Error: Expected '{top}' but found '{lookahead}'."
            
            steps += 1
        return history, None
    except Exception as e:
        return None, str(e)

def render_ll1():
    st.title("🧩 4.5 LL(1) Predictive Parsing Table")
    
    st.markdown(r"""
    This laboratory focuses on the construction of the **Predictive Parsing Table**. The table is used by the parser to decide which rule to apply based on the current non-terminal and the lookahead symbol.
    """)

    st.divider()

    # --- RULES ---
    st.header("🛠️ Construction Rules")
    st.markdown(r"""
    For every production $A \to \alpha$ in the grammar:
    1. For every terminal **$a$** in $\text{FIRST}(\alpha)$, add $A \to \alpha$ to $M[A, a]$.
    2. If $\varepsilon$ is in $\text{FIRST}(\alpha)$, for every terminal **$b$** in $\text{FOLLOW}(A)$, add $A \to \alpha$ to $M[A, b]$.
    3. If $M[A, a]$ has more than one production, the grammar is **NOT LL(1)** (Conflict).
    """)

    st.divider()

    # --- STATIC EXAMPLE ---
    st.subheader("📝 Step-by-Step Example")
    st.markdown("**Grammar:**")
    st.code("E -> T E'\nE' -> + T E' | ε\nT -> F T'\nT' -> * F T' | ε\nF -> ( E ) | id", language="text")
    
    with st.expander("🔍 View constructed Parsing Table"):
        df = pd.DataFrame({
            "id": ["E → T E'", "", "T → F T'", "", "F → id"],
            " + ": ["", "E' → + T E'", "", "T' → ε", ""],
            " * ": ["", "", "", "T' → * F T'", ""],
            " ( ": ["E → T E'", "", "T → F T'", "", "F → ( E )"],
            " ) ": ["", "E' → ε", "", "T' → ε", ""],
            " $ ": ["", "E' → ε", "", "T' → ε", ""]
        }, index=["E", "E'", "T", "T'", "F"])
        st.dataframe(df, use_container_width=True)
        st.info(r"💡 **Note:** Notice how $E' \to \varepsilon$ appears under both `)` and `$` because those are the symbols in $\text{FOLLOW}(E')$.")

    st.divider()

    # --- INTERACTIVE LAB ---
    st.header("🧪 Parsing Table Generator")
    st.markdown("Enter your grammar to generate the table automatically.")

    col1, col2 = st.columns([2, 1])
    with col1:
        u_grammar = st.text_area("LL(1) Grammar:", 
                                 value="E -> T E'\nE' -> + T E' | e\nT -> F T'\nT' -> * F T' | e\nF -> ( E ) | id", 
                                 height=150, key="ll1_sep_lab_input")
    with col2:
        st.info("""
        **Automated Steps:**
        1. FIRST & FOLLOW.
        2. Rule Mapping.
        3. Conflict Check.
        """)

    if st.button("🚀 Generate Parsing Table", use_container_width=True):
        if not u_grammar.strip():
            st.error("Please enter a grammar.")
        else:
            try:
                firsts, follows, nts, terms, rules = compute_first_follow_v2(u_grammar)
                
                def get_key(sym): return f" {sym} "
                common_order = ["id", "+", "-", "*", "/", "(", ")", "num"]
                sorted_terms = sorted(list(terms), key=lambda x: common_order.index(x) if x in common_order else 100)
                table_terms = [get_key(t) for t in sorted_terms] + [get_key("$")]
                
                table = {nt: {t: [] for t in table_terms} for nt in nts}
                conflicts = False
                
                for lhs in nts:
                    for rhs in rules[lhs]:
                        alpha_first = get_first_of_string(rhs, firsts, terms)
                        cleaned_rhs = ["ε" if x == 'e' or x == 'ε' else x for x in rhs]
                        prod_str = f"{lhs} → {' '.join(cleaned_rhs) if cleaned_rhs else 'ε'}"
                        
                        for a in alpha_first:
                            if a != "ε":
                                key = get_key(a)
                                if prod_str not in table[lhs][key]: table[lhs][key].append(prod_str)
                        if "ε" in alpha_first:
                            for b in follows[lhs]:
                                key = get_key(b)
                                if prod_str not in table[lhs][key]: table[lhs][key].append(prod_str)
                
                display_data = []
                for nt in nts:
                    row = {"Non-Terminal": nt}
                    for t in table_terms:
                        cell_prods = table[nt][t]
                        if len(cell_prods) > 1: conflicts = True
                        row[t] = " | ".join(cell_prods)
                    display_data.append(row)
                
                res_df = pd.DataFrame(display_data).set_index("Non-Terminal")
                st.dataframe(res_df, use_container_width=True)
                
                if conflicts: st.warning("⚠️ **Conflict Detected!** Grammar is NOT LL(1).")
                else: st.success("✅ **LL(1) Table Generated!** No conflicts found.")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

    st.divider()

    # Navigation
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Previous: FIRST and FOLLOW Sets"):
            st.session_state.unit1_topic = "4.4 FIRST and FOLLOW Sets"
            st.rerun()
    with c2:
        if st.button("Next: LL(1) Stack Implementation ➡️", use_container_width=True):
            st.session_state.unit1_topic = "4.6 LL(1) Stack Implementation"
            st.rerun()
