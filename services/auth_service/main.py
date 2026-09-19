from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# demo users, no passwords, no tokens - just for the login screen
USERS = [
    {"username": "alice", "role": "student"},
    {"username": "bob", "role": "student"},
    {"username": "carol", "role": "staff"},
    {"username": "dave", "role": "staff"},
]


@app.get("/users")
def list_users():
    return USERS


@app.post("/login")
def login(username: str):
    for u in USERS:
        if u["username"] == username:
            return u
    return {"error": "unknown user"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
