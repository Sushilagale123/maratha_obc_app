import os
import re
import json
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import Google Generative AI
try:
    import google.generativeai as genai
except ImportError:
    genai = None

api_key = os.getenv("GOOGLE_API_KEY")

# Page configuration
st.set_page_config(page_title="मराठा आरक्षण – जनसंपर्क केंद्र", page_icon="🚩", layout="wide")

# Sidebar configuration
with st.sidebar:
    st.title("Settings")
    
  
    
    # Model selection
    model_name = st.selectbox("Model", 
                             ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash"])
    
    # System instruction
    system_instruction = st.text_area(
        "System instruction",
        value="You are a concise, helpful assistant.",
        height=80
    )
    
    # Generation parameters
    st.subheader("Generation Parameters")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    top_p = st.slider("Top-p", 0.0, 1.0, 0.9, 0.05)
    top_k = st.slider("Top-k", 1, 100, 40, 1)
    max_tokens = st.slider("Max output tokens", 32, 2048, 512, 32)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = None

# Cache the model to avoid recreating it
@st.cache_resource(show_spinner=False)
def get_model(api_key, model_name, system_instruction):
    if genai is None:
        raise ImportError("google-generativeai is not installed")
    if not api_key:
        raise ValueError("API key missing")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name, system_instruction=system_instruction)

# Main app
#st.title("Gemini Multi Turn Chat")
# Custom Page Styling (Manoj Jarange theme)
st.markdown(
    """
    <style>
    body {
        background-color: #fff9f2;
    }
    .main {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .title {
        color: #d35400;
        text-align: center;
        font-size: 36px;
        font-weight: bold;
    }
    .subtitle {
        color: #2c3e50;
        text-align: center;
        font-size: 20px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown("<div class='title'>🟧 मराठा आरक्षण – जनसंपर्क केंद्र 🟧</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Inspired by Manoj Dada Jarange’s movement for justice</div>", unsafe_allow_html=True)


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_prompt = st.chat_input("Ask something...")


#ALLOW_PATTERN

with open("ALLOW_PATTERN.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    # Flatten all phrases from all lists in ALLOW_PATTERN
    phrases = []
    for v in data["ALLOW_PATTERN"].values():
        phrases.extend(v)
    # Escape and join phrases for regex
    pattern = r"(" + r"|".join(re.escape(p) for p in phrases) + r")"
    ALLOW_PATTERN = re.compile(pattern, re.IGNORECASE)

# Process user input
if user_prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # Get model
    try:
        model = get_model(api_key, model_name, system_instruction)
    except Exception as e:
        st.error(str(e))
        st.stop()
    
    # Generation configuration
    gen_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_tokens,
        "response_mime_type": "text/plain",
    }
    
    # Initialize chat session if needed
    if st.session_state.chat is None:
        history = []
        for msg in st.session_state.messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": msg["content"]})
        st.session_state.chat = model.start_chat(history=history)
    
    
REFUSAL_EN = "I can only help with Maratha reservation and OBC-related questions in India. Please rephrase your question within that scope."
REFUSAL_MR = "मी फक्त मराठा आरक्षण आणि ओबीसी-संबंधित प्रश्नांवरच मदत करू शकतो/शकते. कृपया तुमचा प्रश्न त्या चौकटीत पुन्हा विचारा."

# POLICY_PROMPT

with open("POLICY_PROMPT.txt", "r", encoding="utf-8") as f:
    POLICY_PROMPT = f.read()
    
    


def refuse_in_user_lang(text):
    return REFUSAL_MR if re.search(r"[ऀ-ॿ]", text) else REFUSAL_EN
    
# Generate response
if user_prompt:
    if not ALLOW_PATTERN.search(user_prompt):
        
        answer = refuse_in_user_lang(user_prompt)
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    full_prompt = f"{POLICY_PROMPT}\n\nUser question:\n{user_prompt}\n\nReturn the answer following the FORMAT section."
                    response = st.session_state.chat.send_message(full_prompt, generation_config=gen_config)
                    answer = response.text or "(No text in response)"
                except Exception as e:
                    answer = f"Error: {e}"
                st.markdown(answer)
        
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})