#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Please install it and try again."
    exit 1
fi

# Create a virtual environment
python3 -m venv gamegauge_env

# Activate the virtual environment
source gamegauge_env/bin/activate

# Install requirements
pip3 install -r requirements.txt

# Make the script executable and move it to a directory in PATH
chmod +x main.py
sudo mv main.py /usr/local/bin/gamegauge

echo "GameGauge has been installed successfully!"
echo "You can now run it by typing 'gamegauge' in your terminal."
