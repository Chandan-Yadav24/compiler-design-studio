# ⚡ Compiler Design Studio
### *Interactive Learning Platform for Compiler Construction* 🚀

Welcome to the **Compiler Design Studio**, a comprehensive, interactive, and visually rich educational platform designed to demystify the complex world of compiler construction. Built using **Streamlit**, this tool allows students and developers to experiment with every phase of a compiler—from raw text scanning to advanced optimizations and JIT compilation.

---

## 🏗️ Project Architecture
The platform is organized into two core modules reflecting the classic compiler pipeline:

### 🔬 Unit 1: The Front End
Focuses on language recognition and structural analysis.
- **Lexical Analysis**: DFA/NFA visualizations, Subset Construction, and Tokenization.
- **Syntax Analysis**: Derivation (LMD/RMD) Labs, Ambiguity Tests, and Parse Tree rendering.
- **First & Follow Solver**: Automated calculation of First and Follow sets for grammars.
- **LL(1) Parsing**: Predictive parsing table generation and stack-based trace simulation.
- **Semantic Analysis**: Type checking and Scope validation.
- **Intermediate Code Generation (ICG)**: Transformation to Three-Address Code (TAC).

### ⚙️ Unit 2: The Back End
Focuses on performance, memory management, and advanced execution models.
- **Code Optimization**: Constant Folding, Dead Code Elimination, and Loop Fusion.
- **Directed Acyclic Graphs (DAG)**: Basic Block construction and optimization.
- **Runtime Environments**: Activation Record visualization, Stack management, and Heap allocation.
- **LLVM Infrastructure**: Deep dive into the industry-standard compiler framework.
- **JIT & JVM**: Exploring Just-In-Time compilation and Bytecode execution.
- **Modern Topics**: Parallel/Concurrent programming support and Domain-Specific Languages (DSLs).

---

## 🧪 Interactive Labs & Playgrounds
This studio is packed with hands-on "Playgrounds" to help you learn by doing:
- **NFA to DFA Converter**: Watch the subset construction algorithm in action.
- **Interactive Derivation Lab**: Trace the LMD/RMD of complex grammars (like the Dangling Else).
- **Optimization Playground**: See how a compiler "cleans" messy code into efficient logic.
- **Mini-DSL "Shape Painter"**: Type simple commands to generate graphics and see the compiler trace.
- **Race Condition Simulator**: Experience why parallel compilers need atomic operations.

---

## 🚀 Getting Started

### 📋 Prerequisites
Ensure you have Python 3.8+ installed. You also need **Graphviz** installed on your system to enable diagram rendering.

**System-Level Graphviz Installation:**
- **Windows**: [Download installer](https://graphviz.org/download/) and add `bin` to your PATH.
- **Linux**: `sudo apt-get install graphviz`
- **macOS**: `brew install graphviz`

### 🛠️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/compiler-design-studio.git
   cd compiler-design-studio
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the Studio:
   ```bash
   streamlit run main.py
   ```

---

## 📸 Guided Tour
Once launched, use the **Sidebar Navigation** to switch between the Home page, Unit 1, and Unit 2. Each section contains detailed "Digitized Notes" along with interactive components.

---

## 🤝 Contributing
Contributions are welcome! If you'd like to add a new parsing algorithm or an optimization pass:
1. Fork the project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes.
4. Push to the Branch.
5. Open a Pull Request.

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

---

**Developed with ❤️ for the Compiler Design community.**
