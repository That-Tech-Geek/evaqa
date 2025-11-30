import json
import requests

def push_to_decile():
    with open("One_Page_Truth.pdf", "rb") as f:
        pdf_data = f.read()

    payload = {
        "startup_name": "ReguBot",
        "status": "Deep Diligence",
        "memo": pdf_data.hex()
    }
    # Placeholder URL; replace with actual Decile Hub API
    response = requests.post("https://decilehub.example.com/api/upload", json=payload)
    print("Push response:", response.status_code)

if __name__ == "__main__":
    push_to_decile()
