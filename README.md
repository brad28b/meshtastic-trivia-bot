# meshtastic-trivia-bot
A trivia bot designed to work on the Meshtastic network. Pre-loaded with 150 trivia questions.

Keeps track of a leaderboard.

The following instructions are for Linux. It does work on Windows with most of the below commands, except for running persistently (work that out yourself for Windows).

The python script 'meshtrivia.py' connects to your Meshtastic node, and allows other nodes to play a game of trivia with it, by sending PM/DMs to it.

# Installation

* cd ~
* git clone https://github.com/brad28b/meshtastic-trivia-bot.git
* cd meshtastic-trivia-bot
* pip3 install -r requirements.txt

# Configuration

First decide if you will connect to your Meshtastic node via serial or tcp, and then edit and save the meshtrivia.py file with your serial or tcp credentials.

Then give execute permissions to start_trivia_bot.sh:

* chmod +x start_trivia_bot.sh

# Usage

To run the Triva Bot:

* python meshtrivia.py
  
![Screenshot 2024-11-12 152504](https://github.com/user-attachments/assets/2dd67008-cdf8-4038-87e5-e3529a46a677)

To quit the trivia bot, use CTRL-C.

![466377238_1765548554279321_3529423627956944720_n](https://github.com/user-attachments/assets/d585ef94-cfc0-45b2-a66d-4fc818062d1f)


# Keep running persistently

* ./start_trivia_bot.sh

The above command will restart the trivia bot if for some reason it crashes. To quit, use CTRL-C twice.




