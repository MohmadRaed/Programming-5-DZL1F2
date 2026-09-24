from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

NOTIFY_URL = "http://localhost:8003/broadcast"

# the only place tickets are stored
tickets = []
next_id = 1


@app.get("/tickets")
def list_tickets():
    return tickets


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    for t in tickets:
        if t["id"] == ticket_id:
            return t
    return {"error": "not found"}


@app.post("/tickets")
def create_ticket(name: str, title: str):
    global next_id
    ticket = {"id": next_id, "name": name, "title": title, "status": "open", "staff": None}
    tickets.append(ticket)
    next_id += 1
    httpx.post(NOTIFY_URL, json={"event": "ticket_created", "ticket": ticket})
    return ticket


@app.patch("/tickets/{ticket_id}")
def update_ticket(ticket_id: int, status: str = None, staff: str = None):
    for t in tickets:
        if t["id"] == ticket_id:
            if status:
                t["status"] = status
            if staff:
                t["staff"] = staff
            httpx.post(NOTIFY_URL, json={"event": "ticket_updated", "ticket": t})
            return t
    return {"error": "not found"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
