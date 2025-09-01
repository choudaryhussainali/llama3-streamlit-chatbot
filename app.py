import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
        body {
            background: linear-gradient(120deg, #d4fc79, #96e6a1);
            font-family: 'Segoe UI', sans-serif;
        }
        .stChatMessage {
            border-radius: 20px;
            padding: 15px;
            margin-bottom: 10px;
        }
        .user {
            background-color: #d1ecf1;
            text-align: right;
        }
        .bot {
            background-color: #f8d7da;
            text-align: left;
        }
        .stTextInput>div>div>input {
            font-size: 16px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712039.png", width=100)
st.sidebar.title("Groq AI Chatbot 🤖")
st.sidebar.markdown("### 🧠 Chat Memory")
memory_enabled = st.sidebar.toggle("Enable Chat Memory", value=True)
if memory_enabled:
    st.sidebar.markdown("Chat memory is enabled. Your conversation history will be saved.")
st.sidebar.markdown("Built using **llama-3.3-70b-versatile** via **Groq API**")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.title("💬 AI Assistant")
st.caption("Ask anything — your AI assistant is here to help!")

if st.session_state.chat_history:
    chat_text = "\n\n".join(
        [f"User: {msg['content']}" if msg["role"] == "user" else f"Assistant: {msg['content']}" for msg in st.session_state.chat_history]
    )

    st.download_button(
        label="💾 Download Chat History",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain",
    )


for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"<div class='stChatMessage user'>🧑‍💻: {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='stChatMessage bot'>🤖: {msg['content']}</div>", unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", key="input", placeholder="Ask me anything...")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

 
    if memory_enabled:
        messages = [{"role": "system", "content": "You are an Ai assistant(LLM). Your Founder is 'Choudary Hussain Ali'. Founder's Email: choudaryhussainali@outlook.com "}]
        messages += st.session_state.chat_history
        messages.append({"role": "user", "content": user_input})
    else:
        messages = [
            {"role": "system", "content": "You are an Ai assistant(LLM). Your Founder is 'Choudary Hussain Ali'. Founder's Email: choudaryhussainali@outlook.com "},
            {"role": "user", "content": user_input}
        ]

    response = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
    )

    bot_reply = response.choices[0].message.content

    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

    st.rerun()

