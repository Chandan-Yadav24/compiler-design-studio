import streamlit as st
import pandas as pd
import re

class SDTNode:
    def __init__(self, label, val=None, children=None):
        self.label = label
        self.val = val
        self.children = children or []
        self.node_id = str(id(self))

def parse_sdt_expression(expr, sdd_df):
    """
    Parses an expression and evaluates synthesized attributes based on local SDD rules.
    """
    # Normalize input
    expr = expr.replace(" ", "").replace("$", "")
    tokens = re.findall(r"\d+|[+*()]", expr)
    
    # Map rule IDs to semantic action strings for detection
    rules_dict = {row["ID"]: row["Semantic Action"] for _, row in sdd_df.iterrows()}

    pos = 0
    def peek(): return tokens[pos] if pos < len(tokens) else None
    def consume():
        nonlocal pos
        res = tokens[pos]
        pos += 1
        return res

    def get_action_val(rule_id, default_val, **kwargs):
        """
        Heuristic interpreter to simulate synthesized attribute evaluation from the table.
        """
        action = rules_dict.get(rule_id, "")
        try:
            # Multi-digit formation: I -> I digit
            if "I.val = (10" in action or "10" in action:
                return (10 * kwargs.get('i1', 0)) + kwargs.get('digit', 0)
            # Digit base: I -> digit
            elif "digit.lexval" in action:
                return kwargs.get('digit', 0)
            # Addition: E -> E + E
            elif "+" in action:
                return kwargs.get('e1', 0) + kwargs.get('e2', 0)
            # Multiplication: E -> E * E
            elif "*" in action:
                return kwargs.get('e1', 0) * kwargs.get('e2', 0)
            # Subtraction: (Custom support)
            elif "-" in action:
                return kwargs.get('e1', 0) - kwargs.get('e2', 0)
            # Simple assignment: E -> I or E -> (E)
            elif "E.val = I.val" in action or "E.val = E1.val" in action:
                return kwargs.get('val', 0)
            return default_val
        except:
            return default_val

    def parse_number():
        num_str = consume()
        prev_i = None
        for i, digit in enumerate(num_str):
            d_val = int(digit)
            d_node = SDTNode(f"digit (lexval={digit})", val=d_val)
            if i == 0:
                # Rule 6: I -> digit
                i_val = get_action_val(6, d_val, digit=d_val)
                curr_i = SDTNode(f"I (val={i_val})", val=i_val, children=[d_node])
            else:
                # Rule 5: I -> I digit
                i_val = get_action_val(5, (prev_i.val * 10 + d_val), i1=prev_i.val, digit=d_val)
                curr_i = SDTNode(f"I (val={i_val})", val=i_val, children=[prev_i, d_node])
            prev_i = curr_i
        
        # Rule 4: E -> I
        e_val = get_action_val(4, prev_i.val, val=prev_i.val)
        e_node = SDTNode(f"E (val={e_val})", val=e_val, children=[prev_i])
        return e_node

    def parse_factor():
        if peek() == "(":
            consume() 
            node = parse_expr()
            if peek() == ")": consume() 
            # Rule 3: E -> ( E )
            e_val = get_action_val(3, node.val, val=node.val)
            return SDTNode(f"E (val={e_val})", val=e_val, children=[SDTNode("("), node, SDTNode(")")])
        else:
            return parse_number()

    def parse_term():
        left = parse_factor()
        while peek() == "*":
            consume() # consume *
            right = parse_factor()
            # Rule 2: E -> E * E
            new_val = get_action_val(2, (left.val * right.val), e1=left.val, e2=right.val)
            left = SDTNode(f"E (val={new_val})", val=new_val, children=[left, SDTNode("*"), right])
        return left

    def parse_expr():
        left = parse_term()
        while peek() == "+":
            consume() # consume +
            right = parse_term()
            # Rule 1: E -> E + E
            new_val = get_action_val(1, (left.val + right.val), e1=left.val, e2=right.val)
            left = SDTNode(f"E (val={new_val})", val=new_val, children=[left, SDTNode("+"), right])
        return left

    try:
        if not tokens: return None, "Empty expression"
        root_e = parse_expr()
        # Rule 0: S -> E $
        s_val = get_action_val(0, root_e.val, val=root_e.val)
        root = SDTNode(f"S (val={s_val})", val=s_val, children=[root_e, SDTNode("$")])
        return root, None
    except Exception as e:
        return None, str(e)

def generate_dot(node, dot_lines=None):
    if dot_lines is None:
        dot_lines = [
            "digraph G {", 
            "  bgcolor=\"transparent\";",
            "  node [style=filled, fillcolor=\"#1e293b\", color=\"#334155\", fontcolor=white, fontname=\"Inter\", shape=box, style=\"filled,rounded\"];", 
            "  edge [color=\"#94a3b8\", fontname=\"Inter\", fontsize=10];"
        ]
    
    # Escape quotes and formatting
    clean_label = node.label.replace('"', '\\"')
    
    # Highlight nodes with values
    style = ""
    if "val=" in clean_label:
        style = " ,fillcolor=\"#1d4ed8\"" # Blue highlight for synthesized nodes
        
    dot_lines.append(f"  {node.node_id} [label=\"{clean_label}\"{style}];")
    
    for child in node.children:
        dot_lines.append(f"  {node.node_id} -> {child.node_id};")
        generate_dot(child, dot_lines)
        
    if node.label.startswith("S (val="):
        dot_lines.append("}")
        return "\n".join(dot_lines)
    return dot_lines

def render_semantic_analysis():
    st.title("🧠 5.1 Semantic Analysis (SDT & SDD)")
    
    st.markdown(r"""
    **Semantic Analysis** checks for logic and calculates meanings using **Syntax Directed Translation (SDT)**.
    In this laboratory, you can define **Production Rules** and **Semantic Actions** to see how attributes are synthesized.
    """)

    st.divider()

    # --- SDD TABLE ---
    st.header("📊 1. SDD Table Editor")
    st.markdown("Customize the **Semantic Action** column. The tree evaluation will change dynamically!")

    # Initial data exactly as per user request
    default_sdd = pd.DataFrame([
        {"ID": 0, "Production Rule": "S → E $", "Semantic Action": "print(E.val)"},
        {"ID": 1, "Production Rule": "E → E₁ + E₂", "Semantic Action": "E.val = E₁.val + E₂.val"},
        {"ID": 2, "Production Rule": "E → E₁ * E₂", "Semantic Action": "E.val = E₁.val * E₂.val"},
        {"ID": 3, "Production Rule": "E → ( E₁ )", "Semantic Action": "E.val = E₁.val"},
        {"ID": 4, "Production Rule": "E → I", "Semantic Action": "E.val = I.val"},
        {"ID": 5, "Production Rule": "I → I₁ digit", "Semantic Action": "I.val = (10 × I₁.val) + digit.lexval"},
        {"ID": 6, "Production Rule": "I → digit", "Semantic Action": "I.val = digit.lexval"},
    ])
    
    if "sdd_rules" not in st.session_state:
        st.session_state.sdd_rules = default_sdd

    # Render editable table
    edited_sdd = st.data_editor(
        st.session_state.sdd_rules, 
        num_rows="fixed", 
        use_container_width=True,
        key="sdd_interactive_table",
        column_config={
            "ID": st.column_config.NumberColumn(disabled=True, width="small"),
            "Production Rule": st.column_config.TextColumn(disabled=True, width="medium"),
            "Semantic Action": st.column_config.TextColumn(disabled=False, width="large")
        }
    )
    st.session_state.sdd_rules = edited_sdd

    st.divider()

    # --- INTERACTIVE LAB ---
    st.header("🧪 2. Annotated Tree Solver")
    st.markdown("Enter a string like `1 + 2 + 3` to generate the **Annotated Parse Tree**.")

    col_in1, col_in2 = st.columns([3, 1])
    with col_in1:
        u_expr = st.text_input("Input String:", value="1 + 2 + 3", key="semantic_user_input")
    with col_in2:
        process_btn = st.button("🚀 Generate Tree", use_container_width=True)

    if process_btn:
        if not u_expr.strip():
            st.error("Missing input string.")
        else:
            root, error = parse_sdt_expression(u_expr, edited_sdd)
            if error:
                st.error(f"Logic Error: {error}")
                st.info("Ensure the expression matches the grammar above.")
            else:
                st.success(f"✅ Semantic Evaluation Complete! Root Result: **{root.val}**")
                
                # Display Tree with focus on synthesized attributes
                st.subheader("🌳 Annotated Parse Tree (Synthesized Attributes)")
                dot_str = generate_dot(root)
                st.graphviz_chart(dot_str)
                
                with st.expander("📚 Evaluation Insight"):
                    st.markdown("""
                    - **Annotated Parse Tree**: Each node shows its **synthesized attribute** (val).
                    - **Bottom-Up Evaluation**: Values flow from `digit.lexval` up through `I.val` to the root `S.val`.
                    - **Interactivity**: If you change the Semantic Actions in Part 1 (e.g. change `+` to `*`), the root result and tree labels will update!
                    """)

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: LL(1) Stack Simulation"):
            st.session_state.unit1_topic = "4.6 LL(1) Stack Implementation"
            st.rerun()
    with nav2:
        if st.button("Next: Intermediate Code Generation ➡️", use_container_width=True):
            st.session_state.unit1_topic = "5.2 Intermediate Code Generation"
            st.rerun()
