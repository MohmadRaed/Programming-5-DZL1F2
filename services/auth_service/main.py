from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

STAFF = {
    "carol": "carol123",
    "dave": "dave123",
}


@app.post("/login")
def login(username: str, password: str):
    if STAFF.get(username) == password:
        return {"username": username, "role": "staff"}
    return {"error": "invalid credentials"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
