#!/bin/bash
python3 services/auth_service/main.py &
python3 services/ticket_service/main.py &
python3 services/notify_service/main.py &
python3 services/staff_service/main.py &
python3 services/stats_service/main.py &
wait
