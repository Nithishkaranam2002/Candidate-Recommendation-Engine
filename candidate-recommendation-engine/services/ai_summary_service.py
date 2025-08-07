import openai

def generate_fit_summary(resume_text, job_description):
    prompt = (
        f"Given this resume:\n{resume_text}\n\n"
        f"And this job description:\n{job_description}\n\n"
        "Write a brief summary explaining why this candidate is a good fit for this job."
    )
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant for recruiting."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.7
    )
    summary = response.choices[0].message.content
    return summary
