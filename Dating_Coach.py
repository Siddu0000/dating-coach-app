import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load the API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# App UI settings
st.set_page_config(page_title="Dating Coach AI 💘", page_icon="💌")
st.title("💘 AI Dating Chat Coach")
st.markdown("_Train your dating game by chatting with AI personalities and getting feedback!_")

# Define girl personalities
personalities = {
    "Sweet & Shy": {
        "prompt": "Respond like a sweet, soft-spoken girl who’s a bit shy but friendly. Be polite, modest, and warm.",
        "avatar": "https://i.pravatar.cc/150?img=47"
    },
    "Bold & Flirty": {
        "prompt": "Respond like a bold, confident girl who's playful and flirty. Be fun, a little cheeky, and charming.",
        "avatar": "https://i.pravatar.cc/150?img=65"
    },
    "Witty & Sarcastic": {
        "prompt": "Respond like a smart, witty girl with a sarcastic sense of humor. Be clever, teasing, and confident.",
        "avatar": "https://i.pravatar.cc/150?img=58"
    },
    "Friendly & Chill": {
        "prompt": "Respond like a relaxed, easy-going girl who's just being friendly and casual. Keep it cool and genuine.",
        "avatar": "https://i.pravatar.cc/150?img=64"
    }
}

# Sidebar for personality selection
with st.sidebar:
    st.header("💃 Choose Personality")
    selected = st.selectbox("Select girl persona", list(personalities.keys()))
    st.image(personalities[selected]["avatar"], width=150, caption=selected)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "score_history" not in st.session_state:
    st.session_state.score_history = []

# Function to get girl's response
def get_girl_response(user_msg, persona):
    prompt = f"""You are roleplaying as a girl on a dating app. {persona}
Respond to: "{user_msg}"
Keep it casual and under 50 words."""
    res = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.9
    )
    return res.choices[0].message.content.strip()

# Function to score user's message
def score_user_message(user_msg):
    prompt = f"""You are a dating expert. Score this message out of 10 for:
- Friendliness
- Effort
- Tone (flirty, respectful)
Give a short tip for improvement.

Message: "{user_msg}"
"""
    res = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return res.choices[0].message.content.strip()

# Input box for user's message
user_input = st.text_input("💬 Type your message", max_chars=200, placeholder="e.g. That smile in your pic could end wars 😄")
if st.button("💌 Send"):
    if user_input.strip() != "":
        with st.spinner("Simulating reply..."):
            reply = get_girl_response(user_input, personalities[selected]["prompt"])
            feedback = score_user_message(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Her", reply))
        st.session_state.score_history.append((user_input, feedback))

# Chat display
if st.session_state.chat_history:
    st.subheader("🗨️ Chat History")
    for speaker, msg in st.session_state.chat_history[::-1]:
        prefix = "👩 Her" if speaker == "Her" else "🧑 You"
        st.markdown(f"**{prefix}:** {msg}")

# Feedback display
if st.session_state.score_history:
    st.subheader("📊 Feedback")
    for i, (msg, fb) in enumerate(st.session_state.score_history[::-1], 1):
        with st.expander(f"Message {len(st.session_state.score_history)-i+1}: \"{msg}\""):
            st.info(fb)
