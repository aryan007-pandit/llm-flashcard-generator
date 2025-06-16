# 🧠 LLM-Powered Flashcard Generator

This is a lightweight yet powerful tool that:
- Extracts content from PDFs or text files
- Uses a Large Language Model (LLaMA 3 via Groq) to generate flashcards
- Displays the flashcards in a user-friendly web UI
- Exports the cards in CSV or JSON for studying or app import

---

## 🚀 Features

- 📄 PDF/Text file parser using `pdfplumber`
- 🤖 LLM integration with Groq's blazing-fast `LLaMA 3`
- 🧠 Auto-generates question-answer flashcards
- 🌐 Streamlit-based UI with upload & export support
- 💾 Download results as `.json` or `.csv`

---

## 🛠️ How It Works

1. **Text Extraction**
   - Uses `pdfplumber` to extract and clean text from educational PDFs.

2. **Flashcard Generation**
   - Sends the cleaned text to Groq’s hosted LLaMA 3 model via an OpenAI-compatible API.
   - Prompts the model to return 10–15 flashcards in JSON.

3. **Web UI with Streamlit**
   - Drag-and-drop your `flashcards.json`
   - View them in a table
   - Export to CSV or JSON with a single click

---

## 📦 Setup

### 1. Clone the repo

```bash
git clone https://github.com/aryan007-pandit/flashcard-generator.git
cd flashcard-generator
