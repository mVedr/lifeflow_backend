#!/bin/bash
uvicorn db_server.main:app --reload   --port 8001 &\
uvicorn notifier.main:app --reload --port 8002 &\
uvicorn verifier.main:app --reload --port 8003 