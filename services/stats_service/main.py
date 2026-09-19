from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

TICKET_URL = "http://localhost:8002/tickets"


@app.get("/stats")
def stats():
    tickets = httpx.get(TICKET_URL).json()
    counts = {}
    for t in tickets:
        counts[t["status"]] = counts.get(t["status"], 0) + 1
    return {"total": len(tickets), "by_status": counts}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
