import os
import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks
from typing import Dict, Any
from engine import YCAI_Analyst

# Initialize the App and the ML Brain
app = FastAPI(title="YC AI Investment Committee")
analyst = YCAI_Analyst()

def parse_tally_payload(payload: Dict[str, Any]) -> Dict[str, str]:
    """Flattens Tally nested JSON."""
    raw_fields = payload.get("data", {}).get("fields", [])
    flat_data = {}
    for field in raw_fields:
        label = field.get("label")
        value = field.get("value")
        if isinstance(value, list): value = ", ".join(str(v) for v in value)
        elif value is None: value = ""
        if label: flat_data[label] = str(value)
    
    # Pass raw payload for debugging if needed
    if 'socials_dump' not in flat_data:
        flat_data['socials_dump'] = str(payload)
        
    return flat_data

def process_application(data: Dict[str, str]):
    print(f"\n[WEBHOOK] analyzing new deal: {data.get('What are you building?', 'Unknown')}...")
    
    # 1. Run the ML Analyst
    # This will trigger training (3-5s) on the first run only
    result = analyst.analyze(data)
    
    # 2. Print the Investment Memo
    print("\n" + "="*60)
    print(f"      🤖 YC AI ANALYST REPORT      ")
    print("="*60)
    print(f"PROJECT: {result['meta']['project']}")
    print(f"SECTOR:  {result['meta']['sector']} | RAISE: {result['meta']['raise']}")
    print("-" * 30)
    print(f"ML SCORE: {result['ml_score']} / 100")
    print(f"VERDICT:  {result['decision']}")
    print("-" * 30)
    print("DRIVERS (Why this score?):")
    for reason in result['explainability']:
        print(f"  {reason}")
    print("="*60 + "\n")

@app.post("/webhook/tally")
async def receive_submission(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    clean_data = parse_tally_payload(payload)
    
    # Run heavy ML logic in background
    background_tasks.add_task(process_application, clean_data)
    
    return {"status": "analyzing", "project": clean_data.get("What are you building?", "Unknown")}

if __name__ == "__main__":
    # Pre-train the model on startup so the first request isn't slow
    print("Pre-training the brain...")
    analyst.train_model()
    uvicorn.run(app, host="0.0.0.0", port=8000)
