import streamlit as st
import modules.unit1_recursion as recursion
import modules.unit2_loop_opt as loop_opt
import modules.unit2_data_flow as data_flow
import modules.unit2_codegen as codegen
import modules.unit2_runtime as runtime
import modules.unit2_advanced as advanced

def render():
    st.markdown("""
    <div class="premium-card">
        <h2>🛠️ Module I - Unit 2: Back End of Compiler</h2>
        <p>The back end optimizes the intermediate representation and generates the target machine code.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # optimizing with dropdown
    topics = [
        "6.1 Loop Optimization",
        "6.2 Data Flow Analysis",
        "6.3 Code Generation Techniques",
        "7.1 Runtime Environments & Error Handling",
        "7.2 Activation Records & Stack Mgmt",
        "7.3 Heap Memory Mgmt",
        "7.4 Call & Return Mechanisms",
        "7.5 Exception Handling",
        "8.1 Advanced Topics: Intro",
        "8.2 Compiler Tools & Techniques",
        "8.3 Lex & Syntax Generators",
        "8.4 Code Gen & LLVM",
        "8.5 Debugging & Testing",
        "8.6 JIT Compilation",
        "8.7 Parallel Programming",
        "8.8 Optimization Frameworks",
        "8.9 Domain-Specific Languages"
    ]
    
    # Persist topic in session state
    if "unit2_topic" not in st.session_state:
        st.session_state.unit2_topic = topics[0]

    # Find index of current topic
    try:
        default_index = topics.index(st.session_state.unit2_topic)
    except ValueError:
        default_index = 0

    selected_topic = st.selectbox("Select Topic", topics, index=default_index)
    st.session_state.unit2_topic = selected_topic
    
    st.markdown("---")
    
    if selected_topic == "6.1 Loop Optimization":
        loop_opt.render_loop_opt()
    elif selected_topic == "6.2 Data Flow Analysis":
        data_flow.render_data_flow()
    elif selected_topic == "6.3 Code Generation Techniques":
        codegen.render_codegen()
    elif selected_topic == "7.1 Runtime Environments & Error Handling":
        runtime.render_runtime()
    elif selected_topic == "7.2 Activation Records & Stack Mgmt":
        runtime.render_activation_records()
    elif selected_topic == "7.3 Heap Memory Mgmt":
        runtime.render_heap_mgmt()
    elif selected_topic == "7.4 Call & Return Mechanisms":
        runtime.render_call_return()
    elif selected_topic == "7.5 Exception Handling":
        runtime.render_exception_handling()
    elif selected_topic == "8.1 Advanced Topics: Intro":
        advanced.render_advanced_intro()
    elif selected_topic == "8.2 Compiler Tools & Techniques":
        advanced.render_advanced_tools()
    elif selected_topic == "8.3 Lex & Syntax Generators":
        advanced.render_advanced_generators()
    elif selected_topic == "8.4 Code Gen & LLVM":
        advanced.render_advanced_codegen()
    elif selected_topic == "8.5 Debugging & Testing":
        advanced.render_advanced_debugging()
    elif selected_topic == "8.6 JIT Compilation":
        advanced.render_jit_compilation()
    elif selected_topic == "8.7 Parallel Programming":
        advanced.render_parallel_programming()
    elif selected_topic == "8.8 Optimization Frameworks":
        advanced.render_optimization_frameworks()
    elif selected_topic == "8.9 Domain-Specific Languages":
        advanced.render_advanced_dsl()
        
    elif selected_topic == "Error Handling":
        st.subheader("Lexical & Syntax Error Handling")
        st.write("Error recovery strategies, Error reporting.")
