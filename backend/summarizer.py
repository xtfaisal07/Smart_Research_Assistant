from utils.gemini import gemini_chat

def summarize(text):
    prompt = f"Summarize this document in under 150 words:\n\n{text}"
    response = gemini_chat(prompt)
    return response.get("feedback", "Summary not available.")
