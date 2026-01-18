import streamlit as st
import os
import re

def tokenize_rule(text):
    """Robust tokenization: identifiers/keywords or single special characters."""
    return re.findall(r"[a-zA-Z0-9]+|[^a-zA-Z0-9\s]", text)

def get_longest_common_prefix_tokens(token_lists):
    if not token_lists or len(token_lists) < 2: return []
    
    first = token_lists[0]
    prefix = []
    for i in range(len(first)):
        curr_sym = first[i]
        for tokens in token_lists[1:]:
            if i >= len(tokens) or tokens[i] != curr_sym:
                return prefix
        prefix.append(curr_sym)
    return prefix

def render_left_factoring():
    st.title("📑 4.3 Left Factoring")
    
    st.markdown(r"""
    ### 📖 Definition
    **Left Factoring** is a grammar transformation technique used to remove ambiguity. It occurs when two or more productions for a non-terminal begin with the **same prefix**. 
    
    By "factoring out" this common prefix, the parser can delay making a decision until it has seen enough of the input to make the correct choice.
    """)

    st.info(r"""
    **Formal Rule:**
    If we have productions:
    $A \to \alpha \beta_1 \mid \alpha \beta_2 \mid \dots \mid \alpha \beta_n \mid \gamma$
    
    We transform them into:
    1. $A \to \alpha A' \mid \gamma$
    2. $A' \to \beta_1 \mid \beta_2 \mid \dots \mid \beta_n$
    
    *(Where $\alpha$ is the longest common prefix)*
    """)

    st.divider()

    st.subheader("📝 Example: Applying Left Factoring")
    st.markdown(r"""
    **Given Grammar (Dangling Else Problem):**
    $S \to i c t S \mid i c t S e S \mid a$
    """)

    with st.expander("🔍 Step-by-Step Factoring", expanded=True):
        st.markdown(r"""
        1. **Identify Common Prefix:** 
           Comparing $i c t S$ and $i c t S e S$, the common prefix is $\alpha = i c t S$.
        
        2. **Determine $\beta$ segments:**
           - $\beta_1 = \varepsilon$ (empty, as nothing follows the first rule).
           - $\beta_2 = e S$ (what remains after $i c t S$).
        
        3. **Determine $\gamma$ segments:**
           - $\gamma = a$ (does not start with the prefix).
        
        4. **Apply Transformation:**
        """)
        st.latex(r"S \to i c t S S' \mid a")
        st.latex(r"S' \to \varepsilon \mid e S")

    st.divider()

    # --- INTERACTIVE LAB ---
    st.header("🧪 Left Factoring Lab")
    st.markdown("Enter your rules to factor out common prefixes automatically.")

    col_l1, col_l2 = st.columns([2, 1])
    with col_l1:
        u_input = st.text_area("Enter rules (e.g., A -> ab | abc | d):", 
                               value="S -> i c t S | i c t S e S | a", 
                               height=100, key="factoring_input")
    with col_l2:
        st.info("""
        **Tips:**
        - Enter one non-terminal rule per line.
        - Use `|` to separate options.
        - The engine detects the longest common prefix.
        """)

    if st.button("🚀 Factor Grammar", use_container_width=True):
        lines = [line.strip() for line in u_input.split("\n") if "->" in line]
        if not lines:
            st.error("Invalid format. Use `LHS -> RHS | RHS`.")
        else:
            final_grammar = []
            for line in lines:
                lhs, rhs_blob = line.split("->")
                lhs = lhs.strip()
                options = [opt.strip() for opt in rhs_blob.split("|") if opt.strip()]
                
                # Tokenize all options first
                tokenized_options = [tokenize_rule(opt) for opt in options]
                
                # Group options by their first token
                groups = {}
                for i, tokens in enumerate(tokenized_options):
                    first = tokens[0] if tokens else "ε"
                    if first not in groups: groups[first] = []
                    groups[first].append(tokens)
                
                with st.expander(f"🔍 Analyzing **{lhs}**", expanded=True):
                    untouched_options = []
                    new_rules = []
                    
                    for first_sym, group_token_lists in groups.items():
                        if len(group_token_lists) > 1:
                            # Find LCP tokens for this specific group
                            lcp_tokens = get_longest_common_prefix_tokens(group_token_lists)
                            alpha = " ".join(lcp_tokens)
                            
                            st.success(r"✅ Common Prefix Found for group starting with `" + first_sym + r"`: `" + alpha + r"`")
                            
                            betas = []
                            for tokens in group_token_lists:
                                rem = tokens[len(lcp_tokens):]
                                border = " " if rem and len(rem) > 1 else ""
                                betas.append(" ".join(rem) if rem else "ε")
                            
                            new_nt = f"{lhs}'"
                            # Handle duplicate prime names if multiple groups exist
                            active_groups = [g for g in groups.values() if len(g) > 1]
                            if len(active_groups) > 1:
                                new_nt = f"{lhs}_{first_sym}'"
                                
                            untouched_options.append(f"{alpha} {new_nt}")
                            new_rules.append(f"{new_nt} -> " + " | ".join(betas))
                        else:
                            untouched_options.append(" ".join(group_token_lists[0]))

                    # Create the main rule
                    main_rule = f"{lhs} -> " + " | ".join(untouched_options)
                    st.latex(main_rule.replace("->", r"\to"))
                    for r in new_rules:
                        st.latex(r.replace("->", r"\to"))
                    
                    final_grammar.append(main_rule)
                    final_grammar.extend(new_rules)

            st.divider()
            st.markdown("### ✅ Resulting Grammar")
            st.code("\n".join(final_grammar), language="text")

    # Navigation
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Previous: Left Recursion"):
            st.session_state.unit1_topic = "4.2 Left Recursion (Elimination)"
            st.rerun()
    with c2:
        if st.button("Next: FIRST and FOLLOW Sets ➡️", use_container_width=True):
            st.session_state.unit1_topic = "4.4 FIRST and FOLLOW Sets"
            st.rerun()
