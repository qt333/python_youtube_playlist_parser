#!/bin/bash
set -e

cd /home/ubuntu/python_youtube_playlist_parser
chmod +x start_parse.sh
uv sync
uv run youtube_update_existing_file.py
# source venv/bin/activate
# python3 youtube_update_existing_file.py