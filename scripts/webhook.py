from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx
import os

router = APIRouter()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/evaqa/trigger")

class FounderTrigger(BaseModel):
    startup: str
    url: str
    founder: str
    email: Optional[str] = None
    pitch: Optional[str] = None

@router.post("/webhook/founder")
async def founder_trigger(payload: FounderTrigger, request: Request):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                N8N_WEBHOOK_URL,
                json=payload.dict()
            )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"n8n failed: {response.text}")

        return {
            "status": "queued",
            "message": "Founder accepted. Evaqa pipeline triggered.",
            "startup": payload.startup
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
