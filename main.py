import os
import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks
from typing import Dict, Any, List
from screener import StartupScreener

# Initialize the App and the Logic Engine
app = FastAPI(title="Investment Committee Webhook")
screener = StartupScreener()

# --- HELPER: MAP TALLY PAYLOAD TO SCREENER INPUT ---
def parse_tally_payload(payload: Dict[str, Any]) -> Dict[str, str]:
    """
    Tally sends data as: {'data': {'fields': [{'label': 'Question?', 'value': 'Answer'}, ...]}}
    We need to flatten this into: {'Question?': 'Answer'}
    """
    raw_fields = payload.get("data", {}).get("fields", [])
    
    # Flatten the list into a dictionary
    flat_data = {}
    for field in raw_fields:
        label = field.get("label")
        value = field.get("value")
        
        # Handle different Tally value types (text, number, multiple choice)
        if isinstance(value, list):
            # For checkboxes, join with commas
            value = ", ".join(str(v) for v in value)
        elif value is None:
            value = ""
        
        if label:
            flat_data[label] = str(value)

    return flat_data

# --- CORE LOGIC ---
def process_application(application_data: Dict[str, str]):
    """
    Runs the screener logic and prints the Memo to console logs.
    In a real deployment, this would email you or post to Slack.
    """
    print(f"\n[WEBHOOK] Processing application for: {application_data.get('What are you building?', 'Unknown Project')}")
    
    # 1. Run the Math
    report = screener.evaluate_application(application_data)
    
    # 2. Get the Memo (Pass API Key from ENV for security)
    # export GEMINI_API_KEY="your_key_here"
    api_key = os.getenv("GEMINI_API_KEY") 
    memo = screener.get_gemini_memo(report, api_key=api_key)
    
    print("\n" + "="*60)
    print(f"      NEW DEAL FLOW: {report['Project']}      ")
    print("="*60)
    print(f"SCORE: {report['Final_Weighted_Score']} ({report['Algorithmic_Decision']})")
    print("-" * 30)
    print(memo)
    print("="*60 + "\n")

# --- ENDPOINT ---
@app.post("/webhook/tally")
async def receive_submission(request: Request, background_tasks: BackgroundTasks):
    """
    Tally hits this URL. We acknowledge immediately (200 OK) 
    and process the heavy logic in the background.
    """
    payload = await request.json()
    
    # Parse generic Tally structure into our specific format
    clean_data = parse_tally_payload(payload)
    
    # Run logic in background so Tally doesn't time out
    background_tasks.add_task(process_application, clean_data)
    
    return {"status": "received", "project": clean_data.get("What are you building?", "Unknown")}

# For local testing
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
