import streamlit as st

def render_fa_content():
    st.header("2.4 Finite Automata (FA) & Subset Construction")
    
    st.markdown("""
    <div class="premium-card">
        <h3>I) Finite Automata (FA) — Introduction</h3>
        <p>Finite Automaton = a mathematical machine used to recognize regular languages (used in lexical analysis).</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.info("🎯 **Key Points**")
        st.markdown("""
        - Has finite number of states.
        - Reads input one symbol at a time.
        - Moves between states using transition function.
        - If input ends in a final state, string is accepted.
        """)
    
    with col2:
        st.success("🖼️ **Simple FA Diagram**")
        st.graphviz_chart('''
        digraph {
            rankdir=LR;
            bgcolor="transparent";
            node [shape=circle, fontcolor=white, color=white];
            edge [color=white, fontcolor=white];
            start [shape=none, label=""];
            q2 [shape=doublecircle];
            start -> q0;
            q0 -> q1 [label="a"];
            q1 -> q2 [label="b"];
        }
        ''')

    st.markdown("---")
    st.subheader("II) Formal Definition (5-tuple)")
    st.latex(r"M = (Q, \Sigma, \delta, q_0, F)")
    
    st.markdown(r"""
    **Where:**
    - **Q**: finite set of states
    - **Σ**: input alphabet
    - **δ**: transition function
        - **DFA**: $\delta: Q \times \Sigma \rightarrow Q$
        - **NFA**: $\delta: Q \times \Sigma \rightarrow 2^Q$
    - **$q_0$**: start state
    - **F**: set of final (accepting) states ($F \subseteq Q$)
    """)

    st.markdown("---")
    st.subheader("III) Types of Finite Automata")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 1) DFA (Deterministic FA)")
        st.info("Exactly one next state for each input. No ε-moves.")
        st.graphviz_chart('''
        digraph {
            rankdir=LR; bgcolor="transparent";
            node [shape=circle, fontcolor=white, color=white];
            edge [color=white, fontcolor=white];
            q0 -> q1 [label="a"];
        }
        ''')
        
    with c2:
        st.markdown("### 2) NFA (Non-Deterministic FA)")
        st.warning("Multiple choices or ε-moves allowed.")
        st.graphviz_chart('''
        digraph {
            rankdir=LR; bgcolor="transparent";
            node [shape=circle, fontcolor=white, color=white];
            edge [color=white, fontcolor=white];
            q0 -> q1 [label="a"];
            q0 -> q2 [label="a"];
        }
        ''')
    
    st.markdown("> [!IMPORTANT]\n> **Fact:** Every NFA has an equivalent DFA.")

    st.markdown("---")
    st.subheader("IV) NFA → DFA Conversion (Subset Construction)")
    
    st.markdown("#### Core Formula")
    st.latex(r"\delta_{DFA}(S, x) = \epsilon\text{-closure}\left( \bigcup_{q \in S} \delta_{NFA}(q, x) \right)")
    
    st.markdown(r"""
    #### 📝 Exam Flow (Steps)
    1. Make **NFA transition table**.
    2. Start DFA with state: **$[q_0]$** (or $\epsilon$-closure of $q_0$).
    3. For each DFA subset state, compute transitions on each symbol.
    4. Any subset containing an NFA final state $\Rightarrow$ **DFA final state**.
    5. Draw DFA graph (add trap/dead state for $\emptyset$).
    """)

    st.markdown("---")
    st.subheader("V) Worked Example")
    
    with st.expander("📖 View Problem Definition"):
        st.markdown(r"""
        **NFA Definition:**
        - $Q = \{q_0, q_1, q_2\}$
        - $\Sigma = \{a, b\}$
        - Start: $q_0$, Final: $F = \{q_2\}$
        """)
        
        st.write("**NFA Transition Table:**")
        st.table({
            "State": ["→ q0", "q1", "* q2"],
            "a": ["{q1}", "∅", "{q0, q1}"],
            "b": ["{q2}", "{q0}", "∅"]
        })

    st.markdown("#### 1) NFA Diagram")
    st.graphviz_chart('''
    digraph {
        rankdir=LR; bgcolor="transparent";
        node [shape=circle, fontcolor=white, color=white];
        edge [color=white, fontcolor=white];
        start [shape=none, label=""];
        q2 [shape=doublecircle];
        start -> q0;
        q0 -> q1 [label="a"];
        q0 -> q2 [label="b"];
        q1 -> q0 [label="b"];
        q2 -> q0 [label="a"];
        q2 -> q1 [label="a"];
    }
    ''')

    st.markdown("#### 2) DFA Transition Table (Subset Construction)")
    st.markdown("DFA states are subsets of NFA states.")
    
    st.table({
        "DFA State": ["→ [q0]", "[q1]", "* [q2]", "[q0, q1]", "* [q2, q0]", "[∅] (trap)"],
        "on a": ["[q1]", "[∅]", "[q0, q1]", "[q1]", "[q0, q1]", "[∅]"],
        "on b": ["[q2]", "[q0]", "[∅]", "[q2, q0]", "[q2]", "[∅]"]
    })
    st.caption("Final states: Any subset containing $q_2$ (marked with *)")

    st.markdown("#### 3) Final DFA Graph")
    st.graphviz_chart('''
    digraph {
        rankdir=LR; bgcolor="transparent";
        node [shape=circle, fontcolor=white, color=white];
        edge [color=white, fontcolor=white];
        
        node [shape=doublecircle] q2, q2_0;
        node [shape=circle] q0, q1, q0_1, trap;
        
        q0 [label="[q0]"];
        q1 [label="[q1]"];
        q2 [label="[q2]"];
        q0_1 [label="[q0, q1]"];
        q2_0 [label="[q2, q0]"];
        trap [label="[∅]"];
        
        start [shape=none, label=""];
        start -> q0;
        
        q0 -> q1 [label="a"];
        q0 -> q2 [label="b"];
        
        q1 -> trap [label="a"];
        q1 -> q0 [label="b"];
        
        q2 -> q0_1 [label="a"];
        q2 -> trap [label="b"];
        
        q0_1 -> q1 [label="a"];
        q0_1 -> q2_0 [label="b"];
        
        q2_0 -> q0_1 [label="a"];
        q2_0 -> q2 [label="b"];
        
        trap -> trap [label="a, b"];
    }
    ''')
    
    if st.button("Next Topic: NFA to DFA Lab 🚀"):
        st.session_state.unit1_topic = "2.6 NFA to DFA Conversion Lab"
        st.rerun()
