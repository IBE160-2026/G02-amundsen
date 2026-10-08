from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Career Transition Assistant backend is running"}