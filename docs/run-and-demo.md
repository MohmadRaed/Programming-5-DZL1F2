# Run it and demo it

## Install

```bash
pip install -r requirements.txt
```

## Start the 5 services

```bash
./run_all.sh
```

Or use 5 separate terminals for the demo, so you can point at each one:

```bash
python3 services/auth_service/main.py
python3 services/ticket_service/main.py
python3 services/notify_service/main.py
python3 services/staff_service/main.py
python3 services/stats_service/main.py
```

## Start the web client

Serve it from inside its own folder (do not just double-click the HTML file):

```bash
cd clients/web_client
python3 -m http.server 8080
```

Open `http://localhost:8080` and pick **Student** or **Staff**. Staff logs in
with one click (`carol` / `carol123` or `dave` / `dave123`).

## Start the staff CLI (optional)

```bash
python3 clients/cli_client/cli.py
```

Demo staff logins: `carol` / `carol123` or `dave` / `dave123`.

## Demo script (4 steps)

1. Open the web page, choose **Student**, and submit a ticket (no login). The
   page shows "Your ticket #1" and starts tracking it live.
2. In another tab, choose **Staff** and log in with one click as `carol`. The
   ticket is already there, with no refresh and no polling.
3. As `carol`, click "Assign to me" or change the status dropdown. Switch back
   to the student tab: the progress tracker advances and the "Live updates"
   box changes instantly, because that page opened a WebSocket for just that
   ticket number.
4. Point at the "Stats" panel on the staff page (or choose "View stats" in the
   CLI) to show `stats-service` pulling live counts from `ticket-service`
   over plain HTTP.
