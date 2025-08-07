# 🧑‍💼 Candidate Recommendation Engine

**A smart, AI-powered platform to instantly match the best candidates to any job, saving recruiters hours and ensuring the right fit every time.**

## 📲 How to Use (For Recruiters & Clients)

1. **Go to the app ([Live Link](https://share.streamlit.io/yourusername/candidate-recommendation-engine)).**
2. **First time? Click the “Sign Up” tab on the login page.**
    - Enter your desired username and password to register.
3. **Returning user? Use the “Sign In” tab.**
    - Log in with your registered credentials.
4. **Paste the job description** for your open role.
5. **Upload one or more resumes** (PDF, DOCX, or TXT).
6. **Click “Recommend Top Candidates.”**
7. **Review the results:**
    - The best matches are shown at the top, with similarity scores.
    - Read the “AI Summary” for a quick assessment of fit.
    - The top 5 are already pre-selected (you can add/remove any).
8. **Download** your selected candidates as a CSV file for easy sharing.


---

## 🌟 What Does This App Do?

**Imagine:**  
You have dozens—or hundreds—of resumes, and one job description.  
*Which candidates are the best fit?*  
*Why?*  
*How fast can you find them?*

**This app solves all of that, automatically:**
- Upload your job description.
- Upload a batch of candidate resumes.
- Get an instant, ranked list of top candidates, with AI-generated summaries of why they’re the right choice.
- Download your selections in one click!

---

## ⚡️ Key Features

- **Instant Matching:** Upload job description + resumes, get results in seconds.
- **AI-Powered Ranking:** Uses cutting-edge AI (OpenAI embeddings) to deeply understand and match resumes to jobs—beyond just keywords.
- **Top Picks, Auto-Selected:** The top 5 best-fit candidates are automatically highlighted for you.
- **AI Fit Summaries:** For every candidate, see a smart, readable summary of why they fit the job.
- **Flexible Selection:** Add or remove candidates from your selection with one click.
- **CSV Export:** Download the shortlist and share with your team.
- **Simple Login:** Secure access for your demo or team.
- **Modern, Intuitive Interface:** No training needed—just upload and go!

---

## 👀 Live Demo

**Try it here:**  
[https://share.streamlit.io/yourusername/candidate-recommendation-engine](https://share.streamlit.io/yourusername/candidate-recommendation-engine)  
*(Replace with your real link after deployment)*

**Demo Login:**  
- Username: `demo`  
- Password: `demo123`

---

## 📸 Quick Screenshot

| Dashboard with Results | AI-Generated Fit Summary |
|:---------------------:|:-----------------------:|
| ![Screenshot 1](link_to_screenshot1) | ![Screenshot 2](link_to_screenshot2) |

---

## 🚀 How to Use (For Recruiters & Clients)

1. **Go to the app (link above) and log in** with the demo account or sign up for your own.
2. **Paste the job description** for your open role.
3. **Upload one or more resumes** (PDF, DOCX, or TXT).
4. **Click “Recommend Top Candidates”**.
5. **Review the results:**  
   - The best matches are shown at the top, with similarity scores.
   - Read the “AI Summary” for a quick assessment of fit.
   - The top 5 are already pre-selected (you can add/remove any).
6. **Download** your selected candidates as a CSV file for easy sharing.

**It’s that easy!**

---

## 🛠️ For Developers

### 1. **Clone the Repository**
``bash
git clone https://github.com/yourusername/candidate-recommendation-engine.git
cd candidate-recommendation-engine



2. Install Requirements
pip install -r requirements.txt
3. Configure OpenAI Key
Create a file called .env in the project root:
OPENAI_API_KEY=sk-...your-key...
Note: .env is excluded from version control for security.
4. Run the App Locally
streamlit run app.py
Visit http://localhost:8501 in your browser.
📦 Project Structure

.
├── app.py                    # Main Streamlit application
├── requirements.txt          # Dependencies
├── .gitignore
├── README.md
├── config/                   # App settings
├── models/                   # Data structures
├── services/                 # Embedding, similarity, parsing, and summary services
├── utils/                    # Helper functions (file_utils, etc.)
├── data/                     # (Ignored) Sample resumes, embeddings cache
🧠 How It Works (Under the Hood)

Embeddings: The app uses OpenAI's advanced language models to turn both the job description and each resume into high-dimensional vectors (embeddings) that capture meaning, not just keywords.
Similarity Scoring: It then compares the job and resumes using cosine similarity to find the best matches—even if the language is different.
AI Summaries: For every candidate, OpenAI generates a brief, business-friendly explanation of their fit for the job.
UI: Built in Streamlit for speed and simplicity.
🤖 Why This App Stands Out

Goes beyond keyword matching: Understands context, skills, and requirements—even if phrased differently in resumes.
Saves time for recruiters: Top candidates are highlighted instantly.
Transparent: Shows you why each person is a good fit, not just a score.
Extensible: Easily swap in new models or add features.
🔒 Security & Privacy

Your .env and API keys are never tracked in git or uploaded to the cloud.
Uploaded resumes are processed in memory, not stored long-term.
Basic authentication is for demo purposes. For production, use enterprise auth.

Contact & Credits

Developed by Nithish karanam
Email:nithishkaranam15@gmail.com
Feel free to reach out for questions or support!
