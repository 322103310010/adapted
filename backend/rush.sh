#!/bin/bash

echo "=========================================="
echo "AdaptEd Backend Setup & Run"
echo "=========================================="
echo ""

if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install Python3 first."
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Starting Flask server..."
echo "=========================================="
echo ""
echo "Server will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
