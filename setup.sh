#!bin/bash

# Exit on error
# set -e

# Set where DB is, SafeLocation, ...
export db_file='./../data/backend.db'
SAFE_LOCATION="/path/to/SafeLocation"
PROJECT_DIR="project"

# Check if SafeLocation exists
if [ ! -d "$SAFE_LOCATION" ]; then
  echo "Error: SafeLocation does not exist at $SAFE_LOCATION"
  # exit 1
fi


# 1. Create venv
# 1.1 Check if $1 exist 
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <arg1>"
    echo "where arg1 is the env name"
    # exit 1
fi

# 1.2 Check if venv has been created
venv_name=".$1" # sbox2 will become .sbox2
if [ ! -d "./../$venv_name" ]; then
    # python3 -m venv "./../$venv_name"
    echo "Virtual environment $venv_name created."
else 
    echo "Virtual environment $venv_name already exist."
fi

# 1.3 activate venv
source "./../$venv_name/bin/activate"
echo "Virtual environment $venv_name activated."

# # 2. install
# # 2.1 backend & pages
# pip install fastapi uvicorn jinja2
# # 2.3 frontend
# cd frontend
# if [ ! -d "sveltekit-app" ]; then
#   npm create svelte@latest sveltekit-app --yes
#   cd sveltekit-app
#   npm install
# else
#   echo "SvelteKit app already exists. Skipping SvelteKit setup."
# fi

# # 3. Copy vanila from SafeLocation
# # 3.1
# mkdir -p {backend/{templates,static},frontend/sveltekit-app}
# # 3.2 Copy the skeleton code from SafeLocation
# echo "Copying initial skeleton code from SafeLocation..."
# # Copy backend skeleton files (e.g., FastAPI main.py, templates, and static files)
# cp -R $SAFE_LOCATION/backend/* ../../backend/
# # Copy frontend skeleton files for SvelteKit
# cp -R $SAFE_LOCATION/frontend/* .

## Assumption you are in current project dir

echo "
To start development servers:
1. FastAPI (backend):
   cd project/backend
   source env/bin/activate
   uvicorn main:app --reload

2. SvelteKit (frontend):
   cd project/frontend/sveltekit-app
   npm run dev

Access Points:
- FastAPI + HTMX: http://localhost:8000/
- SvelteKit Product Form: http://localhost:3000/
"

