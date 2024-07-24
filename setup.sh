#!/usr/bin/env bash

log_info() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1"
}

if [ -x ".venv" ]; then
	log_info "Virtual environment already exists."
else
	python3 -m venv .venv
fi

log_info "Activating virtual environment..."
source .venv/bin/activate

log_info "Upgrading pip..."
pip install --upgrade pip -q -q

# Find all requirements.txt files in the current directory and its subdirectories
echo -e "\n"
for file in $(find . -type f -name "requirements.txt") 
do
	# Install dependencies for each requirements.txt file
	log_info "Installing dependencies for $file..."
	python -m pip install -r "$file" -q -q
done

log_info "Deactivating virtual environment..."
deactivate
