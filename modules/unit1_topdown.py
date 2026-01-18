import streamlit as st

def render_topdown_overview():
    st.title("🏗️ 4.0 Syntax Analysis Overview & Top-Down Parsing")
    
    st.markdown("""
    ### 📖 Syntax Analysis: Overview
    Syntax analysis involves taking a string of tokens and organizing them into a hierarchical structure called a **Parse Tree**.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌳 The Parse Tree")
        st.markdown("""
        The graphical representation of a **Derivation** or **Reduction**. It shows how the string is structured according to the grammar.
        """)
        
        st.subheader("🎯 The Goal")
        st.markdown("""
        To find a path (sequence of production rules) that moves from the **Start Symbol** to the target **String**.
        """)

    with col2:
        st.subheader("🔄 Derivation Types")
        st.markdown("""
        - **LMD (Leftmost Derivation):** Expanding from left to right.
        - **RMD (Rightmost Derivation):** Expanding from right to left.
        - **Reverse Derivation:** Linked to the process of **Reduction** (Bottom-Up Parsing).
        """)

    st.divider()

    st.header("🔝 Top-Down Parser")
    st.markdown("""
    A **Top-Down Parser** starts from the root (**Start Symbol**) and works its way down to the leaves (**Input String**).
    
    It tries to "predict" which production rule to use to generate the next token in the input.
    """)

    st.subheader("🛠️ Construction: Recursive Descent Parser")
    st.markdown("""
    To successfully construct a **Recursive Descent Parser**, you need to handle several prerequisites and core components:
    """)

    c1, c2 = st.columns(2)
    with c1:
        st.info(r"""
        **1. 🚫 Left Recursion**
        You must eliminate **Left Recursion** (e.g., $A \to A \alpha \mid \beta$) to prevent the parser from getting stuck in an infinite loop.
        """)
        
        st.info(r"""
        **2. 📑 Left Factoring**
        This is used to resolve ambiguities when multiple production rules start with the same symbol (e.g., $A \to \alpha \beta_1 \mid \alpha \beta_2$).
        """)

    with c2:
        st.success(r"""
        **3. 🎯 FIRST and FOLLOW Sets**
        You must calculate these sets to understand which terminals can start a production and which can follow a non-terminal.
        """)
        
        st.success(r"""
        **4. 📊 Parsing Table**
        A table constructed using the **FIRST** and **FOLLOW** sets to guide the parser's decisions during top-down expansion.
        """)

    st.divider()

    # Navigation Buttons
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Previous: Parse Trees & Ambiguity"):
            st.session_state.unit1_topic = "3.6 Parse Trees & Ambiguity (Digitized Notes)"
            st.rerun()
    
    with col_nav2:
        if st.button("Next: Introduction to Parsers ➡️", use_container_width=True):
            st.session_state.unit1_topic = "4.1 Introduction to Parsers"
            st.rerun()
