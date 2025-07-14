 
# 🧠 Smart Research Assistant

A GenAI-powered assistant that reads uploaded documents and helps users:
- Answer complex, logic-based questions
- Summarize research material
- Evaluate user comprehension
- Justify all answers with references from source

---

## 🌐 Live Link

https://smartassistant07.streamlit.app/

---

## 🎥 Demo Photo/Video

---

<img width="1440" height="829" alt="Demo Photo1" src="https://github.com/user-attachments/assets/4791994a-9c0b-49d7-b3b6-5593ad43face" />

---

<img width="1440" height="829" alt="Demo Photo2" src="https://github.com/user-attachments/assets/880061c2-db0b-4e9c-8ea5-56aebf519dc4" />

---

📹 Loom: https://www.loom.com/share/7428481428be46c683076394076ecd04?sid=7f527cb6-3644-4ef9-b233-a62d18ffc192

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/xtfaisal07/smart-research-assistant.git
cd smart-research-assistant
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate      # For Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app/main.py
```

---

## 📂 Project Structure

```
smart-research-assistant/
├── README.md
├── requirements.txt
├── postman/
│   └── smart-assistant.postman_collection.json
├── app/
│   ├── main.py
│   ├── logic.py
│   ├── utils.py
├── templates/
  └── index.html
```

---

## 🧱 Architecture / Reasoning Flow

### Modules:

- **main.py** – User interface (Streamlit) and backend interaction
- **logic.py** – Core logic, LLM interaction, document processing
- **utils.py** – Helper functions for parsing, prompting, evaluation

### Flow:

1. Upload PDF or document file
2. App parses and indexes content
3. User asks questions
4. Model answers + explains reasoning using references

---

## 🧪 Tech Stack

- Python 3.10+
- Streamlit
- OpenAI / Perplexity API
- LangChain (optional)
- PyMuPDF or pdfminer.six (PDF parsing)

---

## 🎥 Demo Photo/Video 



📹 Loom: [https://www.loom.com/share/your-demo-link](https://www.loom.com/share/7428481428be46c683076394076ecd04?sid=bec0108d-2ef9-4b83-85c0-7c351c55aaed)

---

## 🧑‍💻 Author

**Faisal Naseer**  
[GitHub](https://github.com/xtfaisal07)

---

Built with ❤️ using Gemini + Streamlit By Faisal Naseer
