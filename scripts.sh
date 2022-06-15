#!/bin/bash

crond -L /var/log/cron.log &
python3 spotify/dashboard/app.py
