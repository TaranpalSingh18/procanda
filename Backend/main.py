import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from Agent.confidence import run_evaluator


class DetailRequest(BaseModel):
    skill: str = Field(min_length=1)
    question_type: str = Field(min_length=1)
    candidate_answer: str = Field(min_length=1)


class DetailResponse(BaseModel):
    skill: str
    question_type: str
    candidate_answer: str
    score: int
    reasoning: str
    confidence: float


app = FastAPI()

@app.get('/')
async def get_health():
    return {"message":"healthy"}

@app.post('/details')
async def get_details(state: DetailRequest) -> DetailResponse:
    try:
        result = await asyncio.to_thread(
            run_evaluator,
            state.skill,
            state.question_type,
            state.candidate_answer,
        )
        return DetailResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Evaluation failed") from exc


