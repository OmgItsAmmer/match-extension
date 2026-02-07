from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from selenium_backend import MatchAutomator
import uuid

app = FastAPI()

class ProfileRequest(BaseModel):
    email: str
    password: str
    name: str

def run_automation_task(email, password, name):
    automator = MatchAutomator()
    try:
        automator.run_registration(email, password, name)
    except Exception as e:
        print(f"Automation failed: {e}")
    finally:
        # Keep open for now or close? 
        # For a real API, we usually close or use a pool.
        automator.close()

@app.post("/automate")
async def start_automation(request: ProfileRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_automation_task, request.email, request.password, request.name)
    return {"status": "started", "email": request.email}

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Match Selenium API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
