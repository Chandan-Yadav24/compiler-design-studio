import streamlit as st
import pandas as pd
import re

class DAGNode:
    def __init__(self, value, left=None, right=None, node_id=None):
        self.value = value
        self.left = left
        self.right = right
        self.node_id = node_id

def build_dag(expression):
    """
    Builds a Directed Acyclic Graph from an infix expression.
    Detects common sub-expressions by hashing (value, left_id, right_id).
    """
    prec = {'^': 4, '*': 3, '/': 3, '%': 3, '+': 2, '-': 2, '(': 1}
    op_stack = []
    val_stack = []
    
    # Value numbering table
    dag_nodes = {} # Key: (value, left_id, right_id) -> NodeID
    node_list = [] # To keep track of created nodes for rendering
    node_counter = 0

    def get_or_create_node(val, left_id=None, right_id=None):
        nonlocal node_counter
        key = (val, left_id, right_id)
        if key in dag_nodes:
            return dag_nodes[key]
        
        node_id = f"n{node_counter}"
        node_counter += 1
        new_node = DAGNode(val, left_id, right_id, node_id)
        dag_nodes[key] = node_id
        node_list.append(new_node)
        return node_id

    # Tokenize
    tokens = re.findall(r'[a-zA-Z0-9]+|\(|\)|\^|\*|/|%|\+|-', expression)
    
    try:
        for t in tokens:
            if re.match(r'[a-zA-Z0-9]+', t):
                # Leaf node
                val_stack.append(get_or_create_node(t))
            elif t == '(':
                op_stack.append(t)
            elif t == ')':
                while op_stack and op_stack[-1] != '(':
                    op = op_stack.pop()
                    r = val_stack.pop()
                    l = val_stack.pop()
                    val_stack.append(get_or_create_node(op, l, r))
                if op_stack: op_stack.pop()
            else:
                while op_stack and prec.get(op_stack[-1], 0) >= prec.get(t, 0):
                    op = op_stack.pop()
                    r = val_stack.pop()
                    l = val_stack.pop()
                    val_stack.append(get_or_create_node(op, l, r))
                op_stack.append(t)
        
        while op_stack:
            op = op_stack.pop()
            r = val_stack.pop()
            l = val_stack.pop()
            val_stack.append(get_or_create_node(op, l, r))
            
        return node_list, val_stack[-1] if val_stack else None, None
    except Exception as e:
        return None, None, f"Invalid Expression Syntax: {str(e)}"

def generate_dag_dot(node_list, root_id):
    """
    Generates Graphviz DOT source for the DAG.
    """
    dot = 'digraph DAG {\n'
    dot += '    rankdir=TB;\n'
    dot += '    bgcolor="transparent";\n'
    dot += '    node [shape=circle, style=filled, fillcolor="white", fontcolor="black", fontname="Courier"];\n'
    dot += '    edge [color=white, fontcolor=white];\n'
    
    for node in node_list:
        label = node.value
        dot += f'    {node.node_id} [label="{label}"];\n'
        if node.left:
            dot += f'    {node.node_id} -> {node.left} [label="L"];\n'
        if node.right:
            dot += f'    {node.node_id} -> {node.right} [label="R"];\n'
            
    # Highlight root
    if root_id:
        dot += f'    {root_id} [fillcolor="#e6ffed", penwidth=2];\n'
        
    dot += '}'
    return dot

def render_dag():
    st.title("🏗️ 5.5 Directed Acyclic Graph (DAG)")
    
    st.markdown("""
    A **Directed Acyclic Graph (DAG)** is a hierarchical representation of an expression that identifies and reuses common sub-expressions.
    """)

    st.divider()

    # --- SECTION 1: THEORY ---
    st.header("📘 1. Why use a DAG?")
    st.markdown("""
    Unlike a Syntax Tree, a DAG does not repeat nodes for the same sub-expression. 
    
    **Key Characteristics:**
    *   **Nodes:** Represent operators.
    *   **Leaves:** Represent operands (identifiers or constants).
    *   **Edges:** Connect operators to their operands.
    *   **Optimization:** Automatically identifies **Common Sub-expressions (CSEs)**.
    """)
    
    with st.expander("💡 AST vs DAG Comparison"):
        st.markdown("For expression: `a + a * (b - c) + (b - c) * d`")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Abstract Syntax Tree (AST)**")
            st.info("AST repeats `a` and `(b-c)` multiple times.")
        with c2:
            st.markdown("**Directed Acyclic Graph (DAG)**")
            st.success("DAG reuses a single node for `a` and `(b-c)`.")

    st.divider()

    # --- SECTION 2: INTERACTIVE DAG GENERATOR ---
    st.header("🧪 2. Interactive DAG Generator")
    st.markdown("Enter an expression to see how the compiler identifies and reuses sub-expressions.")

    default_expr = "a + a * (b - c) + (b - c) * d"
    u_expr = st.text_input("Input Expression:", value=default_expr, key="dag_expr_input")

    if u_expr:
        nodes, root, error = build_dag(u_expr)
        
        if error:
            st.error(error)
        elif nodes:
            st.success("✅ DAG Generated Successfully!")
            
            # Step-by-Step Explanation
            with st.expander("🚶‍♂️ How it was built (Logic)"):
                st.markdown("""
                1.  **Tokenization**: Split expression into operators and operands.
                2.  **Value Numbering**: Before creating a new node, check if a node with the same `(Value, Left, Right)` already exists.
                3.  **Reuse**: If it exists, return the existing Node ID instead of creating a duplicate.
                """)
                
                # Show node table
                table_data = []
                for n in nodes:
                    table_data.append([n.node_id, n.value, n.left if n.left else "-", n.right if n.right else "-"])
                st.table(pd.DataFrame(table_data, columns=["Node ID", "Label", "Left Child", "Right Child"]))

            # Visualization
            st.subheader("🖼️ DAG Visualization")
            dot_source = generate_dag_dot(nodes, root)
            st.graphviz_chart(dot_source)
            
            st.info("✨ **Note:** The light green node is the final root. Parallel edges to the same node indicate reused sub-expressions.")

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: Dead Code Elimination"):
            st.session_state.unit1_topic = "5.4 Dead Code Elimination"
            st.rerun()
    with nav2:
        if st.button("🎉 Unit 1 Complete!", use_container_width=True):
            st.success("Module I - Unit 1 - Front End of Compiler - Completed!")
            st.balloons()
