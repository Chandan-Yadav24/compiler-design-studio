import streamlit as st

def render_data_flow():
    st.title("🔀 6.2 Data Flow Analysis")
    
    st.markdown("""
    **Data Flow Analysis** tracks how variables and expressions move through the program's control flow graph. Compilers like **GCC** and **LLVM** use this to remove waste and speed up applications.
    """)

    st.divider()

    # --- THE 4 KEY TECHNIQUES ---
    st.header("📘 The 4 Key Techniques")
    st.info("💡 **Quick Pro-Tip:** Focus on what each technique **tracks** to understand its purpose.")

    # 1. Reaching Definitions
    with st.expander("🎯 1. Reaching Definitions", expanded=True):
        st.markdown("""
        Checks if a variable assignment "reaches" a certain point in the code without being overwritten.
        *   **Memory Key:** "No kill = reaches" (A 'kill' is a later assignment like `x = 7` overwriting `x = 0`).
        *   **Real-World:** **GCC** uses this to identify and delete code that can never be reached/used.
        """)
        st.code("""
x = 0;  // This definition...
...
y = x + 1; // ...reaches here if 'x' isn't changed in between.
        """, language="cpp")

    # 2. Live Variables
    with st.expander("⚖️ 2. Live Variables"):
        st.markdown("""
        Identifies which variables will be used later (live) vs. those that are no longer needed (dead).
        *   **Memory Key:** "Used before redefine = live".
        *   **Real-World:** **LLVM** uses this to clear registers and save memory in high-end phone games.
        """)
        st.code("""
x = 5; 
print(x); // x is LIVE here.
x = 10;   // x was killed/redefined. If never used after, it was DEAD.
        """, language="cpp")

    # 3. Available Expressions
    with st.expander("♻️ 3. Available Expressions"):
        st.markdown("""
        Determines if an expression's result has already been computed and is still valid for reuse.
        *   **Memory Key:** "Computed & alive = reuse".
        *   **Real-World:** **Clang** uses this to speed up heavy JavaScript execution in browsers like Chrome.
        """)
        st.code("""
a = x + y; // Compute x + y
...
b = x + y; // Reuse the result of x + y (don't redo the math!)
        """, language="cpp")

    # 4. Constant Propagation
    with st.expander("➕ 4. Constant Propagation"):
        st.markdown("""
        Spreads known constant values through the code to simplify calculations early.
        *   **Memory Key:** "Propagate & fold".
        *   **Real-World:** The **V8 Engine** uses this to make complex Google apps run significantly faster.
        """)
        st.code("""
x = 5;
y = x + 3; // Propagate 5 -> y = 5 + 3 -> y = 8 (Folded!)
        """, language="cpp")

    st.divider()

    # --- MNEMONIC SECTION ---
    st.header("🧠 Mnemonic for Exam Prep")
    st.success("""
    ### **RLAC** ➜ "Relax, Learn And Code!"
    
    *   **R**eaching Defs
    *   **L**ive Vars
    *   **A**vailable Exprs
    *   **C**onstant Prop
    
    **Just memorize the 4 names + "what they track". Done!** ✅
    """)

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: Loop Optimization"):
            st.session_state.unit2_topic = "6.1 Loop Optimization"
            st.rerun()
    with nav2:
        if st.button("Next Topic: Code Generation ➡️", use_container_width=True):
            # This will be implemented in the next step
            st.session_state.unit2_topic = "Code Generation"
            st.rerun()
