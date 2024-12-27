#!/bin/bash

# Navigate to the directory
cd ~/v3/Hubstaff-Keka-Integration-Bacancy/employee_logs_cron || { echo "Directory not found"; exit 1; }

# Run the Python script
python3 main.py
