import flask
from flask import Flask, render_template, request
import os
import requests
import json
from openai import OpenAI

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")

persona_prompts = {
         "hr": """
You are an experienced HR interviewer coaching a candidate. Evaluate the candidate's answer to the behavioral question. Provide:
- score: a number between 0 and 10
- feedback: concise paragraph explaining strengths and weaknesses
- tip: one practical recommendation for improvement
Output ONLY valid JSON:
{
  "score": ...,
  "feedback": "...",
  "tip": "..."
}
Candidate Answer:
Question: {question}
Answer: {answer}
""",

    "tech": """
You are a technical interviewer coaching a candidate on problem-solving and coding skills. Evaluate the candidate's answer. Provide:
- score: a number between 0 and 10
- feedback: concise paragraph explaining strengths and weaknesses
- tip: one practical recommendation for improvement
Output ONLY valid JSON:
{
  "score": ...,
  "feedback": "...",
  "tip": "..."
}
Candidate Answer:
Question: {question}
Answer: {answer}
""",

    "manager": """
You are a manager-level interviewer coaching a candidate on leadership, decision-making, and impact. Evaluate the candidate's answer. Provide:
- score: a number between 0 and 10
- feedback: concise paragraph explaining strengths and weaknesses
- tip: one practical recommendation for improvement
Output ONLY valid JSON:
{
  "score": ...,
  "feedback": "...",
  "tip": "..."
}
Candidate Answer:
Question: {question}
Answer: {answer}
""" }



@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.json
    persona = data.get("persona")
    question = data.get("question")
    answer = data.get("answer")

    client = OpenAI(api_key=api_key)

    system_prompt = persona_prompts.get(persona, persona_prompts["hr"])
    formatted_prompt = system_prompt.format(question=question,answer=answer)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": formatted_prompt}
        ],
        temperature=0.7,
        max_tokens=250
    )


    reply = response.choices[0].message.content
    print("Assistant:", reply)




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat():
    persona = request.args.get("persona", "hr")
    return render_template("chat.html", persona=persona)


if __name__ == "__main__":
    app.run()
