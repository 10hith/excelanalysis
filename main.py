from fastapi import FastAPI
import uvicorn

app = FastAPI()

# 11.15.93.81

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="11.15.93.81", port=8000, reload=True)