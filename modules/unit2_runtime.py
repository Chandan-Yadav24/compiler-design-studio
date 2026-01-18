import streamlit as st
import pandas as pd

def render_runtime():
    st.title("🛡️ 7.1 Runtime Environments & Error Handling")
    
    st.markdown("""
    Imagine your code as a **live concert** – the runtime environment is the stage, activation records are the setlist, and the stack/heap are the crowd zones. 
    This chapter is about the behind-the-scenes magic that keeps your app running smooth without crashing!
    """)

    st.divider()

    # --- 7.0 OBJECTIVES ---
    st.header("🎯 7.0 Objectives (5 Big Wins)")
    st.markdown("Build your compiler superpowers with these core goals:")
    
    objectives = [
        "**Activation Records Basics**: Understand the 'life story' of function calls.",
        "**Stack & Heap Mgmt**: Quick auto-clean for locals (Stack) vs. manual big data (Heap).",
        "**Garbage Collection**: Auto-clean heap trash using techniques like Mark-Sweep (JVM).",
        "**Call/Return + Params**: Master function flow, parameter passing, and return mechanics.",
        "**Exception Handling & Errors**: Handle 'oops' moments and fix Lexical/Syntax bugs."
    ]
    
    for obj in objectives:
        st.markdown(f"* {obj}")
        
    st.success("🧠 **Mnemonic:** **ASGCE** ➜ 'Ace Super Good Compiler Exams!'")

    st.divider()

    # --- 7.1 INTRODUCTION ---
    st.header("📘 7.1 Introduction")
    st.markdown("""
    **Runtime Environment Management** is how code "lives" during execution. Compilers like **GCC** and **LLVM** optimize these to make apps like Fortnite or Instagram run efficiently.
    """)

    tabs = st.tabs(["Activation Records", "Stack vs Heap", "Error Handling"])

    with tabs[0]:
        st.subheader("📋 Activation Records")
        st.markdown("""
        Every time a function is called, a "snapshot" of its data is stored.
        *   **Includes:** Local variables, parameters, return addresses, and control links.
        *   **Analogy:** A musician's **setlist** — specific instructions and data for that one performance.
        """)
        st.info("💡 **ABI Context:** x86 and ARM have strictly defined 'Application Binary Interfaces' (ABI) for how these records are structured.")

    with tabs[1]:
        st.subheader("🏗️ Memory Management")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**1. The Stack**")
            st.code("""
void func() {
    int x = 10; // Stack Allocated
} // x is auto-cleaned here!
            """, language="cpp")
            st.info("Fast, structured, and automatic.")
        with c2:
            st.markdown("**2. The Heap**")
            st.code("""
int* p = malloc(sizeof(int));
// ... use p ...
free(p); // Manual Cleanup
            """, language="cpp")
            st.info("Dynamic, flexible, but requires care (or GC).")

    with tabs[2]:
        st.subheader("🐛 Error Handling Strategies")
        st.markdown("""
        Compilers must be "unbreakable." They handle errors at different stages:
        """)
        
        error_data = [
            {"Stage": "Lexical", "Problem": "Bad Tokens (e.g., '1abc')", "Strategy": "Skip to next delimiter"},
            {"Stage": "Syntax", "Problem": "Grammar Fails (e.g., 'x = ;')", "Strategy": "Panic Mode Recovery"},
            {"Stage": "Runtime", "Problem": "Exceptions (e.g., Div by 0)", "Strategy": "Stack Unwinding (Try-Catch)"}
        ]
        st.table(pd.DataFrame(error_data))

    st.divider()

    # --- FINAL WRAP-UP ---
    st.header('🚀 The "Unbreakable" Goal')
    st.markdown("""
    Mastering runtime environments allows you to direct a flawless show. In the real world, **LLVM** in iOS apps handles heap garbage collection to prevent leaks and maximize battery life.
    """)
    
    st.success("💡 **Exam One-Liner:** 'Runtime = Stage for code drama; master it to direct flawless shows!'")

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: Code Generation"):
            st.session_state.unit2_topic = "6.3 Code Generation Techniques"
            st.rerun()
    with nav2:
        if st.button("Next Topic: Topic 7.2 ➡️", use_container_width=True):
            st.session_state.unit2_topic = "7.2 Activation Records & Stack Mgmt"
            st.rerun()

def render_activation_records():
    st.title("🥞 7.2 Activation Records & Stack Mgmt")
    
    st.markdown("""
    Think of activation records as **"VIP passes"** for functions – they store all the details (vars, returns) on a **"pancake stack"** (call stack). 
    Pop one off when done!
    """)

    st.divider()

    # --- SECTION 1: THE BIG PICTURE ---
    st.header("📘 1. The Big Picture")
    st.markdown("""
    *   **What?** Stack frames hold function info (vars, params) on a LIFO stack.
    *   **Why?** Enables recursion, nesting, and memory efficiency.
    *   **Real-World:** **GCC** optimizes stack for Android games; an overflow makes the app crash like a Jenga tower!
    """)

    # Visual Example of Flow
    st.info("🔄 **Stack Flow:** Push record on call ➜ Use ➜ Pop on return (LIFO magic!)")
    
    st.divider()

    # --- SECTION 2: STRUCTURE (RPCASLT) ---
    st.header("🏗️ 2. Structure of an Activation Record")
    st.success("🧠 **Mnemonic:** **RPCASLT** ➜ 'Rapid Penguins Can Always Swim Like Tigers!'")
    
    ar_data = [
        {"Component": "Return Address", "What It Does": "Where to jump back after function ends.", "Analogy": "'Home address' for the caller."},
        {"Component": "Parameters", "What It Does": "Inputs passed (by value/ref).", "Analogy": "'Gifts' from caller to function."},
        {"Component": "Control Link", "What It Does": "Points to caller's record for continuity.", "Analogy": "'Phone line' back to boss function."},
        {"Component": "Access Link", "What It Does": "Addr of caller's record (for non-locals).", "Analogy": "'VIP list' to outer scopes."},
        {"Component": "Saved Machine Status", "What It Does": "Registers/return addr before call.", "Analogy": "'Snapshot' to restore after party."},
        {"Component": "Local Data", "What It Does": "Function's own variables.", "Analogy": "'Private room' for quick calcs."},
        {"Component": "Temporaries", "What It Does": "Temp storage for mid-computes.", "Analogy": "'Scratch paper' – trashed after."}
    ]
    st.table(pd.DataFrame(ar_data))

    st.divider()

    # --- SECTION 3: STACK MANAGEMENT ---
    st.header("🥞 3. Stack Management (Pancake Boss)")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📍 SP vs FP")
        st.markdown("""
        *   **Stack Pointer (SP):** Points to the current top of the stack. Moves dynamically.
        *   **Frame Pointer (FP):** Fixed base of the current frame. Used for stable variable access.
        """)
        st.info("💡 **FPO (Frame Pointer Omission):** GCC can omit FP for more registers, making code even faster!")
    
    with c2:
        st.subheader("🖼️ Stack Frame Visual")
        st.graphviz_chart('''
        digraph G {
            node [shape=record, style=filled, fillcolor="white", fontname="Courier"];
            rankdir=BT;
            
            frame [label="{ Temporaries | Local Data | Saved Status | Access Link | Control Link | Parameters | Return Address }", fillcolor="#e6f4ff"];
            
            sp [label="Stack Pointer (SP)", shape=none, fontcolor="#d32f2f"];
            fp [label="Frame Pointer (FP)", shape=none, fontcolor="#1976d2"];
            
            sp -> frame:nw [label=" Points top"];
            fp -> frame:sw [label=" Base of frame"];
        }
        ''')

    st.divider()

    # --- SECTION 4: ROLES ---
    st.header("⚙️ 4. Functional Roles (7 Key Points)")
    roles = [
        "**Parsing/Syntax:** Spots calls + params.",
        "**Symbol Table:** Tracks types and scopes for resolution.",
        "**Type Checking:** Ensures param types match (no int-string mixups).",
        "**ICG:** Builds stack frames for params/locals.",
        "**Optimization:** Inlines small functions to cut calls.",
        "**Code Gen:** Turns logic into machine stack operations.",
        "**Swift/Rust:** **LLVM** uses this for safe call management."
    ]
    for role in roles:
        st.write(f"* {role}")

    st.divider()

    # --- SECTION 5: INTERACTIVE LAB ---
    st.header("🧪 5. Interactive Stack Lab")
    st.markdown("Choose a scenario or generate a **Random Example** to see how the stack grows practically.")

    examples = {
        "Simple Addition": {
            "code": "int add(int a, int b) {\n    int res = a + b;\n    return res;\n}",
            "ar": {
                "Return Address": "0x4005e8 (main+42)",
                "Parameters": "a=5, b=10",
                "Control Link": "ptr to main_frame",
                "Access Link": "None (Global Scope)",
                "Saved Status": "EAX, EBX saved",
                "Local Data": "res=15",
                "Temporaries": "t1=15"
            }
        },
        "Recursive Factorial": {
            "code": "int fact(int n) {\n    if (n <= 1) return 1;\n    return n * fact(n-1);\n}",
            "ar": {
                "Return Address": "0x4006c2 (fact+18)",
                "Parameters": "n=3",
                "Control Link": "ptr to fact(4)_frame",
                "Access Link": "None",
                "Saved Status": "Return EIP saved",
                "Local Data": "None",
                "Temporaries": "t1=fact(2), t2=3*t1"
            }
        },
        "String Print (Pointer)": {
            "code": "void print(char* s) {\n    int len = strlen(s);\n    puts(s);\n}",
            "ar": {
                "Return Address": "0x400a10 (init+12)",
                "Parameters": "s=0x7ffee1 (ptr to 'Hi')",
                "Control Link": "ptr to init_frame",
                "Access Link": "0x7ffee1",
                "Saved Status": "BP, SP saved",
                "Local Data": "len=2",
                "Temporaries": "None"
            }
        }
    }

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("🎲 Generate Random Example"):
            import random
            st.session_state.stack_ex = random.choice(list(examples.keys()))
    
    selected_ex_name = st.selectbox("Select Example Case:", list(examples.keys()), key="stack_ex_select", 
                                    index=list(examples.keys()).index(st.session_state.get('stack_ex', 'Simple Addition')))
    
    ex = examples[selected_ex_name]
    
    st.subheader(f"📝 Case: {selected_ex_name}")
    st.code(ex["code"], language="cpp")

    c_lab1, c_lab2 = st.columns([1, 1])
    
    with c_lab1:
        st.markdown("**Activation Record Details:**")
        df_ex = pd.DataFrame(list(ex["ar"].items()), columns=["Component", "Snapshot Value"])
        st.table(df_ex)
        
    with c_lab2:
        st.markdown("**Stack Visual (LIFO):**")
        dot_code = f'''
        digraph G {{
            node [shape=record, style=filled, fillcolor="white", fontname="Courier"];
            rankdir=BT;
            
            frame [label="{{ {ex["ar"]["Temporaries"]} | {ex["ar"]["Local Data"]} | {ex["ar"]["Saved Status"]} | {ex["ar"]["Access Link"]} | {ex["ar"]["Control Link"]} | {ex["ar"]["Parameters"]} | {ex["ar"]["Return Address"]} }}", fillcolor="#fff3e0"];
            
            p1 [label="Stack Top", shape=none, fontcolor="#e65100"];
            p1 -> frame:nw;
        }}
        '''
        st.graphviz_chart(dot_code)

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: Runtime Intro"):
            st.session_state.unit2_topic = "7.1 Runtime Environments & Error Handling"
            st.rerun()
    with nav2:
        if st.button("Next Topic: Topic 7.4 ➡️", use_container_width=True):
            st.session_state.unit2_topic = "7.4 Call & Return Mechanisms"
            st.rerun()

def render_call_return():
    st.title("📞 7.4 Call & Return Mechanisms")
    
    st.markdown("""
    Calling a function is like dialing a friend – pass info (params), chat (execute), and hang up (return). 
    Modern compilers optimize this so there are no "dropped calls" in your apps!
    """)

    st.divider()

    # --- 7.4.1 CALL MECHANISM ---
    st.header("📲 7.4.1 Call Mechanism (The Dial-Up)")
    st.success("🧠 **Mnemonic:** **FPSR** ➜ 'Fast Phone Stack Ring!'")
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("""
        1.  **Function Call:** Jumps control from caller to callee.
        2.  **Parameters:** Pass args (by value/ref) – like texting details.
        3.  **Stack Frame:** Push new activation record onto stack.
        4.  **Return Address:** Save "come back here" spot.
        """)
        st.info("🚀 **Real-World:** **GCC** pushes frames for C calls – powers quick math in scientific calculators.")
    with col2:
        st.graphviz_chart('''
        digraph G {
            rankdir=TB;
            node [shape=box, style=filled, fillcolor="#e1f5fe"];
            caller [label="Caller (Main)"];
            callee [label="Callee (Func)"];
            caller -> callee [label="1. Call + Params (FPSR)"];
            callee -> caller [label="2. Return (ERCT)"];
        }
        ''')

    st.divider()

    # --- 7.4.2 RETURN MECHANISM ---
    st.header("🔌 7.4.2 Return Mechanism (The Hang-Up)")
    st.success("🧠 **Mnemonic:** **ERCT** ➜ 'End Run, Clean Trash!'")
    
    st.markdown("""
    1.  **Function Exec:** Callee runs its code and finishes the task.
    2.  **Return Value:** Compute and store results in a register or stack.
    3.  **Stack Cleanup:** Pop frame (unwind stack) to free memory.
    4.  **Control Transfer:** Jump back using the saved return address.
    """)
    st.info("🎯 **Real-World:** **JVM** returns results smoothly in Java – keeps Android games running without lag.")

    st.divider()

    # --- SECTION 7.4.3: INTERACTIVE LAB ---
    st.header("🧪 7.4.3 Interactive Lab: Function Call Trace")
    st.markdown("""
    Practice the **FPSR** (Call) and **ERCT** (Return) phases. Step through a nested call sequence to see how the stack behaves!
    """)

    if 'call_stack' not in st.session_state:
        st.session_state.call_stack = [
            {"name": "main()", "params": "argv[]", "addr": "0x400"}
        ]

    c_trace1, c_trace2 = st.columns([1, 1])

    with c_trace1:
        st.subheader("🛠️ Call Control")
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            if st.button("🔽 Step Into: func_A()"):
                st.session_state.call_stack.append({"name": "func_A()", "params": "x=10", "addr": "0x510"})
                st.rerun()
            if st.button("🔽 Step Into: func_B()"):
                st.session_state.call_stack.append({"name": "func_B()", "params": "y=20", "addr": "0x620"})
                st.rerun()
        
        with col_b2:
            if st.button("🔼 Step Out (Return)"):
                if len(st.session_state.call_stack) > 1:
                    st.session_state.call_stack.pop()
                    st.rerun()
            if st.button("🔄 Reset Trace"):
                st.session_state.call_stack = [{"name": "main()", "params": "argv[]", "addr": "0x400"}]
                st.rerun()

    with c_trace2:
        st.subheader("🖼️ Stack Visual")
        if st.session_state.call_stack:
            # Build stack visualization
            dot_trace = "digraph G { rankdir=BT; node [shape=record, style=filled, fontname='Courier']; "
            stack_content = " | ".join([f"<f{i}> {f['name']}\\n{f['params']}" for i, f in enumerate(st.session_state.call_stack)][::-1])
            dot_trace += f'stack [label="{{ {stack_content} }}", fillcolor="#e1f5fe"]; '
            dot_trace += "}"
            st.graphviz_chart(dot_trace)
        else:
            st.warning("Stack is empty!")

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: Heap Mgmt"):
            st.session_state.unit2_topic = "7.3 Heap Memory Mgmt"
            st.rerun()
    with nav2:
        if st.button("Next Topic: Topic 7.5 ➡️", use_container_width=True):
            st.session_state.unit2_topic = "7.5 Exception Handling"
            st.rerun()

def render_exception_handling():
    st.title("🚨 7.5 Exception Handling")
    
    st.markdown("""
    Exceptions are "code emergencies" – like a fire alarm. 
    Compilers generate try-catch magic to handle glitches without a total meltdown!
    """)

    st.divider()

    # --- KEY POINTS ---
    st.header("📘 Key Points (The Safety Net)")
    st.success("🧠 **Mnemonic:** **LPSTIOCE** ➜ 'Let\\'s Party Safely Till It\\'s Over, Code Experts!'")
    
    points_data = [
        {"Key": "a. Language Support", "Detail": "Built-in syntax in Java/C#."},
        {"Key": "b. Code Gen", "Detail": "Translate try-catch to machine throw/catch instructions."},
        {"Key": "c. Propagation", "Detail": "Bubble exceptions up the stack until caught."},
        {"Key": "d. Stack Unwinding", "Detail": "Dealloc resources during propagation."},
        {"Key": "e. Types/Handlers", "Detail": "Type-matching in catch blocks."},
        {"Key": "f. Resource Mgmt", "Detail": "Auto-close files (RAII style)."},
        {"Key": "g. Optimizations", "Detail": "Minimize overhead for 'happy path' speed."},
        {"Key": "h. Error Reporting", "Detail": "Generate stack traces for debugging."}
    ]
    st.table(pd.DataFrame(points_data))

    st.divider()

    st.info("🚁 **Real-World:** **JVM's GC + Exceptions** in Java allow banking software to recover from errors without crashing your transaction.")
    
    st.success("💡 **Exam Tip:** Exceptions = Detect ➜ Propagate ➜ Handle + Clean.")

    st.divider()

    # --- SECTION 7.5.3: INTERACTIVE LAB ---
    st.header("🧪 7.5.3 Interactive Lab: Stack Unwinding")
    st.markdown("""
    What happens when an error occurs deep inside nested calls? 
    Watch the compiler **Unwind the Stack** (Propagate) until it finds a handler!
    """)

    if 'exception_state' not in st.session_state:
        st.session_state.exception_state = {
            "stack": ["Main (Try-Catch)", "ProcessData()", "Fetch()", "Connect()"],
            "status": "Running Smoothly",
            "message": "App is healthy.",
            "color": "blue"
        }

    c_unwind1, c_unwind2 = st.columns([1, 2])

    with c_unwind1:
        st.subheader("⚡ Trigger Event")
        if st.button("💥 Throw Exception (Connect Failed)"):
            st.session_state.exception_state["status"] = "Propagating..."
            st.session_state.exception_state["message"] = "Exception thrown in Connect()! Searching for catch block..."
            st.session_state.exception_state["color"] = "orange"
            st.rerun()

        if st.session_state.exception_state["status"] == "Propagating...":
            if st.button("⏭️ Next Step (Unwind Frame)"):
                if len(st.session_state.exception_state["stack"]) > 1:
                    popped = st.session_state.exception_state["stack"].pop()
                    if "Main" in st.session_state.exception_state["stack"][-1]:
                        st.session_state.exception_state["status"] = "Caught!"
                        st.session_state.exception_state["message"] = f"Unwound {popped}. Found handler in Main()!"
                        st.session_state.exception_state["color"] = "green"
                    else:
                        st.session_state.exception_state["message"] = f"No handler in {popped}. Unwinding further..."
                st.rerun()

        if st.button("🔄 Reset Simulator"):
            st.session_state.exception_state = {
                "stack": ["Main (Try-Catch)", "ProcessData()", "Fetch()", "Connect()"],
                "status": "Running Smoothly",
                "message": "App is healthy.",
                "color": "blue"
            }
            st.rerun()

    with c_unwind2:
        st.subheader("🖼️ Unwinding Visual")
        status_color = st.session_state.exception_state["color"]
        st.markdown(f"**Current Status:** :{status_color}[{st.session_state.exception_state['status']}]")
        st.info(st.session_state.exception_state["message"])

        # Display stack as vertical blocks
        for i, frame in enumerate(reversed(st.session_state.exception_state["stack"])):
            f_color = "#ffecb3" if "Main" in frame else "#ffcdd2"
            if i == 0 and st.session_state.exception_state["status"] == "Propagating...":
                f_color = "#e53935" # Red for the exploding frame
            
            st.markdown(f"""
            <div style="background-color: {f_color}; padding: 10px; border: 2px solid #333; border-radius: 5px; margin-bottom: 5px; text-align: center; color: black; font-weight: bold;">
                {frame}
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: Call & Return"):
            st.session_state.unit2_topic = "7.4 Call & Return Mechanisms"
            st.rerun()
    with nav2:
        if st.button("Next Topic: Advanced Topics ➡️", key="next_from_75"):
            st.session_state.unit2_topic = "Advanced Topics"
            st.rerun()

def render_heap_mgmt():
    st.title("🔋 7.3 Heap Memory Mgmt")
    
    st.markdown("""
    While the **Stack** is like a tidy fridge (fixed, auto-clean), the **Heap** is your messy garage – dynamic space for big stuff (arrays, objects) that you alloc/dealloc on the fly. 
    Compilers handle this to prevent "out of space" crashes!
    """)

    st.divider()

    # --- SECTION 1: STACK VS HEAP ---
    st.header("⚖️ 1. Stack vs Heap (The Great Divide)")
    diff_data = [
        {"Aspect": "Allocation", "Stack": "Auto / Fixed (locals, calls)", "Heap": "Manual / Dynamic (big, flex data)"},
        {"Aspect": "Speed", "Stack": "Super Fast (LIFO)", "Heap": "Slower (search required)"},
        {"Aspect": "Size", "Stack": "Limited (Overflow risk)", "Heap": "Huge (Fragment risk)"},
        {"Aspect": "Mgmt", "Stack": "Auto dealloc on return", "Heap": "Manual free or GC"},
        {"Aspect": "Use Case", "Stack": "Quick math, local vars", "Heap": "Dynamic playlists, complex objects"}
    ]
    st.table(pd.DataFrame(diff_data))
    st.info("🚀 **Real-World:** **JVM** uses the Stack for quick math and the Heap for dynamic playlists in Spotify.")

    st.divider()

    # --- SECTION 2: 8 KEY POINTS ---
    st.header("📘 2. Heap Mgmt: 8 Key Points")
    st.success("🧠 **Mnemonic:** **DHAF MGMC** ➜ 'Don't Have A Freaky Memory GC Mess, Compiler!'")
    
    points_data = [
        {"Point": "Dynamic Alloc", "Meaning": "Alloc at runtime via malloc/new.", "Impact": "Powers dynamic TikTok feeds."},
        {"Point": "Heap Structures", "Meaning": "Arrays, lists, trees, objects.", "Impact": "Used in game engines like Unity."},
        {"Point": "Alloc Algorithms", "Meaning": "First-fit / Best-fit blocks.", "Impact": "LLVM cuts waste in iOS apps."},
        {"Point": "Fragmentation", "Meaning": "Scattered free space.", "Impact": "Slows down Android games."},
        {"Point": "Memory Leaks", "Meaning": "Forgot to free alloc'd memory.", "Impact": "One leak can crash a Chrome tab."},
        {"Point": "Garbage Collection", "Meaning": "Auto-reclaim unused memory.", "Impact": "Keeps Minecraft servers running smooth."},
        {"Point": "Manual Mgmt", "Meaning": "You handle alloc/free.", "Impact": "Rust ownership prevents these crashes."},
        {"Point": "Compiler Opts", "Meaning": "Pooling and stack tricks.", "Impact": "Siri uses this for faster AI."}
    ]
    st.table(pd.DataFrame(points_data))

    st.divider()

    # --- SECTION 3: ALLOC/DEALLOC TECHNIQUES ---
    st.header("⚙️ 3. Allocation & Deallocation Techniques")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🅰️ Allocation (SDSPB)")
        st.markdown("*   **Static:** Fixed at compile-time.")
        st.markdown("*   **Dynamic:** Runtime via malloc/new.")
        st.markdown("*   **Stack:** Auto for locals.")
        st.markdown("*   **Pooled:** Reuse pre-alloc'd blocks.")
        st.markdown("*   **Bump:** Sequential alloc (fast).")
        st.info("🧠 'Super Duper Stack Pool Bump!'")

    with c2:
        st.subheader("🅱️ Deallocation (MRPS)")
        st.markdown("*   **Manual:** You call free/delete.")
        st.markdown("*   **Ref Counting:** Auto-free at 0 refs.")
        st.markdown("*   **Pool:** Return to reusable pool.")
        st.markdown("*   **Scoped:** Auto-free at scope end (RAII).")
        st.info("🧠 'Mr. PS, Dealloc Please!'")

    st.divider()

    # --- SECTION 4: GARBAGE COLLECTION ---
    st.header("♻️ 4. Garbage Collection (Auto-Cleanup)")
    st.success("🧠 **Mnemonic:** **RMG** ➜ 'Remember My Garbage!'")
    
    gc_data = [
        {"Method": "Ref Counting", "How It Works": "Count refs; free at 0.", "Real-World": "Python scripts"},
        {"Method": "Mark-and-Sweep", "How It Works": "Mark live objs; sweep the rest.", "Real-World": "Java Servers"},
        {"Method": "Generational GC", "How It Works": "Young vs Old Generations.", "Real-World": "Android / V8 (JS)"}
    ]
    st.table(pd.DataFrame(gc_data))

    st.divider()

    # --- SECTION 5: INTERACTIVE HEAP LAB ---
    st.header("🧪 5. Interactive Heap Lab (Fragmentation)")
    st.markdown("""
    Use the buttons to **Allocate** or **Free** blocks. Witness how the heap gets fragmented and how the compiler/runtime must manage these "holes."
    """)

    # State for Simulator
    if 'heap_blocks' not in st.session_state or not st.session_state.heap_blocks:
        st.session_state.heap_blocks = [
            {"id": "Block A", "size": 20, "status": "Allocated", "color": "#ffcdd2"},
            {"id": "Free 1", "size": 10, "status": "Free", "color": "#e8f5e9"},
            {"id": "Block B", "size": 30, "status": "Allocated", "color": "#e1f5fe"},
            {"id": "Free 2", "size": 40, "status": "Free", "color": "#e8f5e9"}
        ]

    cols_sim = st.columns([2, 1])
    
    with cols_sim[1]:
        st.subheader("🛠️ Commands")
        if st.button("➕ Allocate Block C (15 units)"):
            # Simple First-Fit logic
            for i, block in enumerate(st.session_state.heap_blocks):
                if block["status"] == "Free" and block["size"] >= 15:
                    remainder = block["size"] - 15
                    st.session_state.heap_blocks[i] = {"id": "Block C", "size": 15, "status": "Allocated", "color": "#f3e5f5"}
                    if remainder > 0:
                        st.session_state.heap_blocks.insert(i+1, {"id": f"Fragment {i}", "size": remainder, "status": "Free", "color": "#e8f5e9"})
                    break
            st.rerun()

        if st.button("🧹 Free Block B"):
            for block in st.session_state.heap_blocks:
                if block["id"] == "Block B":
                    block["status"] = "Free"
                    block["color"] = "#e8f5e9"
            st.rerun()

        if st.button("🔄 Reset Heap"):
            st.session_state.heap_blocks = [
                {"id": "Block A", "size": 20, "status": "Allocated", "color": "#ffcdd2"},
                {"id": "Free 1", "size": 10, "status": "Free", "color": "#e8f5e9"},
                {"id": "Block B", "size": 30, "status": "Allocated", "color": "#e1f5fe"},
                {"id": "Free 2", "size": 40, "status": "Free", "color": "#e8f5e9"}
            ]
            st.rerun()

    with cols_sim[0]:
        st.subheader("🖼️ Heap Visualization")
        # Build horizontal layout with Graphviz
        gv_code = "digraph G { rankdir=LR; node [shape=box, style=filled, fontname='Courier']; "
        
        gv_items = []
        for i, b in enumerate(st.session_state.heap_blocks):
            label = f"{b['id']}\\n({b['size']} units)"
            color = b["color"]
            # Use simple numeric IDs for nodes to avoid any issues
            gv_items.append(f'n{i} [label="{label}", fillcolor="{color}"]')
        
        gv_code += "; ".join(gv_items) + "; "
        
        if len(st.session_state.heap_blocks) > 1:
            edge_list = []
            for i in range(len(st.session_state.heap_blocks)-1):
                edge_list.append(f"n{i} -> n{i+1}")
            gv_code += "; ".join(edge_list) + "; "
        
        gv_code += "}"
        st.graphviz_chart(gv_code)
        st.info("💡 **Fragmentation:** Notice how smaller 'Free' holes appear between allocated blocks. The compiler must decide whether to compact these or wait for a bigger request.")

    st.divider()

    # --- SECTION 6: PYTHON MEMORY LAB ---
    st.header("🐍 6. Python Memory Lab (User Interaction)")
    st.markdown("""
    Python's memory management is unique. It uses **Reference Counting** and a **Cycle Detector**. 
    Try the interactive inputs below to see how Python IDs and references work!
    """)

    py_col1, py_col2 = st.columns(2)

    with py_col1:
        st.subheader("1. Reference Exploration")
        val = st.text_input("Enter a value (e.g., 5 or 'Hello'):", value="Compiler Design")
        if val:
            import sys
            st.write(f"*   **Memory ID (Address):** `{id(val)}`")
            st.write(f"*   **Type:** `{type(val).__name__}`")
            st.write(f"*   **Ref Count (approx):** `{sys.getrefcount(val)}`")
            st.warning("⚠️ sys.getrefcount is usually higher because the function itself creates a temporary reference!")

    with py_col2:
        st.subheader("2. Identity vs Equality")
        st.markdown("""
        ```python
        a = [1, 2]
        b = [1, 2]
        print(a == b) # True (Same value)
        print(a is b) # False (Different memory!)
        ```
        """)
        
        test_val = st.slider("Integer Caching Test (Pick a number):", -10, 300, 256)
        st.write(f"In Python, integers from -5 to 256 are **cached**. Let's check `{test_val}`:")
        x = int(test_val)
        y = int(test_val)
        is_same = (x is y)
        if is_same:
            st.success(f"✅ `x is y` is **{is_same}**! Python reused the cache for `{test_val}`.")
        else:
            st.error(f"❌ `x is y` is **{is_same}**! A new object was created for `{test_val}`.")

    st.divider()

    # Navigation
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous: Activation Records"):
            st.session_state.unit2_topic = "7.2 Activation Records & Stack Mgmt"
            st.rerun()
    with nav2:
        if st.button("Next Topic: Advanced Topics ➡️", key="next_from_73"):
            st.session_state.unit2_topic = "Advanced Topics"
            st.rerun()
