from fastapi import FastAPI
from pydantic import BaseModel
from HiveMindV3 import graph

app=FastAPI()

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