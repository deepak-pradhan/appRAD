#!bin/bash

export db_file='./../data/backend.db'

# run python_scripts/01a_create_tables.py to create tables
# 
python3 scripts/01a_create_pilot_tables.py

# run python_scripts/01b_load_data.py to load initial data
python3 scripts/01b_load_pilot_data.py