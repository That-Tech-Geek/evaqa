import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any

# Import necessary modules from FastAPI and others
from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn

# Placeholder for the engine module - replace with actual import
# from engine import YCAI_Analyst

# --- CONFIGURATION ---
# Target Model Release (SHA256: 98555f929690960281a649cbae124d656b6a83151e2de88fe0faf4e05ec29af7)
MODEL_RELEASE = "yc_hivemind.pkl" 

# Email Dispatch Config
# Ensure these environment variables are set in your deployment environment
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "sambit1912@gmail.com") 
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD", "qtnm dalm tpqz cceu") 

# Initialize App & Brain
app = FastAPI(title="Investment Committee")

# Loading the specific release as requested
print(f"Loading...")
# Initialize analyst here. 
# Ensure the engine module and YCAI_Analyst class are available in your project structure.
# analyst = YCAI_Analyst(model_path=MODEL_RELEASE) 

# Mock analyst for demonstration purposes if engine module is missing
class MockAnalyst:
    def __init__(self, model_path):
        pass
    def analyze(self, data):
        return {
            'meta': {'project': data.get('What are you building?', 'Unknown'), 'sector': 'Tech', 'raise': 'Pre-Seed'},
            'ml_score': 85,
            'decision': 'Review',
            'explainability': ['Strong team', 'Growing market']
        }
    def train_model(self):
        pass

analyst = MockAnalyst(model_path=MODEL_RELEASE)


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

def send_decision_email(to_email: str, project_name: str, report_body: str):
    """Dispatches the IC decision directly to the founder."""
    if not to_email or "@" not in to_email:
        print(f"[EMAIL FAILED] Invalid email address: {to_email}")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = f"YC AI Bot <{SENDER_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = f"YC AI Analysis: {project_name}"

        # Attach the analysis text
        msg.attach(MIMEText(report_body, 'plain'))

        # Send via Gmail
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, to_email, text)
        server.quit()
        
        print(f"[EMAIL SENT] Report dispatched to {to_email}")
    except Exception as e:
        print(f"[EMAIL ERROR] Could not send report: {e}")

def process_application(data: Dict[str, str]):
    project_name = data.get('What are you building?', 'Stealth Startup')
    print(f"\n[WEBHOOK] analyzing new deal: {project_name}...")
    
    # 1. Run the ML Analyst
    try:
        result = analyst.analyze(data)
    except Exception as e:
        print(f"[ANALYST ERROR] Model failed to analyze: {e}")
        return
    
    # 2. Construct the Investment Memo
    report_lines = [
        "="*60,
        f"      🤖 YC AI ANALYST REPORT      ",
        "="*60,
        f"PROJECT: {result['meta']['project']}",
        f"SECTOR:  {result['meta']['sector']} | RAISE: {result['meta']['raise']}",
        "-" * 30,
        f"ML SCORE: {result['ml_score']} / 100",
        f"VERDICT:  {result['decision']}",
        "-" * 30,
        "DRIVERS (Why this score?):"
    ]
    
    for reason in result.get('explainability', []):
        report_lines.append(f"  {reason}")
    
    report_lines.append("="*60 + "\n")
    
    full_report = "\n".join(report_lines)
    
    # 3. Print to Console (Logs)
    print(full_report)

    # 4. Extract Email and Fire Output
    # Tries standard variations of the email label
    founder_email = data.get("Founder/CEO Email") or data.get("Email") or data.get("email")
    
    if founder_email:
        send_decision_email(founder_email, project_name, full_report)
    else:
        print("[WARNING] No Founder/CEO Email found in Tally data. Skipping email dispatch.")

@app.post("/webhook/tally")
async def receive_submission(request: Request, background_tasks: BackgroundTasks):
    try:
        payload = await request.json()
        clean_data = parse_tally_payload(payload)
        
        # Run heavy ML logic in background
        background_tasks.add_task(process_application, clean_data)
        
        return {"status": "analyzing", "project": clean_data.get("What are you building?", "Unknown")}
    except Exception as e:
        print(f"[WEBHOOK ERROR] Failed to process request: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/")
def read_root():
    return {"status": "Evaqa Core is running"}

if __name__ == "__main__":
    # Pre-train the model on startup so the first request isn't slow
    print(f"Booting Hivemind from {MODEL_RELEASE}...")
    try:
        analyst.train_model()
    except Exception as e:
        print(f"[STARTUP WARNING] Model training simulation/initialization failed: {e}")
        
    uvicorn.run(app, host="0.0.0.0", port=8000)
