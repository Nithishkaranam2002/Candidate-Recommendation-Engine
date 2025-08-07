import streamlit as st
import json, os, re, io, csv
from dotenv import load_dotenv

load_dotenv()

# ---- 0. Auth Utilities ----
USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def signup(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = password
    save_users(users)
    return True, "User created successfully!"

def login(username, password):
    users = load_users()
    return username in users and users[username] == password

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# ---- 1. App Config ----
st.set_page_config(page_title="Candidate Recommendation Engine", layout="wide")

# ---- 2. Login/Signup UI ----
def show_login_signup():
    st.title("🔒 Candidate Recommendation Engine - Login")
    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In", key="login_btn"):
            if login(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success(f"Login successful! Welcome, {username}.")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        new_user = st.text_input("Create Username", key="signup_user")
        new_pass = st.text_input("Create Password", type="password", key="signup_pass")
        if st.button("Sign Up", key="signup_btn"):
            ok, msg = signup(new_user, new_pass)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

if not st.session_state["authenticated"]:
    show_login_signup()
    st.stop()
else:
    st.sidebar.markdown(f"Logged in as: <span style='color:#32CD32'><b>{st.session_state['username']}</b></span>", unsafe_allow_html=True)
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = ""
        st.rerun()

# ---- 3. App Core ----

from services import embedding_service, similarity_service, ai_summary_service, parser_service
from utils.file_utils import get_file_extension
import openai

def extract_key_points(text):
    api_key = os.environ.get("OPENAI_API_KEY")
    try:
        client = openai.OpenAI(api_key=api_key)
        prompt = (
            "From the following job description, extract and list only the most important keywords, "
            "skills, or requirements as bullet points (no explanations, just the words or phrases):\n"
            f"{text}"
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}],
            max_tokens=150,
            temperature=0.3
        )
        points = response.choices[0].message.content.strip()
        return points
    except Exception as e:
        keywords = re.findall(r"\b([A-Za-z]{3,})\b", text)
        keywords = list(set([k.lower() for k in keywords if k.lower() not in ['the','and','for','with','this','will','you','our','are','all']]))
        return "\n".join(f"- {kw.title()}" for kw in keywords[:8])

def extract_email(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else ""

def extract_phone(text):
    match = re.search(r"(\+?\d[\d\-\(\) ]{7,}\d)", text)
    return match.group(0) if match else ""

st.markdown("<h1>🧑‍💼 Candidate Recommendation Engine</h1>", unsafe_allow_html=True)

# -------- LEFT SIDEBAR: KEY JOB POINTS --------
if "job_desc" not in st.session_state:
    st.session_state["job_desc"] = ""
if "job_points" not in st.session_state:
    st.session_state["job_points"] = ""

with st.sidebar:
    st.markdown("#### <span style='color:#FFD700'>🔑 Key Job Points</span>", unsafe_allow_html=True)
    if st.session_state["job_points"]:
        st.markdown(st.session_state["job_points"], unsafe_allow_html=True)

# --------- STEP 1: JOB DESCRIPTION -------------
st.markdown("## Step 1: <span style='color:#3797EC'>Enter Job Description</span>", unsafe_allow_html=True)
job_desc = st.text_area("Paste the job description here", value=st.session_state["job_desc"], height=180)
if job_desc and (job_desc != st.session_state["job_desc"]):
    st.session_state["job_desc"] = job_desc
    keypoints = extract_key_points(job_desc)
    st.session_state["job_points"] = keypoints

# --------- STEP 2: UPLOAD RESUMES -------------
st.markdown("## Step 2: Upload Candidate Resumes (PDF, DOCX, TXT)  <a href='#'>&#x1F517;</a>", unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "Upload one or more resume files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    key="file_uploader"
)

class Candidate:
    def __init__(self, name, resume_text):
        self.name = name
        self.resume_text = resume_text
        self.email = extract_email(resume_text)
        self.phone = extract_phone(resume_text)
        self.embedding = None
        self.score = None
        self.summary = None

candidates = []
if uploaded_files:
    for file in uploaded_files:
        ext = get_file_extension(file.name)
        if ext == ".pdf":
            text = parser_service.parse_pdf(file)
        elif ext == ".docx":
            text = parser_service.parse_docx(file)
        elif ext == ".txt":
            text = parser_service.parse_txt(file)
        else:
            text = ""
        if text:
            name = file.name.split(".")[0]
            candidate = Candidate(name=name, resume_text=text)
            candidates.append(candidate)
        else:
            st.warning(f"Could not parse file: {file.name}")

if "results" not in st.session_state:
    st.session_state["results"] = []
if "selected_candidates" not in st.session_state:
    st.session_state["selected_candidates"] = []
if "results_page" not in st.session_state:
    st.session_state["results_page"] = 1

def color_score(score):
    color = "#17C964" if score >= 0.6 else "#FF5252" if score < 0.45 else "#FFB800"
    return f"<span style='color:{color}; font-weight:bold;'>{score:.3f}</span>"

PAGE_SIZE = 3

def show_results_page(results, page, selected_candidates):
    total_pages = (len(results) - 1) // PAGE_SIZE + 1
    start = (page-1) * PAGE_SIZE
    end = min(page * PAGE_SIZE, len(results))
    for i, c in enumerate(results[start:end], start=start+1):
        st.markdown(f"### {i}. {c.name}")
        st.markdown(f"Similarity Score: {color_score(c.score)}", unsafe_allow_html=True)
        st.markdown(f"**Email:** `{c.email or 'Not Found'}`   **Phone:** `{c.phone or 'Not Found'}`")
        st.markdown(f"**AI Summary:** {c.summary}")
        checked = st.checkbox(
            "Select this candidate",
            key=f"select_{i}_{c.name}",
            value=(c in selected_candidates)
        )
        if checked and c not in selected_candidates:
            selected_candidates.append(c)
        elif not checked and c in selected_candidates:
            selected_candidates.remove(c)
        st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if page > 1:
            if st.button("⬅ Previous", key=f"prev_{page}"):
                st.session_state["results_page"] = page-1
                st.rerun()
    with col3:
        if page < total_pages:
            if st.button("Next ➡", key=f"next_{page}"):
                st.session_state["results_page"] = page+1
                st.rerun()
    st.write(f"Results Page {page} of {total_pages}")

if st.button("🔍 Recommend Top Candidates", key="recommend_btn"):
    if not job_desc or not candidates:
        st.warning("Please provide both a job description and at least one resume.")
    else:
        job_embedding = embedding_service.get_embedding(job_desc)
        for c in candidates:
            c.embedding = embedding_service.get_embedding(c.resume_text)
            c.score = similarity_service.cosine_similarity(job_embedding, c.embedding)
            try:
                c.summary = ai_summary_service.generate_fit_summary(c.resume_text, job_desc)
            except Exception as e:
                c.summary = f"AI Summary could not be generated. ({e})"
        candidates.sort(key=lambda x: x.score, reverse=True)
        st.session_state["results"] = candidates
        st.session_state["results_page"] = 1
        # Auto-select top 5 candidates
        st.session_state["selected_candidates"] = candidates[:5]

if st.session_state["results"]:
    st.markdown("## Step 3: Results & AI-Powered Summaries <a id='step-3-results-ai-powered-summaries'></a>", unsafe_allow_html=True)
    show_results_page(st.session_state["results"], st.session_state["results_page"], st.session_state["selected_candidates"])

if st.session_state["selected_candidates"]:
    st.markdown("### Download Selected Results:")
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["Name", "Email", "Phone", "Similarity", "Summary"])
    for c in st.session_state["selected_candidates"]:
        writer.writerow([c.name, c.email, c.phone, f"{c.score:.3f}", c.summary])
    st.download_button(
        label="Download as CSV",
        data=csv_buffer.getvalue().encode('utf-8'),
        file_name="selected_candidates.csv",
        mime="text/csv"
    )
    import pandas as pd
    df = pd.DataFrame([{
        "Name": c.name,
        "Email": c.email,
        "Phone": c.phone,
        "Similarity": f"{c.score:.3f}",
        "Summary": c.summary[:80]+"..." if len(c.summary) > 80 else c.summary
    } for c in st.session_state["selected_candidates"]])
    st.dataframe(df, use_container_width=True)

st.caption("Need help? Contact nithishkaranam15@gmail.com | © 2025 Candidate Recommendation Engine")
