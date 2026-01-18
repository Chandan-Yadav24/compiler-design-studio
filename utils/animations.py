import json
import streamlit as st

# Currently just a placeholder for lottie integration if we add it later
# For now, we rely on Streamlit's native animations
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
