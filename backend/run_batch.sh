#!/bin/bash
export GOOGLE_API_KEY=""
export SAMPLE_SIZE=54
cd /home/fernandosilvav/Proyecto-Prueba/backend
rm -f outputs/.batch_state.pkl
exec python3 -u batch_process.py > outputs/batch_run_54.log 2>&1
