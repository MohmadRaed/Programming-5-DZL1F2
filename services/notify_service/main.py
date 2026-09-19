from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# the one place that holds live WebSocket connections
connections = []


@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # clients don't send anything, just keeps the socket open
    except WebSocketDisconnect:
        connections.remove(websocket)


@app.post("/broadcast")
async def broadcast(event: dict):
    dead = []
    for ws in connections:
        try:
            await ws.send_json(event)
        except Exception:
            dead.append(ws)
    for ws in dead:
        connections.remove(ws)
    return {"sent_to": len(connections)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
