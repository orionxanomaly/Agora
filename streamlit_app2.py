
import streamlit as st
import os
import shutil
from datetime import datetime
from fullsynthesisideologies import extract_text_from_html_files, run_all_ideologies, synthesize_reactions
import re
import textwrap
import streamlit.components.v1 as components
import uuid
import zipfile
import io



SESSION_ID = str(uuid.uuid4())[:8]  # Short unique ID per user session
st.info(f"🔐 Session ID: `{SESSION_ID}`")



st.title("🏛🗳👑 Welcome to the e-Agora, Citizen!  Remember, Nothing is Above Politics - Be Careful! 🛡️⚔️")
st.markdown("Upload saved HTML article files (you must use the browser extension, see below) OR paste any article text in the box below to generate political reactions from our 5 largest ideological factions and a summary by the Archon of Athens.")

st.info("🌟For the best experience, we recommend you use a Browser Extension called SingleFile, found [here](https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle). Install the (amazingly useful!) extension and you will be able to visit any web page and save the page as a clean single HTML file which is readable. After installing, visit a page with an article or other text, and click the add-on icon on your browser (Chrome or Opera compatible) and the page will save and download. Then click below to upload the downloaded HTML from your downloads folder.")



# Create directories if they don't exist
html_dir = f"saved_html_files_{SESSION_ID}"
extracted_dir = f"extracted_articles_{SESSION_ID}"
TXT_OUTPUT_DIR = extracted_dir


os.makedirs(html_dir, exist_ok=True)
os.makedirs(extracted_dir, exist_ok=True)


# Optional: Manual text input
manual_text = st.text_area("Or paste article text directly (optional)", height=300)

# Upload HTML files
uploaded_files = st.file_uploader("Upload one or more HTML files", type=["html"], accept_multiple_files=True)


# Clear previous text outputs
if os.path.exists(TXT_OUTPUT_DIR):
    for old_txt in os.listdir(TXT_OUTPUT_DIR):
        file_path = os.path.join(TXT_OUTPUT_DIR, old_txt)
        if file_path.endswith(".txt"):
            os.remove(file_path)
            
            
# Save manual input if provided
if manual_text.strip():
    with open(os.path.join(extracted_dir, "manual_input.txt"), "w", encoding="utf-8") as f:
        f.write(manual_text)
    st.success("✅ Manual input saved.")  


# Clear old HTML files
if os.path.exists(html_dir):
    for old_file in os.listdir(html_dir):
        file_path = os.path.join(html_dir, old_file)
        if file_path.endswith(".html"):
            os.remove(file_path)



# Save uploaded HTML files
if uploaded_files:
    for file in uploaded_files:
        filepath = os.path.join(html_dir, file.name)
        with open(filepath, "wb") as f:
            f.write(file.read())
        st.success(f"Saved: {file.name}")
        
        # ✅ Render the HTML content directly for preview
        with open(filepath, "r", encoding="utf-8") as html_file:
            html_content = html_file.read()
        st.markdown("**🔍 Preview of uploaded HTML:**")
        components.html(html_content, height=600, scrolling=True)

 

if st.button("📣 Ask the political factions on the Agora for their opinions!  This can take up to 2 minutes, please patiently wait for all to speak!"):
    
    
    # ✅ Save manual input (again — just in time)
    if manual_text.strip():
        with open(os.path.join(extracted_dir, "manual_input.txt"), "w", encoding="utf-8") as f:
            f.write(manual_text)

    
    
   
    
    
    st.info("🔄 Extracting article content from uploaded HTML or manual input...")
    extract_text_from_html_files()

    st.info("🧠 Listening to the Denizens of the Agora...")
    run_dir, timestamp, synthesis_path = run_all_ideologies()



    # 🗂️ Display the 5 ideological reactions in tabs
    st.markdown("### 🗂️ Reactions from the 5 Factions")
    tabs = st.tabs(["🦅🏡🧱 Traditionalist", "⚡🔱🔥 Promethean", "🏛️💼🧠 Managerialist", "📜⚖️🐍 Legalist", "✊🌈☭ Liberationist"])


    ideologies = ["Traditionalist", "Promethean", "Managerialist", "Legalist", "Liberationist"]

    for i, ideology in enumerate(ideologies):
        filename = f"{ideology}_reaction_{timestamp}.txt"
        filepath = os.path.join(run_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
                wrapped_lines = [textwrap.fill(line, width=130) if line.strip() != "" else "" for line in content.splitlines()]
                wrapped_content = "\n".join(wrapped_lines)
                tabs[i].markdown(f"<div style='white-space: pre-wrap; font-size: 1.0rem'>{wrapped_content}</div>", unsafe_allow_html=True)
                



    st.success("✅ Ok they're all done talking! (Finally).")

    st.info("🧠 The Archon of Athens explains the different perspectives to the Demos...")
    synthesis_path = os.path.join(run_dir, f"synthesis_output_{timestamp}.txt")


    st.markdown("### The Archon Explains")
    if os.path.exists(synthesis_path):
        with open(synthesis_path, "r", encoding="utf-8") as f:
            synthesis_text = f.read()
            
            
        synthesis_text = re.sub(r"(?m)^(\d+)\.\s*\n", r"\1. ", synthesis_text)
        
        synthesis_lines = synthesis_text.splitlines()
        wrapped_synthesis = "\n".join([
            textwrap.fill(line, width=150) if line.strip() != "" else ""
            for line in synthesis_lines
        ])
        
        
        
        st.markdown(f"<div style='white-space: pre-wrap; font-size: 1.0rem'>{wrapped_synthesis}</div>", unsafe_allow_html=True)





    st.success("✅ The Demos may now deliberate on the matter further.")



st.markdown("### Download All Outputs")

# Create a zip in memory
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, "w") as zip_file:
    for fname in os.listdir(run_dir):
        filepath = os.path.join(run_dir, fname)
        zip_file.write(filepath, arcname=fname)

# Reset buffer position to the start
zip_buffer.seek(0)

# Create one download button for the zip
st.download_button(
    label="📦 Download All Outputs (ZIP)",
    data=zip_buffer,
    file_name=f"Agora_Outputs_{timestamp}.zip",
    mime="application/zip"
)

# ✅ Optional: Clean up session-specific folders
shutil.rmtree(html_dir, ignore_errors=True)
shutil.rmtree(extracted_dir, ignore_errors=True)










            




