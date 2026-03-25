import streamlit as st
import PyPDF2
import requests
from bs4 import BeautifulSoup
from datetime import date
import matplotlib.pyplot as plt

st.set_page_config(page_title="Opportunity Finder AI", layout="wide")

# ---------------- CUSTOM UI STYLE ----------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
}
.chat-user {
    background-color: #1f77b4;
    padding: 10px;
    border-radius: 10px;
    color: white;
}
.chat-ai {
    background-color: #2e2e2e;
    padding: 10px;
    border-radius: 10px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Opportunity Finder AI Agent")

# ---------------- SIDEBAR ----------------
st.sidebar.header("👤 User Profile")

skills = st.sidebar.text_input("Enter your skills")
interest = st.sidebar.selectbox("Interest", ["AI", "Web", "Data Science"])
uploaded_file = st.sidebar.file_uploader("Upload Resume (PDF)", type="pdf")

# ---------------- CHAT MEMORY ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_skills" not in st.session_state:
    st.session_state.last_skills = []

if "last_interest" not in st.session_state:
    st.session_state.last_interest = ""

# ---------------- FUNCTIONS ----------------
def extract_skills_from_resume(file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text().lower()
    except:
        return []

    skills_db = ["python","java","html","css","javascript","sql","machine learning","react"]
    return [skill for skill in skills_db if skill in text]

def calculate_score(skills_list):
    score = 0
    if "python" in skills_list: score += 30
    if "machine learning" in skills_list: score += 40
    if "html" in skills_list: score += 20
    if "sql" in skills_list: score += 20
    return min(score, 100)

def improve_resume(skills_list, interest):
    return "👉 Improve by adding projects, skills, and achievements."

def get_opportunities(skills, interest):
    skills_list = [s.strip().lower() for s in skills.split(",") if s.strip()]

    result = "### 🔹 Internships\n"

    if "python" in skills_list:
        result += "- [Google AI Intern](https://careers.google.com)\n"
    else:
        result += "- [TCS Intern](https://tcs.com)\n"

    result += "\n### 🔹 Hackathons\n- Smart India Hackathon\n"
    return result, skills_list

def chatbot_response(user_input):
    skills = st.session_state.last_skills
    interest = st.session_state.last_interest

    if "ai" in user_input.lower():
        return f"Focus on ML & projects. Your skills: {skills}"
    return f"Improve based on your interest: {interest}"

def fetch_internships():
    try:
        r = requests.get("https://internshala.com/internships/", timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        return [j.text.strip() for j in soup.select(".heading_4_5.profile")][:5]
    except:
        return []

# ---------------- MAIN ACTION ----------------
if st.sidebar.button("🚀 Find Opportunities"):

    if uploaded_file:
        extracted = extract_skills_from_resume(uploaded_file)
        skills += "," + ",".join(extracted)

    result, skills_list = get_opportunities(skills, interest)

    st.session_state.last_skills = skills_list
    st.session_state.last_interest = interest

    col1, col2 = st.columns(2)

    # LEFT PANEL
    with col1:
        st.subheader("📊 Profile Analysis")

        score = calculate_score(skills_list)
        st.metric("Score", f"{score}/100")

        if score < 70:
            st.warning("Needs Improvement")
            st.info(improve_resume(skills_list, interest))
        else:
            st.success("Strong Profile")

        st.subheader("📊 Skill Chart")
        if skills_list:
            fig, ax = plt.subplots()
            ax.bar(skills_list, [1]*len(skills_list))
            st.pyplot(fig)

    # RIGHT PANEL
    with col2:
        st.subheader("🌟 Opportunities")
        st.markdown(result)

        st.subheader("🌐 Live Internships")
        for job in fetch_internships():
            st.write(f"- {job}")

    # DEADLINES
    st.subheader("📅 Deadlines")
    st.write("Smart India Hackathon → 15 days left")

# ---------------- CHATBOT UI ----------------
st.markdown("---")
st.subheader("💬 AI Career Assistant")

user_input = st.text_input("Ask something...")

if st.button("Send") and user_input:
    reply = chatbot_response(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("AI", reply))

# Display chat nicely
for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f'<div class="chat-user">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-ai">{msg}</div>', unsafe_allow_html=True)