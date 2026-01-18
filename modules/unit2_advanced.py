import streamlit as st
import re
import pandas as pd

def render_advanced_intro():
    st.title("🚀 8.0 & 8.1 Advanced Topics: Objectives & Introduction")
    
    st.markdown("""
    <div class="premium-card">
        <h3>🎯 8.0 OBJECTIVE</h3>
        <p>The primary objectives of this chapter are to:</p>
        <ul>
            <li><b>Understand</b> the core components of modern compilers.</li>
            <li><b>Explore</b> advanced technologies like <b>LLVM</b> for cross-platform code generation.</li>
            <li><b>Develop</b> skills for debugging, testing, and verifying compiler correctness.</li>
            <li><b>Support</b> modern programming needs through <b>parallel and concurrent</b> programming.</li>
            <li><b>Design & Implement</b> Domain-Specific Languages (<b>DSLs</b>) for specialized problems.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.header("🌐 8.1 INTRODUCTION")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("""
        Compilers are the bridge between human creativity and machine execution. While foundational compilers were simple translators, modern systems are incredibly sophisticated.
        
        **Key areas we explore:**
        *   **Lexical & Syntax Generators:** Automating the "Front-End" with tools.
        *   **LLVM Infrastructure:** The industry standard for high-performance code generation.
        *   **JIT Compilation:** How Java and JavaScript optimize code *while* it runs.
        *   **Optimization Frameworks:** Squeezing every bit of performance out of the CPU.
        *   **DSL Compilation:** Creating languages like SQL or CSS tailored to specific domains.
        """)
        
        st.success("💡 **Practical Context:** From the **Uber ride tracker** (LLVM/Swift) to **Netflix streaming** (JIT/V8), advanced compiler topics power the modern world!")

    with col2:
        st.image("https://llvm.org/img/LLVMLogo.png", width=200, caption="LLVM: The backbone of modern compilers.")
        st.info("""
        **Core Pillars:**
        1. Correctness 
        2. Performance 
        3. Portability
        4. Maintainability
        """)

    st.divider()

    # Call to action / Exam Tip
    st.warning("📝 **Exam Insight:** For Topic 8, focus on the 'Why' – why do we need LLVM? (Portability). Why JIT? (Speed for dynamic languages).")

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: Exception Handling"):
            st.session_state.unit2_topic = "7.5 Exception Handling"
            st.rerun()
    with nav2:
        if st.button("Next: 8.2 Tools & Tech ➡️", use_container_width=True):
            st.session_state.unit2_topic = "8.2 Compiler Tools & Techniques"
            st.rerun()

def render_advanced_tools():
    st.title("🛠️ 8.2 Introduction to Compiler Tools and Techniques")
    
    st.markdown("""
    Compiler tools and techniques are the foundation for transforming high-level logic into machine execution. 
    This section explores the automation and methodologies that make modern software possible.
    """)

    st.divider()

    # --- 8.2.1 OVERVIEW ---
    st.header("🗂️ 8.2.1 Overview of Compiler Design")
    
    # 8.2.1.1 Purpose
    st.subheader("🎯 8.2.1.1 Definition and Purpose")
    st.markdown("""
    A compiler is a sophisticated software tool that converts high-level languages (C, Java, Python) into binary machine code.
    
    | Goal | Purpose |
    | :--- | :--- |
    | **a. Translation** | Source → Machine code conversion. |
    | **b. Optimization** | Improving execution speed and resource usage. |
    | **c. Error Detection** | Identifying syntax/logic mistakes early. |
    | **d. Abstraction** | Letting humans write code that's easy to maintain. |
    """)

    # 8.2.1.2 Phases
    st.subheader("🛤️ 8.2.1.2 Phases of Compilation")
    st.markdown("""
    The compilation process is a pipeline of 6 key phases:
    """)
    
    phases = [
        {"Phase": "a. Lexical Analysis", "Purpose": "Scanner: Source → Tokens.", "Process": "Regex matching, stripping whitespace."},
        {"Phase": "b. Syntax Analysis", "Purpose": "Parser: Tokens → Parse Tree.", "Process": "Grammar checking using CFGs."},
        {"Phase": "c. Semantic Analysis", "Purpose": "Checker: Meaning & Logic.", "Process": "Type checking and scope validation."},
        {"Phase": "d. Optimization", "Purpose": "Efficiency Booster.", "Process": "Constant folding, loop unrolling."},
        {"Phase": "e. Code Generation", "Purpose": "Machine Whisperer.", "Process": "High-level → Low-level instructions."},
        {"Phase": "f. Code Optimization", "Purpose": "Refiner.", "Process": "Register allocation, peep-hole opt."}
    ]
    st.table(phases)

    st.divider()

    # --- 8.2.2 TOOLS ---
    st.header("⚙️ 8.2.2 Compiler Construction Tools")
    st.markdown("Tools that automate the creation of lexers and parsers, reducing human error.")

    tool_col1, tool_col2 = st.columns(2)

    with tool_col1:
        st.subheader("🔍 Lexical Generators")
        st.markdown("""
        **Lex & Flex**
        *   **Lex:** The classic Unix-based tool for regex matching.
        *   **Flex:** The "Fast" modern version. Generates high-performance C code for tokenization.
        *   **Usage:** Define tokens in a `.l` file → Generate `yylex()`.
        """)
        st.info("💡 **Mnemonic:** **LF** (Lex/Flex) = Look Fast! (Tokens are fast).")

    with tool_col2:
        st.subheader("🏗️ Syntax Generators")
        st.markdown("""
        **Yacc & Bison**
        *   **Yacc:** "Yet Another Compiler Compiler". Original grammar parser.
        *   **Bison:** Modern, flexible, and fully compatible with Yacc files. Handles GLR parsing.
        *   **Usage:** Define grammar in a `.y` file → Generate `yyparse()`.
        """)
        st.info("💡 **Mnemonic:** **YB** (Yacc/Bison) = Yield Best! (Parsers yield trees).")

    st.divider()

    st.success("🤖 **Future Scope:** Modern compilers like **LLVM** use these components but provide a modular framework to build for 50+ CPUs at once!")

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: 8.0 Objectives"):
            st.session_state.unit2_topic = "8.1 Advanced Topics: Intro"
            st.rerun()
    with nav2:
        if st.button("Next: 8.3 Generators ➡️", use_container_width=True):
            st.session_state.unit2_topic = "8.3 Lex & Syntax Generators"
            st.rerun()

def render_advanced_generators():
    st.title("🧬 8.3 Lexical and Syntax Analyzer Generators")
    
    st.markdown("""
    Analyzers are the "Eyes and Ears" of the compiler. They transform raw text into structural meaning. 
    Here, we delve into how these components are generated and how they function internally.
    """)

    st.divider()

    # --- 8.3.1 LEXICAL ANALYZERS ---
    st.header("🔍 8.3.1 Lexical Analyzers (The Scanners)")
    
    col_lex1, col_lex2 = st.columns([1.2, 1])
    
    with col_lex1:
        st.subheader("🛠️ 8.3.1.1 Role in Compilation")
        st.markdown("""
        The Lexical Analyzer (Lexer) is the first line of defense. It processes raw characters to produce structured **Tokens**.
        
        *   **Tokenization:** Identifying keywords, operators, and identifiers.
        *   **Cleanup:** Stripping whitespace (` `) and comments (`/* ... */`).
        *   **Error Detection:** Catching illegal symbols (e.g., `@` where not allowed).
        """)
        
    with col_lex2:
        st.subheader("📝 8.3.1.2 Patterns (Regex)")
        st.markdown("""
        Regex defines the "rules" for tokens:
        *   **Keywords:** `if`, `else`, `while`.
        *   **Identifiers:** `[a-zA-Z_][a-zA-Z0-9_]*`
        *   **Numbers:** `[0-9]+`
        *   **Strings:** `\".*?\"`
        """)

    # --- PRACTICAL: TOKENIZER LAB ---
    st.info("🧪 **Practical Lab: Tokenization Playground**")
    user_code = st.text_input("Enter a line of code to tokenize:", value="int x = 10 + data;")
    
    if user_code:
        # Simple regex tokenizer
        token_specs = [
            ('KEYWORD', r'\b(int|float|return|if|else|while)\b'),
            ('ID',      r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NUMBER',  r'\d+'),
            ('OP',      r'[+\-*/=]'),
            ('PUNCT',   r'[;(),{}]'),
            ('SKIP',    r'[ \t]+'),
            ('MISMATCH',r'.'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
        tokens = []
        for mo in re.finditer(tok_regex, user_code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'SKIP': continue
            tokens.append({"Kind": kind, "Lexeme": value})
        
        st.write("**Generated Token Stream:**")
        st.table(tokens)

    st.divider()

    # --- 8.3.2 SYNTAX ANALYZERS ---
    st.header("🏗️ 8.3.2 Syntax Analyzers (The Parsers)")
    
    tab_parser1, tab_parser2 = st.tabs(["📘 Parser Roles", "📐 CFG & Techniques"])
    
    with tab_parser1:
        st.subheader("8.3.2.1 Role in Compilation")
        st.markdown("""
        The Parser builds a **Hierarchy** (Syntax Tree) from the token stream.
        1.  **Construction:** Organizing tokens into meaningful expressions.
        2.  **Structural Validation:** Ensuring parentheses match and semicolons exist.
        """)
        st.info("🚀 **Tooling:** Yacc and Bison automate this by reading grammar rules and generating parser code.")

    with tab_parser2:
        st.subheader("8.3.2.2 Context-Free Grammars (CFG)")
        st.markdown("""
        **Components (NTP S):**
        *   **N**: Non-Terminals (Variables to expand).
        *   **T**: Terminals (Actual tokens).
        *   **P**: Production Rules (Rules for expansion).
        *   **S**: Start Symbol.
        
        **Parsing Types:**
        *   **Top-Down:** Start symbol → Leaves (e.g., Recursive Descent).
        *   **Bottom-Up:** Tokens → Start symbol (e.g., LR Parsing).
        """)

    # --- PRACTICAL: PARSE TREE VISUAL ---
    st.info("🧪 **Practical Lab: Parse Tree Visualization**")
    st.markdown("Try visualizing the structure of a common expression: `a = b + c`")
    
    if st.button("Generate Parse Tree Visual"):
        st.graphviz_chart('''
        graph G {
            node [shape=box, style=filled, fillcolor="#e3f2fd", fontname="Courier"];
            Assignment -- ID_a [label="LHS"];
            Assignment -- Expr [label="RHS"];
            Expr -- Term1;
            Expr -- Term2;
            Expr -- Plus [label="Operator"];
            Term1 -- ID_b;
            Term2 -- ID_c;
            ID_a [label="id (a)", fillcolor="#fff9c4"];
            ID_b [label="id (b)", fillcolor="#fff9c4"];
            ID_c [label="id (c)", fillcolor="#fff9c4"];
            Plus [label="+", shape=circle, fillcolor="#ffccbc"];
        }
        ''')

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: 8.2 Tools & Tech"):
            st.session_state.unit2_topic = "8.2 Compiler Tools & Techniques"
            st.rerun()
    with nav2:
        if st.button("Next: 8.4 LLVM & Code Gen ➡️", use_container_width=True):
            st.session_state.unit2_topic = "8.4 Code Gen & LLVM"
            st.rerun()

def render_advanced_codegen():
    st.title("🏗️ 8.4 Code Generation Frameworks & LLVM")
    
    st.markdown("""
    Code generation is where the "Abstract becomes Actual". It is the final translation from logical constructs to electrical signals (Machine Code).
    """)

    st.divider()

    # --- 8.4.1 INTRODUCTION ---
    st.header("🌐 8.4.1 Introduction to Code Generation")
    
    col_cg1, col_cg2 = st.columns(2)
    
    with col_cg1:
        st.subheader("🎯 8.4.1.1 Objectives (EOCPM)")
        st.markdown("""
        The goals of code generation are:
        *   **a. Efficiency:** Faster execution, less CPU heat.
        *   **b. Optimization:** Eliminating redundant instructions.
        *   **c. Correctness:** Ensuring behavior matches logic.
        *   **d. Portability:** Running on Intel, ARM, or RISC-V.
        *   **e. Maintainability:** Clean code for future updates.
        """)

    with col_cg2:
        st.subheader("🌉 8.4.1.2 Intermediate Representations (IR)")
        st.markdown("""
        IR is the "Bridge" between languages and hardware.
        *   **AST:** Structural representation.
        *   **TAC:** Three-Address Code (Flattened logic).
        *   **SSA:** Static Single Assignment (Variable tracking).
        *   **LLVM IR:** Standardized, platform-neutral assembly.
        """)

    st.divider()

    # --- 8.4.2 LLVM ---
    st.header("🐉 8.4.2 LLVM (Low-Level Virtual Machine)")
    st.markdown("""
    LLVM is the **Industry Standard** for building compilers. It power languages like Swift, Rust, Clang (C++), and Julia.
    """)

    # Architecture Diagram
    st.subheader("🏗️ 8.4.2.2 LLVM Architecture")
    st.graphviz_chart('''
    digraph {
        rankdir=LR;
        bgcolor="transparent";
        node [shape=box, style=filled, fillcolor="white", fontcolor="black", fontname="Arial"];
        edge [color=white, fontcolor=white, fontname="Arial"];

        S [label="Source: C/Rust/Swift"];
        MC [label="Machine Code: x86/ARM/WASM"];

        subgraph cluster_llvm {
            label="LLVM Infrastructure";
            color=white;
            fontcolor=white;
            IR [label="LLVM IR"];
            IR_OPT [label="Optimized IR"];
        }

        S -> IR [label="Frontend"];
        IR -> IR_OPT [label="Optimizer (Middle-End)"];
        IR_OPT -> MC [label="Backend"];
    }
    ''')

    st.markdown("""
    **Core Components:**
    1.  **Frontend:** Translates Source → LLVM IR.
    2.  **Optimizer:** Rewrites IR for speed without changing meaning.
    3.  **Backend:** Translates IR → Target instructions (x86/ARM).
    4.  **JIT Compiler:** Compiles code *at runtime* for dynamic speed.
    """)

    st.divider()

    # --- PRACTICAL: LLVM PIPELINE SIMULATOR ---
    st.info("🧪 **Practical Lab: LLVM Pipeline Simulator**")
    st.markdown("See how `x = a + 5` travels through the LLVM pipeline!")
    
    source_example = "x = a + 5"
    
    p_step1, p_step2, p_step3, p_step4 = st.tabs(["1. AST", "2. LLVM IR", "3. Optimized IR", "4. Machine Code"])
    
    with p_step1:
        st.code("""
Assignment
 ├── target: ID(x)
 └── value: BinaryOp(+)
      ├── left: ID(a)
      └── right: Const(5)
        """, language="text")
        st.caption("Structural view of the code.")

    with p_step2:
        st.code("""
%1 = load i32, i32* %a_addr
%2 = add nsw i32 %1, 5
store i32 %2, i32* %x_addr
        """, language="llvm")
        st.caption("Standardized internal representation.")

    with p_step3:
        st.code("""
; Optimizer detects 'a' is a constant 10 in context
store i32 15, i32* %x_addr
        """, language="llvm")
        st.success("⚡ Optimization: Constant folding applied!")

    with p_step4:
        st.code("""
mov eax, [ebp-4]    ; Load a
add eax, 5          ; Add 5
mov [ebp-8], eax    ; Store x
        """, language="nasm")
        st.caption("Final assembly for the processor (x86).")

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: 8.3 Generators"):
            st.session_state.unit2_topic = "8.3 Lex & Syntax Generators"
            st.rerun()
    with nav2:
        if st.button("Next: 8.5 Debugging ➡️", use_container_width=True):
            st.session_state.unit2_topic = "8.5 Debugging & Testing"
            st.rerun()

def render_advanced_debugging():
    st.title("🐞 8.5 Debugging and Testing Compilers")
    
    st.markdown("""
    Compilers must be **Bug-Free**. A single error in a compiler can cause millions of bugs in the software it generates. 
    This section covers how we ensure compiler correctness and reliability.
    """)

    st.divider()

    # --- 8.5.1 IMPORTANCE & BUGS ---
    st.header("🗂️ 8.5.1 Importance and Common Issues")
    
    col_debug1, col_debug2 = st.columns(2)
    
    with col_debug1:
        st.subheader("🎯 Common Compiler Bugs (PS COP)")
        st.markdown("""
        *   **a. Parsing Errors:** Incorrectly handling edge cases in syntax.
        *   **b. Semantic Errors:** Logic flaws in type checking or scope.
        *   **c. Code Gen Errors:** Wrong assembly for a high-level command.
        *   **d. Optimization Issues:** Regressions that break working code.
        *   **e. Platform Problems:** x86 code that crashes on ARM.
        """)

    with col_debug2:
        st.subheader("🛡️ Debugging Strategies")
        st.markdown("""
        *   **Incremental Dev:** Build & test bit by bit.
        *   **Debug Info:** Generating symbols for GDB/DWARF.
        *   **Regression Testing:** Ensuring old bugs don't return.
        *   **Static Analysis:** Using tools to scan compiler source.
        *   **Logging/Tracing:** Printing the internal state of the IR.
        """)

    st.divider()

    # --- 8.5.2 TOOLS ---
    st.header("🛠️ 8.5.2 Tools for Testing Compilers")
    
    tab_tool1, tab_tool2 = st.tabs(["🧪 Testing Frameworks", "🔍 Debugging Tools"])
    
    with tab_tool1:
        st.markdown("""
        **Unit Testing & Fuzzing:**
        *   **Unit Tests:** Testing individual components (e.g., the Lexer).
        *   **Fuzz Testing:** Injecting **random/mutated inputs** to crash the compiler.
        *   **Mutation Testing:** Changing the IR to see if tests detect the "mutation".
        """)
        st.warning("💡 **Pro-Tip:** Fuzzing found thousands of bugs in industrial compilers like GCC and Clang!")

    with tab_tool2:
        st.markdown("""
        **Standard Debuggers:**
        *   **GDB (GNU Debugger):** To step through the compiler's C++/C code.
        *   **Valgrind:** To find memory leaks (Crucial for compilers written in C/C++).
        """)

    st.divider()

    # --- PRACTICAL: COMPILER BUG HUNTER ---
    st.info("🧪 **Practical Lab: Compiler Bug Hunter**")
    st.markdown("Identify the **Type of Bug** based on the compiler's behavior.")
    
    scenario_id = st.radio("Choose a Debugging Scenario:", 
                          ["Scenario A", "Scenario B", "Scenario C"], 
                          horizontal=True)
    
    if scenario_id == "Scenario A":
        st.error("❌ **Compiler Output:** `Error: Undefined variable 'count' at line 45 (Scope: main)`")
        ans = st.selectbox("What type of bug is this?", ["Parsing Error", "Semantic Error", "Code Gen Error"])
        if ans == "Semantic Error": st.success("✅ Correct! This is a Scope/Symbol resolution issue.")
    
    elif scenario_id == "Scenario B":
        st.error("❌ **Compiler Output:** `Error: Expecting ';' but found 'return' at line 12`")
        ans = st.selectbox("What type of bug is this?", ["Parsing Error", "Semantic Error", "Optimization Issue"])
        if ans == "Parsing Error": st.success("✅ Correct! This is a syntax structure violation.")
        
    elif scenario_id == "Scenario C":
        st.warning("⚠️ **Execution Output:** `Program prints 10 but expected 20 after '-O3' optimization`")
        ans = st.selectbox("What type of bug is this?", ["Platform Problem", "Lexical Error", "Optimization Issue"])
        if ans == "Optimization Issue": st.success("✅ Correct! The optimizer changed the program's logic incorrectly.")

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: 8.4 Code Gen"):
            st.session_state.unit2_topic = "8.4 Code Gen & LLVM"
            st.rerun()
    with nav2:
        if st.button("Next: 8.6 JIT Compilation ➡️", use_container_width=True):
            st.session_state.unit2_topic = "8.6 JIT Compilation"
            st.rerun()

def render_jit_compilation():
    st.title("⚡ 8.6 Just-In-Time (JIT) Compilation")
    
    st.markdown("""
    JIT Compilation is the "Secret Sauce" of modern high-performance languages like Java, JavaScript, and C#. 
    It combines the portability of an interpreter with the speed of a machine-code compiler!
    """)

    st.divider()

    # --- 8.6.1 INTRODUCTION ---
    st.header("📘 8.6.1 Introduction to JIT")
    
    st.subheader("⚔️ JIT vs AOT: The Ultimate Showdown")
    
    # Comparison Data
    comparison_data = [
        {"Feature": "Compilation Time", "AOT (Ahead-of-Time)": "Before execution (Build time)", "JIT (Just-in-Time)": "During execution (Run time)"},
        {"Feature": "Startup Speed", "AOT (Ahead-of-Time)": "Fast (Code ready)", "JIT (Just-in-Time)": "Slower (Need to compile first)"},
        {"Feature": "Optimization", "AOT (Ahead-of-Time)": "Static (One-size-fits-all)", "JIT (Just-in-Time)": "Adaptive (Adapts to real usage)"},
        {"Feature": "Bundle Size", "AOT (Ahead-of-Time)": "Smaller (Native binary)", "JIT (Just-in-Time)": "Larger (Includes compiler runtime)"},
        {"Feature": "Compatibility", "AOT (Ahead-of-Time)": "Limited (Need specific build for CPU)", "JIT (Just-in-Time)": "High (Compile for the current CPU)"},
        {"Feature": "Error Catching", "AOT (Ahead-of-Time)": "Caught during build", "JIT (Just-in-Time)": "Discovered at runtime"},
    ]
    st.table(comparison_data)

    st.markdown("---")

    col_jit1, col_jit2 = st.columns(2)
    
    with col_jit1:
        st.success("🌟 **Benefits of JIT**")
        st.markdown("""
        *   **Hot Spot Optimization:** Finding and turbo-charging the most used code paths.
        *   **Deoptimization:** If code patterns change, JIT can swap back to safer code.
        *   **Runtime Profiling:** Real-data drives smarter speedups.
        """)
        
    with col_jit2:
        st.error("⚠️ **Challenges of JIT**")
        st.markdown("""
        *   **Overhead:** Compiling while the app is running takes CPU time.
        *   **Memory:** Needs extra RAM to store the compiler and the new code.
        *   **Complex Debugging:** Errors can be elusive and timing-dependent.
        """)

    st.divider()

    # --- 8.6.2 TECHNIQUES ---
    st.header("⚙️ 8.6.2 JIT Techniques")
    
    tech_tab1, tech_tab2 = st.tabs(["🚀 Dynamic Generation", "🧠 Adaptive Strategies"])
    
    with tech_tab1:
        st.markdown("""
        **How JIT works its magic:**
        *   **Inline Caching:** Remembering the address of a function call to skip "lookup" next time.
        *   **Speculative Optimization:** Making "smart guesses" about code types to skip checks.
        """)
        st.info("💡 **Analogy:** Speculative Opt is like a waiter bringing water before you ask because they saw you're thirsty!")

    with tech_tab2:
        st.markdown("""
        **Lifecycle of Optimization:**
        *   **Profile:** Watch which functions are called 1000+ times.
        *   **Compile:** Turn those "Hot" functions into native code.
        *   **Deoptimize:** If the "guess" was wrong (e.g., a number suddenly becomes a string), revert to safe code.
        """)

    st.divider()

    # --- 8.6.3 EXAMPLES ---
    st.header("🏢 8.6.3 Industry Examples")
    
    ex_col1, ex_col2 = st.columns(2)
    
    with ex_col1:
        st.markdown("☕ **Java HotSpot VM**")
        st.caption("The legend of JIT. Uses **Escape Analysis** to decide if objects can live on the stack (fast) instead of the heap.")

    with ex_col2:
        st.markdown("💠 **.NET CLR JIT**")
        st.caption("Powering Windows apps. Uses **Tiered Compilation** to balance fast startup (Quick JIT) with high peak speed (Full JIT).")

    st.divider()

    # --- PRACTICAL: JIT VS AOT BATTLE ---
    st.info("🧪 **Practical Lab: JIT vs AOT Battle**")
    st.markdown("Choose a scenario and see which compilation strategy wins!")
    
    use_case = st.selectbox("Scenario:", 
                          ["A Mobile App for a weak-CPU phone", 
                           "A Server processing millions of transactions", 
                           "A fast-updating Website during development"])
    
    if "Mobile" in use_case:
        st.markdown("**Winner: 🥇 AOT**")
        st.write("Why? Because weak CPUs shouldn't waste energy compiling code on the fly. Pre-compiled code starts instantly.")
    elif "Server" in use_case:
        st.markdown("**Winner: 🥇 JIT**")
        st.write("Why? Because servers run for months. JIT can profile the traffic and optimize the code perfectly for the specific hardware.")
    elif "Website" in use_case:
        st.markdown("**Winner: 🥇 JIT**")
        st.write("Why? Because developers want to see changes instantly without waiting for a full build process.")

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: 8.5 Debugging"):
            st.session_state.unit2_topic = "8.5 Debugging & Testing"
            st.rerun()
    with nav2:
        if st.button("Next: 8.7 Parallel Support ➡️", use_container_width=True):
            st.session_state.unit2_topic = "8.7 Parallel Programming"
            st.rerun()

def render_parallel_programming():
    st.title("🧵 8.7 Parallel and Concurrent Programming Support")
    
    st.markdown("""
    Modern CPUs have multiple cores. A compiler's job is to ensure code isn't just "correct", but also "multi-threaded" to squeeze every bit of performance out of the hardware.
    """)

    st.divider()

    # --- 8.7.1 INTRODUCTION ---
    st.header("📘 8.7.1 Introduction to Parallelism & Concurrency")
    
    col_pc1, col_pc2 = st.columns(2)
    
    with col_pc1:
        st.subheader("🏎️ Parallel Programming")
        st.markdown("""
        Splitting a big task into sub-tasks that run **at the exact same time** on different processors.
        *   **Goal:** Boosting speed.
        *   **Analogy:** 5 chefs cooking 5 different dishes simultaneously.
        """)

    with col_pc2:
        st.subheader("🤹 Concurrent Programming")
        st.markdown("""
        Managing multiple tasks that **overlap** in time. Focuses on interaction and resource sharing.
        *   **Goal:** Efficiency & Responsiveness.
        *   **Analogy:** 1 chef multitasking between chopping, boiling, and frying.
        """)

    st.markdown("---")

    st.subheader("⚠️ The Great Challenges")
    st.markdown("""
    | Challenge | Description |
    | :--- | :--- |
    | **Race Conditions** | Outcome depends on which thread "wins" the race to a shared variable. |
    | **Deadlocks** | Thread A waits for B, and B waits for A. Everything halts! |
    | **Scalability** | Code that runs fast on 2 cores might crawl on 64 due to communication overhead. |
    """)

    st.divider()

    # --- 8.7.2 COMPILER TECHNIQUES ---
    st.header("⚙️ 8.7.2 Compiler Techniques for Parallelism")
    st.markdown("Compilers use advanced math to prove that code is safe to run in parallel.")

    tab_dep1, tab_dep2 = st.tabs(["🧩 Data Dependency Analysis", "🔄 Loop Transformations"])
    
    with tab_dep1:
        st.subheader("8.7.2.2 Data Dependence Analysis")
        st.markdown("""
        To parallelize, the compiler must ensure the order doesn't matter.
        
        1.  **Flow Dependence (True):** Read after Write ($S1 \rightarrow S2$).
        2.  **Anti-dependence:** Write after Read ($S1 \leftarrow S2$).
        3.  **Output Dependence:** Write after Write ($S1=x, S2=x$).
        """)
        st.info("💡 **Compilers must respect Flow Dependence** – you can't read a value before it's calculated!")

    with tab_dep2:
        st.subheader("8.7.2.3 Loop Optimizations")
        st.markdown("""
        *   **Loop Unrolling:** Reducing jump overhead.
        *   **Loop Tiling (Blocking):** Breaking big loops into cache-sized "tiles".
        *   **Loop Fusion:** Combining loops that use the same data.
        """)

    st.divider()

    # --- 8.7.3 TOOLS ---
    st.header("🛠️ 8.7.3 Tools & Frameworks")
    
    tool_col1, tool_col2 = st.columns(2)
    
    with tool_col1:
        st.subheader("🔌 OpenMP")
        st.code("#pragma omp parallel for", language="cpp")
        st.caption("Shared Memory API. Uses 'Pragmas' to tell the compiler: 'Parallelize this loop!'")

    with tool_col2:
        st.subheader("📡 MPI")
        st.code("MPI_Send(&data, ...);", language="cpp")
        st.caption("Distributed Memory API. Processes talk to each other by 'passing messages'.")

    st.divider()

    # --- PRACTICAL: DATA DEPENDENCY LAB ---
    st.info("🧪 **Practical Lab: Data Dependency & Race Condition**")
    
    lab_choice = st.radio("Choose Lab View:", ["Dependency Visualizer", "Race Condition Simulator"], horizontal=True)
    
    if lab_choice == "Dependency Visualizer":
        st.markdown("Identify the dependence in this code:")
        st.code("""
        S1: A = B + C
        S2: D = A * 2
        """, language="python")
        
        dep_type = st.radio("What type is S1 -> S2?", ["Flow (True)", "Anti", "Output"])
        if dep_type == "Flow (True)":
            st.success("✅ Correct! S2 needs the value of 'A' produced by S1. This **cannot** be parallelized easily.")
        else:
            st.error("❌ Try again! S2 reads what S1 writes.")

    else:
        st.markdown("### 🏁 The Race Condition Simulator")
        st.write("Two threads increment a shared counter `x` (Initial x = 0).")
        
        speed1 = st.slider("Thread A Speed (ms delay)", 0, 100, 50)
        speed2 = st.slider("Thread B Speed (ms delay)", 0, 100, 20)
        
        if st.button("Run Simulation"):
            # Theoretical outcome
            st.warning("⚠️ **Race Result:** Final X = 1")
            st.error("❌ **Error:** Both threads read 0, incremented to 1, and wrote back 1. We lost an increment!")
            st.info("🛠️ **Solution:** Use `#pragma omp atomic` or Mutexes to lock the counter.")

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: 8.6 JIT"):
            st.session_state.unit2_topic = "8.6 JIT Compilation"
            st.rerun()
    with nav2:
        if st.button("Next: 8.8 Optimization Frameworks ➡️", use_container_width=True):
            st.session_state.unit2_topic = "8.8 Optimization Frameworks"
            st.rerun()

def render_optimization_frameworks():
    st.title("🚀 8.8 Compiler Optimization Frameworks")
    
    st.markdown("""
    Optimization is the "Magic" of compilation. It turns a correct-but-slow program into a lightning-fast masterpiece by rewriting the logic without changing the result.
    """)

    st.divider()

    # --- 8.8.1 INTRODUCTION ---
    st.header("📘 8.8.1 Introduction to Optimization")
    
    col_opt_goals, col_opt_types = st.columns(2)
    
    with col_opt_goals:
        st.subheader("🎯 Optimization Goals (PCSM)")
        st.markdown("""
        *   **Performance (P):** Make it run faster.
        *   **Code Size (C):** Make it smaller (Crucial for microchips).
        *   **Speed/Power (S):** Reduce battery drain.
        *   **Maintainability (M):** Clean code for the CPU.
        """)

    with col_opt_types:
        st.subheader("📐 Types of Optimization")
        st.markdown("""
        *   **Local:** Inside a single block of code.
        *   **Global:** Across multiple blocks in one function.
        *   **Interprocedural:** Across different functions or files.
        """)

    st.markdown("---")

    st.subheader("⏳ Static vs. Dynamic Optimization")
    st.markdown("""
    | Feature | Static (at Build Time) | Dynamic (at Runtime/JIT) |
    | :--- | :--- | :--- |
    | **Timing** | Happens once during `gcc` / `clang`. | Happens while the app is running. |
    | **Knowledge** | Limited to the source code. | Knows real CPU and real data. |
    | **Overhead** | Zero impact on user. | Can cause slight lag (JIT pauses). |
    | **Examples** | Loop Unrolling, Inlining. | Inline Caching, Speculative Opt. |
    """)

    st.divider()

    # --- 8.8.2 COMMON TECHNIQUES ---
    st.header("⚙️ 8.8.2 Common Optimization Techniques")
    
    tech_opt_col1, tech_opt_col2 = st.columns(2)
    
    with tech_opt_col1:
        st.markdown("### 🧱 Fundamental Techniques")
        st.markdown("""
        *   **Inlining:** Replacing a function call with its code.
        *   **Constant Folding:** `x = 2 + 2` becomes `x = 4`.
        *   **Dead Code Elimination (DCE):** Removing code that never runs or whose result is ignored.
        """)

    with tech_opt_col2:
        st.markdown("### 🏹 Advanced Hardware Control")
        st.markdown("""
        *   **Register Allocation:** Keeping the most used variables in CPU registers (ultra-fast).
        *   **Instruction Scheduling:** Reordering steps to avoid CPU "stalls".
        *   **Vectorization (SIMD):** Doing 4-8 additions in a single CPU tick.
        """)

    st.divider()

    # --- 8.8.3 FRAMEWORKS ---
    st.header("🏗️ 8.8.3 Industry Frameworks")
    
    tab_llvm, tab_gcc = st.tabs(["🛡️ LLVM (The Modern King)", "🐧 GCC (The Reliable Legend)"])
    
    with tab_llvm:
        st.markdown("""
        **LLVM Optimization Passes:**
        LLVM treats optimization as a sequence of "Passes". You can run them manually:
        ```bash
        opt -O3 input.ll -o optimized.ll
        ```
        *   **`-O1`**: Basic optimization.
        *   **`-O2`**: Standard balance of speed/size.
        *   **`-O3`**: Maximum speed (might increase code size).
        *   **`-Os`**: Optimize for smallest size.
        """)

    with tab_gcc:
        st.markdown("""
        **GCC Optimization Flags:**
        GCC uses flags like `-O2` or `-Ofast`. 
        *   It is known for its highly mature **Global Data Flow Analysis**.
        *   Used widely in Linux Kernel and low-level system software.
        """)

    st.divider()

    # --- PRACTICAL: OPTIMIZATION PLAYGROUND ---
    st.info("🧪 **Practical Lab: Optimization Playground**")
    st.markdown('See how a compiler "cleans" your code!')
    
    opt_mode = st.selectbox("Choose Optimization Pass:", 
                          ["Constant Folding", "Dead Code Elimination", "Loop Fusion"])
    
    lab_colA, lab_colB = st.columns(2)
    
    if opt_mode == "Constant Folding":
        with lab_colA:
            st.markdown("**Original Code**")
            st.code("""
            a = 10
            b = 20
            c = a + b + 5
            """, language="python")
        with lab_colB:
            st.markdown("**Optimized (Pass: ConstProp)**")
            st.code("""
            a = 10
            b = 20
            c = 35
            """, language="python")
            st.success("⚡ Result: Math done at compile time!")

    elif opt_mode == "Dead Code Elimination":
        with lab_colA:
            st.markdown("**Original Code**")
            st.code("""
            def run():
                x = 100
                y = x * 2
                return "Done"
            """, language="python")
        with lab_colB:
            st.markdown("**Optimized (Pass: DCE)**")
            st.code("""
            def run():
                return "Done"
            """, language="python")
            st.success("⚡ Result: Unused variables `x` and `y` removed!")

    elif opt_mode == "Loop Fusion":
        with lab_colA:
            st.markdown("**Original Code**")
            st.code("""
            for i in range(10):
                a[i] = 1
            for i in range(10):
                b[i] = 2
            """, language="python")
        with lab_colB:
            st.markdown("**Optimized (Pass: LoopFusion)**")
            st.code("""
            for i in range(10):
                a[i] = 1
                b[i] = 2
            """, language="python")
            st.success("⚡ Result: Reduced loop control overhead!")

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: 8.7 Parallel Support"):
            st.session_state.unit2_topic = "8.7 Parallel Programming"
            st.rerun()
    with nav2:
        if st.button("Next: 8.9 DSLs ➡️", use_container_width=True):
            st.session_state.unit2_topic = "8.9 Domain-Specific Languages"
            st.rerun()

def render_advanced_dsl():
    st.title("🎨 8.9 Domain-Specific Languages (DSL)")
    
    st.markdown("""
    While Python and C++ are "General Purpose", **DSLs** are specialized languages designed for a specific task (e.g., SQL for data, HTML for webs, or CSS for styling). 
    They sacrifice generality for **extreme efficiency** and **ease of use** in their domain.
    """)

    st.divider()

    # --- 8.9.1 INTRODUCTION TO DSLs ---
    st.header("🌐 8.9.1 Introduction to DSLs")
    
    col_def, col_ben = st.columns(2)
    
    with col_def:
        st.subheader("📖 8.9.1.1 Definition")
        st.markdown("""
        **Domain-Specific Languages (DSLs)** are programming languages tailored to a specific problem domain. 
        Unlike General Purpose Languages (GPLs), DSLs use notation and abstractions that are already familiar to domain experts.
        """)

    with col_ben:
        st.subheader("🌟 Benefits")
        st.markdown("""
        *   **Expressiveness:** Directly map concepts to code.
        *   **Abstraction:** Hide low-level "plumbing" code.
        *   **Productivity:** Work faster with domain-native workflows.
        *   **Validation:** Catch domain-specific errors early.
        """)

    st.markdown("### 🛠️ 8.9.1.2 Famous Examples")
    
    ex_sql, ex_html, ex_regex = st.columns(3)
    
    with ex_sql:
        st.markdown("**1. SQL**")
        st.caption("Structured Query Language for database manipulation.")
        st.code("SELECT name FROM users;", language="sql")

    with ex_html:
        st.markdown("**2. HTML**")
        st.caption("Hypertext Markup Language for structuring web content.")
        st.code("<h1>Hello World</h1>", language="html")

    with ex_regex:
        st.markdown("**3. Regex**")
        st.caption("A DSL for pattern matching and text processing.")
        st.code(r"[a-zA-Z0-9]+", language="text")

    st.divider()

    # --- 8.9.2 DESIGNING A DSL ---
    st.header("📐 8.9.2 Designing a DSL")
    
    col_dsl1, col_dsl2 = st.columns(2)
    
    with col_dsl1:
        st.subheader("💡 Key Considerations")
        st.markdown("""
        *   **Domain Scope:** What is the limit? (e.g., only music or only shapes).
        *   **Abstraction Level:** Hide complexity (e.g., `play C#` instead of MIDI frequencies).
        *   **Syntax:** Should it look like English, JSON, or Math?
        *   **Tooling:** Will it have auto-complete and error highlighting?
        """)

    with col_dsl2:
        st.subheader("📜 Syntax & Semantics")
        st.markdown("""
        *   **Syntax (The Grammar):** Defined using **EBNF**.
            *   *Example:* `Command := "draw" Shape "at" Coordinates`
        *   **Semantics (The Meaning):** What happens when the command runs?
            *   *Example:* Drawing pixels on a canvas.
        """)

    st.divider()

    # --- 8.9.3 IMPLEMENTING A DSL ---
    st.header("🛠️ 8.9.3 Implementing a DSL Compiler")
    
    st.markdown("""
    Building a DSL compiler follows the standard compiler phases but is usually **lighter**:
    1.  **Parsing:** Turning text into an **AST**.
    2.  **Validation:** Checking for semantic errors (e.g., `draw triangle at blue` is a type error).
    3.  **Code Gen:** Translating DSL commands into a host language like Python or JS.
    """)
    
    st.markdown("### 🧰 Popular Tools")
    st.info("""
    *   **ANTLR:** The industry standard parser generator (Java, C#, Python targets).
    *   **JetBrains MPS:** A "Projectional Editor" where you don't even type text—you manipulate nodes directly.
    *   **Xtext:** Build full-featured DSLs with IDE support (Auto-complete, Rename refactoring).
    """)

    st.divider()

    # --- PRACTICAL: MINI-DSL SHAPE PAINTER ---
    st.info("🧪 **Practical Lab: Mini-DSL 'Shape Painter'**")
    st.markdown("Try out a simple DSL! Commands: `draw circle`, `draw square`, `color red`, `color blue`.")
    
    dsl_input = st.text_input("Enter DSL Commands (e.g., 'draw circle'):", "draw circle")
    
    # Simple DSL Interpreter Logic
    tokens = dsl_input.lower().split()
    
    with st.expander("🔍 Compiler Trace (Tokenization & Parsing)"):
        st.write(f"**Tokens:** `{tokens}`")
        if len(tokens) >= 2:
            st.success(f"**AST Node:** `Action: {tokens[0]}, Object: {tokens[1]}`")
        else:
            st.error("❌ Syntax Error: Incomplete command.")

    # Visualization
    if len(tokens) >= 2 and tokens[0] == "draw":
        shape = tokens[1]
        color = "white"
        
        # Check if color was set previously or in command (simulating state)
        if "color" in dsl_input:
            parts = dsl_input.split("color")
            if len(parts) > 1: color = parts[1].strip().split()[0]

        st.markdown(f"**Executing Object Code (Rendering {shape} in {color})...**")
        
        # Dot visualization for the "Object Code" (Canvas)
        if shape == "circle":
            st.graphviz_chart(f'digraph {{ node [shape=circle, style=filled, fillcolor={color}]; A [label="DSL Object"]; }}')
        elif shape == "square":
            st.graphviz_chart(f'digraph {{ node [shape=square, style=filled, fillcolor={color}]; A [label="DSL Object"]; }}')
        else:
            st.warning("⚠️ Semantic Error: Unknown shape.")

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: 8.8 Optimization"):
            st.session_state.unit2_topic = "8.8 Optimization Frameworks"
            st.rerun()
    with nav2:
        st.button("🎯 Unit 2 Advanced Completed!", disabled=True, use_container_width=True)
