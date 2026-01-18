import streamlit as st
import pandas as pd
import re
from collections import deque

def render_parsing_intro():
    st.title("🛡️ 4.1 Introduction to Parsers")
    st.markdown(r"""
    A **Parser** is the core component of a compiler's syntax analysis phase. It takes a stream of tokens (input symbols) and builds a structural representation, usually a **Parse Tree**.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1️⃣ Top-Down Parser")
        st.markdown(r"""
        - **Approach:** Starts from the **Start Symbol** and tries to derive the input string.
        - **Logic:** Expansion (Derivation).
        - **Direction:** Root to Leaves.
        - **Primary Method:** Left-Most Derivation (LL Parsing).
        """)
    
    with col2:
        st.subheader("2️⃣ Bottom-Up Parser")
        st.markdown(r"""
        - **Approach:** Starts from the **Input Symbols** and tries to reduce them back to the Start Symbol.
        - **Logic:** Reduction.
        - **Direction:** Leaves to Root.
        - **Primary Method:** Reverse Right-Most Derivation (LR Parsing).
        """)

    st.divider()

    st.header("🏗️ Bottom-Up Parser (Shift-Reduce Parser)")
    st.markdown("""
    Bottom-up parsing is the most popular technique for production compilers. It is often called **Shift-Reduce Parsing** because of its two primary operations.
    """)

    st.subheader("🕹️ The Four Basic Operations")
    
    op_cols = st.columns(4)
    with op_cols[0]:
        st.markdown("**1. Shift**")
        st.caption("Move one symbol from the input buffer onto the parser stack.")
    with op_cols[1]:
        st.markdown("**2. Reduce**")
        st.caption("Replace a 'Handle' (RHS matching substring) on the stack with its LHS non-terminal.")
    with op_cols[2]:
        st.markdown("**3. Accept**")
        st.caption("Success! Entire input processed and only the Start Symbol remains on stack.")
    with op_cols[3]:
        st.markdown("**4. Error**")
        st.caption("Fail! No valid shift or reduce action possible.")

    st.divider()
    render_shift_reduce_simulator()
    st.divider()
    render_user_sr_solver()

def render_user_sr_solver():
    st.header("🎮 Ultra-Scalable Shift-Reduce Solver")
    st.markdown(r"""
    This solver uses **BFS (Breadth-First Search)** to explore all possible parsing paths. 
    It will find the valid "Accept" sequence even if there are Shift-Reduce conflicts (like standard multiplication precedence).
    """)
    
    c1, c2 = st.columns([2, 1])
    with c1:
        u_rules = st.text_area("Grammar (e.g., E -> E+E | a):", value="E -> E+E\nE -> E*E\nE -> (E)\nE -> id", height=150, key="custom_sr_rules_ultra")
        u_str = st.text_input("Input String (e.g., id + id * id):", value="id + id * id", key="custom_sr_str_ultra")
    with c2:
        st.info("""
        **🚀 Ultra Scalable Mode:**
        1. **Conflict Resolution:** Finds the path to the Start Symbol by exploring all shifts and reductions.
        2. **Intelligent Lexer:** Automatically detects tokens even without spaces.
        3. **Robustness:** Handles complex grammars that simple greedy solvers fail on.
        """)

    if st.button("🚀 Solve with BFS (Ultra Scalable)", use_container_width=True):
        try:
            # --- 1. Robust Grammar Extraction ---
            grammar_rules = [] # List of (LHS, [RHS_tokens])
            non_terminals = set()
            all_symbols = set()
            
            for line in u_rules.split("\n"):
                if "->" in line:
                    lhs, rhs_blob = line.split("->")
                    lhs = lhs.strip()
                    non_terminals.add(lhs)
                    all_symbols.add(lhs)
                    
                    # Split RHS by '|'
                    options = rhs_blob.split("|")
                    for opt in options:
                        # Use regex to find alphanumeric words or single special chars
                        rhs_tokens = re.findall(r"[a-zA-Z0-9]+|[^a-zA-Z0-9\s]", opt)
                        grammar_rules.append((lhs, rhs_tokens))
                        for t in rhs_tokens: all_symbols.add(t)

            start_symbol = grammar_rules[0][0] if grammar_rules else None
            
            # --- 2. Advanced Tokenizer ---
            # Sort symbols by length to match longest tokens first (e.g., 'id' before 'i')
            sorted_symbols = sorted(list(all_symbols), key=len, reverse=True)
            # Add general alphanumeric pattern to match "id" even if it's not explicitly a terminal symbol in some contexts
            token_pattern = "|".join([re.escape(s) for s in sorted_symbols if s.strip()] + [r"[a-zA-Z0-9]+"])
            
            def tokenize(text):
                # Only use regex if there are no spaces (otherwise trust user spaces)
                if " " in text.strip():
                    return text.strip().split()
                return re.findall(token_pattern, text.replace(" ", ""))

            input_tokens = tokenize(u_str)
            
            # --- 3. BFS Solver ---
            # State: (tuple(stack), tuple(input_buffer), list(history))
            initial_state = (("$",), tuple(input_tokens + ["$"]), [])
            queue = deque([initial_state])
            visited = set()
            
            final_history = None
            max_iterations = 2000
            iterations = 0
            
            while queue and iterations < max_iterations:
                curr_stack, curr_input, curr_history = queue.popleft()
                iterations += 1
                
                state_key = (curr_stack, curr_input)
                if state_key in visited: continue
                visited.add(state_key)
                
                # Check for Accept
                if curr_stack == ("$", start_symbol) and curr_input == ("$",):
                    final_history = curr_history + [{"Stack": " ".join(curr_stack), "Input": " ".join(curr_input), "Action": "Accept"}]
                    break
                
                # Possible Action: SHIFT
                if len(curr_input) > 1: # Last token is always '$'
                    next_token = curr_input[0]
                    new_stack = curr_stack + (next_token,)
                    new_input = curr_input[1:]
                    new_hist = curr_history + [{"Stack": " ".join(curr_stack), "Input": " ".join(curr_input), "Action": f"Shift {next_token}"}]
                    queue.append((new_stack, new_input, new_hist))
                
                # Possible Actions: REDUCE
                for lhs, rhs in grammar_rules:
                    if not rhs or rhs == [""]: continue # No epsilons for now
                    n = len(rhs)
                    if len(curr_stack) >= n:
                        if list(curr_stack[-n:]) == rhs:
                            new_stack = curr_stack[:-n] + (lhs,)
                            rhs_str = ' '.join(rhs)
                            action_str = f"Reduce: Handle = {rhs_str} --> {lhs}"
                            new_hist = curr_history + [{"Stack": " ".join(curr_stack), "Input": " ".join(curr_input), "Action": action_str}]
                            queue.append((new_stack, curr_input, new_hist))

            # --- 4. Display Results ---
            st.subheader("📊 Shift-Reduce Parsing Table")
            if input_tokens:
                st.info(f"🔍 **Detected Tokens:** `{'`, `'.join(input_tokens)}`")
            
            if final_history:
                st.table(pd.DataFrame(final_history))
                st.success("✅ **Accept!** The string is valid according to the grammar.")
                st.balloons()
            else:
                st.error("❌ **Parsing Failed.** No valid sequence of shift/reduce reached the start symbol.")
                st.info("""
                **Possible Reasons:**
                1. The string is truly invalid for this grammar.
                2. The start symbol was never reached.
                3. The search space exceeded the limit (2000 states).
                """)

        except Exception as e:
            st.error(f"Solver Error: {e}")

def render_shift_reduce_simulator():
    st.header("🧪 Interactive Shift-Reduce Lab")
    st.markdown("""
    Let's simulate a **Real Shift-Reduce Parser** using the following grammar:
    
    - $E \\to E + E$
    - $E \\to E * E$
    - $E \\to a \\mid b \\mid c$
    
    **Target String:** `a + b * c$`
    """)

    # Steps data based on user request
    parsing_steps = [
        {"stack": "$", "input": "a + b * c $", "action": "Initial State"},
        {"stack": "$ a", "input": "+ b * c $", "action": "Shift a"},
        {"stack": "$ E", "input": "+ b * c $", "action": "Reduce E → a (Handle = a)"},
        {"stack": "$ E +", "input": "b * c $", "action": "Shift +"},
        {"stack": "$ E + b", "input": "* c $", "action": "Shift b"},
        {"stack": "$ E + E", "input": "* c $", "action": "Reduce E → b (Handle = b)"},
        {"stack": "$ E + E *", "input": "c $", "action": "Shift *"},
        {"stack": "$ E + E * c", "input": "$", "action": "Shift c"},
        {"stack": "$ E + E * E", "input": "$", "action": "Reduce E → c (Handle = c)"},
        {"stack": "$ E + E", "input": "$", "action": "Reduce E → E * E (Handle = E*E)"},
        {"stack": "$ E", "input": "$", "action": "Reduce E → E + E (Handle = E+E)"},
        {"stack": "$ E", "input": "$", "action": "Accept"},
    ]

    if 'sr_step' not in st.session_state:
        st.session_state.sr_step = 0

    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("⏪ Reset", use_container_width=True):
            st.session_state.sr_step = 0
            st.rerun()
    with c2:
        if st.button("⏭️ Next Step", type="primary", use_container_width=True):
            if st.session_state.sr_step < len(parsing_steps) - 1:
                st.session_state.sr_step += 1
                st.rerun()
    with c3:
        if st.button("⏩ Complete All", use_container_width=True):
            st.session_state.sr_step = len(parsing_steps) - 1
            st.rerun()

    current_idx = st.session_state.sr_step
    
    # Progress Bar
    progress = (current_idx + 1) / len(parsing_steps)
    st.progress(progress, text=f"Step {current_idx + 1} of {len(parsing_steps)}")

    # Visualization of the Parser State
    st.markdown("---")
    v1, v2, v3 = st.columns(3)
    
    with v1:
        st.markdown("##### 📚 Stack")
        st.markdown(f"""
            <div style="background: #1e293b; padding: 20px; border-radius: 10px; border: 2px solid #3b82f6; text-align: center; font-family: monospace; font-size: 1.5rem;">
                {parsing_steps[current_idx]['stack']}
            </div>
        """, unsafe_allow_html=True)
    
    with v2:
        st.markdown("##### 📥 Input Buffer")
        st.markdown(f"""
            <div style="background: #1e293b; padding: 20px; border-radius: 10px; border: 2px solid #64748b; text-align: center; font-family: monospace; font-size: 1.5rem;">
                {parsing_steps[current_idx]['input']}
            </div>
        """, unsafe_allow_html=True)

    with v3:
        st.markdown("##### ⚙️ Parser Action")
        action = parsing_steps[current_idx]['action']
        color = "#10b981" if action == "Accept" else "#3b82f6"
        st.markdown(f"""
            <div style="background: #111827; padding: 20px; border-radius: 10px; border: 2px solid {color}; text-align: center; font-weight: bold; font-size: 1.1rem; color: {color};">
                {action}
            </div>
        """, unsafe_allow_html=True)

    # History Table
    st.markdown("---")
    st.subheader("📜 Parsing History")
    
    history_df = pd.DataFrame(parsing_steps[:current_idx + 1])
    # Rename columns for display
    history_df.columns = ["Stack", "Input", "Action"]
    
    st.table(history_df)

    if current_idx == len(parsing_steps) - 1:
        st.success("🎉 **Accept!** The string is valid according to the grammar.")
        st.balloons()

    st.info("""
    > **Summary Note:** 
    > In the example above, the parser identifies **handles** (the part of the stack that matches a grammar rule) and performs reductions until only the start symbol **E** remains.
    """)

    st.divider()
    col_bn1, col_bn2 = st.columns(2)
    with col_bn1:
        if st.button("⬅️ Previous: Syntax Analysis Overview"):
            st.session_state.selected_topic = "4.0 Syntax Analysis Overview & Top-Down Parser"
            st.rerun()
    with col_bn2:
        if st.button("Next: Left Recursion (Elimination) ➡️", use_container_width=True):
            st.session_state.selected_topic = "4.2 Left Recursion (Elimination)"
            st.rerun()
