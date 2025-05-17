# voice_ui_app.py

import streamlit as st
from voice_functions import listen, threaded_speak, ask_gemini, stop_tts
import time

st.set_page_config(page_title="Voice Assistant", layout="centered")

# Title and navbar style
st.markdown("""
<nav style='background-color: #0f172a; padding: 10px; border-radius: 10px; text-align: center;'>
    <span style='color: white; margin-right: 20px;'>Home</span>
    <span style='color: white; margin-right: 20px;'>About</span>
    <span style='color: white;'>Contact</span>
</nav>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .wave {
            display: inline-block;
            width: 6px;
            height: 20px;
            margin: 0 2px;
            background: #6c63ff;
            animation: wave 1s infinite ease-in-out;
        }

        .wave:nth-child(2) {
            animation-delay: 0.2s;
        }
        .wave:nth-child(3) {
            animation-delay: 0.4s;
        }
        @keyframes wave {
            0%, 100% {
                transform: scaleY(1);
            }
            50% {
                transform: scaleY(2);
            }
        }
    </style>
""", unsafe_allow_html=True)


# Theme toggle
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

if st.checkbox("🔆light Mode"):
    st.session_state.dark_mode = True
else:
    st.session_state.dark_mode = False

if st.session_state.dark_mode:
    st.markdown("""
        <style>
            body, .stApp { background-color: white; color: black; }
        </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Voice Assistant Bot")


st.markdown("Ask a question using your voice. Click **Ask** to begin, or **Stop** to pause speech.")



# Session state setup
if 'status' not in st.session_state:
    st.session_state.status = 'idle'

if 'response' not in st.session_state:
    st.session_state.response = ""

if 'history' not in st.session_state:
    st.session_state.history = []

if 'paused' not in st.session_state:
    st.session_state.paused = False

# Buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🎤 Ask", type="primary"):
        st.session_state.status = 'listening'

        with st.spinner("🎧 Listening... Please speak now"):
            user_input = listen()

        if "ERROR" not in user_input:
            st.session_state.user_input = user_input
            st.markdown(f"**🗣️ You said:** `{user_input}`")

            with st.spinner("💡 Thinking..."):
                response = ask_gemini(user_input)

            st.session_state.response = response
            st.session_state.history.append((user_input, response))
            st.markdown("""
                <div class="wave"></div>
                <div class="wave"></div>
                <div class="wave"></div>
            """, unsafe_allow_html=True)
            threaded_speak(response)
        else:
            st.warning("Could not understand your voice input.")
            st.session_state.response = ""

with col2:
    if st.button("⏸️ Stop/Resume",type="primary"):
        if not st.session_state.paused:
            stop_tts()
            st.session_state.paused = True
            st.info("🔇 Speech output stopped.")
        else:
            # Resume speaking the last response
            st.session_state.paused = False
            threaded_speak(st.session_state.response)
            st.markdown("🔊 Resuming speech.")

with col3:
    if st.button("🧹 Clear History", type="primary"):
        st.session_state.history = []
        st.session_state.response = ""
        st.markdown("🧾 Chat history cleared.")

with col4:
    if st.button("🔚 End Conversation", type="primary"):
        st.markdown("👋 Conversation ended. You may now close the app.")
        st.stop()

# Show full conversation history
if st.session_state.history:
    st.markdown("### 💬 Conversation History")
    for i, (q, r) in enumerate(st.session_state.history):
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Gemini:** {r}")
