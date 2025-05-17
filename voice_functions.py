# voice_functions.py

import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import threading

# Gemini setup
genai.configure(api_key="AIzaSyAQSvLsUaeDS_BYFnw9RBUgSNaFf9Q2IEE")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize TTS engine once
tts_engine = pyttsx3.init()
tts_lock = threading.Lock()
tts_thread = None
is_speaking = False  # Global state to track speaking


def threaded_speak(text):
    global tts_thread, is_speaking

    def _speak():
        global is_speaking
        with tts_lock:
            try:
                is_speaking = True
                tts_engine.say(text)
                tts_engine.runAndWait()
            except RuntimeError as e:
                print("TTS RuntimeError:", e)
            finally:
                is_speaking = False

    if tts_thread is None or not tts_thread.is_alive():
        tts_thread = threading.Thread(target=_speak)
        tts_thread.start()


def stop_tts():
    global is_speaking
    with tts_lock:
        if is_speaking:
            print("Stopping TTS...")
            tts_engine.stop()
            is_speaking = False
        else:
            print("Nothing to stop.")


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            text = r.recognize_google(audio)
            print("Heard:", text)
            return text
        except sr.UnknownValueError:
            print("Didn't understand.")
            return "ERROR: Could not understand audio."
        except sr.RequestError as e:
            print(f"Error with speech service: {e}")
            return "ERROR: Speech service unavailable."


def ask_gemini(text):
    try:
        response = model.generate_content(text)
        print("Gemini Response:", response.text)
        return response.text
    except Exception as e:
        print(f"Gemini error: {e}")
        return "Sorry, Gemini failed to respond."
