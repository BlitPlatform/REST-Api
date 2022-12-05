#!/bin/bash
#conda activate blitairest
#exec python -m pytest
uvicorn main:app 
#exec gunicorn -k uvicorn.workers.UvicornWorker