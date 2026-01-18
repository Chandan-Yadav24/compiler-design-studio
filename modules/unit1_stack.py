import streamlit as st
import pandas as pd
import re

# Need tokenizer and logic from ll1 or shared
from modules.unit1_ll1 import compute_first_follow_v2, get_first_of_string, tokenize

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

def render_stack_simulation():
    st.title("⚙️ 4.6 LL(1) Stack Implementation")
    
    st.markdown(r"""
    The **Stack** is the core operational component of an LL(1) parser. It drives the process of **Predicting** (expanding non-terminals) and **Matching** (consuming input symbols).
    """)

    st.divider()

    # --- SIMULATOR ---
    st.header("🧪 LL(1) Parsing Simulator")
    st.markdown("Enter your grammar and a string to simulate the step-by-step stack operations.")

    col1, col2 = st.columns([2, 1])
    with col1:
        u_grammar = st.text_area("Grammar:", 
                                 value="E -> T E'\nE' -> + T E' | e\nT -> F T'\nT' -> * F T' | e\nF -> ( E ) | id", 
                                 height=150, key="stack_sim_sep_grammar")
        u_input = st.text_input("Input String:", value="id + id * id", key="stack_sim_sep_input")
        
    with col2:
        st.info("""
        🚀 **Simulator Rules:**
        1. Grammar must be LL(1).
        2. Input tokens must match grammar terminals.
        3. The table is built automatically in the background.
        """)

    if st.button("▶️ Run Simulation", use_container_width=True):
        if not u_grammar.strip() or not u_input.strip():
            st.error("Please provide both grammar and input string.")
        else:
            try:
                firsts, follows, nts, terms, rules = compute_first_follow_v2(u_grammar)
                history, error = simulate_ll1_logic(firsts, follows, nts, terms, rules, u_input)
                
                if error:
                    st.error(error)
                    if history:
                        st.subheader("📉 Simulation Trace (Partial)")
                        st.dataframe(pd.DataFrame(history), use_container_width=True)
                else:
                    st.success(f"✅ String '{u_input}' Accepted!")
                    st.subheader("📋 Stack Execution Trace")
                    st.dataframe(pd.DataFrame(history), use_container_width=True)
            except Exception as e:
                st.error(f"Logic Error: {str(e)}")

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: LL(1) Parsing Table"):
            st.session_state.unit1_topic = "4.5 LL(1) Predictive Parsing Table"
            st.rerun()
    with nav2:
        if st.button("Next: Semantic Analysis (Topic 5.1) ➡️", use_container_width=True):
            st.session_state.unit1_topic = "5.1 Semantic Analysis (SDT & SDD)"
            st.rerun()
