from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

TICKET_URL = "http://localhost:8002/tickets"

STAFF = ["carol", "dave"]


@app.get("/staff")
def list_staff():
    return STAFF


@app.post("/assign")
def assign(ticket_id: int, staff: str):
    # staff-service doesn't own ticket data, it just asks ticket-service to update it
    r = httpx.patch(f"{TICKET_URL}/{ticket_id}", params={"staff": staff, "status": "assigned"})
    return r.json()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
