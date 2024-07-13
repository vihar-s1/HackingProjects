#!/usr/bin/env bash

log_info() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1"
}

if [ -x $VIRTUAL_ENV ]; then
    deactivate
fi

if [ -x ".venv" ]; then 
    log_info "Removing the virtual environment..."
    rm -rf .venv
fi

log_info "Cleanup complete."