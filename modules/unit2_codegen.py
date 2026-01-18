import streamlit as st
import pandas as pd

def render_codegen():
    st.title("🏗️ 6.3 Code Generation Techniques")
    
    st.markdown("""
    **Code Generation** is the "grand finale" where high-level code (your Java/C++) turns into machine code (.exe, .class). 
    It's the "Final Boss" of compilers because it must juggle instructions, registers, and memory like a DJ mixing tracks.
    """)

    st.divider()

    # --- MUST-HAVE PROPERTIES ---
    st.header("🛡️ 2 Must-Have Properties")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("1. Preserve Meaning")
        st.success("The output must do exactly what the source intended – no bugs added!")
    with c2:
        st.subheader("2. Efficiency")
        st.success("Smart use of CPU registers and memory – like packing a suitcase perfectly.")

    st.divider()

    # --- 1. TARGET MACHINE DESCRIPTION ---
    st.header("📘 1. Target Machine Description")
    st.markdown("Compilers tailor code to specific architectures (e.g., **x86** for PCs, **ARM** for phones).")
    
    tab1, tab2, tab3 = st.tabs(["Instruction Set", "Addressing Modes", "Instruction Formats"])
    
    with tab1:
        st.subheader("Instruction Set (The Command List)")
        st.markdown("""
        The set of commands available to the hardware (ADD, SUB, JZ, MOV).
        *   **Types:** Arithmetic, Logical, Conditional, Data Move.
        *   **Real-World:** **GCC** uses x86 sets for Windows games; **LLVM** optimizes for Apple's **M1 chips**.
        """)
        
    with tab2:
        st.subheader("Addressing Modes (How to fetch data)")
        st.markdown("Modern magic happens in how data is accessed.")
        
        mode_data = [
            {"Mode": "Register", "Example": "MOV A, B", "Logic": "Fast: Data between registers (A gets B's value)"},
            {"Mode": "Immediate", "Example": "MVI A, 05H", "Logic": "Direct number (load 5 into A)"},
            {"Mode": "Direct", "Example": "LDA A, 1000H", "Logic": "From memory address (load from 1000 into A)"}
        ]
        st.table(pd.DataFrame(mode_data))
        st.info("💡 **JVM's** bytecode uses these for cross-platform magic – runs on any device!")

    with tab3:
        st.subheader("Instruction Formats")
        st.markdown("""
        How commands are written in memory.
        *   **Standard:** `[Label] Opcode [Operand/s]` (e.g., `L1: ADD N`)
        *   **Real-World:** **Clang** in Xcode auto-picks formats for iOS apps to save battery life.
        """)

    st.divider()

    # --- 2. ASSEMBLY PROCESS OVERVIEW ---
    st.header("⚙️ 2. Assembly Process (The 9-Step Factory)")
    st.markdown("How assembly code turns into machine bits, step-by-step:")
    
    steps = [
        "**Scan instruction** ➜ Make tokens (opcode, operands).",
        "**Identify symbols/vars** ➜ Add to symbol table.",
        "**Spot literals** ➜ Add to literal table.",
        "**Update location counter** (tracks memory addresses).",
        "**Allocate memory** to variables.",
        "**Check instruction** in the opcode table.",
        "**Syntax check** (character-by-character match).",
        "**Semantic check** (does the logic make sense?).",
        "**Generate final instruction** by extracting opcode + addresses."
    ]
    
    for i, step in enumerate(steps, 1):
        st.markdown(f"{i}. {step}")
        
    st.info("🚀 **Context:** **LLVM** does this in passes – optimizes **TensorFlow AI** code for GPUs, making self-driving cars smarter!")

    st.divider()

    # --- MNEMONIC SECTION ---
    st.header("🧠 Mnemonic for Quick Recall")
    st.success("""
    ### **PEIMF** ➜ "Please Eat Ice-cream More Frequently!"
    
    *   **P**reserve Meaning
    *   **E**fficient
    *   **I**nstructions
    *   **M**odes
    *   **F**ormats
    
    **In modern compilers like GCC's -O2, this process makes your code run 2x faster!** 💥
    """)

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: Data Flow Analysis"):
            st.session_state.unit2_topic = "6.2 Data Flow Analysis"
            st.rerun()
    with nav2:
        if st.button("Next Topic: Runtime Environments ➡️", use_container_width=True):
            st.session_state.unit2_topic = "Runtime Environments"
            st.rerun()
