import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="LLM Flashcard Viewer", page_icon="🧠", layout="wide")

st.title("🧠 LLM-Powered Flashcard Viewer")
st.markdown("Easily browse and study flashcards generated from your educational content.")


st.sidebar.title("📂 Upload Flashcards")
uploaded = st.sidebar.file_uploader("Upload `flashcards.json`", type=["json"])


if uploaded:
    raw = uploaded.read().decode("utf-8")
else:
    st.info("No file uploaded. Using default sample flashcards.")
    raw = json.dumps([
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What process do plants use to make food?", "answer": "Photosynthesis"},
        {"question": "Which force pulls objects toward the Earth?", "answer": "Gravity"},
    ])


try:
    cards = json.loads(raw)
    df = pd.DataFrame(cards)
except Exception as e:
    st.error("❌ Could not parse flashcards. Please check your file.")
    st.stop()


search = st.text_input("🔍 Search flashcards by keyword")
if search:
    df = df[df.apply(lambda row: search.lower() in row['question'].lower() or search.lower() in row['answer'].lower(), axis=1)]



if not df.empty:
    st.subheader("🎴 Flashcard Viewer")

    if len(df) == 1:
        card = df.iloc[0]
        st.info("Only 1 card matches your search.")
    else:
        index = st.slider("Choose a card", 1, len(df), 1)
        card = df.iloc[index - 1]
        
        
    st.markdown(f"""
    <div style='
    background-color:#fdf6e3;  /* soft beige */
    padding: 20px;
    border-radius: 12px;
    margin-top: 10px;
    border: 1px solid #ddd;
    color: #2e7d32;            /* deep green */'>
    <h3 style='color:black;'>🧠 Q: {card['question']}</h3>
    <hr style='border-top:1px solid #cfcfcf'>
    <p style='font-size:18px; color:black;'>
        <strong>✅ A:</strong> {card['answer']}
    </p>
    </div>""", unsafe_allow_html=True)


else:
    st.warning("No flashcards match your search. Try a different keyword.")


with st.expander("📋 See All Flashcards"):
    st.dataframe(df, use_container_width=True)


col1, col2 = st.columns(2)
with col1:
    st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode('utf-8'), "flashcards.csv", "text/csv")
with col2:
    st.download_button("⬇️ Download JSON", json.dumps(cards, indent=2).encode('utf-8'), "flashcards.json", "application/json")


anki_lines = df.apply(lambda row: f"{row['question']}\t{row['answer']}", axis=1)
anki_text = "\n".join(anki_lines.tolist()).encode("utf-8")

col3, col4 = st.columns(2)
with col3:
    st.download_button(
        label="🗃️ Export for Anki (.txt)",
        data=anki_text,
        file_name="anki_flashcards.txt",
        mime="text/plain"
    )
with col4:
    st.download_button(
        label="📘 Export for Quizlet (.tsv)",
        data=anki_text,
        file_name="quizlet_flashcards.tsv",
        mime="text/tab-separated-values"
    )
