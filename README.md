# meshtastic-trivia-bot
A trivia bot designed to work on the Meshtastic network.

The python script meshttrivia.py connects to your Meshtastic node, and allows other nodes to play a game of trivia with it, by sending PM/DMs to it.

# Installation

* cd ~
* git clone https://github.com/brad28b/meshtastic-trivia-bot.git
* cd meshtastic-trivia-bot
* pip3 install -r requirements.txt

# Configuration

First decide if you will connect to your Meshtastic node via serial or TCP, and then edit and save the meshtrivia.py file with your serial or tcp credentials.

Then give execute permissions to start_trivia_bot.sh:

* chmod +x start_trivia_bot.sh

# Usage

To run the Triva Bot:

* python meshtrivia.py
  
![Screenshot 2024-11-12 143016](https://github.com/user-attachments/assets/46ccc792-6250-4e26-aeb1-d01b520d0d9e)

To quit the trivia bot, use CTRL-C.


# Keep running persistenly

* ./start_trivia_bot.sh

The above command will restart the trivia bot if for some reason it crashes. To quit, use CTRL-C twice.




