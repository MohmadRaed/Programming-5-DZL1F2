# Campus Help Desk

A distributed back-end for the Programming 5 course: 5 small FastAPI
microservices that talk over HTTP, with real-time ticket updates pushed to
clients over WebSockets.

Students report a problem without logging in and watch its status change live.
Staff log in, assign tickets and move them through `open → assigned →
in_progress → done`. Clients: a student web page, a staff web page and a
staff CLI.

## Documentation (in `docs/`)

- [Architecture](docs/architecture.md): services, ports, endpoints, clients and the component diagram
- [Sequence diagrams](docs/sequence-diagram.md): a simple and a detailed version
- [Run it and demo it](docs/run-and-demo.md): install, start commands and the 4-step demo script

## Quick start

```bash
pip install -r requirements.txt
./run_all.sh
cd clients/web_client && python3 -m http.server 8080
```

Open `http://localhost:8080`. Demo staff logins: `carol` / `carol123`,
`dave` / `dave123`.

## Project layout

- `services/`: five microservices, one `main.py` each (ports 8001-8005)
- `clients/`: `web_client` (3 HTML files) and `cli_client` (`cli.py`)
- `docs/`: project description and diagrams (Mermaid)
