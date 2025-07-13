from utils.gemini import gemini_chat
from utils.snippet_extractor import extract_snippet


def evaluate_answers(question, user_answer, correct_answer, doc_text):
    from utils.gemini import call_gemini
    from utils.snippet_extractor import extract_snippet
    import json

    prompt = f"""
Evaluate the user's answer compared to the correct answer based on the document. 

Return a JSON with:
- feedback: constructive response
- justification: supporting explanation (can include snippet)

Question: {question}
Correct Answer: {correct_answer}
User Answer: {user_answer}
"""

    response = call_gemini(prompt)

    # ✅ Handle if it's already parsed
    if isinstance(response, dict):
        result = response
    else:
        try:
            result = json.loads(response)
        except:
            # fallback if response is raw text
            result = {
                "feedback": response.strip() if isinstance(response, str) else "No feedback.",
                "justification": extract_snippet(doc_text, correct_answer)
            }

    return {
        "feedback": result.get("feedback", "No feedback."),
        "justification": result.get("justification", "No justification.")
    }
