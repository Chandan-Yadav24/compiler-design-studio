import streamlit as st
import pandas as pd
import random
import re

def render_grammar_basics():
    st.subheader("3.1 Grammar Basics: The Mathematical Model")
    st.markdown(r"""
    ### 📖 What is a Grammar?
    In compiler design, a **Grammar** is a mathematical model used to define the syntax or structure of a language. It is the core of the **Parsing (Syntax Analysis)** phase.

    ---

    #### 🧩 Formal Definition (The 4-Tuple)
    Every formal grammar $G$ is defined as:
    """)
    st.latex(r"G = (N, T, P, S)")
    
    st.markdown(r"""
    | Component | Full Name | Meaning & Role |
    | :--- | :--- | :--- |
    | **N** | **Non-Terminals** | Placeholders (variables) that must be expanded. They don't appear in the final string. |
    | **T** | **Terminals** | The actual symbols of the language (a, b, 0, 1, keywords). They appear in final output. |
    | **P** | **Production Rules** | Rules describing how strings are formed: $\alpha \to \beta$ |
    | **S** | **Start Symbol** | The special non-terminal where the derivation begins ($S \in N$). |

    > **Important Rule:** $N \cap T = \emptyset$ (A symbol cannot be both a variable and a final character!)

    ---

    ### ⚙️ Production Rules ($\alpha \to \beta$)
    The heart of the grammar! It tells the compiler: *"If you see $\alpha$, you can replace it with $\beta$."*
    
    **Example:** $S \to aSb \mid \epsilon$
    *   This means $S$ can be replaced by $aSb$ OR by $\epsilon$ (empty string).

    ### 🎯 Why Grammar Matters for Compilers?
    1.  **Validation:** It checks if your code (e.g., `if (x < 5) { ... }`) follows the rules.
    2.  **Parse Trees:** It helps build the structure (tree) that represents your code.
    3.  **Ambiguity Check:** It helps ensure every piece of code has only ONE logical meaning.
    """)
    
    if st.button("Next: 3.2 Chomsky Hierarchy (Types of Grammar) ➡️", use_container_width=True):
        st.session_state.unit1_topic = "3.2 Chomsky Hierarchy (Types of Grammar)"
        st.rerun()

def render_chomsky_hierarchy():
    st.subheader("3.2 Chomsky Hierarchy: The 4 Types of Language Power")
    
    st.info("💡 **History:** Proposed by Noam Chomsky in 1956. It classifies grammars based on the restrictions on their production rules.")
    
    st.markdown(r"""
    ### 👑 The Hierarchy Table
    | Type | Grammar Name | Recognizing Machine | Rule Format | Typical Use |
    | :--- | :--- | :--- | :--- | :--- |
    | **Type 0** | **Unrestricted** | Turing Machine | $\alpha \to \beta$ | Theoretical Logic |
    | **Type 1** | **Context-Sensitive** | LBA | $\alpha A \beta \to \alpha \gamma \beta$ | Complex logic |
    | **Type 2** | **Context-Free (CFG)** | Pushdown (PDA) | $A \to \gamma$ | **Compiler Parsing** |
    | **Type 3** | **Regular** | Finite Automata | $A \to aB \mid a$ | **Lexical Analysis** |

    ---

    #### 0️⃣ Type 0: Unrestricted Grammar
    *   **Power:** Most powerful. Can generate any language a computer can recognize.
    *   **Rule:** $\alpha \to \beta$, where $\alpha$ contains at least one Non-terminal.
    *   **Machine:** Turing Machine.

    #### 1️⃣ Type 1: Context-Sensitive Grammar (CSG)
    *   **Rule:** $\alpha A \beta \to \alpha \gamma \beta$
    *   **Constraint:** Length of RHS $\ge$ Length of LHS. It never "shrinks" strings.
    *   **Machine:** Linear Bounded Automaton (LBA).

    #### 2️⃣ Type 2: Context-Free Grammar (CFG) ⭐
    *   **The Backbone of Compilers!** 
    *   **Rule:** $A \to \gamma$ (LHS must be a **single** Non-terminal).
    *   **Machine:** Pushdown Automata (uses a Stack).
    *   **Example:** Used for matching brackets, if-else nesting, arithmetic.

    #### 3️⃣ Type 3: Regular Grammar
    *   **Most Restricted, but Fastest.**
    *   **Rule:** $A \to aB$ or $A \to a$ (Linear forms).
    *   **Machine:** Finite Automata (DFA/NFA).
    *   **Example:** Used for recognizing tokens (identifiers, numbers).
    """)

    st.success("✅ **Summary:** Type 3 is used for Tokens (Lexer), Type 2 is used for Structure (Parser)!")

    if st.button("Next: 3.3 Parse Trees & Grammar Capabilities ➡️", use_container_width=True):
        st.session_state.unit1_topic = "3.3 Parse Trees & Grammar Capabilities"
        st.rerun()

def render_parse_trees():
    st.subheader("3.3 Parse Trees & Grammar Capabilities")

    st.markdown("""
    ### 🔋 I. Capabilities of Grammars
    The **"capability"** of a grammar refers to its **Generative Power**—the range and complexity of languages it can produce. 
    """)

    st.table(pd.DataFrame([
        {"Grammar Type": "Type 3 (Regular)", "Computational Capability": "Simple pattern matching; no memory.", "Real-World Application": "Lexical Analysis: Identifying keywords & variables."},
        {"Grammar Type": "Type 2 (Context-Free)", "Computational Capability": "Handles nested structures; uses a stack.", "Real-World Application": "Syntax Analysis: Matching brackets () or {} and blocks."},
        {"Grammar Type": "Type 1 (Context-Sensitive)", "Computational Capability": "Understands context; remembers symbols.", "Real-World Application": "Semantic Analysis: Checking variable declaration before use."},
        {"Grammar Type": "Type 0 (Unrestricted)", "Computational Capability": "Universal computation; any computable logic.", "Real-World Application": "Theory: Defines mathematical limits of computing."}
    ]))

    st.markdown("---")

    st.markdown("""
    ### 🌳 II. Parse Trees (Derivation Trees)
    A **Parse Tree** is a graphical representation of a derivation. It shows how the start symbol of a grammar is transformed into a specific string of terminals.

    #### 1. Structural Components
    *   **Root Node:** Always the **Start Symbol (S)** of the grammar.
    *   **Interior Nodes:** Always **Non-Terminals (N)**. They represent a production rule being applied.
    *   **Leaf Nodes:** These are **Terminals (T)** or the empty string ($\lambda$). Read from left to right to form the yield.
    *   **Branches:** Represent the application of a production rule ($A \to XYZ$).

    #### 2. Properties of Parse Trees
    *   **Yield:** The string formed by concatenating the leaves from left to right.
    *   **In-Order Traversal:** Walking the tree from left to right generates the original input string.
    *   **Ambiguity:** If a string has **two or more different parse trees** for the same grammar, the grammar is **Ambiguous**. *Compilers hate ambiguity!*
    """)

    st.info("💡 **Ambiguity** is dangerous because it leads to multiple interpretations of the same code (e.g., math precedence).")

    st.markdown("---")

    st.markdown("""
    ### 📝 III. Example: From Rule to Tree
    Suppose we have a **Type 2 Grammar (CFG)** for simple math:
    1. $E \to E + E$
    2. $E \to id$

    **To derive the string** `id + id`:
    1. Start with **E** (Root).
    2. Apply $E \to E + E$ (Internal nodes $E$, $E$ and terminal $+$).
    3. Apply $E \to id$ for both children.
    4. **Result:** The leaves read "id + id".
    """)

    st.graphviz_chart('''
    digraph {
        rankdir=TB;
        bgcolor="transparent";
        node [shape=circle, fontcolor=white, color=white];
        edge [color=white, fontcolor=white];
        
        E1 [label="E (Root)"];
        E2 [label="E"];
        Plus [label="+ (Terminal)", shape=none];
        E3 [label="E"];
        id1 [label="id (Leaf)", shape=none];
        id2 [label="id (Leaf)", shape=none];
        
        E1 -> E2;
        E1 -> Plus;
        E1 -> E3;
        E2 -> id1;
        E3 -> id2;
    }
    ''')

    st.markdown("### 🏁 Summary: Grammar vs. Machine")
    st.table(pd.DataFrame([
        {"Grammar Type": "Type 3", "Machine Equivalent": "Finite Automata", "Memory Type": "None"},
        {"Grammar Type": "Type 2", "Machine Equivalent": "Pushdown Automata", "Memory Type": "Stack"},
        {"Grammar Type": "Type 1", "Machine Equivalent": "Linear Bounded Automata", "Memory Type": "Restricted Tape"},
        {"Grammar Type": "Type 0", "Machine Equivalent": "Turing Machine", "Memory Type": "Infinite Tape"}
    ]))

    if st.button("Next: 3.4 Derivations (LMD & RMD) ➡️", use_container_width=True):
        st.session_state.unit1_topic = "3.4 Derivations (LMD & RMD)"
        st.rerun()

def render_derivations():
    st.subheader("3.4 Derivations: The Path to Generation")
    
    st.markdown(r"""
    ### 1️⃣ Meaning / Definition
    A **derivation** is a step-by-step process of generating a string from a grammar by repeatedly applying production rules.
    
    Let a grammar be $G = (N, T, P, S)$. A derivation starts from the start symbol $S$ and applies rules in $P$ until a string made only of terminals is obtained:
    """)
    st.latex(r"S \Rightarrow \alpha_1 \Rightarrow \alpha_2 \Rightarrow \dots \Rightarrow \alpha_n")
    
    st.markdown(r"""
    *   Each $\alpha_i \in (N \cup T)^*$ is called a **sentential form**.
    *   If $\alpha_n \in T^*$, it is a valid string of the language.

    #### 📝 Notation
    | Symbol | Meaning |
    | :--- | :--- |
    | $\Rightarrow$ | One-step derivation (apply one rule once) |
    | $\Rightarrow^*$ | Zero or more steps (multi-step) |
    | $\Rightarrow^+$ | One or more steps |
    | $S \Rightarrow^* w$ | The grammar **generates** string $w$ (where $w \in T^*$) |

    ---

    ### 2️⃣ Types of Derivation
    
    #### A) Left-Most Derivation (LMD)
    The **left-most non-terminal** is always replaced first at every step.
    *   **Notation:** $\Rightarrow_{lm}$
    *   **Use:** Standard for **Top-Down Parsing** (e.g., LL Parsers).

    """)

    st.markdown(r"""
    #### B) Right-Most Derivation (RMD)
    The **right-most non-terminal** is always replaced first at every step.
    *   **Notation:** $\Rightarrow_{rm}$
    *   **Use:** Standard for **Bottom-Up Parsing** (LR Parsers use the reverse of RMD).
    """)

    st.markdown(r"""
    ---

    ### 🎓 Example: $id + id * id$
    **Formal Specification:**
    *   **N** = {E}
    *   **T** = {id, +, *}
    *   **P** = { 
        *   $E \to E + E$
        *   $E \to E * E$
        *   $E \to (E)$
        *   $E \to id$
    }
    *   **S** = E
    
    | Left-Most Derivation (LMD) | Right-Most Derivation (RMD) |
    | :--- | :--- |
    | $E \Rightarrow_{lm} E + E$ | $E \Rightarrow_{rm} E + E$ |
    | $\Rightarrow_{lm} id + E$ | $\Rightarrow_{rm} E + E * E$ |
    | $\Rightarrow_{lm} id + E * E$ | $\Rightarrow_{rm} E + E * id$ |
    | $\Rightarrow_{lm} id + id * E$ | $\Rightarrow_{rm} E + id * id$ |
    | $\Rightarrow_{lm} id + id * id$ | $\Rightarrow_{rm} id + id * id$ |

    ---

    ### 🎲 Practice: Random Derivation Examples
    """)

    if st.button("Generate Random Example 🔄"):
        exs = [
            {
                "N": ["E"], "T": ["id", "+", "*", "(", ")"], "S": "E",
                "rules": "E -> E+E | E*E | (E) | id",
                "gram_desc": "Arithmetic Grammar",
                "str": "id+id*id",
            },
            {
                "N": ["S"], "T": ["(", ")", "ε"], "S": "S",
                "rules": "S -> SS | (S) | ε",
                "gram_desc": "Balanced Parentheses",
                "str": "(()())",
            },
            {
                "N": ["S"], "T": ["a", "b", "ε"], "S": "S",
                "rules": "S -> aSa | bSb | a | b | ε",
                "gram_desc": "Palindrome Grammar",
                "str": "aba",
            }
        ]
        sel = random.choice(exs)
        st.session_state.rand_derivation = sel

    if "rand_derivation" in st.session_state:
        d = st.session_state.rand_derivation
        
        # Consistent Grammar Parsing for Solver
        grammar = {}
        P_display = []
        for line in d['rules'].split("|"):
            if "->" in line:
                lhs, rhs = line.split("->")
                lhs = lhs.strip()
                rhs = rhs.strip()
            else:
                lhs = d['S']
                rhs = line.strip()
            
            if lhs not in grammar: grammar[lhs] = []
            # Only treat as epsilon if it's the standalone right-hand side
            clean_rhs = "" if rhs.strip() in ["ε", "e", "lambda"] else rhs.strip()
            grammar[lhs].append(clean_rhs)
            P_display.append(f"{lhs} → {rhs.strip()}")

        st.markdown("#### 📐 Formal Specification")
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            st.markdown(f"**N**: {{{', '.join(d['N'])}}}  \n**T**: {{{', '.join(d['T'])}}}  \n**S**: {d['S']}")
        with c_r2:
            st.markdown("**P (Productions):**")
            for p in P_display: st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;• {p}")
        
        st.info(f"**Target String:** `{d['str']}` ({d.get('gram_desc', '')})")
        
        # BFS Searcher logic
        N_set = set(d['N'])
        nt_regex = "|".join([re.escape(nt) for nt in sorted(list(N_set), key=len, reverse=True)])

        def solve(mode="LMD"):
            from collections import deque
            # Handle ε, e, lambda in grammar
            clean_grammar = {}
            for line in d['rules'].split("|"):
                if "->" in line:
                    lhs, rhs = line.split("->")
                    lhs = lhs.strip(); rhs = rhs.strip()
                else:
                    lhs = d['S']; rhs = line.strip()
                
                if lhs not in clean_grammar: clean_grammar[lhs] = []
                rhs_clean = "" if rhs.strip() in ["ε", "e", "lambda"] else rhs.strip()
                clean_grammar[lhs].append(rhs_clean)

                target_norm = " ".join(d['str'].split())
                queue = deque([(d['S'], [d['S']])])
                visited = {} # string -> shortest_path_length
                visited[d['S']] = 0
                all_shortest_paths = []
                shortest_len = float('inf')
                
                while queue:
                    curr, path = queue.popleft()
                    if len(path) > shortest_len: break
                    
                    if " ".join(curr.split()) == target_norm:
                        shortest_len = len(path)
                        all_shortest_paths.append(path)
                        continue
                    
                    if len(curr) > len(d['str']) + 15: continue
                    matches = list(re.finditer(nt_regex, curr))
                    if not matches: continue
                    m = matches[0] if mode == "LMD" else matches[-1]
                    target_nt = m.group(); idx = m.start()
                    for replacement in clean_grammar.get(target_nt, []):
                        new_str = curr[:idx] + replacement + curr[idx + len(target_nt):]
                        if new_str not in visited or visited[new_str] == len(path):
                            visited[new_str] = len(path)
                            queue.append((new_str, path + [new_str]))
            
            unique_paths = []
            for p in all_shortest_paths:
                if p not in unique_paths: unique_paths.append(p)
            return unique_paths

        def render_deriv_steps(paths, title, align="left"):
            st.markdown(f"##### {title}")
            if not paths:
                st.warning("No derivation found")
                return

            for idx, steps in enumerate(paths):
                if len(paths) > 1:
                    st.caption(f"Path Option {idx + 1}:")
                
                deriv_html = []
                for i, s in enumerate(steps):
                    disp = s if s != "" else "ε"
                    if i == 0:
                        line = f"{disp}"
                    else:
                        if align == "left":
                            line = f"&#8658; {disp}"
                        else:
                            line = f"{disp} &#8656;"
                    deriv_html.append(f"<div style='margin-bottom: 8px; white-space: nowrap;'>{line}</div>")
                
                st.markdown(f"""
                    <div style='background: #111827; padding: 20px; border-radius: 10px; border: 1px solid #3b82f6; 
                                color: #f9fafb; font-family: "Inter", "Source Code Pro", monospace; 
                                text-align: {align}; font-size: 1.1rem; overflow-x: auto; margin-bottom: 15px;'>
                        {''.join(deriv_html)}
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        l_paths = solve("LMD")
        r_paths = solve("RMD")

        # Ambiguity Status for Random Examples
        if len(l_paths) > 1:
            st.error("⚖️ **Note:** This example grammar is **AMBIGUOUS** for this string!")
            st.warning(f"Found {len(l_paths)} distinct Left-Most Derivations.")
        
        c1, c2 = st.columns(2)
        with c1: render_deriv_steps(l_paths, "⬅️ Left-Most Derivation", align="left")
        with c2: render_deriv_steps(r_paths, "➡️ Right-Most Derivation", align="right")

    st.markdown("---")
    st.subheader("🛠️ Interactive Derivation Lab")
    st.write("Enter your grammar rules and a target string to see the step-by-step LMD/RMD!")

    col1, col2 = st.columns([2, 1])
    with col1:
        user_rules = st.text_area("Enter Rules (one per line, e.g., S -> aS | b)", value="E -> E+E | id")
        user_string = st.text_input("Target String (e.g., id+id):", value="id+id")
    
    with col2:
        st.caption("Instructions:")
        st.markdown("""
        - Use `->` for rules.
        - Use `|` for multiple choices.
        - First rule's LHS is the **Start Symbol**.
        """)

    if st.button("🧩 Solve Derivation"):
        # Improved Parser for User Grammar
        grammar = {}
        start_sym = None
        N = set()
        T = set()
        P_list = []
        
        try:
            # First pass: Identify Non-Terminals (N) and Start Symbol (S)
            for line in user_rules.split("\n"):
                line = line.strip()
                if not line or "->" not in line: continue
                lhs, rhs = line.split("->")
                lhs = lhs.strip()
                if not start_sym: start_sym = lhs
                N.add(lhs)
                
            # Sort NTs by length descending for better matching
            sorted_nts = sorted(list(N), key=len, reverse=True)
            nt_regex_pre = "|".join([re.escape(nt) for nt in sorted_nts]) if sorted_nts else r"(?!)"
            
            # Second pass: Build Grammar and Identify Terminals (T)
            for line in user_rules.split("\n"):
                line = line.strip()
                if not line or "->" not in line: continue
                lhs, rhs = line.split("->")
                lhs = lhs.strip()
                choices = [c.strip() for c in rhs.split("|")]
                if lhs not in grammar: grammar[lhs] = []
                
                for res in choices:
                    # Only treat as epsilon if it's the standalone right-hand side
                    clean_res = "" if res.strip() in ["ε", "e", "lambda"] else res.strip()
                    grammar[lhs].append(clean_res)
                    P_list.append(f"{lhs} → {res}")
                    
                    # Improved Terminal Detection: use non-terminal regex to avoid splitting (e.g., S')
                    tokens = re.findall(nt_regex_pre + r"|id|[a-zA-Z]+|[^a-zA-Z\sεe|]", res)
                    for tok in tokens:
                        if tok not in N and tok not in ['ε', 'e', ' ', '|']:
                            T.add(tok)

            # --- Display Formal Specification ---
            st.markdown("#### 📐 Formal Specification")
            col_spec1, col_spec2 = st.columns(2)
            with col_spec1:
                st.markdown(f"**N (Non-Terminals):** {{{', '.join(sorted(N))}}}")
                st.markdown(f"**T (Terminals):** {{{', '.join(sorted(T))}}}")
                st.markdown(f"**S (Start Symbol):** {start_sym}")
            with col_spec2:
                st.markdown("**P (Productions):**")
                for p in P_list:
                    st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;• {p}")

            # --- Improved BFS Derivation Searcher ---
            from collections import deque
            
            # Sort NTs by length descending to match longest possible NT first
            sorted_nts = sorted(list(N), key=len, reverse=True)
            nt_regex = "|".join([re.escape(nt) for nt in sorted_nts])

            def get_derivations(mode="LMD"):
                # Returns a list of all shortest paths
                target_norm = " ".join(user_string.split())
                queue = deque([(start_sym, [start_sym])])
                visited = {} # string -> shortest_path_length
                visited[start_sym] = 0
                all_shortest_paths = []
                shortest_len = float('inf')
                
                while queue:
                    curr, path = queue.popleft()
                    
                    if len(path) > shortest_len:
                        break # Found all shortest paths already
                        
                    if " ".join(curr.split()) == target_norm:
                        shortest_len = len(path)
                        all_shortest_paths.append(path)
                        continue
                        
                    if len(curr) > len(user_string) + 15: continue
                    if len(path) > 15: continue # Safety break
                    
                    # Find all non-terminals in current sentential form
                    matches = list(re.finditer(nt_regex, curr))
                    if not matches: continue
                    
                    # Pick target NT based on mode
                    m = matches[0] if mode == "LMD" else matches[-1]
                    target_nt = m.group()
                    idx = m.start()

                    for replacement in grammar.get(target_nt, []):
                        new_str = curr[:idx] + replacement + curr[idx + len(target_nt):]
                        
                        # In BFS, the first time we see a node it's via the shortest path.
                        # However, we want to find ALL paths of that same shortest length.
                        if new_str not in visited or visited[new_str] == len(path):
                            visited[new_str] = len(path)
                            queue.append((new_str, path + [new_str]))
                
                # Filter to unique paths (standard LMD should be unique if same choices, but BFS might explore overlap)
                unique_paths = []
                for p in all_shortest_paths:
                    if p not in unique_paths:
                        unique_paths.append(p)
                return unique_paths

            lmd_paths = get_derivations("LMD")
            rmd_paths = get_derivations("RMD")

            st.markdown("---")
            
            # --- Ambiguity Result ---
            is_ambiguous = len(lmd_paths) > 1
            if is_ambiguous:
                st.error("⚖️ **Grammar is AMBIGUOUS!**")
                st.warning(f"Found {len(lmd_paths)} distinct Left-Most Derivation paths for `{user_string}`.")
            else:
                if lmd_paths:
                    st.success("⚖️ **Grammar is UNAMBIGUOUS** (for this string shortest path).")
                else:
                    st.error("❌ No derivation found for the given string.")

            c1, c2 = st.columns(2)
            
            def render_interactive_box(paths, title, align="left"):
                st.markdown(f"##### {title}")
                if not paths:
                    st.warning("No path found")
                    return

                for idx, steps in enumerate(paths):
                    if len(paths) > 1:
                        st.caption(f"Path Option {idx + 1}:")
                    
                    deriv_html = []
                    for i, s in enumerate(steps):
                        disp = s if s != "" else "ε"
                        if i == 0:
                            line = f"{disp}"
                        else:
                            if align == "left":
                                line = f"&#8658; {disp}"
                            else:
                                line = f"{disp} &#8656;"
                        deriv_html.append(f"<div style='margin-bottom: 8px; white-space: nowrap;'>{line}</div>")
                    
                    st.markdown(f"""
                        <div style='background: #111827; padding: 20px; border-radius: 10px; border: 1px solid #3b82f6; 
                                    color: #f9fafb; font-family: "Inter", "Source Code Pro", monospace; 
                                    text-align: {align}; font-size: 1.1rem; overflow-x: auto; margin-bottom: 15px;'>
                            {''.join(deriv_html)}
                        </div>
                    """, unsafe_allow_html=True)

            with c1: render_interactive_box(lmd_paths, "⬅️ Left-Most Derivation", align="left")
            with c2: render_interactive_box(rmd_paths, "➡️ Right-Most Derivation", align="right")
                
        except Exception as e:
            st.error(f"Solver Error: {e}")

    st.markdown("---")
    st.markdown("### 📌 Key Exam Points")
    st.markdown(r"""
    1.  **Sentential Forms:** These are strings like $(\text{id} + E)$ that contain both terminals and non-terminals.
    2.  **LMD vs RMD:** LMD expands the left-most non-terminal first; RMD expands the right-most.
    3.  **Unique Derivations:** For unambiguous grammars, there is exactly one LMD and one RMD for any valid string.
    """)

    if st.button("Next: Reduction ➡️", use_container_width=True):
        st.session_state.selected_topic = "3.5 Reduction (Process & Example)"
        st.rerun()

def render_reduction():
    st.header("📉 3.5 Reduction: The Reverse Process")
    
    st.markdown("""
    ### 🧬 Definition
    **Reduction** refers to the process of replacing a sequence of symbols (a string) that matches the **Right-Hand Side (R.H.S.)** of a production rule with the **Non-Terminal symbol** on the **Left-Hand Side (L.H.S.)**.
    
    Effectively, this process works backward to reduce a string of terminals and non-terminals closer to the **Start Symbol** of the grammar.
    """)

    st.info(r"""
    💡 **Key Insight:** Reduction is the **reverse of derivation**. 
    - **Derivation:** Start Symbol $\Rightarrow$ String (Expansion)
    - **Reduction:** String $\Rightarrow$ Start Symbol (Contraction)
    """)

    st.warning("⚠️ **Note:** Not all strings are reducible to the start symbol. Only valid strings belonging to the grammar can be fully reduced.")

    st.divider()
    st.subheader("📝 Example: Step-by-Step Reduction")
    
    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        st.markdown("**1. Given Grammar**")
        st.code("""
E -> E + T
E -> T
T -> id
        """, language="text")
    
    with col_ex2:
        st.markdown("**2. Target String**")
        st.markdown("`id + id`")

    st.markdown("**3. Reduction Process**")
    st.markdown("We search for matches on the Right-Hand Side (R.H.S.) and replace them with the corresponding Left-Hand Side (L.H.S.).")

    reduction_data = [
        {"Current String": "id + id", "Reduction Applied": "Initial String", "Rule Used": "-"},
        {"Current String": "T + id", "Reduction Applied": "Replace first `id` with `T`", "Rule Used": "T → id"},
        {"Current String": "E + id", "Reduction Applied": "Replace `T` with `E`", "Rule Used": "E → T"},
        {"Current String": "E + T", "Reduction Applied": "Replace second `id` with `T`", "Rule Used": "T → id"},
        {"Current String": "E", "Reduction Applied": "**Start Symbol reached**", "Rule Used": "E → E + T"},
    ]
    
    df_reduction = pd.DataFrame(reduction_data)
    st.table(df_reduction)

    st.markdown("### 🔄 Reverse Derivation Summary")
    st.markdown("The sequence of reductions performed (read from top to bottom) is exactly the inverse of a Right-Most Derivation in reverse.")
    
    st.success("🎉 **Reduction Complete!** The string `id + id` is valid.")

    st.divider()
    st.subheader("🧪 Interactive Reduction Lab")
    st.markdown("Try your own grammar and string to see the step-by-step reduction process.")
    
    ir_c1, ir_c2 = st.columns([2, 1])
    with ir_c1:
        u_rules_redir = st.text_area("Grammar (e.g., E -> E+T | T):", value="E -> E+T | T\nT -> id", key="redu_rules")
        u_str_redir = st.text_input("Target String:", value="id+id", key="redu_str")
    with ir_c2:
        st.info("""
        **Solver Logic:**
        - This tool finds a sequence of **Reductions** (L.H.S. replacements) that lead back to the Start Symbol.
        - It's essentially the inverse of a Right-Most Derivation.
        """)

    if st.button("🔍 Solve Step-by-Step Reduction", use_container_width=True):
        from collections import deque
        import re
        try:
            # 1. Parse Grammar & Extract All Symbols
            grammar_list = []
            non_terminals = set()
            all_grammar_symbols = set()
            start_symbol = None
            
            for line in u_rules_redir.split("\n"):
                if "->" in line:
                    lhs, rhs_blob = line.split("->")
                    lhs = lhs.strip()
                    if not start_symbol: start_symbol = lhs
                    non_terminals.add(lhs)
                    all_grammar_symbols.add(lhs)
                    # Extract tokens from RHS to build a master lexer
                    rhs_opts = rhs_blob.split("|")
                    for opt in rhs_opts:
                        # Extract symbols like alphanumeric words or single special chars
                        syms = re.findall(r"[a-zA-Z0-9]+|[^a-zA-Z0-9\s]", opt)
                        grammar_list.append((lhs, syms))
                        for s in syms: all_grammar_symbols.add(s)

            # 2. Robust Tokenizer (Reuse logic from Shift-Reduce fix)
            sorted_symbols = sorted(list(all_grammar_symbols), key=len, reverse=True)
            token_regex = "|".join([re.escape(s) for s in sorted_symbols if s.strip()])

            def intelligent_tokenize(text):
                # If there are spaces, tokenize by spaces first, then check bits
                if " " in text.strip():
                    raw_parts = text.strip().split()
                    out = []
                    for p in raw_parts:
                        found = re.findall(token_regex, p, re.IGNORECASE)
                        out.extend(found if found else [p])
                    return out
                else:
                    # No spaces: use the grammar symbols to partition the string
                    return re.findall(token_regex, text, re.IGNORECASE)

            # Map tokens back to the exact case used in the grammar
            raw_input_tokens = intelligent_tokenize(u_str_redir)
            input_tokens = []
            for rit in raw_input_tokens:
                match = next((s for s in all_grammar_symbols if s == rit), None)
                if not match:
                    match = next((s for s in all_grammar_symbols if s.lower() == rit.lower()), rit)
                input_tokens.append(match)

            st.info(f"🔍 **Detected Tokens:** `{'`, `'.join(input_tokens)}`")

            # 3. BFS Reduction Search
            queue = deque([(tuple(input_tokens), [])])
            visited = set()
            final_path = None
            max_states = 2000
            count = 0

            # Sort grammar by RHS length (longest first) for slightly better search
            sorted_grammar = sorted(grammar_list, key=lambda x: len(x[1]), reverse=True)

            while queue and count < max_states:
                curr_tokens, history = queue.popleft()
                count += 1
                
                if curr_tokens in visited: continue
                visited.add(curr_tokens)

                # Check Success
                if list(curr_tokens) == [start_symbol]:
                    final_path = history + [{"Current String": " ".join(curr_tokens), "Reduction Applied": "**Start Symbol reached**", "Rule Used": "-"}]
                    break

                # Try all possible reductions
                for lhs, rhs in sorted_grammar:
                    n = len(rhs)
                    if not rhs or rhs == [""]: continue
                    for i in range(len(curr_tokens) - n + 1):
                        if list(curr_tokens[i:i+n]) == rhs:
                            new_toks = curr_tokens[:i] + (lhs,) + curr_tokens[i+n:]
                            action = f"Replace `{' '.join(rhs)}` with `{lhs}`"
                            new_hist = history + [{"Current String": " ".join(curr_tokens), "Reduction Applied": action, "Rule Used": f"{lhs} → {' '.join(rhs)}"}]
                            queue.append((new_toks, new_hist))

            if final_path:
                st.subheader("📊 Reduction Table")
                st.table(pd.DataFrame(final_path))
                st.success("✅ **Reduction Successful!**")
                st.balloons()
            else:
                st.error("❌ **No reduction path found.**")
                st.warning("""
                **Possible Reasons:**
                1. **Grammar Mismatch:** Your grammar might be missing a rule (e.g., if you have `cond` in the string but no rule like `S -> if E then ...`).
                2. **Start Symbol:** The parser assumed the first non-terminal defined is your target Start Symbol.
                3. **Complex Conflicts:** Some reductions might prevent others (though BFS usually finds a path if one exists).
                """)

        except Exception as e:
            st.error(f"Solver Error: {e}")

    st.divider()
    if st.button("⬅️ Previous: Derivations"):
        st.session_state.selected_topic = "3.4 Derivations (LMD & RMD)"
        st.rerun()
    
    if st.button("Next: Parse Trees & Ambiguity ➡️", use_container_width=True):
        st.session_state.selected_topic = "3.6 Parse Trees & Ambiguity (Digitized Notes)"
        st.rerun()

def render_parse_tree_notes():
    st.title("📌 3.6 Parse Trees & Ambiguity (Digitized Notes)")
    st.markdown("""
    Based on the digitized handwritten notes, this section covers the graphical representation of derivations and the fundamental concept of grammar ambiguity.
    """)

    st.markdown("---")
    st.header("1. Core Concepts: Derivation & Reduction")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.subheader("🔄 Derivation")
        st.markdown("""
        The process of **generating** a valid string starting from the Start Symbol ($S$).
        - **Flow:** $S \Rightarrow \text{LMD} / \text{RMD} \Rightarrow \text{String}$
        """)
    with col_c2:
        st.subheader("🔍 Reduction")
        st.markdown("""
        The process of **recognizing** or parsing a valid string from bottom-up.
        - **Flow:** $\text{String} \Rightarrow \text{Parsing} \Rightarrow S$
        """)

    st.info("💡 **N, T, P, S** (Non-terminals, Terminals, Productions, Start Symbol) are the inputs for both processes.")

    st.markdown("---")
    st.header("2. Parse Tree")
    st.markdown("""
    **Definition:** A **Parse Tree** is the graphical representation of a **Derivation** or **Reduction**.
    It shows how a string is derived/reduced using the production rules of a grammar.
    """)

    st.subheader("📝 Example 1: Arithmetic Expression")
    st.markdown("**Target String:** `id + id * id`  \n**Grammar:** $E \to E + E \mid E * E \mid id$")

    t_col1, t_col2 = st.columns(2)

    with t_col1:
        st.markdown("#### Case A: L.M.D Parse Tree")
        st.caption("Associates multiplication first ($id + (id * id)$)")
        dot_lmd = """
        digraph LMD {
            bgcolor="transparent";
            node [fontname="Source Code Pro", shape=circle, style=filled, fillcolor="#1e293b", fontcolor="#f8fafc", color="#3b82f6"];
            edge [color="#64748b", arrowhead=none];
            E1 [label="E"];
            E1 -> E2, PLUS, E3;
            E2 [label="E"];
            PLUS [label="+", shape=none, fillcolor=none, fontcolor="#3b82f6"];
            E3 [label="E"];
            E2 -> id1;
            id1 [label="id", shape=none, fillcolor=none, fontcolor="#10b981"];
            E3 -> E4, STAR, E5;
            E4 [label="E"];
            STAR [label="*", shape=none, fillcolor=none, fontcolor="#3b82f6"];
            E5 [label="E"];
            E4 -> id2;
            E5 -> id3;
            id2 [label="id", shape=none, fillcolor=none, fontcolor="#10b981"];
            id3 [label="id", shape=none, fillcolor=none, fontcolor="#10b981"];
        }
        """
        st.graphviz_chart(dot_lmd)

    with t_col2:
        st.markdown("#### Case B: R.M.D Parse Tree")
        st.caption("Associates addition first ($(id + id) * id$)")
        dot_rmd = """
        digraph RMD {
            bgcolor="transparent";
            node [fontname="Source Code Pro", shape=circle, style=filled, fillcolor="#1e293b", fontcolor="#f8fafc", color="#3b82f6"];
            edge [color="#64748b", arrowhead=none];
            E1 [label="E"];
            E1 -> E2, STAR, E3;
            E2 [label="E"];
            STAR [label="*", shape=none, fillcolor=none, fontcolor="#3b82f6"];
            E3 [label="E"];
            E2 -> E4, PLUS, E5;
            E4 [label="E"];
            PLUS [label="+", shape=none, fillcolor=none, fontcolor="#3b82f6"];
            E5 [label="E"];
            E4 -> id1;
            E5 -> id2;
            id1 [label="id", shape=none, fillcolor=none, fontcolor="#10b981"];
            id2 [label="id", shape=none, fillcolor=none, fontcolor="#10b981"];
            E3 -> id3;
            id3 [label="id", shape=none, fillcolor=none, fontcolor="#10b981"];
        }
        """
        st.graphviz_chart(dot_rmd)

    st.markdown("---")
    st.header("3. Ambiguous Grammar")
    st.warning("""
    **Observation:** The string `id + id * id` produced **two different parse trees** with different meanings (precedence) using the same grammar.
    
    **Rule:** If a string produced by a grammar has more than one distinct parse tree (different structures), the grammar is **Ambiguous**.
    """)

    st.markdown("""
    ### ⚖️ The Ambiguity Test
    For any string generated by a grammar:
    - If the **Left Most Parse Tree (LMPT)** and the **Right Most Parse Tree (RMPT)** are **IDENTICAL**, the grammar is **Unambiguous**.
    - If they are **DIFFERENT**, the grammar is **Ambiguous**.
    """)

    st.markdown("---")
    st.header("4. Example 2: Parentheses String")
    st.markdown("**Target String:** `( ) ( )`  \n**Grammar:** $S \to (S)S \mid \epsilon$")
    
    p_col1, p_col2 = st.columns([1, 1])
    with p_col1:
        st.markdown("#### L.M.D Parse Tree")
        dot_paren = """
        digraph PAREN {
            bgcolor="transparent";
            node [fontname="Source Code Pro", shape=circle, style=filled, fillcolor="#1e293b", fontcolor="#f8fafc", color="#3b82f6"];
            edge [color="#64748b", arrowhead=none];
            S1 [label="S"];
            S1 -> L1, S2, R1, S3;
            L1 [label="(", shape=none, fontcolor="#3b82f6"];
            S2 [label="S"];
            R1 [label=")", shape=none, fontcolor="#3b82f6"];
            S3 [label="S"];
            S2 -> EPS1 [label="λ"];
            EPS1 [label="λ", shape=none, fontcolor="#64748b"];
            S3 -> L2, S4, R2, S5;
            L2 [label="(", shape=none, fontcolor="#3b82f6"];
            S4 [label="S"];
            R2 [label=")", shape=none, fontcolor="#3b82f6"];
            S5 [label="S"];
            S4 -> EPS2 [label="λ"];
            EPS2 [label="λ", shape=none, fontcolor="#64748b"];
            S5 -> EPS3 [label="λ"];
            EPS3 [label="λ", shape=none, fontcolor="#64748b"];
        }
        """
        st.graphviz_chart(dot_paren)
    
    with p_col2:
        st.markdown("#### Derivation Steps (LMD)")
        st.code("""
1. S → (S)S
2. S → (λ)S      = ()S
3. S → ()(S)S   = ()(S)S
4. S → ()(λ)S   = ()()S
5. S → ()()λ    = ()()
        """, language="text")

    st.markdown("---")
    st.header("5. 🧪 Live Ambiguity Test Lab")
    st.write("Enter your grammar rules and a target string. If the system finds more than one shortest Left-Most Derivation (LMD), the grammar is officially **Ambiguous** for that string.")

    lab_c1, lab_c2 = st.columns([2, 1])
    with lab_c1:
        u_rules = st.text_area("Enter Grammar (LHS -> RHS | RHS):", value="E -> E+E | id", key="ambig_rules")
        u_str = st.text_input("Target String:", value="id+id+id", key="ambig_str")
    with lab_c2:
        st.caption("Instructions:")
        st.markdown("""
        - Use `->` for rules.
        - First LHS is **Start Symbol**.
        - `|` separates options.
        """)

    if st.button("⚖️ Run Ambiguity Test", use_container_width=True):
        # --- Local Solver for Ambiguity Lab ---
        from collections import deque
        try:
            grammar = {}
            start_sym = None
            N = set()
            
            for line in u_rules.split("\n"):
                line = line.strip()
                if not line or "->" not in line: continue
                lhs, rhs = line.split("->")
                lhs = lhs.strip(); rhs = [c.strip() for c in rhs.split("|")]
                if not start_sym: start_sym = lhs
                N.add(lhs)
                if lhs not in grammar: grammar[lhs] = []
                for r in rhs:
                    clean_r = "" if r.strip() in ["ε", "e", "lambda"] else r.strip()
                    grammar[lhs].append(clean_r)

            sorted_nts = sorted(list(N), key=len, reverse=True)
            nt_reg = "|".join([re.escape(nt) for nt in sorted_nts])

            def find_all_lmds(target):
                target_norm = " ".join(target.split())
                queue = deque([(start_sym, [start_sym])])
                visited = {} # string -> min_steps
                visited[start_sym] = 0
                results = []
                min_len = float('inf')
                
                while queue:
                    curr, path = queue.popleft()
                    if len(path) > min_len: break
                    
                    if " ".join(curr.split()) == target_norm:
                        min_len = len(path)
                        if path not in results: results.append(path)
                        continue
                    
                    if len(curr) > len(target) + 15: continue
                    if len(path) > 15: continue
                    
                    matches = list(re.finditer(nt_reg, curr))
                    if not matches: continue
                    
                    m = matches[0] # Always Left-Most for LMD
                    t_nt = m.group(); idx = m.start()
                    for repl in grammar.get(t_nt, []):
                        nxt = curr[:idx] + repl + curr[idx + len(t_nt):]
                        if nxt not in visited or visited[nxt] == len(path):
                            visited[nxt] = len(path)
                            queue.append((nxt, path + [nxt]))
                return results

            steps_list = find_all_lmds(u_str)

            st.markdown("### 📊 Test Result")
            if not steps_list:
                st.error("❌ **No derivation found.** The string cannot be generated by this grammar.")
            elif len(steps_list) > 1:
                st.error(f"⚖️ **Status: AMBIGUOUS**")
                st.warning(f"Found **{len(steps_list)}** distinct Left-Most Derivations for `{u_str}`.")
                
                # Show all paths side-by-side or in sequence
                cols = st.columns(len(steps_list))
                for i, path in enumerate(steps_list):
                    with cols[i]:
                        st.caption(f"Path Option {i+1}:")
                        html = []
                        for j, step in enumerate(path):
                            disp = step if step != "" else "ε"
                            line = f"{disp}" if j == 0 else f"&#8658; {disp}"
                            html.append(f"<div style='margin-bottom: 5px; font-family: monospace;'>{line}</div>")
                        st.markdown(f"<div style='background: #111827; padding:15px; border-radius:10px; border:1px solid #ef4444;'>{''.join(html)}</div>", unsafe_allow_html=True)
            else:
                st.success("⚖️ **Status: UNAMBIGUOUS**")
                st.info(f"Only one shortest Left-Most Derivation found for `{u_str}`. This suggests the grammar is unambiguous for this specific string.")
                path = steps_list[0]
                html = []
                for j, step in enumerate(path):
                    disp = step if step != "" else "ε"
                    line = f"{disp}" if j == 0 else f"&#8658; {disp}"
                    html.append(f"<div style='margin-bottom: 5px; font-family: monospace;'>{line}</div>")
                st.markdown(f"<div style='background: #111827; padding:15px; border-radius:10px; border:1px solid #10b981;'>{''.join(html)}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error in Ambiguity Checker: {e}")

    st.markdown("---")
    if st.button("⬅️ Previous: Reduction"):
        st.session_state.selected_topic = "3.5 Reduction (Process & Example)"
        st.rerun()

    st.markdown("### 📌 Key Exam Points")
    st.markdown(r"""
    1.  **Sentential Forms:** Can contain both terminals and non-terminals.
    2.  **LMD vs RMD:** LMD expands from the left; RMD expands from the right.
    3.  **Ambiguity:** Grammar is ambiguous if a string has more than one parse tree.
    """)

    if st.button("Next: Syntax Analysis Overview ➡️", use_container_width=True):
        st.session_state.selected_topic = "4.0 Syntax Analysis Overview & Top-Down Parser"
        st.rerun()
# Heartbeat: 2026-01-16 14:15
