from fastapi import FastAPI
from pydantic import BaseModel
from HiveMindV3 import graph
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ResearchRequest(BaseModel):
    query:str

@app.get("/")
def home():
    return{"message":"HiveMind API is running"}

@app.post("/research")
def research(request:ResearchRequest):
    state = {
        "messages":[],
        "query":request.query,
        "research":"",
        "analysis":"",
        "need_critic":False,
        "critique":"",
        "final_answer":"",
        "memory":"",
        "memory_distance":0.0
    }
    result=graph.invoke(state)
    return{"answer":result["final_answer"]}