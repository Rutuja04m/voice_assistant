# voice_assistant
Voice Assistant Bot with Streamlit + Gemini AI

A lightweight voice-based assistant built using Python, Streamlit, and Google's Gemini AI (1.5 Flash). This bot listens to your voice input, generates responses using Gemini, and speaks back the answers.

## 🚀 Features

- 🎧 Voice input using microphone
- 🤖 Gemini AI integration for smart answers
- 🔊 Speech output using pyttsx3 (offline TTS)
- 🌓 Light/Dark mode toggle
- ⏸️ Stop/Resume voice output
- 🧹 Clear conversation history
- 🔚 End conversation button
- 🎛️ Animated UI with Streamlit

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend**:
  - SpeechRecognition (voice input)
  - pyttsx3 (text-to-speech)
  - Google Generative AI (Gemini 1.5 Flash)

## 📁 Project Structure

voice_assistant/
│
├── voice_ui_app.py # Streamlit Frontend
├── voice_functions.py # Voice logic
├── venv/ # Virtual environment
├── requirements.txt # Dependencies
└── README.md # Project documentation

## ⚙️ Installation

```bash

git clone <repo-url>
cd voice_assistant
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

--> Configuration

Replace your Gemini API Key inside voice_functions.py:

genai.configure(api_key="YOUR_API_KEY")

--> How it Works:

Click Ask to speak a question.

The bot converts your voice to text.

Gemini AI processes the query and returns a response.

The bot reads out the response.

Use Stop/Resume to pause or continue TTS.

Use Clear History to reset conversation.

Use End Conversation to stop the app cleanly.


