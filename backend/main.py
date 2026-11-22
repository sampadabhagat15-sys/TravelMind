
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.agent import agent


# ==========================================
# INITIALIZE FASTAPI
# ==========================================

app = FastAPI(
    title="TravelMind API",
    description="AI-powered travel planning using a ReAct agent",
    version="1.0.0"
)


# ==========================================
# ENABLE CORS FOR REACT FRONTEND
# ==========================================


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://travel-mind-beta.vercel.app",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# ==========================================
# REQUEST SCHEMA
# ==========================================

class TravelRequest(BaseModel):
    message: str = Field(min_length=1)


# ==========================================
# HEALTH CHECK ENDPOINT
# ==========================================

@app.get("/")
def home():
    return {
        "app": "TravelMind",
        "status": "running",
        "message": "TravelMind API is ready!"
    }


# ==========================================
# AI TRAVEL PLANNING ENDPOINT
# ==========================================

@app.post("/plan")
def plan_trip(request: TravelRequest):

    try:
        result = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": request.message
                }
            ]
        })

        final_response = result["messages"][-1].text

        tools_used = []

        for message in result["messages"]:
            for call in getattr(message, "tool_calls", []) or []:
                tools_used.append(call["name"])

        return {
            "success": True,
            "response": final_response,
            "tools_used": tools_used
        }

    except Exception as error:
        print(f"TravelMind API error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Travel planning failed. Please try again."
        ) from error
