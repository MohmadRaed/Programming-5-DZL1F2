import json
import threading

import httpx
from websockets.sync.client import connect

AUTH_URL = "http://localhost:8001"
TICKET_URL = "http://localhost:8002/tickets"
STAFF_URL = "http://localhost:8004"
STATS_URL = "http://localhost:8005/stats"
WS_URL = "ws://localhost:8003/ws?role=staff"


def listen_for_events():
    with connect(WS_URL) as ws:
        for message in ws:
            event = json.loads(message)
            print(f"\n[LIVE] {event['event']}: {event['ticket']}\n> ", end="", flush=True)


def login():
    print("Staff login (demo: carol/carol123 or dave/dave123)")
    while True:
        username = input("Username: ")
        password = input("Password: ")
        result = httpx.post(f"{AUTH_URL}/login", params={"username": username, "password": password}).json()
        if "error" not in result:
            return result
        print(result["error"])


def main():
    user = login()
    print(f"Logged in as {user['username']} ({user['role']})")

    threading.Thread(target=listen_for_events, daemon=True).start()

    while True:
        print("\n1. List tickets\n2. Change ticket status\n3. Assign ticket\n4. View stats\n5. Quit")
        choice = input("> ")
        if choice == "1":
            print(httpx.get(TICKET_URL).json())
        elif choice == "2":
            tid = int(input("Ticket id: "))
            status = input("New status (open/assigned/in_progress/done): ")
            httpx.patch(f"{TICKET_URL}/{tid}", params={"status": status})
        elif choice == "3":
            tid = int(input("Ticket id: "))
            staff = input("Staff username: ")
            httpx.post(f"{STAFF_URL}/assign", params={"ticket_id": tid, "staff": staff})
        elif choice == "4":
            print(httpx.get(STATS_URL).json())
        elif choice == "5":
            break


if __name__ == "__main__":
    main()
