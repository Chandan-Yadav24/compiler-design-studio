import streamlit as st

def render_loop_opt():
    st.title("⚙️ 6.1 Loop Optimization")
    
    st.markdown("""
    **Loop Optimization** is designed to improve performance by reducing repeated work and "overhead" (extra work like checking conditions) inside loops that execute many times.
    """)

    st.divider()

    # --- SECTION 1: TYPES OF LOOP OPTIMIZATION ---
    st.header("📘 1. Primary Methods")
    st.markdown("""
    There are five primary methods detailed in architectural compiler design for optimizing loops:
    """)
    
    methods = {
        "Loop Invariant Code Motion": "Moving code that doesn't change inside the loop to the outside.",
        "Induction Variable Elimination": "Removing redundant variables used for counting.",
        "Loop Unrolling": "Duplicating the loop body to reduce the number of times the loop condition is checked.",
        "Loop Jamming (Fusion)": "Combining multiple adjacent loops into one.",
        "Strength Reduction": "Replacing expensive operations (like multiplication) with cheaper ones (like addition)."
    }
    
    for method, desc in methods.items():
        st.markdown(f"*   **{method}:** {desc}")

    st.divider()

    # --- SECTION 2: LOOP UNROLLING ---
    st.header("🔄 2. Loop Unrolling")
    st.markdown("""
    This technique involves duplicating the body of the loop multiple times.
    *   **Goal:** To reduce "loop control overhead" and increase performance.
    *   **Advantages:** Fewer jumps/tests and higher instruction throughput (useful in high-performance computing).
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("❌ Original Loop (Runs 100 times)")
        st.code("""
while (i < 100) {
    A[i] = 0;
    i = i + 1;
}
        """, language="cpp")
        st.info("The condition `i < 100` is checked 100 times.")
        
    with col2:
        st.subheader("✅ Optimized Loop (Runs 50 times)")
        st.code("""
while (i < 100) {
    A[i] = 0;
    A[i+1] = 0;
    i = i + 2;
}
        """, language="cpp")
        st.success("The condition `i < 100` is now only checked 50 times!")

    st.divider()

    # --- SECTION 3: LOOP JAMMING (FUSION) ---
    st.header("🍯 3. Loop Jamming (Fusion)")
    st.markdown("""
    Loop jamming is the process of combining two or more adjacent loops that have the same loop count into a single loop.
    *   **Goal:** To reduce the total loop overhead.
    *   **Result:** One of the loop structures completely disappears, and its work is moved into the remaining loop.
    """)
    
    col_j1, col_j2 = st.columns(2)
    with col_j1:
        st.subheader("❌ Separate Loops")
        st.code("""
for (i = 0; i < n; i++) {
    A[i] = B[i] + 1;
}

for (i = 0; i < n; i++) {
    C[i] = A[i] + B[i];
}
        """, language="cpp")
        
    with col_j2:
        st.subheader("✅ Jammed Loop")
        st.code("""
for (i = 0; i < n; i++) {
    A[i] = B[i] + 1;
    C[i] = A[i] + B[i];
}
        """, language="cpp")
        st.success("The overhead of the second loop is eliminated entirely.")

    st.divider()

    # --- SECTION 4: INTERACTIVE LAB ---
    st.header("🧪 4. Interactive Transformation Lab")
    st.markdown("Select an optimization type to see the **Step-by-Step Logic** solution.")

    opt_type = st.radio(
        "Select Optimization to demonstrate:",
        ["Loop Unrolling", "Loop Jamming"],
        horizontal=True
    )

    if opt_type == "Loop Unrolling":
        st.subheader("Step-by-Step Solution: Loop Unrolling")
        st.markdown("""
        **User Input Expression:** `for (i=0; i<30; i++) { x[i] = a; }`
        
        1.  **Analyze Overhead:** Currently, the loop checks `i < 30` and increments `i` thirty times.
        2.  **Decide Factor:** Let's unroll by a factor of 3.
        3.  **Duplicate Body:** Insert 3 assignments into the body.
        4.  **Update Step:** Change `i++` to `i += 3`.
        
        **Final Optimized Logic:**
        ```cpp
        for (i=0; i < 30; i += 3) {
            x[i] = a;
            x[i+1] = a;
            x[i+2] = a;
        }
        ```
        """)
    else:
        st.subheader("Step-by-Step Solution: Loop Jamming")
        st.markdown("""
        **User Input Case:** 
        Two separate loops iterating from `1` to `MAX`. 
        Loop 1: `arr[i] = 0` 
        Loop 2: `total += arr[i]`
        
        1.  **Identify Symmetry:** Both loops share the same range (`1` to `MAX`).
        2.  **Verify Dependency:** Loop 2 starts after Loop 1 finishes.
        3.  **Merge Structures:** Create a single loop header.
        4.  **Combine Bodies:** Place both statements inside the new header.
        
        **Final Optimized Logic:**
        ```cpp
        for (i = 1; i <= MAX; i++) {
            arr[i] = 0;
            total += arr[i];
        }
        ```
        """)

    # Navigation
    st.divider()
    nav1, nav2 = st.columns(2)
    with nav2:
        if st.button("Next Topic: Code Generation ➡️", use_container_width=True):
            st.session_state.unit2_topic = "Code Generation"
            st.rerun()
