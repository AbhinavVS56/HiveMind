from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return{"message":"HiveMind API is running"}

@app.post("/research")
def research():
    return{"answer":"HiveMind will answer here"}