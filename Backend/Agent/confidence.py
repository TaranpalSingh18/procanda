from langgraph.graph import START, END, StateGraph
from typing import TypedDict
from langchain_groq import ChatGroq
import os
import json
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

class AgentState(TypedDict):
    skill: str
    question_type: str
    candidate_answer: str
    score: int
    reasoning: str
    confidence: float

def validate_answer(state: AgentState):

    ans = state["candidate_answer"].strip()
    if not ans:
        return {
            **state,
            "score": 0,
            "reasoning": "Answer is too short",
            "confidence": 1.0
        }
    
    if len(ans.split()) < 5:
        return {
            **state,
            "score": 1,
            "reasoning": "Answer is too short to be evalutated",
            "confidence": 0.8
        }
    return state


def score_with_llm(state: AgentState):
    prompt = f"""
    You are a strict interview evaluator.

    Your task is to evaluate a candidate's answer for a specific skill.

    Skill: {state['skill']}
    Question Type: {state['question_type']}
    Candidate Answer: {state['candidate_answer']}

    ----------------------
    SCORING RUBRIC (STRICT)
    ----------------------

    Score 0:
    - Empty, meaningless, or completely irrelevant answer

    Score 1-2:
    - Mostly off-topic OR extremely vague
    - No demonstration of the required skill

    Score 3-4:
    - Very basic understanding
    - Lacks clarity, structure, or relevance
    - No concrete examples

    Score 5-6:
    - Some understanding of the skill
    - Partially relevant answer
    - Limited explanation or weak example

    Score 7-8:
    - Good understanding of the skill
    - Clear and structured answer
    - Includes at least one relevant example or explanation

    Score 9-10:
    - Excellent demonstration of the skill
    - Strong, specific examples with clear impact/results
    - Highly structured, persuasive, and relevant

    ----------------------
    EVALUATION INSTRUCTIONS
    ----------------------

    - Be strict and objective
    - Do NOT give high scores unless clearly justified
    - Consider:
    - relevance to the skill
    - clarity and structure
    - depth of explanation
    - use of examples
    - real-world applicability

    - If the answer is:
    - empty → score = 0
    - very short (<5 words) → max score = 2
    - off-topic → max score = 2

    ----------------------
    OUTPUT FORMAT (STRICT JSON)
    ----------------------

    Return ONLY valid JSON. No extra text.

    {{
        "score": integer (0-10),
        "reasoning": "2-3 concise sentences explaining why this score was given",
        "confidence": float (0-1)
    }}
    """

    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=groq_api_key, temperature=0.2)

    res = llm.invoke(prompt)

    try:
        data = json.loads(res.content)
        return {
            **state,
            "score": int(data.get("score", 0)),
            "reasoning": data.get("reasoning", ""),
            "confidence": float(data.get("confidence", 0))
        }
    
    except Exception:
        return {
            **state,
            "score": 3,
            "reasoning": "Could process the query",
            "confidence":0.3
       }



builder = StateGraph(AgentState)

builder.add_node("validate", validate_answer)
builder.add_node("score", score_with_llm)
builder.set_entry_point("validate")
builder.add_edge("validate", "score")
builder.add_edge("score", END)

graph = builder.compile()

result = graph.invoke({
    "skill": "Sales Persuasion",
    "question_type": "experience",
    "candidate_answer": "I convinced a hesitant client by understanding their needs and showing ROI."
})

print(result)