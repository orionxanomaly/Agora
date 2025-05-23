
import streamlit as st
import os
import shutil
from datetime import datetime
from fullsynthesisideologies import extract_text_from_html_files, run_all_ideologies, synthesize_reactions




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

if st.button("Ask the political factions on the Agora for their opinions!"):
    st.info("🔄 Extracting article content from uploaded HTML...")
    extract_text_from_html_files()

    st.info("🧠 Listening to the Denizens of the Agora...")
    run_dir, timestamp = run_all_ideologies()


    st.success("✅ Ok they're all done talking! (Finally).")

    st.info("🧠 The Archon explains the different perspectives to the Demos...")
    synthesis_path = os.path.join(run_dir, f"synthesis_output_{timestamp}.txt")




    st.success("✅ The Demos may now deliberate on the matter further.")


    st.markdown("### Download Outputs")
    for fname in os.listdir(run_dir):
        with open(os.path.join(run_dir, fname), "rb") as f:
            st.download_button(label=f"Download {fname}", data=f, file_name=fname)

    with open(synthesis_path, "rb") as f:
        st.download_button(label="Download Final Synthesis", data=f, file_name=os.path.basename(synthesis_path))
