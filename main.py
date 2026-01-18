import streamlit as st
import importlib
import modules.unit1 as unit1
import modules.unit2 as unit2

# Force reload modules to avoid caching issues
importlib.reload(unit1)
importlib.reload(unit2)

# Page Configuration
st.set_page_config(
    page_title="Compiler Design Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS & Tailwind
def load_css(file_name):
    # Tailwind CSS CDN
    st.markdown('<script src="https://cdn.tailwindcss.com"></script>', unsafe_allow_html=True)
    
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css("assets/style.css")
except FileNotFoundError:
    st.error("CSS file not found. Please ensure 'assets/style.css' exists.")

# Application Logic
def main():
    # Initialize session state for navigation
    if 'page' not in st.session_state:
        st.session_state.page = "Home"

    st.title("⚡ Compiler Design Studio")
    st.markdown("### Interactive Learning Platform for Compiler Construction")
    
    with st.sidebar:
        st.header("Navigation")
        
        # Function to update page from sidebar
        def set_page():
            st.session_state.page = st.session_state.sidebar_selection

        # Sidebar navigation using On_Change
        st.radio(
            "Select Unit",
            ["Home", "Unit 1: Front End", "Unit 2: Back End"],
            key="sidebar_selection",
            on_change=set_page,
            index=["Home", "Unit 1: Front End", "Unit 2: Back End"].index(st.session_state.page)
        )
        
        st.divider()
        st.info("💡 **Tip:** Explore the visualizations in each tab.")
        
    if st.session_state.page == "Home":
        render_home()
    elif st.session_state.page == "Unit 1: Front End":
        unit1.render()
    elif st.session_state.page == "Unit 2: Back End":
        unit2.render()

def render_home():
    # Trigger balloons only once per session or on specific action if needed
    if 'balloons_shown' not in st.session_state:
        st.balloons()
        st.session_state['balloons_shown'] = True

    # Using Tailwind classes for layout and styling
    st.markdown("""
    <div class="p-6 bg-gray-800 rounded-lg border border-gray-700 shadow-lg mb-6">
        <h2 class="text-3xl font-bold text-blue-400 mb-2">Welcome to the Course: MODULE - I</h2>
        <p class="text-gray-300">This platform provides a comprehensive, interactive journey through the design and construction of compilers.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="h-full p-6 bg-gray-900 rounded-lg border border-gray-700 hover:border-blue-500 transition-colors duration-300">
            <h3 class="text-xl font-semibold text-green-400 mb-4">🔬 Unit 1: Front End</h3>
            <ul class="list-disc pl-5 space-y-2 text-gray-400 mb-6">
                <li>Lexical Analysis</li>
                <li>Syntax Analysis</li>
                <li>Semantic Analysis</li>
                <li>Intermediate Code Generation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Unit 1 🚀", use_container_width=True):
            st.session_state.page = "Unit 1: Front End"
            st.rerun()
        
    with col2:
        st.markdown("""
        <div class="h-full p-6 bg-gray-900 rounded-lg border border-gray-700 hover:border-purple-500 transition-colors duration-300">
            <h3 class="text-xl font-semibold text-purple-400 mb-4">⚙️ Unit 2: Back End</h3>
            <ul class="list-disc pl-5 space-y-2 text-gray-400 mb-6">
                <li>Code Optimization</li>
                <li>Code Generation</li>
                <li>Runtime Environments</li>
                <li>Advanced Topics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Unit 2 🚀", use_container_width=True):
            st.session_state.page = "Unit 2: Back End"
            st.rerun()

if __name__ == "__main__":
    main()

