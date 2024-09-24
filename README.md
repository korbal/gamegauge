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



I've created a one-stop installation script for GameGauge, but I strongly encourage you to review the script before running it.

### Safe Installation Steps

To ensure a safe and successful installation, please follow these steps:

#### 1. Download the Script
```bash
curl -O https://raw.githubusercontent.com/korbal/gamegauge/master/install.sh
```

#### 2. Review the Script's Contents
```bash
cat install.sh
```
Take a moment to read through the script and understand what it will do on your system.

#### 3. Make the Script Executable
```bash
chmod +x install.sh
```

#### 4. Run the Installation Script
```bash
./install.sh
```
This script will:

* Detect your package manager and shell
* Install necessary dependencies (python3-venv and pip3 if not present)
* Create a virtual environment
* Install GameGauge and its dependencies
* Make the 'gamegauge' command globally accessible

If the script runs successfully, you should be able to start GameGauge by typing:

```bash
gamegauge
```

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
