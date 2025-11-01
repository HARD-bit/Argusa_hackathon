import streamlit as st
import requests
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="RAG chatbot", layout="centered")

st.title("RAG System")
st.write("Insert a Prompt here, the response will be in a Json format.")

# --- USER IMPUT ---
backend_url = st.text_input("Backend URL", "http://localhost:8000/rag")  # endpoint backend
prompt = st.text_area("Prompt:", placeholder="Write your request here...")

# --- SENDING REQUEST ---
if st.button("SEND"):
    if not prompt.strip():
        st.warning(" Insert a prompt before sending")
    else:
        with st.spinner("⏳ The request is been processing..."):
            try:
                response = requests.post(
                    backend_url,
                    json={"prompt": prompt},
                    timeout=30
                )

                # Showing answer
                if response.status_code == 200:
                    try:
                        data = response.json()
                        st.subheader("JSON response")
                        st.json(data)
                    except json.JSONDecodeError:
                        st.error("The Json responce from the backend is not valid")
                        st.text(response.text)
                else:
                    st.error(f"Backend error ({response.status_code})")
                    st.text(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f" Connection error: {e}")
