import streamlit as st
from utils.parser import parse_document
from backend.summarizer import summarize
from backend.qa_engine import answer_question_with_memory, generate_questions
from backend.evaluator import evaluate_answers

st.set_page_config(
    page_title="Smart Research Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for style
st.markdown("""
    <style>
    .summary-box {
        background-color: #e3f2fd;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        color: #0d47a1;
        font-size: 1.1rem;
    }
    .justification-box {
        background-color: #fff3e0;
        border-left: 6px solid #ffb300;
        padding: 1rem 1.5rem;
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
        font-style: italic;
        color: #bf360c;
    }
    .feedback-box {
        background-color: #e8f5e9;
        border-left: 6px solid #43a047;
        padding: 1rem 1.5rem;
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
        color: #1b5e20;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="color:#4a90e2;font-weight:700;">🧠 Smart Research Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#6c757d;font-size:1.2rem;">Summarize, question, and learn from your documents or pasted text.</p>', unsafe_allow_html=True)

# --- Task Bar with Tabs ---
tab1, tab2 = st.tabs(["📂 Upload File", "✍️ Paste/Type Text"])

doc_text = None

with tab1:
    st.subheader("Upload a PDF or TXT File")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"])
    if uploaded_file:
        try:
            doc_text = parse_document(uploaded_file)
            st.session_state['doc_text'] = doc_text
            st.session_state['chat_history'] = []
            st.success("File uploaded and processed successfully!")
        except Exception as e:
            st.error(f"❌ Error parsing document: {e}")
            st.stop()
    if doc_text:
        with st.expander("📖 Preview File (first 600 characters)"):
            st.write(doc_text[:600] + ("..." if len(doc_text) > 600 else ""))

with tab2:
    st.subheader("Paste or Type Text")
    pasted_text = st.text_area("Paste or type your text here", height=250)
    if pasted_text.strip():
        doc_text = pasted_text.strip()
        st.session_state['doc_text'] = doc_text
        st.session_state['chat_history'] = []
        st.success("Text received and ready for processing!")
    if doc_text:
        with st.expander("📖 Preview Text (first 600 characters)"):
            st.write(doc_text[:600] + ("..." if len(doc_text) > 600 else ""))

# --- Shared workflow for both tabs ---
if "doc_text" in st.session_state and st.session_state['doc_text']:
    doc_text = st.session_state['doc_text']
    st.markdown("---")
    st.subheader("📌 Auto Summary")
    with st.spinner("Generating summary..."):
        try:
            summary = summarize(doc_text)
            st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Error generating summary: {e}")
            st.stop()

    mode = st.radio("Choose Mode", ["Ask Anything", "Challenge Me"], horizontal=True)

    if mode == "Ask Anything":
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_question = st.text_input("❓ Ask a question based on the document or text")
        if user_question:
            try:
                response = answer_question_with_memory(doc_text, user_question, st.session_state.chat_history)
                st.session_state.chat_history.append({"question": user_question, "answer": response["answer"]})

                st.markdown("### ✅ Answer")
                st.write(response['answer'])
                st.markdown(
                    f'<div class="justification-box"><strong>Justification (Document Snippet):</strong><br>{response["justification"]}</div>',
                    unsafe_allow_html=True,
                )

                if st.session_state.chat_history:
                    st.markdown("### 🧠 Memory (Q&A History):")
                    for i, mem in enumerate(st.session_state.chat_history):
                        st.markdown(f"**{i+1}. Q:** {mem['question']}")
                        st.markdown(f"**   A:** {mem['answer']}")

            except Exception as e:
                st.error(f"❌ Error answering question: {e}")

    elif mode == "Challenge Me":
        if "challenge_index" not in st.session_state:
            st.session_state.challenge_index = 0
            st.session_state.challenge_questions = []
            st.session_state.challenge_complete = False

        st.markdown("### 📝 Challenge Mode")

        if st.button("🔁 Reset Challenge"):
            st.session_state.challenge_index = 0
            st.session_state.challenge_questions = []
            st.session_state.challenge_complete = False

        if st.button("Generate Questions"):
            try:
                questions = generate_questions(doc_text)
                if questions and questions[0].get("question") == "Unable to parse valid questions":
                    st.warning("⚠️ Gemini returned an unstructured response. Please refine the document or check token limits.")
                    st.json(questions)
                else:
                    st.session_state.challenge_questions = questions
                    st.session_state.challenge_index = 0
                    st.session_state.challenge_complete = False
            except Exception as e:
                st.error(f"❌ Error generating questions: {e}")

        if st.session_state.challenge_questions and not st.session_state.challenge_complete:
            q_index = st.session_state.challenge_index
            question_data = st.session_state.challenge_questions[q_index]

            st.markdown(f"### Q{q_index + 1}: {question_data['question']}")
            user_input = st.text_input("Your Answer", key=f"user_input_{q_index}")

            if st.button("Submit Answer", key=f"submit_{q_index}"):
                try:
                    result = evaluate_answers(
                        question_data["question"],
                        user_input,
                        question_data["answer"],
                        doc_text
                    )
                    st.markdown(
                        f'<div class="feedback-box"><strong>Feedback:</strong> {result["feedback"]}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="justification-box"><strong>Justification:</strong> {result["justification"]}</div>',
                        unsafe_allow_html=True,
                    )

                    if q_index + 1 < len(st.session_state.challenge_questions):
                        st.session_state.challenge_index += 1
                    else:
                        st.session_state.challenge_complete = True
                        st.success("🎉 All questions completed!")
                except Exception as e:
                    st.error(f"❌ Error evaluating answer: {e}")
else:
    st.info("👆 Select a tab and provide your input to get started.")

st.markdown("---")
st.markdown(
    """
    <p style="text-align:center; color:#888; font-size:0.9rem;">
    © 2025 Smart Research Assistant | Made with ❤️ using Streamlit
    </p>
    """,
    unsafe_allow_html=True,
)