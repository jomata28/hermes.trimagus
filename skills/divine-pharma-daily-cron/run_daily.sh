#!/bin/bash
# Wrapper script for divine-pharma-daily-cron cron job

source "$HOME/.hermes/hermes-agent/venv/bin/activate"
cd "$HOME/.hermes/skills/divine-pharma-daily-cron"

# Run the processor
python3 process_episode.py

# Deactivate venv
deactivate
