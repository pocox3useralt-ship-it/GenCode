#!/bin/bash

clear

echo "============================================================"
echo "  ######   #######   #####    #####   #######   ######     "
echo "  #     #  #        #     #  #     #  #        #     #     "
echo "  #     #  #        #        #        #        #           "
echo "  ######   #####     #####    #####   #####     #####      "
echo "  #   #    #              #        #   #              #     "
echo "  #    #   #        #     #  #     #   #        #     #    "
echo "  #     #  #######   #####    #####    #######   ######     "
echo "============================================================"
echo ""
echo "                Welcome To GenCode"
echo ""
echo "============================================================"
echo "Start? (y/n)"
read choice

if [[ "$choice" =~ ^[Yy]$ ]]; then

    echo "Checking Python..."

    if command -v python >/dev/null 2>&1; then
        echo "Python found."

        echo "Installing required packages..."
        python -m pip install flask flask-session pyyaml

        echo "Starting program..."

        # FIX: run inside Startup so config.yaml works
        SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
        cd "$SCRIPT_DIR/Startup"
        python M.py

    else
        echo "Python is not installed."
        exit 1
    fi

else
    echo "Cancelled."
    exit 0
fi
