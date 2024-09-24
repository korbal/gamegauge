#!/bin/sh

# Function to detect package manager
detect_package_manager() {
    if command -v apt-get >/dev/null 2>&1; then
        echo "apt"
    elif command -v dnf >/dev/null 2>&1; then
        echo "dnf"
    elif command -v yum >/dev/null 2>&1; then
        echo "yum"
    elif command -v pacman >/dev/null 2>&1; then
        echo "pacman"
    elif command -v zypper >/dev/null 2>&1; then
        echo "zypper"
    else
        echo "unknown"
    fi
}

# Function to install package
install_package() {
    package_manager=$(detect_package_manager)
    package_name=$1

    case $package_manager in
        apt)
            sudo apt-get update && sudo apt-get install -y "$package_name"
            ;;
        dnf)
            sudo dnf install -y "$package_name"
            ;;
        yum)
            sudo yum install -y "$package_name"
            ;;
        pacman)
            sudo pacman -Sy --noconfirm "$package_name"
            ;;
        zypper)
            sudo zypper install -y "$package_name"
            ;;
        *)
            echo "Unsupported package manager. Please install $package_name manually."
            exit 1
            ;;
    esac
}

# Check if python3-venv is installed
if ! command -v python3 -m venv >/dev/null 2>&1; then
    echo "python3-venv is not installed. Attempting to install..."
    install_package "python3-venv"
fi

# Check if pip is installed
if ! command -v pip3 >/dev/null 2>&1; then
    echo "pip3 is not installed. Attempting to install..."
    install_package "python3-pip"
fi

# Create a virtual environment
python3 -m venv gamegauge_env

# Detect the current shell
current_shell=$(basename "$SHELL")

# Activate the virtual environment based on the shell
case $current_shell in
    bash|sh)
        . ./gamegauge_env/bin/activate
        ;;
    zsh)
        . ./gamegauge_env/bin/activate
        ;;
    fish)
        . ./gamegauge_env/bin/activate.fish
        ;;
    csh|tcsh)
        source ./gamegauge_env/bin/activate.csh
        ;;
    *)
        echo "Unsupported shell. Please activate the virtual environment manually."
        exit 1
        ;;
esac

# Install requirements
pip install -r requirements.txt

# Make the script executable and move it to a directory in PATH
chmod +x main.py
sudo mv main.py /usr/local/bin/gamegauge

echo "GameGauge has been installed successfully!"
echo "You can now run it by typing 'gamegauge' in your terminal."

# Deactivate the virtual environment
case $current_shell in
    fish)
        functions -e deactivate
        ;;
    *)
        deactivate
        ;;
esac
