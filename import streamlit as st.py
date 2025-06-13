import streamlit as st
import requests

st.title("Free GenAI Chatbot (Hugging Face)")

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_hf_response(prompt):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer YOUR_HF_API_TOKEN"}  # Optional: For higher rate limits
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 128, "temperature": 0.7},
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"].replace(prompt, "").strip()
    else:
        return "Sorry, the model is busy or unavailable."

user_input = st.text_input("You:", key="input")

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("AI is typing..."):
        ai_response = get_hf_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**AI:** {msg['content']}")