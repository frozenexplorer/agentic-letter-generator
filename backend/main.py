from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Offer Letter Generator API is running."}