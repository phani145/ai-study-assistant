# AI Study Assistant

An AI-powered study assistant that helps students learn from PDF study materials using Generative AI, PDF summarization, question answering, Speech-to-Text, and Text-to-Speech.

---

## 1. Project Title

**AI Study Assistant**

The AI Study Assistant is a GenAI-powered application designed to help students understand and revise their study materials efficiently.

---

## 2. Problem Statement

Students often spend a lot of time reading lengthy study materials and searching for important concepts, definitions, examples, and exam-related information.

The AI Study Assistant allows students to upload their PDF study materials and interact with them using AI.

The application can summarize study material, answer questions based on the uploaded PDF, generate study resources, and support voice-based interaction.

---

## 3. Objectives

- Provide an AI-powered personal study assistant.
- Allow students to upload PDF study materials.
- Extract text from PDF documents.
- Generate short and detailed summaries.
- Answer questions based on uploaded study materials.
- Provide page references when possible.
- Generate MCQs for exam preparation.
- Generate flashcards for quick revision.
- Generate important exam questions.
- Provide Speech-to-Text functionality.
- Provide Text-to-Speech functionality.
- Use a local Ollama AI model.
- Provide a simple and user-friendly interface.

---

## 4. Features

### PDF Upload

- Upload PDF study materials.
- Extract text from PDF files.
- Display document information.
- Detect scanned or image-only PDFs.

### AI Summarization

The application provides:

- Short Summary
- Detailed Summary
- Important Concepts
- Definitions
- Examples
- Formulas
- Exam-oriented information

### PDF Question Answering

Students can ask questions about the uploaded PDF.

The assistant:

- Searches the uploaded study material.
- Uses relevant PDF content to generate answers.
- Provides page references when possible.
- Avoids generating information that is not available in the uploaded material.

If the information is not found:

> I couldn't find this information in the uploaded PDF.

### Study Tools

The application can generate:

- Multiple Choice Questions (MCQs)
- Flashcards
- Important Exam Questions

### Voice Interaction

The application supports:

- Speech-to-Text using Whisper
- Voice-based questions
- Text-to-Speech using gTTS
- Audio playback of AI responses

### Local AI

The application uses:

- Ollama
- Gemma 3 1B

The AI model runs locally through Ollama.

---

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| PyMuPDF | PDF text extraction |
| Ollama | Local AI model runtime |
| Gemma 3 1B | Generative AI model |
| Requests | Ollama API communication |
| python-dotenv | Environment variable management |
| Faster-Whisper | Speech-to-Text |
| gTTS | Text-to-Speech |

---

## 6. Application Architecture

**```text
                         ┌──────────────────┐
                         │       User       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    Streamlit     │
                         │      app.py      │
                         └────────┬─────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
       │ PDF Upload  │     │ AI Summary  │     │    Voice    │
       │             │     │ & Q&A       │     │ Interface   │
       └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
              │                   │                   │
              ▼                   ▼                   ▼
       ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
       │  PyMuPDF    │     │   Ollama    │     │   Whisper   │
       │ PDF Service │     │ Gemma 3 1B  │     │    STT      │
       └─────────────┘     └─────────────┘     └─────────────┘
                                                      │
                                                      ▼
                                               ┌─────────────┐
                                               │    gTTS     │
                                               │    TTS      │
                                               └─────────────┘
***************PROJECT STRUCTURE***********
ai-study-assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
│
├── components/
│   ├── __init__.py
│   ├── pdf_uploader.py
│   ├── chat_interface.py
│   ├── summary_view.py
│   └── voice_interface.py
│
├── services/
│   ├── __init__.py
│   ├── pdf_service.py
│   ├── ollama_service.py
│   ├── stt_service.py
│   └── tts_service.py
│
├── prompts/
│   ├── summary_prompts.py
│   └── qa_prompts.py
│
└── screenshots/
7. Installation Steps
Step 1: Clone the Repository
git clone YOUR_GITHUB_REPOSITORY_URL

Go into the project folder:

cd ai-study-assistant
Step 2: Create a Virtual Environment
python -m venv venv
Step 3: Activate the Virtual Environment

For Windows:

venv\Scripts\activate

You should see:

(venv) PS C:\AI_Study_Assistant>
Step 4: Install Dependencies
pip install -r requirements.txt
8. Environment Setup

Create a .env file in the project root directory.

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:1b

No API key is required because the application uses a local Ollama model.

Ollama Setup

Check whether Ollama is installed:

ollama --version

Check available models:

ollama list

Make sure the following model is available:

gemma3:1b

If it is not installed:

ollama pull gemma3:1b

Test the model:

ollama run gemma3:1b

Note: gemma3:1b is an Ollama model name. It is not a Windows or PowerShell command by itself.

9. How to Run
Step 1: Activate Virtual Environment
venv\Scripts\activate
Step 2: Start Ollama

Make sure Ollama is running and gemma3:1b is available.

ollama list
Step 3: Run Streamlit
streamlit run app.py

The application will open in your browser.

Default URL:

http://localhost:8501
Step 4: Use the Application
Upload a PDF.
Wait for the PDF to be processed.
Generate a short or detailed summary.
Ask questions about the PDF.
Generate MCQs.
Generate flashcards.
Generate important exam questions.
Use voice input.
Listen to AI responses using Text-to-Speech.
10. Screenshots

Add screenshots of the application inside the screenshots/ folder.

Recommended screenshots:

Home Page
PDF Upload
AI Summary
Question Answering
Voice Interface
MCQ Generation
Flashcards

Example:

![Home Page](screenshots/home.png)

![PDF Upload](screenshots/pdf-upload.png)

![AI Summary](screenshots/summary.png)

![Question Answering](screenshots/question-answer.png)

![Voice Interface](screenshots/voice.png)
11. Future Enhancements
OCR support for scanned PDFs.
Support for DOCX, PPTX, and TXT files.
Retrieval-Augmented Generation (RAG).
Vector database integration using FAISS or ChromaDB.
Personalized study plans.
Learning progress tracking.
Weak-topic identification.
Adaptive difficulty levels.
Automatic question-paper generation.
Previous-year-question analysis.
Timed mock tests.
Automatic answer evaluation.
Multilingual Speech-to-Text.
Multilingual Text-to-Speech.
Student accounts and authentication.
Saved study materials and chat history.
Cloud deployment.
Conclusion

The AI Study Assistant provides students with an interactive platform to learn from their own study materials.

By combining PDF processing, Generative AI, Speech-to-Text, and Text-to-Speech, the application helps students summarize content, ask questions, revise important concepts, and prepare for examinations through a single interface.

Author
Phani
B.Tech Computer Science Engineering Student**
