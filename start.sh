#!/bin/bash
cd "$(dirname "$0")"
source venv/Scripts/activate
python main.py
read -p "Press [Enter] to close..."