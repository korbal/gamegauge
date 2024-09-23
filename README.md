**GameGauge**

A command-line tool designed to help gamers make informed purchase decisions.
It aggregates data from multiple sources, providing key information about games such as playtime, user scores, and reviews, all in one convenient interface.

### About GameGauge:

GameGauge was born out of a simple need: to make informed gaming purchase decisions quickly and efficiently. As a gamer myself, I often found the process of researching games time-consuming and scattered across multiple websites. I created GameGauge to consolidate this information into a single, easy-to-use command-line tool.

My design philosophy is centered around enabling the fastest decision-making process possible. I believe that by presenting the most crucial information upfront - playtime, user scores, and recent reviews - gamers can quickly gauge whether a game aligns with their preferences and available time.

This release (v1.0) is just the beginning. I have plans to expand and refine GameGauge.

### Features

* Quick game lookup with data from HowLongToBeat and Steam
* Display of crucial game information including playtime estimates and user scores
* Access to recent user reviews
* Simple, intuitive command-line interface

### Installation

To install GameGauge, follow these steps:

1. Ensure you have Python 3.7 or higher installed on your system.
2. Just use this one stop install script
   ```curl
curl -sSL https://raw.githubusercontent.com/korbal/gamegauge/main/install.sh | bash
```

The installation script will set up a virtual environment, install all necessary dependencies, and make the 'gamegauge' command globally accessible.

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
* Release date and platform availability (for performance reasons, only the first 3 (most relevant) games' release date are displayed. To be improved later.)

The interface is designed to be intuitive and easy to navigate, with clear instructions provided at each step.

### Feedback and Support

If you encounter any issues or have suggestions for improving GameGauge, please don't hesitate to open an issue on our GitHub repository. We value your feedback and are committed to making GameGauge as useful as possible for the gaming community.

### License

GameGauge is released under the MIT License. 

### Acknowledgements

GameGauge uses data from HowLongToBeat and Steam. I am grateful for these services and the gaming community that contributes to them.

Thank you for using GameGauge! I hope it helps you make great gaming decisions.
