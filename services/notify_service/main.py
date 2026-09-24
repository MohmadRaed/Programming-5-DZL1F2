from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# the one place that holds live WebSocket connections
# staff connect with ?role=staff and see everything
# students connect with ?ticket=<id> and only see events for that ticket
connections = []


@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket, role: str = None, ticket: int = None):
    await websocket.accept()
    conn = {"ws": websocket, "role": role, "ticket": ticket}
    connections.append(conn)
    try:
        while True:
            await websocket.receive_text()  # clients don't send anything, just keeps the socket open
    except WebSocketDisconnect:
        connections.remove(conn)


@app.post("/broadcast")
async def broadcast(event: dict):
    ticket_id = event["ticket"]["id"]
    dead = []
    for conn in connections:
        if conn["role"] == "staff" or conn["ticket"] == ticket_id:
            try:
                await conn["ws"].send_json(event)
            except Exception:
                dead.append(conn)
    for conn in dead:
        connections.remove(conn)
    return {"sent_to": len(connections)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
