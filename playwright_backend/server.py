"""
FastAPI server to expose Playwright automation as a REST API.
This allows testing via Postman or other HTTP clients.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
from .automator import run_automation

app = FastAPI(
    title="Match.com Automation API",
    description="API to trigger Playwright-based registration automation",
    version="1.0.0"
)

class RegistrationRequest(BaseModel):
    email: str
    password: str
    name: str
    photo_path: Optional[str] = "automation-extension/assets/img.png"
    region: Optional[str] = "us"
    headless: Optional[bool] = False

class RegistrationResponse(BaseModel):
    success: bool
    message: str

@app.post("/register", response_model=RegistrationResponse)
async def register(request: RegistrationRequest):
    """
    Trigger the Match.com registration automation.
    """
    try:
        success = await run_automation(
            email=request.email,
            password=request.password,
            name=request.name,
            photo_path=request.photo_path,
            region=request.region,
            headless=request.headless
        )
        
        if success:
            return RegistrationResponse(
                success=True, 
                message="Registration automation completed successfully."
            )
        else:
            return RegistrationResponse(
                success=False, 
                message="Registration automation finished but might have encountered issues (check logs)."
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Automation error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "online", "engine": "playwright"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
