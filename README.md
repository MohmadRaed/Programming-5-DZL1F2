# Campus Help Desk — Distributed Back-End Project

## 1. The idea

A tiny help-desk ticket system: a **student** submits a ticket describing a problem,
**staff** picks it up and changes its status, and everyone watching (student and
staff, on the CLI or the web page) sees the status change **live**, the instant it
happens — no refresh needed. It's simple because there is exactly one piece of
data (a ticket) and one thing that changes about it (its status), which is enough
to justify 5 microservices and a real-time push without any extra complexity.

## 2. Architecture

```
                 ┌───────────────┐
                 │  auth-service │  (login / demo users)
                 │   port 8001   │
                 └───────────────┘

┌────────────┐   HTTP    ┌────────────────┐   HTTP POST    ┌─────────────────┐
│ staff-svc  │ ────────▶ │  ticket-service │ ─────────────▶ │  notify-service  │
│ port 8004  │  PATCH    │   port 8002     │  /broadcast    │   port 8003      │
└────────────┘           └────────────────┘                └─────────────────┘
                                  ▲                                   │
                                  │ GET /tickets                      │ WebSocket
                          ┌───────┴───────┐                           ▼
                          │ stats-service │                  ┌──────────────────┐
                          │  port 8005    │                  │  CLI client       │
                          └───────────────┘                  │  Web client       │
                                                              └──────────────────┘
```

Students and staff talk to `ticket-service`, `staff-service`, `stats-service` and
`auth-service` directly over plain HTTP from the clients. `notify-service` is the
only service that holds WebSocket connections; every other service just does a
normal HTTP POST to it when something happens, and it pushes that event out to
every connected client.

### Services, ports, endpoints

| Service          | Port | Endpoints                                   | Talks to |
|-------------------|------|----------------------------------------------|----------|
| auth-service      | 8001 | `GET /users`, `POST /login`                   | —        |
| ticket-service    | 8002 | `GET /tickets`, `POST /tickets`, `PATCH /tickets/{id}` | notify-service |
| notify-service    | 8003 | `WS /ws`, `POST /broadcast`                   | —        |
| staff-service     | 8004 | `GET /staff`, `POST /assign`                  | ticket-service |
| stats-service     | 8005 | `GET /stats`                                   | ticket-service |

### Clients

- **CLI client** (`clients/cli_client/cli.py`): menu-driven, talks to the services
  over HTTP with `httpx`, and listens for live events over WebSocket in a
  background thread.
- **Web client** (`clients/web_client/index.html`): one plain HTML file, vanilla
  JS, `fetch()` for HTTP calls and the browser's built-in `WebSocket`.

No database: everything lives in a Python list/dict inside `ticket-service`
(and small hardcoded lists in `auth-service`/`staff-service`). No Docker:
every service is a single `main.py` you run directly with `python3`.

## 3. Install & run

From the project root, in one terminal:

```bash
pip install -r requirements.txt
```

### Run every service

Either use the helper script (all 5 in one terminal, backgrounded):

```bash
./run_all.sh
```

Or, for the demo, open **5 separate terminals** so you can show each service
starting and point at its logs:

```bash
python3 services/auth_service/main.py
python3 services/ticket_service/main.py
python3 services/notify_service/main.py
python3 services/staff_service/main.py
python3 services/stats_service/main.py
```

### Run the web client

The page must be served from inside its own folder (opening the HTML file
directly also works for the demo, but serving it avoids any browser file://
quirks):

```bash
cd clients/web_client
python3 -m http.server 8080
```

Then open `http://localhost:8080` in a browser.

### Run the CLI client

In another terminal:

```bash
python3 clients/cli_client/cli.py
```

## 4. Demo script (4 steps)

1. Start all 5 services (show the 5 terminals / `run_all.sh`), then open the
   web client in a browser and log in as `alice` (student) with one click.
2. In the CLI client, log in as `carol` (staff) — choice `3` in the login menu.
3. On the web page, submit a ticket as alice. Immediately point at the CLI:
   it prints a `[LIVE] ticket_created` event with no manual refresh.
4. In the CLI, use option 4 to assign the ticket to `carol`, or option 3 to
   change its status. Switch back to the browser: the ticket list and the
   "Live updates" log update instantly, then show `GET /stats` (CLI option 5
   or `curl localhost:8005/stats`) to show the aggregated counts.

## 5. Defense cheat-sheet

**Why microservices instead of one app?**
Each service owns one small responsibility (auth, tickets, notifications,
staff, stats) and they only know each other's HTTP address — nothing is
shared in memory or imported between them. That's the whole point to defend:
independent, replaceable, single-purpose processes.

**How do the services talk to each other?**
Plain HTTP with `httpx`: `staff-service` calls `PATCH /tickets/{id}` on
`ticket-service` to assign a ticket; `stats-service` calls `GET /tickets` on
`ticket-service` to compute counts; `ticket-service` calls `POST /broadcast`
on `notify-service` whenever a ticket is created or updated.

**Where is the real-time part?**
`notify-service` is the only service holding WebSocket connections
(`/ws`). Every other service never talks WebSocket — it just does a normal
HTTP POST to `notify-service`'s `/broadcast`, which then pushes that JSON
event to every connected client (CLI and web) over their open WebSocket.
This keeps "real-time" isolated to one simple service instead of spreading
WebSocket code everywhere.

**Why no database?**
The scope is one in-memory list of tickets. Adding a database would mean
adding schema, migrations and persistence code that doesn't teach anything
new about *microservices* or *WebSockets*, which are the two things being
graded — it would just be more surface area to defend for no benefit. Data
resets when `ticket-service` restarts, which is an accepted trade-off for a
demo.

**Known simplifications (say these upfront in the defense):**
- Login is a name pick with no password/token — deliberately trivial so the
  demo is fast; there is no auth/authorization layer.
- Data is in-memory, so it's lost on restart and isn't shared across
  multiple instances of the same service.
- No retries/circuit breakers on the HTTP calls between services — if
  `notify-service` is down, `ticket-service`'s broadcast call will just
  raise an error (acceptable for the scope of the course).
- CORS is wide open (`allow_origins=["*"]`) since this is a local demo, not
  a deployed system.

## What was tested vs. not

Tested end-to-end during development: full HTTP flow (login, create ticket,
update ticket, assign, stats), WebSocket broadcast on create/update, the CLI
client end-to-end, and the web client end-to-end (login, create, live update
log, ticket list refresh) in a browser.

Not tested: behavior under multiple simultaneous CLI+web clients at once
beyond a basic check, and behavior when a service is killed mid-request
(the simplifications above cover why that's out of scope).
