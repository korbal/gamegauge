**GameGauge**

A command-line tool designed to help gamers make informed purchase decisions.
It aggregates data from multiple sources, providing key information about games such as playtime, user scores, and reviews, all in one convenient interface.

### About GameGauge

GameGauge was born out of a simple need: to make informed gaming purchase decisions quickly and efficiently. As a gamer myself, I often found the process of researching games time-consuming and scattered across multiple websites. I created GameGauge to consolidate this information into a single, easy-to-use command-line tool.

My design philosophy is centered around enabling the fastest decision-making process possible. I believe that by presenting the most crucial information upfront - playtime, user scores, and recent reviews - gamers can quickly gauge whether a game aligns with their preferences and available time.

This release (v1.0) is just the beginning. I have plans to expand and refine GameGauge.

### Features

* Quick game lookup with data from HowLongToBeat and Steam
* Display of crucial game information including playtime estimates and user scores
* Access to recent user reviews
* Simple, intuitive command-line interface

## UX
![image](https://github.com/user-attachments/assets/e4ee7548-5575-4c99-9f72-db5ea877304e)
![image](https://github.com/user-attachments/assets/c5cb713d-2ebd-47d8-b596-cf4bf1966712)
![image](https://github.com/user-attachments/assets/88ac6abd-78d5-4b3d-a7c9-e4578086b87e)


### Installation

### 1. Ensure Python 3.7 or Higher is Installed

Make sure you have Python 3.7 or higher installed on your system. You can check your Python version by running:
```bash
python3 --version
```

### 2. Install Pip (If Necessary)

If pip isn't already installed, install it using the following command:

**Debian/Ubuntu-based Systems:**
```bash
sudo apt-get install python3-pip
```
**Fedora-based Systems:**
```bash
sudo dnf install python3-pip
```

Adjust according to your package manager.

### 3. Clone the GameGauge Repository

Clone the GameGauge repository using:
```bash
git clone https://github.com/korbal/gamegauge.git
```

### 4. Navigate and Install Virtual Env

Navigate to the GameGauge directory:
```bash
cd gamegauge
```

If you're unsure if `venv` is installed, run:
```bash
python3 -m venv --help
```
If you see an error, install `python3-venv` using your system's package manager.

Create a virtual environment in the current directory using:
```bash
python3 -m venv .venv
```

Activate the virtual environment using:
```bash
source .venv/bin/activate
```
**Note:** On Windows, you may need to use `.\.venv\Scripts\activate` instead.

### 5. Install Dependencies

Then, install the required dependencies using:
```bash
pip3 install -r requirements.txt
```

### 6. Make Main Script Executable

Make the main script executable with:
```bash
chmod +x main.py
```

### 7. Run GameGauge 

You can now run GameGauge by executing:
```bash
./main.py
```

**Important Notes**

* These instructions assume a Unix-like system (Linux, macOS). For Windows users, the process might be slightly different.
* If you encounter any issues, please ensure you have the latest version of Python and pip installed, and that you have the necessary permissions to install packages and move files.


### Troubleshooting

If you encounter any issues during installation, please check that you have Python 3 installed on your system. You may need to install additional dependencies manually depending on your system configuration.

Remember, while I've tried to make this script as universal as possible, it may not work perfectly on all systems. If you encounter any problems, please open an issue on the GitHub repository, and I'll do my best to help.

### Usage

After installation, you can use GameGauge by typing `gamegauge` followed by a game name:

```bash
gamegauge "Elden Ring"
```

Follow the on-screen prompts to navigate through the application.

### What to Expect

Upon running GameGauge, you'll be presented with a list of search results. You can then select a game to view detailed information, including:

* Playtime estimates (main story, completionist, etc.)
* User scores
* Recent user reviews
* Release date and platform availability (for performance reasons, only the first 3 most relevant games' release dates are displayed.)

The interface is designed to be intuitive and easy to navigate, with clear instructions provided at each step.

### Feedback and Support

If you encounter any issues or have suggestions for improving GameGauge, please don't hesitate to open an issue on our GitHub repository.

### License

GameGauge is released under the MIT License.

### Acknowledgements

GameGauge uses data from HowLongToBeat and Steam. I am grateful for these services and the gaming community that contributes to them.

Thank you for using GameGauge! I hope it helps you make great gaming decisions.
