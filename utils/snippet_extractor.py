import re

def extract_snippet(text, answer, window=50):
    answer = re.escape(answer.strip())
    match = re.search(rf"(.{{0,{window}}}{answer}.{{0,{window}}})", text, re.IGNORECASE)
    return match.group(0).strip() if match else "Snippet not found."
