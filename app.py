import streamlit as st
import requests
import os

st.set_page_config(page_title="TechFlow Assistant", page_icon="💡")

# 🔧 Вопросы и ответы
faq = {
    "working hours": "Monday–Friday, 09:00–18:00",
    "location": "123 Silicon Avenue, Tashkent",
    "phone number": "+998 90 123 45 67",
    "email address": "support@techflow.uz"
}

# 🔐 GitHub настройки
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = "Abduqodir888/AI-Streamlit"  # формат: username/repo

def create_github_issue(question):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": f"Unanswered question: {question}",
        "body": f"User asked: **{question}**, but no answer was found.",
        "labels": ["support"]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 201

# 💬 Интерфейс
st.title("🤖 TechFlow AI Assistant")
st.write("Ask me anything about our business!")

question = st.text_input("Your question:")

if question:
    matched = None
    for key in faq:
        if key.lower() in question.lower():
            matched = key
            break

    if matched:
        st.success(f"**{matched.title()}**: {faq[matched]}")
    else:
        st.warning("Sorry, I couldn't find an answer to that.")
        if st.button("Raise GitHub Ticket"):
            with st.spinner("Creating ticket..."):
                success = create_github_issue(question)
                if success:
                    st.success("✅ Ticket created successfully!")
                else:
                    st.error("❌ Failed to create ticket.")