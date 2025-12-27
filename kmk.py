import os
from dotenv import load_dotenv
from groq import Groq
from typing import Generator
import streamlit as st

load_dotenv()
#client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(page_title="Groq AI Chatbot", page_icon="👾", layout="wide")

# Top header (tiger logo + title)
st.markdown(
        """
        <div class="app-header">
            <div class="logo">🎃</div>
            <div class="titles">
                <h1>Groq AI Chatbot</h1>
                <p class="tagline">Professional AI assistant — fast, friendly, and private</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
            :root{
                --ig-purple:#833ab4; --ig-pink:#fd1d1d; --ig-orange:#fcb045; --accent:#4facfe;
                --ink:#f5f5f5; --ink-soft:#e5e7eb; --ink-muted:rgba(245,245,245,0.7);
            }
      html, body, [class*="css"], .stApp {
        height:100%;
        background: linear-gradient(135deg, var(--ig-purple), var(--ig-pink), var(--ig-orange));
                font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
                color: var(--ink);
      }
      .app-header{display:flex;align-items:center;gap:18px;padding:22px 24px 8px;}
      .app-header .logo{width:96px;height:96px;border-radius:28px;display:flex;align-items:center;justify-content:center;font-size:46px;background:linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));box-shadow:0 8px 24px rgba(15,23,42,0.25);backdrop-filter: blur(6px);}
      .app-header h1{margin:0;font-size:28px;color:white; font-weight:700;text-shadow:0 2px 12px rgba(0,0,0,0.25)}
      .app-header .tagline{margin:0;font-size:13px;color:rgba(255,255,255,0.9)}

      /* Chat area */
    .stChatMessage{max-width:78%;padding:14px;margin:10px 0;border-radius:16px;box-shadow:0 6px 14px rgba(255,255,255,0.08);transition:transform .18s ease, box-shadow .18s ease;}
    .stChatMessage:hover{transform:translateY(-3px);box-shadow:0 10px 30px rgba(255,255,255,0.14)}
    .user{background: linear-gradient(90deg, var(--ink), var(--ink-soft)); color:#1f2937; margin-left:auto; text-align:right}
    .bot{background: linear-gradient(90deg, rgba(255,255,255,0.95), rgba(255,255,255,0.9)); color:#1f2937; text-align:left}

      /* Input area */
      .stTextInput>div>div>input{padding:14px 16px;border-radius:12px;border:0;box-shadow:inset 0 1px 0 rgba(15,23,42,0.03);font-size:15px}
      .stButton>button{background:linear-gradient(90deg,var(--ig-purple),var(--ig-pink));color:white;border-radius:12px;padding:10px 14px;border:0;font-weight:600}
      .stButton>button:hover{filter:brightness(1.03);transform:translateY(-1px)}

      /* Sidebar tweaks */
      .sidebar .stImage img{border-radius:12px}
    .message-meta{font-size:11px;color:var(--ink-muted);margin-bottom:6px}
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("""
<div style='display:flex;align-items:center;gap:12px;padding:8px 4px'>
    <div style='font-size:32px'>🎃</div>
    <div style='line-height:1'>
        <div style='font-weight:700'>Groq AI Chatbot</div>
        <div style='font-size:12px;color:rgba(255,255,255,0.65)'>Powered by llama-3.3-70b</div>
    </div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("### 🧠 Chat Memory")
memory_enabled = st.sidebar.toggle("Enable Chat Memory", value=True)
if memory_enabled:
        st.sidebar.markdown("Chat memory is enabled. Your conversation history will be saved.")
st.sidebar.markdown("Built using **llama-3.3-70b-versatile** via **Groq API**")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.markdown("""
<div style='padding:6px 24px 18px'>
    <p style='margin:0;color:rgba(255,255,255,0.9)'>Ask anything — your AI assistant is here to help.</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.chat_history:
    chat_text = "\n\n".join(
        [f"User: {msg['content']}" if msg["role"] == "user" else f"Assistant: {msg['content']}" for msg in st.session_state.chat_history]
    )

    st.download_button(
        label="💾 Export Conversation",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain",
    )


for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"<div class='stChatMessage user'><div class='message-meta'>You</div>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='stChatMessage bot'><div class='message-meta'>Groq Assistant</div>{msg['content']}</div>", unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("", key="input", placeholder="Type a message...")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

 
    if memory_enabled:
        messages = [{"role": "system", "content": "You are an Ai assistant(LLM). Your Founder is 'Choudary Hussain Ali' and co-founder'karthikmanikandan'. Founder's Email: choudaryhussainali@outlook.com and co-founder linked in:https://www.linkedin.com/in/karthik-manikandan/"}]
        messages += st.session_state.chat_history
        messages.append({"role": "user", "content": user_input})
    else:
        messages = [
            {"role": "system", "content": "You are an Ai assistant(LLM). Your Founder is 'Choudary Hussain Ali' and co-founder'karthikmanikandan'. Founder's Email: choudaryhussainali@outlook.com and co-founder linked in:https://www.linkedin.com/in/karthik-manikandan/"},
            {"role": "user", "content": user_input}
        ]

    response = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
    )

    bot_reply = response.choices[0].message.content

    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

    st.rerun()



