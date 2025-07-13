import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def call_gemini(prompt: str):
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(GEMINI_URL, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def answer_question_with_memory(doc_text: str, user_question: str, chat_history: list):
    history_prompt = ""
    for entry in chat_history:
        history_prompt += f"Q: {entry['question']}\nA: {entry['answer']}\n"

    prompt = f"""
You are an AI assistant that answers questions using only the following document:

--- Document ---
{doc_text}
----------------

Use prior context if helpful.

{history_prompt}
Now answer:
Q: {user_question}
A:"""

    answer = call_gemini(prompt)

    return {
        "answer": answer.strip(),
        "justification": find_justification(doc_text, answer),
        "memory": chat_history
    }


def generate_questions(doc_text: str):
    prompt = f"""
Read the document below and generate exactly 3 logic-based or comprehension-focused questions.
Respond in valid JSON ONLY like this:

[
  {{"question": "What is X?", "answer": "Y"}},
  {{"question": "How does A work?", "answer": "B"}},
  {{"question": "Why is C important?", "answer": "Because D..."}}
]

Document:
{doc_text}
"""

    response = call_gemini(prompt)

    # Try parsing valid JSON response
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # Attempt to extract using regex (fallback)
        matches = re.findall(r'{"question":\s*"(.*?)",\s*"answer":\s*"(.*?)"}', response)
        if matches:
            return [{"question": q, "answer": a} for q, a in matches]

    # Final fallback
    return [{"question": "Unable to parse valid questions", "answer": "N/A"}]

def highlight_snippet(doc_text: str, question: str, answer: str):
    import difflib

    lines = doc_text.split('\n')
    best_match = ""
    best_ratio = 0

    for line in lines:
        ratio = difflib.SequenceMatcher(None, line.lower(), answer.lower()).ratio()
        if ratio > best_ratio and len(line.strip()) > 20:
            best_ratio = ratio
            best_match = line.strip()

    return best_match if best_ratio > 0.3 else "No exact supporting snippet found."

def find_justification(doc_text: str, answer: str):
    sentences = doc_text.split(".")
    for sentence in sentences:
        if answer[:10].lower() in sentence.lower():
            return sentence.strip() + "."
    return "Could not extract justification from the document."
