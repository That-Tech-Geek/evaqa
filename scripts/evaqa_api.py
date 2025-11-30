from fastapi import FastAPI
from pydantic import BaseModel
from council_agents import run_council
from voting_logic import resolve_votes
from memo_generator.generate_memo import create_pdf

app = FastAPI()

class FounderInput(BaseModel):
    startup: str
    url: str
    founder: str

@app.post("/enrich")
def enrich(data: FounderInput):
    # mock enrichment
    return {
        "tam": 1400000000,
        "growth": 0.42,
        "team": "Strong technical founder",
        "github_commits": 188,
        "market_tailwind": "LLM infrastructure demand"
    }

@app.post("/council")
def council(data: dict):
    return run_council(data)

@app.post("/vote")
def vote(data: dict):
    return resolve_votes(data)

@app.post("/memo")
def memo(result: dict):
    path = create_pdf(result)
    return {"file_path": path}
