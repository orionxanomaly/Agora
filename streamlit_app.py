
import streamlit as st
import os
import shutil
from datetime import datetime
from FullSynthesisIdeologies import extract_html_from_files, run_ideology_analysis, run_synthesis


st.title("Ideological Reactions GPT Demo")
st.markdown("Upload saved HTML article files or paste article text to generate political reactions from 5 ideological perspectives and a final synthesis.")

# Create directories if they don't exist
html_dir = "saved_html_files"
extracted_dir = "extracted_articles"
os.makedirs(html_dir, exist_ok=True)
os.makedirs(extracted_dir, exist_ok=True)

# Optional: Manual text input
manual_text = st.text_area("Or paste article text directly (optional)", height=300)

# Upload HTML files
uploaded_files = st.file_uploader("Upload one or more HTML files", type=["html"], accept_multiple_files=True)

# Save manual input if provided
if manual_text.strip():
    with open(os.path.join(extracted_dir, "manual_input.txt"), "w", encoding="utf-8") as f:
        f.write(manual_text)
    st.success("✅ Manual input saved.")

# Save uploaded HTML files
if uploaded_files:
    for file in uploaded_files:
        filepath = os.path.join(html_dir, file.name)
        with open(filepath, "wb") as f:
            f.write(file.read())
        st.success(f"Saved: {file.name}")

if st.button("Run Full Ideological Analysis"):
    if not manual_text.strip():
        st.info("🔄 Extracting article content from uploaded HTML...")
        extract_html_from_files()

    st.info("🧠 Running GPT reactions for all ideologies...")
    run_dir = run_ideology_analysis()

    st.success("✅ Reactions generated and saved.")

    st.info("🧠 Running final synthesis across all 5 ideologies...")
    synthesis_path = run_synthesis(run_dir)

    st.success("✅ Final synthesis complete.")

    st.markdown("### Download Outputs")
    for fname in os.listdir(run_dir):
        with open(os.path.join(run_dir, fname), "rb") as f:
            st.download_button(label=f"Download {fname}", data=f, file_name=fname)

    with open(synthesis_path, "rb") as f:
        st.download_button(label="Download Final Synthesis", data=f, file_name=os.path.basename(synthesis_path))
