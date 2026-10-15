# Sequence diagrams

## Simple version

One ticket, start to finish, through all five services: staff logs in, a
student reports a problem, staff sees it and picks it up live, and staff
checks the dashboard.

```mermaid
sequenceDiagram
    actor Staff
    actor Student
    participant Auth as auth-service
    participant Tickets as ticket-service
    participant Notify as notify-service
    participant Assign as staff-service
    participant Stats as stats-service

    Staff->>Auth: log in
    Auth-->>Staff: ok, you're staff

    Student->>Tickets: submit ticket
    Tickets->>Notify: ticket created
    Notify--)Staff: live push

    Staff->>Assign: assign to me
    Assign->>Tickets: update ticket
    Tickets->>Notify: ticket updated
    Notify--)Staff: live push
    Notify--)Student: live push

    Staff->>Stats: view stats
    Stats->>Tickets: get all tickets
    Tickets-->>Stats: tickets
    Stats-->>Staff: totals
```

Solid arrows are plain HTTP calls between services. Dashed arrows are the
WebSocket push that notify-service sends out. Staff always gets it, and a
student only gets it for the one ticket they are watching.

## Detailed version

The same flow with the real endpoints, ports and WebSocket connections.

```mermaid
sequenceDiagram
    autonumber
    participant S as Student (web page)
    participant C as Staff client
    participant A as auth-service :8001
    participant SF as staff-service :8004
    participant T as ticket-service :8002
    participant N as notify-service :8003
    participant ST as stats-service :8005

    Note over C,A: 1. Staff logs in
    C->>A: POST /login (username, password)
    A-->>C: ok + role staff
    C-)N: open WebSocket /ws?role=staff

    Note over S,T: 2. Student submits a ticket (no login)
    S->>T: POST /tickets (name, title)
    T->>T: save ticket, status = open
    T-->>S: ticket id 4
    S-)N: open WebSocket /ws?ticket=4
    T->>N: POST /broadcast (ticket_created)
    N-)C: push: new ticket 4

    Note over C,N: 3. Staff assigns the ticket
    C->>SF: POST /assign (ticket 4, carol)
    SF->>T: PATCH /tickets/4 (staff=carol, status=assigned)
    T->>N: POST /broadcast (ticket_updated)
    N-)S: push: your ticket 4 is assigned
    N-)C: push: ticket 4 updated
    T-->>SF: updated ticket
    SF-->>C: 200 OK

    Note over S,T: 4. Student tracks the ticket later
    S->>T: GET /tickets/4
    T-->>S: status: done

    Note over C,ST: 5. Staff views stats
    C->>ST: GET /stats
    ST->>T: GET /tickets
    T-->>ST: all tickets
    ST-->>C: total + count by status
```
