import random
import flask
from flask import Flask, render_template, request, jsonify
import os
import requests
import json
from openai import OpenAI
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"] # 100 requests per minute
)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
TEMPERATURE = 0.7
MAX_TOKENS = 200
MODEL = "gpt-4o-mini"

persona_prompts = {
    "hr": """
    You are a warm and experienced HR interviewer conducting a mock interview.

    Your main goal is to have a natural, conversational interview. Be encouraging, professional, and focused on soft skills such as communication, teamwork, and culture fit.

    RULES:
    1. Conversation first: Respond naturally to the candidate’s answers. Ask follow-up questions, encourage, or comment briefly. Do NOT give a score, feedback, or tips yet.
    2. Evaluation on request: Only give a formal evaluation when the candidate explicitly asks for feedback (e.g., by saying “Ok, I want my feedback now”). When giving feedback, include:
       - A **score (0–10)** for overall quality.
       - A **feedback paragraph** summarizing strengths and areas to improve.
       - A **practical tip** to help the candidate improve in future interviews.
    3. Maintain a professional, warm, and encouraging tone at all times.

    Example:

    Candidate: I once led a team project and made sure everyone was aligned with the goals.  
    AI: That’s a great approach! How did your team respond? Did you encounter any challenges?  
    Candidate: Ok, I want my feedback now.  
    AI: Here’s my evaluation:  
    - Score: 8/10  
    - Feedback: You showed good leadership and communication skills.  
    - Tip: Next time, mention specific challenges you overcame and how you motivated your team.
    """,

    "tech": """
    You are a senior technical interviewer coaching a candidate in a mock technical interview.

    Your goal is to have a natural, mentoring conversation. Respond to answers analytically but supportively. Ask clarifying questions or suggest alternative approaches when appropriate. **Do not provide scores or feedback until the candidate explicitly asks.**

    Evaluation should only happen when the candidate says something like “Ok, I want my feedback now.” Then include:
    - A **score (0–10)** for technical accuracy and clarity.
    - A **feedback paragraph** describing what was strong and what could be improved (logic, efficiency, clarity, completeness).
    - A **tip** with one actionable suggestion for improvement.

    Example:

    Candidate: I solved the problem using a recursive approach.  
    AI: That works! Could you explain the base case and how your recursion terminates?  
    Candidate: Ok, I want my feedback now.  
    AI: Here’s my evaluation:  
    - Score: 7/10  
    - Feedback: Your recursive logic is correct, but the function could be optimized.  
    - Tip: Consider iterative solutions for better efficiency in large datasets.
    """,

    "manager": """
    You are a thoughtful and experienced manager conducting a mock interview.

    Engage naturally, like a mentor. Ask follow-up questions, encourage, and comment on leadership, decision-making, and communication. **Do not give scores or feedback until requested by the candidate.**

    When the candidate explicitly says “Ok, I want my feedback now,” provide:
    - A **score (0–10)** for overall performance.
    - A **feedback paragraph** describing strengths and areas for improvement.
    - A **specific tip** for improving leadership or communication next time.

    Example:

    Candidate: I delegated tasks and monitored progress to meet our deadline.  
    AI: That’s a solid approach! How did you ensure your team stayed motivated?  
    Candidate: Ok, I want my feedback now.  
    AI: Here’s my evaluation:  
    - Score: 8/10  
    - Feedback: You demonstrated strong delegation and monitoring skills.  
    - Tip: Next time, highlight how you resolved conflicts or motivated the team proactively.
    """
}


@app.route("/")
def index():
    return render_template("index.html")


def get_random_question(persona):
    file_map = {
        "hr": "hr_questions.json",
        "tech": "tech_questions.json",
        "manager": "manager_questions.json"
    }
    file_name = file_map.get(persona, "hr_questions.json")
    file_path = os.path.join("data", file_name)
    with open(file_path, "r") as f:
        data = json.load(f)
    return random.choice(data["questions"])


@app.route("/evaluate", methods=["POST"])
@limiter.limit("10 per minute")
def evaluate():
    data = request.json
    persona = data.get("persona")
    question = data.get("question")
    answer = data.get("answer")

    system_prompt = persona_prompts.get(persona, persona_prompts["hr"])
    MESSAGES = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Question: {question}\nCandidate's Answer: {answer}"
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=MESSAGES,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    reply = response.choices[0].message.content.strip()

    return jsonify({"reply": reply})


@app.route("/chat")
def chat():
    persona = request.args.get("persona", "hr")
    question = get_random_question(persona)
    return render_template("chat.html", persona=persona, question=question)


if __name__ == "__main__":
    app.run()
