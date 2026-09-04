from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Swedish News ETL API"}
