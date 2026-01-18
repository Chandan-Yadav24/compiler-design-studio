import streamlit as st
import pandas as pd
import random
import re
import modules.unit1_fa as unit1_fa
import modules.nfa_to_dfa_lab as nfa_to_dfa_lab
import modules.unit1_syntax as unit1_syntax
import modules.unit1_parsing as unit1_parsing
import modules.unit1_topdown as unit1_topdown
import modules.unit1_recursion as unit1_recursion
import modules.unit1_factoring as unit1_factoring
import modules.unit1_ll1 as unit1_ll1
import modules.unit1_stack as unit1_stack
import modules.unit1_semantic as unit1_semantic
import modules.unit1_icg as unit1_icg
import modules.unit1_tac as unit1_tac
import modules.unit1_optimization as unit1_optimization
import modules.unit1_dag as unit1_dag
import modules.unit1_first_follow as unit1_first_follow

def render():
    st.markdown("""
    <div class="premium-card">
        <h2>📂 Module I - Unit 1: Front End of Compiler</h2>
        <p>The front end analyzes the source code to build an intermediate representation (IR). It includes lexical, syntax, and semantic analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Optimized topics list with numbering
    topics = [
        "1.1 Introduction", 
        "1.2 Introduction to Compiler Design",
        "1.3 Role & Importance of Compilers",
        "1.4 Phases of Compilation Process",
        "1.5 Compiler Architecture & Components",
        "2.1 Lexical Analysis",
        "2.2 Regular Expressions",
        "2.3 Standard Regular Expression",
        "2.4 Finite Automata & Subset Construction",
        "2.6 NFA to DFA Conversion Lab",
        "3.1 Grammar Basics (4-Tuple)",
        "3.2 Chomsky Hierarchy (Types of Grammar)",
        "3.3 Parse Trees & Grammar Capabilities",
        "3.4 Derivations (LMD & RMD)",
        "3.5 Reduction (Process & Example)",
        "3.6 Parse Trees & Ambiguity (Digitized Notes)",
        "4.0 Syntax Analysis Overview & Top-Down Parser",
        "4.1 Introduction to Parsers",
        "4.2 Left Recursion (Elimination)",
        "4.3 Left Factoring",
        "4.4 FIRST and FOLLOW Sets",
        "4.5 LL(1) Predictive Parsing Table",
        "4.6 LL(1) Stack Implementation",
        "5.1 Semantic Analysis (SDT & SDD)",
        "5.2 Intermediate Code Generation",
        "5.3 Three-Address Code (TAC)",
        "5.4 Dead Code Elimination",
        "5.5 Directed Acyclic Graph (DAG)"
    ]
    
    # Session state for dropdown navigation
    if "unit1_topic" not in st.session_state:
        st.session_state.unit1_topic = "1.1 Introduction"

    # Ensure the session state value is in the options list
    if st.session_state.unit1_topic not in topics:
        st.session_state.unit1_topic = topics[0]

    selected_topic = st.selectbox("Select Topic", topics, key="unit1_topic")
    
    st.markdown("---")
    
    # ==========================
    # TOPIC 1.1: INTRODUCTION
    # ==========================
    if selected_topic == "1.1 Introduction":
        st.subheader("1.1 Introduction to Compiler Design (Analysis Phase)")
        
        st.markdown("""
        ### 🏗️ FRONT END (Analysis Phase)
        **Source Language Dependent | Target Machine Independent**
        
        The Front End focuses of understanding the source code correctly. It follows the **Analysis → Synthesis Model**.
        
        #### 🔄 5 Main Phases
        1. **Lexical Analysis (Scanner)**: Removes whitespace, tokenizes.
        2. **Syntax Analysis (Parser)**: Checks grammar, builds parse tree.
        3. **Semantic Analysis**: Checks meaning (types, scope).
        4. **Intermediate Code Generation**: Produces IR (e.g., TAC).
        5. **Symbol Table Creation**: Stores variable/function info.
        
        *(Note: Some front-end optimizations are possible here)*
        
        ---
        
        ### 🧠 Quick Recall Mnemonic: **LPSIC-S**
        **L**exical → **P**arsing → **S**emantic → **I**ntermediate Code → **S**ymbol Table
        
        > **Exam One-Liner:** "Front-End = LPSIC → Converts source code → IR + Symbol Table (machine-independent part)"
        """)

        st.markdown("### 🆚 Imperative (C++/Java) vs Functional (Haskell)")
        st.info("Haskell is purely functional... (demonstrating how Front-End depends on Source Language)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.code("""
# HASKELL (Functional)
factorial n = if n == 0 then 1 else n * factorial (n-1)

main = print (factorial 5)
-- Output: 120
            """, language="haskell")
        with col2:
            st.code("""
// C++ (Imperative)
int factorial(int n) {
    if (n == 0) return 1;
    else return n * factorial(n-1);
}
int main() {
    cout << factorial(5);
}
            """, language="cpp")
        
        st.markdown("""
        ### 🆚 Haskell Example (Front-End Differences)
        | Phase | What Happens in Python/C++/Java (Imperative) | What Happens in HASKELL (Functional) |
        | :--- | :--- | :--- |
        | **Lexical** | Reads `int x = 5;` | Reads `x = 5` (No types!) |
        | **Syntax** | Checks semicolons `;`, braces `{}` | Layout (indentation) matters. |
        | **Semantic** | Checks explicit types | **Type Inference!** |
        """)
        
        # Callback for Next Button
        def go_to_1_2():
            st.session_state.unit1_topic = "1.2 Introduction to Compiler Design"
            
        st.button("Next: 1.2 Introduction to Compiler Design ➡️", use_container_width=True, on_click=go_to_1_2)

    # ==========================
    # TOPIC 1.2: COMPILER DESIGN BASICS
    # ==========================
    elif selected_topic == "1.2 Introduction to Compiler Design":
        st.subheader("1.2 Introduction to Compiler Design (Exam Notes)")
        
        st.markdown("""
        #### Compiler = Magic Translator ✨
        *   **High-Level Code (Human)** → **Machine Code (0s & 1s Robot)**
        *   `Source Program` → **Compiler** → `Object/Target Program`
        *   *Without Compiler = Your code is just beautiful poetry that computer ignores!*

        ### 🆚 Compiler vs Assembler (Exam Favorite)
        | Feature | Assembler | Compiler (Boss) |
        | :--- | :--- | :--- |
        | **Intelligence** | Dumb | Super Smart |
        | **Input** | Assembly | C/Java/Python/etc. |
        | **Checks** | Almost nothing | Types, errors, limits |
        | **Speed** | Fast | Slower (but worth it) |
        | **Memory** | Tiny | Eats RAM like monster |

        ### 🕵️ Two Secret Names of Compiler
        1.  **Self Compiler / Resident**: Runs & compiles for same machine.
        2.  **Cross Compiler**: Compiles on Windows → Runs on Android/Linux (God-level power!).

        ### 🔗 The Epic Toolchain (4 Heroes in Order)
        1.  **Preprocessor**: `#include`, `#define` → Replaces macros, pastes files.
        2.  **Compiler**: Real hero! Does Lexical + Syntax + Semantic + IR + Optimization.
        3.  **Assembler**: Assembly → `.o` (object file).
        4.  **Linker**: Joins all `.o` files + libraries → Final EXE.
        
        > **Exam One-Liner:** "Toolchain Order: Preprocessor → Compiler → Assembler → Linker (PCAL)"

        ### 🧩 Types of Compilers
        | Type | Nickname | One-Liner Story |
        | :--- | :--- | :--- |
        | **Single Pass** | One-Shot Hero | Reads line → compiles line → done! (Fast but weak) |
        | **Two Pass** | Double Checker | Front-end once, Back-end once → more powerful |
        | **Multipass** | Perfectionist | Goes back & forth 10 times → GCC style |
        | **JIT (Just-In-Time)** | Runtime Ninja | Compiles while running → Java, JavaScript, PyPy |
        | **Cross Compiler** | Traveler | Compile on laptop → run on phone/Arduino |
        | **Bytecode Compiler** | JVM/CPython style | → `.class` / `.pyc` (portable fake machine code) |
        """)
        
        st.success("Top 3 Exam One-Liners:\n1. Compiler is a smart translator... unlike dumb assembler!\n2. PCAL (Preprocessor -> Linker)\n3. JIT compiles at runtime, Single-pass = fastest but weakest!")

        # Callback for Next Button
        def go_to_1_3():
            st.session_state.unit1_topic = "1.3 Role & Importance of Compilers"

        st.button("Next: 1.3 Role & Importance of Compilers ➡️", use_container_width=True, on_click=go_to_1_3)

    # ==========================
    # TOPIC 1.3: ROLE & IMPORTANCE
    # ==========================
    elif selected_topic == "1.3 Role & Importance of Compilers":
        st.subheader("1.3 ROLE & IMPORTANCE OF COMPILERS (Superhero of Programming)")
        
        st.markdown("""
        ### 🦸 Compiler = Superhero of Programming
        
        #### ❤️ ADVANTAGES (Why We Love Compilers)
        | Advantage | Real-Life Example |
        | :--- | :--- |
        | **Blazing Fast Execution** | C program runs 10–100x faster than same Python script |
        | **Zero Dependency** | You send `.exe` → friend double-clicks → runs! No Python/Java needed |
        | **Super Portable (Write Once)** | Write C → compile for Windows, Linux, Mac, Android, fridge → works! |
        | **Catches Bugs Early** | `int x = "hello";` → Compiler shouts **ERROR** before running! |
        | **Amazing Debugging Tools** | `gcc -g` + `gdb` → step line by line like Netflix pause |
        | **Security Guard** | Stops buffer overflow, type bugs → hackers cry |
        
        #### ⚡ DISADVANTAGES (The Dark Side)
        | Downside | Real Example |
        | :--- | :--- |
        | **Long compilation time** | Compiling Chrome/Chromium = 2+ hours! |
        | **Must recompile for each machine** | Compile on Windows → won't run on Linux without recompiling |
        | **Doesn’t catch all bugs** | Logic errors, infinite loops → compiler says “Looks fine bro” |
        | **Eats RAM & CPU during compile** | `g++ -O3 bigproject.cpp` → your laptop fan goes **BRRR** |
        
        --- 
        
        ### 🌍 USES & APPLICATIONS (Where Compilers Rule the World)
        | Field | Example | Language + Compiler |
        | :--- | :--- | :--- |
        | **Operating Systems** | Windows, Linux kernel | C + GCC/Clang |
        | **Games** | Call of Duty, GTA | C++ + Visual Studio / Clang |
        | **Embedded / IoT** | Your smartwatch, car ECU | C + arm-gcc (cross compiler) |
        | **Phones** | Android apps (native part) | C/C++ + NDK |
        | **High-Performance Science** | Weather prediction, AI training | Fortran/C++ + Intel/GCC |
        | **Browsers** | Chrome, Firefox | C++ + massive compilers |
        
        > **Exam One-Liner (Guaranteed Marks!):**
        > "Compiler gives us speed, portability, security & zero dependency – that's why Linux, games, phones, rockets all use compilers, not interpreters!"
        
        ---
        
        ### 🥊 Bonus Comparison Table (Paste in Answer Sheet!)
        | Feature | Compiler (C/C++) | Interpreter (Python) | Winner? |
        | :--- | :--- | :--- | :--- |
        | **Speed** | Rocket 🚀 | Bicycle 🚲 | **Compiler** |
        | **Startup time** | Slow (compile first) | Instant | **Interpreter** |
        | **Distribution** | Just `.exe` | Need Python installed | **Compiler** |
        | **Debugging errors early** | Yes | No (runtime only) | **Compiler** |
        | **Edit & test speed** | Slow (recompile) | Fast | **Interpreter** |
        
        """)
        
        st.success("Final Quote to Write in Exam:\n'Without compilers, there would be no WhatsApp, no PUBG, no Windows, no cars with ECU – only slow scripts and sad programmers.'")

        # Callback for Next Button
        def go_to_1_4():
            st.session_state.unit1_topic = "1.4 Phases of Compilation Process"

        st.button("Next: 1.4 Phases of Compilation Process ➡️", use_container_width=True, on_click=go_to_1_4)

    # ==========================
    # TOPIC 1.4: PHASES OF COMPILATION
    # ==========================
    elif selected_topic == "1.4 Phases of Compilation Process":
        st.subheader("1.4 THE 6 EPIC PHASES OF A COMPILER")
        
        st.success("""
        **Remember:** L → S → S → I → O → T
        
        **L**exical → **S**yntax → **S**emantic → **I**ntermediate → **O**ptimization → **T**arget Code
        """)

        st.markdown("""
        ### 🛤️ Full Journey with Real Example
        **Source Code:**
        ```c
        int main() {
            int a = 10 + 5 * 2;
        }
        ```

        | Phase | Nickname | Input → Output | Real Example (on above code) |
        | :--- | :--- | :--- | :--- |
        | **1. Lexical Analysis** | Token Maker | Source code → Tokens | `int`, `main`, `(`, `)`, `{`, `int`, `a`, `=`, `10`, `+`, `5`, `*`, `2`, `;` |
        | **2. Syntax Analysis** | Grammar Police | Tokens → Parse Tree | Checks: brackets matched? semicolon? → Builds tree |
        | **3. Semantic Analysis** | Meaning Checker | Parse Tree → Annotated Tree | Checks: `a` is declared? types match? **OK!** |
        | **4. Intermediate Code** | 3-Address Code | Tree → Three Address Code (TAC) | `t1 = 5 * 2` <br> `t2 = 10 + t1` <br> `a = t2` |
        | **5. Code Optimization** | Speed Demon | TAC → Optimized TAC | `t1 = 10` <br> `a = 10 + t1` → `a = 20` (constant folding!) |
        | **6. Target Code Gen** | Machine Whisperer | Optimized TAC → Assembly | `mov eax, 20` <br> etc... |
        
        ---
        
        ### 👁️ One Example → All Phases Visualized!
        
        *   **Lexical**: `<id,a> = <num,10> + <num,5> * <num,2>`
        *   **Syntax Tree**: `( = a ( + 10 ( * 5 2 ) ) )`
        *   **Semantic**: All types `int` → OK
        *   **Intermediate Code**:
            ```text
            t1 = 5 * 2
            t2 = 10 + t1
            a = t2
            ```
        *   **After Optimization**: `a = 20` (Compiler calculated at compile time!)
        *   **Target Code (x86)**: `mov dword ptr [a], 20`
        
        > **Quick Mnemonic:** "Lazy Students Study In Office Time"
        
        ---
        
        ### ⚡ Optimization Techniques (Top 5 for Exam)
        | Technique | What it does | Example |
        | :--- | :--- | :--- |
        | **Constant Folding** | Pre-calculate math | `5 * 2` → `10` |
        | **Constant Propagation** | Replace vars with values | `x=5; y=x+1` → `y=6` |
        | **Dead Code Elimination** | Remove unused code | `int x=10;` (never used) → delete |
        | **Strength Reduction** | Use faster math | `i*2` → `i+i` or `i<<1` |
        | **Common Subexpression** | Reuse results | `a=b+c; d=b+c` → `temp=b+c`... reuse `temp` |
        
        ### 🔄 Front End vs Back End (Most Important!)
        | Front End (Language Dependent) | Back End (Machine Dependent) |
        | :--- | :--- |
        | Lexical + Syntax + Semantic + IC Gen | Optimization + Target Code Gen |
        | Same for C, Java, Python (mostly) | Different for x86, ARM, RISC-V |
        
        ### 🎟️ Passes Explained Simply
        *   **Single Pass**: Does everything in one go (old & rare).
        *   **Two Pass**: Front end → IC → Back end.
        *   **Multi Pass**: GCC does 20+ passes for max optimization (`-O3`).

        """)
        
        st.info("Exam Golden Lines:\n1. 'The 6 phases are: L-S-S-I-O-T'\n2. 'Front-end (first 4) depends on source language, Back-end (last 2) depends on target machine'\n3. 'Optimization turns 5*2+10 into 20 at compile time → saves CPU cycles!'")

        # Callback for Next Button
        def go_to_1_5():
            st.session_state.unit1_topic = "1.5 Compiler Architecture & Components"

        st.button("Next: 1.5 Compiler Architecture & Components ➡️", use_container_width=True, on_click=go_to_1_5)

    # ==========================
    # TOPIC 1.5: ARCHITECTURE & COMPONENTS
    # ==========================
    elif selected_topic == "1.5 Compiler Architecture & Components":
        st.subheader("1.5 COMPILER ARCHITECTURE & COMPONENTS (Super Short & Exam-Ready!)")
        
        st.markdown("""
        ### 🏭 Compiler = Two Big Bosses
        
        | Analysis Phase (Front-End) | Synthesis Phase (Back-End) |
        | :--- | :--- |
        | **Language Expert** 🗣️ | **Machine Expert** ⚙️ |
        | Understands C/Java/Python | Knows x86, ARM, RISC-V |
        | Makes Intermediate Code + Symbol Table | Makes fast machine code |
        
        ---

        #### 🗣️ Front-End (Analysis) – "I Speak Human Language"
        | Component | Nickname | Job (Simple) | Example |
        | :--- | :--- | :--- | :--- |
        | **Scanner / Lexer** | Token Ninja | Chops code into tokens (words) | `int x = 5;` → 5 tokens |
        | **Parser** | Grammar Police | Checks structure → builds AST (tree) | Checks `{ }` match |
        | **Semantic Analyzer** | Logic Detective | Checks meaning (types, declared?) | `x + "hello"` → **ERROR** |
        | **Intermediate Code Gen** | IR Factory | Makes Three-Address Code / LLVM IR | `t1 = a + b` |
        
        #### ⚙️ Back-End (Synthesis) – "I Speak CPU"
        | Component | Job |
        | :--- | :--- |
        | **Instruction Selection** | Picks best CPU instructions |
        | **Code Optimization** | Makes code super fast (register allocation, etc.) |
        | **Code Emission** | Outputs final `.o` (object) or `.exe` file |

        ---
        
        ### 🏛️ Full Architecture Diagram (Draw This in Exam!)
        
        ```text
        Source Code
             ↓
        [ Scanner ] → Tokens
             ↓
        [ Parser ] → AST (Abstract Syntax Tree)
             ↓
        [ Semantic ] → Annotated AST + Symbol Table
             ↓
        [ IR Generator ] → Intermediate Code (e.g., LLVM IR, 3AC)
             ↓
        [ Optimizer ] → Faster IR
             ↓
        [ Code Generator ] → Assembly (.s)
             ↓
        [ Assembler ] → Object File (.o)
             ↓
        [ Linker + Loader ] → Final EXE / Binary
        ```
        
        ### 🚦 Pass vs Phase (Exam Question Alert!)
        | Term | Meaning | Example |
        | :--- | :--- | :--- |
        | **Phase** | One specific job (e.g., Lexical, Parsing) | 1 phase = 1 task |
        | **Pass** | Full traversal of source code | 1 Pass can have many phases |
        
        ---

        ### 🧩 Most Important Concept: Modular Design
        **Why GCC/Clang/LLVM are Legends:** You can mix and match!
        
        **Formula:** `Front-End + Back-End = New Compiler!`
        
        | Front-End | Back-End | Result |
        | :--- | :--- | :--- |
        | C Front-End | x86 Back-End | **GCC for PC** |
        | C Front-End | ARM Back-End | **Android NDK** |
        | Java Front-End | JVM Back-End | **javac** |
        | Rust Front-End | LLVM Back-End | **rustc** |
        
        > **One-Liner to Impress Teacher:**
        > "Modern compilers like LLVM separate Front-End and Back-End completely – so one language can target 50 CPUs, and one CPU can run 50 languages!"
        """)
        
        st.success("""
        **Final Exam Golden Lines (Write & Win!)**
        1. "Compiler has two parts: Analysis (Front-End) → understands language, Synthesis (Back-End) → talks to machine."
        2. "Front-End is language-dependent, Back-End is machine-dependent → that's why we can make cross-compilers!"
        3. "LLVM is the king because 20+ languages (C++, Rust, Swift, Julia) use same LLVM Back-End → one back-end, infinite languages!"
        """)
        
        # Callback for Next Button
        def go_to_2_1():
            st.session_state.unit1_topic = "2.1 Lexical Analysis"

        st.button("Next: 2.1 Lexical Analysis ➡️", use_container_width=True, on_click=go_to_2_1)

    # ==========================
    # TOPIC 2.1: LEXICAL ANALYSIS
    # ==========================
    elif selected_topic == "2.1 Lexical Analysis":
        st.subheader("2.1 LEXICAL ANALYSIS (The First Hero)")
        
        st.markdown("""
        ### 🔎 Lexical Analyzer = Scanner = Token Ninja 🥷 
        **Job:** Chop source code into **Tokens**.
        
        ```c
        int main() { printf("Hello"); }
        ```
        ⬇️ **Becomes** ⬇️
        ```text
        <int> <main> <(> <)> <{> <id,printf> <(> <string,"Hello"> <)> <;> <}>
        ```
        
        ---

        #### 🔑 3 Golden Terms (Must Remember!)
        | Term | Meaning | Example |
        | :--- | :--- | :--- |
        | **Token** | Category / Type | `id`, `keyword`, `number`, `+` |
        | **Lexeme** | Actual text that matches the token | `printf`, `100`, `"hello"`, `=` |
        | **Pattern** | Rule to recognize token | `[a-zA-Z_][a-zA-Z0-9_]*` → `id` |
        
        #### 📝 Example Table (Write in Exam!)
        | Source Code | Token | Lexeme |
        | :--- | :--- | :--- |
        | `int` | keyword | `int` |
        | `count` | id | `count` |
        | `=` | = | `=` |
        | `100` | number | `100` |
        | `+` | + | `+` |
        | `;` | ; | `;` |
        
        ---
        
        ### ⚙️ Role / Tasks of Lexical Analyzer (7 Main Jobs)
        1.  **Read source code** character by character.
        2.  **Group characters** into lexemes.
        3.  **Produce tokens** and send to parser.
        4.  **Remove whitespace** and comments.
        5.  **Insert identifiers** into Symbol Table.
        6.  **Report lexical errors** (e.g., `@abc` illegal).
        7.  **Help show error** line numbers.
        
        ### 🤝 How It Works with Parser
        > **Parser:** "Hey lexer, give me next token!"
        > **Lexer:** reads chars → finds "if" → returns `<keyword, if>`
        > **Parser:** happy → continues building tree
        
        ---

        ### ❓ Why Separate Lexical Analysis from Parsing? (Top Exam Question!)
        | Reason | Benefit |
        | :--- | :--- |
        | **Simplicity** | Parser doesn’t deal with spaces/comments |
        | **Speed** | Lexer uses fast techniques (DFA, buffering) |
        | **Portability** | Input handling stays in lexer only |
        | **Reusability** | Same lexer for compiler, IDE, syntax highlighter |
        
        ### ✅ Advantages vs ❌ Disadvantages
        | Advantages | Disadvantages |
        | :--- | :--- |
        | Faster compiler | Takes time to scan whole file |
        | Cleaner code | Extra memory for symbol table |
        | Easier error reporting | Hard to write lexer by hand (tools like Lex help!) |
        
        ---
        
        ### 🛠️ Tools Used
        *   **Lex / Flex** → Automatically generates lexical analyzer from regular expressions.
        
        """)
        
        st.success("""
        **Best Exam One-Liners**
        1. "Lexical Analyzer is the first phase that converts source code into a sequence of tokens by removing whitespaces and comments."
        2. "Token = category, Lexeme = actual string, Pattern = rule"
        3. "Lexical analysis is separated from parsing for simplicity, efficiency, and portability."
        """)
        
        # Callback for Next Button
        def go_to_2_2():
            st.session_state.unit1_topic = "2.2 Regular Expressions"

        st.button("Next: 2.2 Regular Expressions ➡️", use_container_width=True, on_click=go_to_2_2)
        
    # ==========================
    # TOPIC 2.2: REGULAR EXPRESSIONS
    # ==========================
    elif selected_topic == "2.2 Regular Expressions":
        st.subheader("2.2 REGULAR EXPRESSIONS (Math-Style Exam Notes)")
        
        st.markdown(r"""
        ### 1️⃣ Functions of Lexical Analysis (Scanner)
        **Lexical Analyzer** = 1st phase of compiler. 
        *   **Input** = character stream
        *   **Output** = token stream
        
        #### Main Responsibilities:
        1.  **Tokenization**: $chars \longrightarrow tokens$
        2.  **Remove whitespace & comments**: Ignores blanks, tabs, newlines, comments (not passed to parser).
        3.  **Lexical error detection**: Reports invalid characters / unknown lexemes.
        4.  **Symbol table management**: When identifier lexeme found → enter/update symbol table (name, type, scope, etc.).
        5.  **Interface to parser**: Returns tokens on request (e.g., `getNextToken()`).

        ---

        ### 2️⃣ Regular Expressions (RE)
        
        #### Definition
        A **Regular Expression (RE)** is a pattern describing a set of strings (a language).
        
        Let $T$ be an alphabet (set of symbols).  
        A regular expression $R$ defines a language $L(R) \subseteq T^*$.

        ---

        ### 3️⃣ Recursive (Formal) Definition of RE over alphabet $T$
        
        | Rule | Expression | Language Defined |
        | :--- | :--- | :--- |
        | 1 | $\emptyset$ | $L(\emptyset) = \emptyset$ (empty language) |
        | 2 | $\epsilon$ | $L(\epsilon) = \{\epsilon\}$ (empty string) |
        | 3 | $a, a \in T$ | $L(a) = \{a\}$ |
        | 4 | $P + R$ | $L(P+R) = L(P) \cup L(R)$ (union / OR) |
        | 5 | $P \cdot Q$ (or $PQ$) | $L(PQ) = L(P) L(Q)$ (concatenation) |
        | 6 | $P^*$ | $L(P^*) = (L(P))^*$ (Kleene star) |
        | 7 | — | Nothing else is a regular expression |
        
        #### Notes (symbols):
        *   $+$ = union
        *   $\cdot$ / juxtaposition = concatenation
        *   $^*$ = 0 or more repetitions

        ---

        ### 4️⃣ Quick Examples (Exam-Friendly)
        
        If $T = \{a, b\}$:
        
        *   **Union:**
            *   $R = a + b$
            *   $L(R) = \{a, b\}$
        
        *   **Concatenation:**
            *   $R = ab$
            *   $L(R) = \{ab\}$
            
        *   **Kleene Star:**
            *   $R = a^*$
            *   $L(R) = \{\epsilon, a, aa, aaa, \dots\}$
            
        *   **Combination:**
            *   $R = (a+b)^*$
            *   $L(R) = T^* = \{\epsilon, a, b, ab, ba, aab, \dots\}$
        """)
        
        st.success("Mathematical rigor is key here! Remember the Kleene Star (*) means ZERO or MORE repetitions.")
        
        st.markdown("---")
        st.subheader("🎮 Interactive Regex Playground")
        
        # Tab layout for the two features
        tab1, tab2 = st.tabs(["🎲 Random Regex Challenge", "🛠️ Verify Your Own Regex"])
        
        with tab1:
            st.markdown("#### Test your understanding!")
            if st.button("Generate Random Regex Example"):
                examples = [
                    {
                        "regex": r"^a*b+$", 
                        "desc": "Start with any number of 'a's (including zero), followed by one or more 'b's.", 
                        "explain": "**^** (Start) + **a*** (Zero or more 'a') + **b+** (One or more 'b') + **$** (End)",
                        "match": ["b", "ab", "aaab", "abbb"], 
                        "no_match": ["a", "ba", "bba"]
                    },
                    {
                        "regex": r"^(0|1)*1$", 
                        "desc": "Binary strings strictly ending with 1.", 
                        "explain": "**^** (Start) + **(0|1)*** (Any mix of 0s & 1s) + **1** (Must have '1') + **$** (End)",
                        "match": ["1", "01", "111", "0001"], 
                        "no_match": ["0", "10", "100", ""]
                    },
                    {
                        "regex": r"^[A-Z][a-z]*$", 
                        "desc": "Capitalized words.", 
                        "explain": "**^** (Start) + **[A-Z]** (One Uppercase) + **[a-z]*** (Any Lowercase) + **$** (End)",
                        "match": ["Hello", "A", "Python"], 
                        "no_match": ["hello", "HELLO", "123"]
                    },
                    {
                        "regex": r"^\d{3}-\d{2}-\d{4}$", 
                        "desc": "US SSN format (###-##-####).", 
                        "explain": "**^** (Start) + **\d{3}** (3 digits) + **-** (dash) + **\d{2}** (2 digits) + **-** (dash) + **\d{4}** (4 digits) + **$** (End)",
                        "match": ["123-45-6789"], 
                        "no_match": ["123456789", "12-34-5678"]
                    },
                    {
                        "regex": r"^a(b|c)*d$", 
                        "desc": "Starts with 'a', then any mix of 'b' or 'c', ends with 'd'.", 
                        "explain": "**^** (Start) + **a** (Must be 'a') + **(b|c)*** (Mix of 'b'/'c') + **d** (Must be 'd') + **$** (End)",
                        "match": ["ad", "abd", "acd", "abbccd"], 
                        "no_match": ["abc", "add", "d"]
                    }
                ]
                # Store in session state to persist after reload
                st.session_state.random_regex = random.choice(examples)
            
            if "random_regex" in st.session_state:
                ex = st.session_state.random_regex
                st.info(f"👉 **Pattern:** `{ex['regex']}`")
                
                # Handle legacy session state without crashing
                explanation = ex.get('explain', "Click **Generate Random Regex Example** to see the explanation!")
                st.markdown(f"**👇 Simple Explanation:**\n\n{explanation}")
                
                st.write(f"_{ex['desc']}_")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.success(f"✅ **Matches:** {', '.join(ex['match'])}")
                with c2:
                    st.error(f"❌ **Non-Matches:** {', '.join(ex['no_match'])}")
                    
        with tab2:
            st.markdown("#### 🛠️ Verify & Build Your Own Regex")
            
            # Helper: Cheat Sheet
            with st.expander("📖 Regex Quick Guide (Cheat Sheet) - Click to Open"):
                st.markdown("""
                | Symbol | Name | Meaning | Example |
                | :--- | :--- | :--- | :--- |
                | `^` | **Caret** | Start of string | `^Hello` matches start |
                | `$` | **Dollar** | End of string | `World$` matches end |
                | `.` | **Dot** | Any character (except newline) | `a.c` matches `abc`, `axc` |
                | `*` | **Star** | 0 or more repetitions | `a*` matches `(empty)`, `a`, `aaaa` |
                | `+` | **Plus** | 1 or more repetitions | `a+` matches `a`, `aa` (not empty) |
                | `?` | **Question** | 0 or 1 time (Optional) | `colou?r` matches `color`, `colour` |
                | `\d` | **Digit** | Any number 0-9 | `\d\d` matches `25`, `99` |
                | `[abc]` | **Set** | Character set (only a, b, or c) | `[aeiou]` matches vowels |
                """)

            # Helper: Common Pre-built Patterns
            template = st.selectbox("⚡ Quick Templates (Select to auto-fill):", 
                                    ["Custom (Write your own)", 
                                     "Email Address", 
                                     "Phone Number (US)", 
                                     "Only Digits", 
                                     "Capitalized Word"])
            
            default_regex = r"^a*b+$"
            default_test = "aaab"
            
            if template == "Email Address":
                default_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
                default_test = "test@example.com"
            elif template == "Phone Number (US)":
                default_regex = r"^\d{3}-\d{2}-\d{4}$"
                default_test = "123-45-6789"
            elif template == "Only Digits":
                default_regex = r"^\d+$"
                default_test = "9876543210"
            elif template == "Capitalized Word":
                default_regex = r"^[A-Z][a-z]+$"
                default_test = "Python"

            user_regex = st.text_input("Enter Regular Expression:", value=default_regex)
            test_string = st.text_input("Enter Test String:", value=default_test)
            
            if user_regex and test_string:
                try:
                    if re.search(user_regex, test_string):
                        st.success(f"✅ **Match Found!**")
                        st.write(f"The string `{test_string}` matches the pattern `{user_regex}`")
                    else:
                        st.error(f"❌ **No Match.**")
                        st.write(f"The string `{test_string}` does NOT match `{user_regex}`")
                except re.error as e:
                    st.error(f"⚠️ **Invalid Regex:** {e}")

        # Callback for Next Button
        def go_to_2_3():
            st.session_state.unit1_topic = "2.3 Standard Regular Expression"

        st.button("Next: 2.3 Standard Regular Expression ➡️", use_container_width=True, on_click=go_to_2_3)

    # ==========================
    # TOPIC 2.3: STANDARD REGULAR EXPRESSION
    # ==========================
    elif selected_topic == "2.3 Standard Regular Expression":
        st.subheader("2.3 Standard Regular Expression (Thompson’s Construction)")
        
        st.markdown("""
        ### 🎯 Goal
        Build an **ε-NFA** for any Regular Expression by combining small NFAs with fixed templates.
        
        ---

        ### 1️⃣ Base NFAs (Building Blocks)
        """)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**(a) Null set:** $R = \emptyset$")
            st.graphviz_chart('''
            digraph {
                rankdir=LR;
                bgcolor="transparent";
                edge [color=white, fontcolor=white];
                node [shape=circle, style=filled, fillcolor="white", fontcolor="black"];
                S [label="S"];
                F [label="F", shape=doublecircle];
            }
            ''')
        with c2:
            st.markdown("**(b) Empty:** $R = \epsilon$")
            st.graphviz_chart('''
            digraph {
                rankdir=LR;
                bgcolor="transparent";
                edge [color=white, fontcolor=white];
                node [shape=circle, style=filled, fillcolor="white", fontcolor="black"];
                S [label="S"];
                F [label="F", shape=doublecircle];
                S -> F [label="ε"];
            }
            ''')
        with c3:
            st.markdown("**(c) Symbol:** $R = a$")
            st.graphviz_chart('''
            digraph {
                rankdir=LR;
                bgcolor="transparent";
                edge [color=white, fontcolor=white];
                node [shape=circle, style=filled, fillcolor="white", fontcolor="black"];
                S [label="S"];
                F [label="F", shape=doublecircle];
                S -> F [label="a"];
            }
            ''')
        
        st.markdown("---")
        st.markdown("### 2️⃣ Operators (Templates)")
        
        st.write("**(A) Union:** $R = P + Q$ (Parallel Paths)")
        st.graphviz_chart('''
        digraph {
            rankdir=LR;
            bgcolor="transparent";
            edge [color=white, fontcolor=white];
            node [shape=circle, style=filled, fillcolor="white", fontcolor="black"];
            S [label="Start"];
            F [label="Final", shape=doublecircle];
            SP [label="Start P"]; FP [label="Final P"];
            SQ [label="Start Q"]; FQ [label="Final Q"];
            
            S -> SP [label="ε"];
            S -> SQ [label="ε"];
            SP -> FP [label="P", style=dashed];
            SQ -> FQ [label="Q", style=dashed];
            FP -> F [label="ε"];
            FQ -> F [label="ε"];
        }
        ''')

        st.write("**(B) Concatenation:** $R = PQ$ (Serial Connection)")
        st.graphviz_chart('''
        digraph {
            rankdir=LR;
            bgcolor="transparent";
            edge [color=white, fontcolor=white];
            node [shape=circle, style=filled, fillcolor="white", fontcolor="black"];
            
            SP [label="Start P"]; 
            FP [label="Final P"];
            SQ [label="Start Q"]; 
            FQ [label="Final Q", shape=doublecircle];
            
            SP -> FP [label="P", style=dashed];
            FP -> SQ [label="ε"];
            SQ -> FQ [label="Q", style=dashed];
        }
        ''')

        st.write("**(C) Kleene Star:** $R = P^*$ (Loop + Skip)")
        st.graphviz_chart('''
        digraph {
            rankdir=LR;
            bgcolor="transparent";
            edge [color=white, fontcolor=white];
            node [shape=circle, style=filled, fillcolor="white", fontcolor="black"];
            
            S [label="New Start"];
            F [label="New Final", shape=doublecircle];
            SP [label="Start P"]; 
            FP [label="Final P"];
            
            S -> SP [label="ε (Enter)"];
            S -> F [label="ε (Skip)"];
            SP -> FP [label="P", style=dashed];
            FP -> SP [label="ε (Loop)"];
            FP -> F [label="ε (Exit)"];
        }
        ''')
        
        st.markdown("---")

        st.markdown("### 📝 Complex Example: $R = ab + c^*$")
        st.write("We build **ab** (concat) and **c*** (star), then **Union** them.")
        
        st.graphviz_chart('''
        digraph {
            rankdir=LR;
            bgcolor="transparent";
            edge [color=white, fontcolor=white];
            node [shape=circle, style=filled, fillcolor="white", fontcolor="black"];
            
            # Start and Final
            Start [label="9 (Start)", style=filled, fillcolor="#e0f7fa", fontcolor="black"];
            Final [label="10 (Final)", shape=doublecircle, style=filled, fillcolor="#ffd54f", fontcolor="black"];

            # Upper Path (ab)
            n1 [label="1"]; n2 [label="2"]; n3 [label="3"]; n4 [label="4"];
            
            # Lower Path (c*)
            n7 [label="7"]; n5 [label="5"]; n6 [label="6"]; n8 [label="8"];

            # Edges
            Start -> n1 [label="ε"];
            Start -> n7 [label="ε"];
            
            # ab path
            n1 -> n2 [label="a"];
            n2 -> n3 [label="ε"];
            n3 -> n4 [label="b"];
            n4 -> Final [label="ε"];
            
            # c* path
            n7 -> n5 [label="ε"];
            n7 -> n8 [label="ε (skip)"];
            n5 -> n6 [label="c"];
            n6 -> n5 [label="ε (loop)"];
            n6 -> n8 [label="ε"];
            n8 -> Final [label="ε"];
        }
        ''')
        
        if st.button("Next Topic: Finite Automata 🔜"):
            st.session_state.unit1_topic = "2.4 Finite Automata & Subset Construction"
            st.rerun()
        
        st.markdown("---")
        st.subheader("🛠️ Interactive NFA Generator")
        
        # Import dynamically to avoid top-level issues if file missing initially
        try:
            from utils.nfa_generator import NFAEngine
            nfa_engine = NFAEngine()
            
            nfa_tab1, nfa_tab2, nfa_tab3, nfa_tab4 = st.tabs(["🎲 Random NFA", "✍️ Draw Your Own", "📝 NFA Practice", "🎨 Visual Builder"])
            
            with nfa_tab1:
                if st.button("Generate Random RE & Diagram", key="gen_rand_nfa"):
                    nfa_examples = [
                        "(a|b)*abb",
                        "a(a|b)*b",
                        "a+b*c",
                        "0*1*0",
                        "(0+1)*00(0+1)*"
                    ]
                    st.session_state.random_nfa_re = random.choice(nfa_examples)
                
                if "random_nfa_re" in st.session_state:
                    re_val = st.session_state.random_nfa_re
                    st.markdown(f"**Regular Expression:** `{re_val}`")
                    dot_code = nfa_engine.get_dot(re_val)
                    if "Error" not in dot_code:
                        st.graphviz_chart(dot_code)
                    else:
                        st.error(f"Could not generate: {dot_code}")

            with nfa_tab2:
                user_re = st.text_input("Enter Regular Expression (e.g. `ab*+c`):", value="a+bc*", key="user_re_input")
                st.caption("Notation: `+` or `|` for Union, `*` for Star, `.` or implicit concat.")
                
                if user_re:
                    dot_code = nfa_engine.get_dot(user_re)
                    if dot_code and "Error" not in dot_code:
                        st.graphviz_chart(dot_code)
                    else:
                        st.error(f"Invalid Regex or Not Supported: {dot_code}")

            with nfa_tab3:
                st.markdown("### 📝 RE to NFA Practice")
                st.write("Challenge yourself! Get a random RE and try to build the NFA.")
                
                if st.button("🆕 Get New Challenge", key="get_challenge_btn"):
                    challenges = ["a*b", "a|b*", "(ab)*", "a+b+c", "a(b|c)*"]
                    st.session_state.nfa_challenge = random.choice(challenges)
                    st.session_state.transitions_df = pd.DataFrame([{"From": "1", "To": "2", "Label": "a"}])
                
                if "nfa_challenge" not in st.session_state:
                    st.session_state.nfa_challenge = "a*b" # Default challenge
                
                st.info(f"🎯 **Challenge:** Build NFA for `{st.session_state.nfa_challenge}`")
                
                st.markdown("#### 🏗️ Build Your NFA (Edit the table to draw!)")
                st.caption("Add rows to create transitions. Use 'e' for ε moves.")
                
                if "transitions_df" not in st.session_state:
                     st.session_state.transitions_df = pd.DataFrame([{"From": "1", "To": "2", "Label": "a"}])

                edited_df = st.data_editor(
                    st.session_state.transitions_df,
                    num_rows="dynamic",
                    column_config={
                        "From": st.column_config.TextColumn("From State"),
                        "To": st.column_config.TextColumn("To State"),
                        "Label": st.column_config.TextColumn("Input Label")
                    },
                    use_container_width=True,
                    key="nfa_editor_practice"
                )
                
                st.session_state.transitions_df = edited_df

                if edited_df is not None:
                    st.markdown("#### 🖼️ Live NFA Preview")
                    # Graphviz setup for dark mode visibility
                    user_dot = 'digraph { rankdir=LR; bgcolor="transparent"; edge [color=white, fontcolor=white]; node [shape=circle, style=filled, fillcolor="white", fontcolor="black", width=0.6, height=0.6];'
                    
                    valid_rows = 0
                    for index, row in edited_df.iterrows():
                        # Robust handling of pandas/data_editor partial rows
                        u = str(row.get("From", "")).strip()
                        v = str(row.get("To", "")).strip()
                        l = str(row.get("Label", "")).strip()
                        
                        # Filter out empty or "nan" placeholders
                        if u and v and u.lower() != "nan" and v.lower() != "nan" and u != "" and v != "":
                            lbl = "ε" if l.lower() in ['e', 'eps', 'epsilon', 'nan', '', 'none'] else l
                            user_dot += f'"{u}" -> "{v}" [label="{lbl}"];'
                            valid_rows += 1
                    
                    user_dot += "}"
                    
                    if valid_rows > 0:
                        st.graphviz_chart(user_dot)
                    else:
                        st.warning("⚠️ Enter 'From' and 'To' states in the table to see the diagram.")
                else:
                    st.warning("Start a challenge to see the table builder.")

                st.divider()
                if st.button("👁️ Show Solution", key="show_sol_btn"):
                    solution_dot = nfa_engine.get_dot(st.session_state.nfa_challenge)
                    if solution_dot:
                        st.markdown("**Solution (Thompson's Construction):**")
                        st.graphviz_chart(solution_dot)
                    else:
                        st.error("Error generating solution.")

            with nfa_tab4:
                st.markdown("### 🎨 Visual NFA Builder (Drag & Drop GUI)")
                st.write("The ultimate GUI tool! Click buttons to add elements, then **drag** them to arrange.")
                
                # If a challenge exists, show it here too!
                if "nfa_challenge" in st.session_state:
                    st.info(f"🎯 **Challenge Context:** Try building `{st.session_state.nfa_challenge}` here!")

                # HTML component for vis-network
                vis_html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
                    <style type="text/css">
                        #mynetwork {
                            width: 100%;
                            height: 400px;
                            border: 1px solid #444;
                            background-color: #1a1a1a;
                            border-radius: 8px;
                        }
                        .controls {
                            margin-bottom: 10px;
                            padding: 15px;
                            background: #2d2d2d;
                            border-radius: 8px;
                            color: white;
                            font-family: sans-serif;
                        }
                        button {
                            padding: 8px 15px;
                            margin: 5px;
                            cursor: pointer;
                            background-color: #3b82f6;
                            color: white;
                            border: none;
                            border-radius: 6px;
                            font-weight: bold;
                        }
                        button:hover { background-color: #2563eb; }
                        button.clear { background-color: #ef4444; }
                        button.clear:hover { background-color: #dc2626; }
                        input { padding: 8px; border-radius: 6px; border: 1px solid #444; background: #1e1e1e; color: white; width: 150px; }
                        .hint { font-size: 13px; color: #94a3b8; margin-top: 5px; }
                    </style>
                </head>
                <body>
                    <div class="controls">
                        <strong>Node Creator:</strong>
                        <input type="text" id="nodeLabel" placeholder="State Name (Q0)">
                        <button onclick="addNode()">+ Add State</button>
                        
                        <br><br>
                        <strong>Link Creator:</strong>
                        <input type="text" id="edgeLabel" placeholder="Symbol (a, b, e)">
                        <button onclick="addEdge()">🔗 Connect Selected</button>
                        <button class="clear" onclick="clearCanvas()">🗑️ Clear All</button>
                        <div class="hint">Instructions: To draw an arrow, click a Start node then an End node (hold Ctrl/Cmd to select multiple), then click Connect.</div>
                    </div>
                    <div id="mynetwork"></div>

                    <script type="text/javascript">
                        var nodes = new vis.DataSet([
                            {id: 1, label: 'q0', color: {background: '#93c5fd'}},
                            {id: 2, label: 'q1', shape: 'doublecircle'}
                        ]);
                        var edges = new vis.DataSet([
                            {from: 1, to: 2, label: 'a', arrows: 'to'}
                        ]);

                        var container = document.getElementById('mynetwork');
                        var data = { nodes: nodes, edges: edges };
                        var options = {
                            nodes: {
                                shape: 'circle',
                                size: 30,
                                font: { color: 'black', size: 14, face: 'Tahoma' },
                                color: { background: '#ffffff', border: '#3b82f6', highlight: { background: '#dbeafe' } }
                            },
                            edges: {
                                arrows: { to: { enabled: true, scaleFactor: 1 } },
                                font: { align: 'top', color: '#ffffff', strokeWidth: 0, size: 14 },
                                color: { color: '#64748b', highlight: '#3b82f6' },
                                smooth: { type: 'curvedCW', roundness: 0.2 }
                            },
                            physics: { enabled: true, stabilization: true, barnesHut: { gravitationalConstant: -2000 } },
                            interaction: { multiselect: true, dragNodes: true }
                        };
                        var network = new vis.Network(container, data, options);

                        function addNode() {
                            var label = document.getElementById('nodeLabel').value || 'q' + nodes.length;
                            var id = new Date().getTime(); // Unique ID
                            nodes.add({id: id, label: label});
                            document.getElementById('nodeLabel').value = '';
                        }

                        function addEdge() {
                            var label = document.getElementById('edgeLabel').value || 'ε';
                            var selection = network.getSelectedNodes();
                            if (selection.length >= 2) {
                                edges.add({
                                    from: selection[0], 
                                    to: selection[selection.length - 1], 
                                    label: label, 
                                    arrows: 'to'
                                });
                                document.getElementById('edgeLabel').value = '';
                                network.unselectAll();
                            } else {
                                alert("Step 1: Click a node.\\nStep 2: Hold Ctrl/Cmd and click another node.\\nStep 3: Click 'Connect Selected'.");
                            }
                        }

                        function clearCanvas() {
                            if(confirm("Are you sure you want to clear the canvas?")) {
                                nodes.clear();
                                edges.clear();
                            }
                        }
                    </script>
                </body>
                </html>
                """
                st.components.v1.html(vis_html, height=580)
                st.info("💡 **Pro Tip:** You can move states by dragging them. Use **e** for ε-transitions!")
                            
        except ImportError:
            st.error("NFA Generator module not found. Please check utils/nfa_generator.py")

    # ==================================================
    # TOPIC 2.4: FINITE AUTOMATA & SUBSET CONSTRUCTION
    # ==================================================
    elif selected_topic == "2.4 Finite Automata & Subset Construction":
        unit1_fa.render_fa_content()

    # ==================================================
    # TOPIC 2.6: NFA TO DFA CONVERSION LAB
    # ==================================================
    elif selected_topic == "2.6 NFA to DFA Conversion Lab":
        nfa_to_dfa_lab.render_lab()

    # ==================================================
    # TOPIC 3.1: GRAMMAR BASICS
    # ==================================================
    elif selected_topic == "3.1 Grammar Basics (4-Tuple)":
        unit1_syntax.render_grammar_basics()

    # ==================================================
    # TOPIC 3.2: CHOMSKY HIERARCHY
    # ==================================================
    elif selected_topic == "3.2 Chomsky Hierarchy (Types of Grammar)":
        unit1_syntax.render_chomsky_hierarchy()

    # ==================================================
    # TOPIC 3.3: PARSE TREES
    # ==================================================
    elif selected_topic == "3.3 Parse Trees & Grammar Capabilities":
        unit1_syntax.render_parse_trees()

    # ==================================================
    # TOPIC 3.4: DERIVATIONS
    # ==================================================
    elif selected_topic == "3.4 Derivations (LMD & RMD)":
        unit1_syntax.render_derivations()

    # ==================================================
    # TOPIC 3.5: REDUCTION
    # ==================================================
    elif selected_topic == "3.5 Reduction (Process & Example)":
        unit1_syntax.render_reduction()

    # ==================================================
    # TOPIC 3.6: PARSE TREES & AMBIGUITY
    # ==================================================
    elif selected_topic == "3.6 Parse Trees & Ambiguity (Digitized Notes)":
        unit1_syntax.render_parse_tree_notes()

    # ==================================================
    # TOPIC 4.0: SYNTAX OVERVIEW
    # ==================================================
    elif selected_topic == "4.0 Syntax Analysis Overview & Top-Down Parser":
        unit1_topdown.render_topdown_overview()

    # ==================================================
    # TOPIC 4.1: INTRODUCTION TO PARSERS
    # ==================================================
    elif selected_topic == "4.1 Introduction to Parsers":
        unit1_parsing.render_parsing_intro()

    # ==================================================
    # TOPIC 4.2: LEFT RECURSION
    # ==================================================
    elif selected_topic == "4.2 Left Recursion (Elimination)":
        unit1_recursion.render_left_recursion()

    # ==================================================
    # TOPIC 4.3: LEFT FACTORING
    # ==================================================
    elif selected_topic == "4.3 Left Factoring":
        unit1_factoring.render_left_factoring()

    # ==================================================
    # TOPIC 4.4: FIRST AND FOLLOW SETS
    # ==================================================
    elif selected_topic == "4.4 FIRST and FOLLOW Sets":
        unit1_first_follow.render_first_follow()

    # ==================================================
    # TOPIC 4.5: LL(1) PREDICTIVE PARSING TABLE
    # ==================================================
    elif selected_topic == "4.5 LL(1) Predictive Parsing Table":
        unit1_ll1.render_ll1()

    # ==================================================
    # TOPIC 4.6: LL(1) STACK IMPLEMENTATION
    # ==================================================
    elif selected_topic == "4.6 LL(1) Stack Implementation":
        unit1_stack.render_stack_simulation()

    # ==================================================
    # TOPIC 5.1: SEMANTIC ANALYSIS (SDT)
    # ==================================================
    elif selected_topic == "5.1 Semantic Analysis (SDT & SDD)":
        unit1_semantic.render_semantic_analysis()

    # ==================================================
    # TOPIC 5.2: INTERMEDIATE CODE GENERATION
    # ==================================================
    elif selected_topic == "5.2 Intermediate Code Generation":
        unit1_icg.render_icg()
    elif selected_topic == "5.3 Three-Address Code (TAC)":
        unit1_tac.render_tac()
    elif selected_topic == "5.4 Dead Code Elimination":
        unit1_optimization.render_dead_code()
    elif selected_topic == "5.5 Directed Acyclic Graph (DAG)":
        unit1_dag.render_dag()
