import asyncio
import json
import threading

import httpx
import websockets

AUTH_URL = "http://localhost:8001"
TICKET_URL = "http://localhost:8002/tickets"
STAFF_URL = "http://localhost:8004"
STATS_URL = "http://localhost:8005/stats"
WS_URL = "ws://localhost:8003/ws"


def listen_for_events():
    asyncio.run(ws_loop())


async def ws_loop():
    async with websockets.connect(WS_URL) as ws:
        async for message in ws:
            event = json.loads(message)
            print(f"\n[LIVE] {event['event']}: {event['ticket']}\n> ", end="", flush=True)


def login():
    users = httpx.get(f"{AUTH_URL}/users").json()
    print("Demo users (quick login):")
    for i, u in enumerate(users):
        print(f"  {i + 1}. {u['username']} ({u['role']})")
    choice = int(input("Choose a user by number: ")) - 1
    return users[choice]


def main():
    user = login()
    print(f"Logged in as {user['username']} ({user['role']})")

    # background thread listens for live ticket events while the menu loop keeps running
    threading.Thread(target=listen_for_events, daemon=True).start()

    while True:
        print("\n1. List tickets\n2. Create ticket\n3. Update ticket status\n4. Assign ticket to staff\n5. View stats\n6. Quit")
        choice = input("> ")
        if choice == "1":
            print(httpx.get(TICKET_URL).json())
        elif choice == "2":
            title = input("Ticket title: ")
            httpx.post(TICKET_URL, params={"title": title, "student": user["username"]})
        elif choice == "3":
            tid = int(input("Ticket id: "))
            status = input("New status: ")
            httpx.patch(f"{TICKET_URL}/{tid}", params={"status": status})
        elif choice == "4":
            tid = int(input("Ticket id: "))
            staff = input("Staff username: ")
            httpx.post(f"{STAFF_URL}/assign", params={"ticket_id": tid, "staff": staff})
        elif choice == "5":
            print(httpx.get(STATS_URL).json())
        elif choice == "6":
            break


if __name__ == "__main__":
    main()
