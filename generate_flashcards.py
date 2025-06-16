import os
import json
import openai
from dotenv import load_dotenv

# Load your API key from .env
load_dotenv("file.env")

# ✅ Use Groq API endpoint and key
openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

if not openai.api_key:
    raise ValueError("GROQ_API_KEY not found in environment")

# Load your cleaned assignment text
with open("cleaned_assignment.txt", "r", encoding="utf-8") as f:
    cleaned_text = f.read()

# Prompt for flashcard generation
prompt = (
    "Generate 10 flashcards from the following educational text. "
    "Each flashcard should include a short, clear question and an accurate answer. "
    "Return the result as a JSON array of objects with 'question' and 'answer' keys only.\n\n"
    f"Text:\n{cleaned_text}"
)

# Make the request to Groq (LLaMA 3)
response = openai.ChatCompletion.create(
    model="llama3-8b-8192",  # You can also try "llama3-70b-8192"
    messages=[
        {"role": "system", "content": "You are a flashcard generator."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3,
    max_tokens=1000,
)

# Parse response
import re

reply = response.choices[0].message.content.strip()

# Extract JSON from the response using a regular expression
match = re.search(r"\[\s*{.*?}\s*]", reply, re.DOTALL)
if not match:
    raise ValueError("Couldn't find valid JSON array in model response:\n" + reply)

json_str = match.group(0)

try:
    flashcards = json.loads(json_str)
except json.JSONDecodeError:
    raise ValueError("JSON parsing failed. Extracted string:\n" + json_str)


# Print and save
for i, card in enumerate(flashcards, start=1):
    print(f"\nCard {i}\nQ: {card['question']}\nA: {card['answer']}")

# Save to file
with open("flashcards.json", "w", encoding="utf-8") as out:
    json.dump(flashcards, out, indent=2, ensure_ascii=False)

print("\n✅ Flashcards saved to flashcards.json")
