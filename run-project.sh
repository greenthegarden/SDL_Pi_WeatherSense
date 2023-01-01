#!/usr/bin/env bash

# Start up broker and home assistant
docker compose up

python3 device.py
