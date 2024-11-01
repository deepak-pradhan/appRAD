!bin/bash

clear
# source .sbox1/bin/activate
# fastapi run sbox1/data_loader.py
fastapi run main.py --host 0.0.0.0 --port 8082
# cd frontend
# npm run dev