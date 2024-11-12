#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Meshtastic Trivia Bot
Version: 1.0
Author: Brad Hughes
Github: https://github.com/brad28b
Description: A trivia bot for Meshtastic networks with persistent statistics and automatic reconnection
License: MIT
"""

import time
import json
import os
from datetime import datetime
import random
from pubsub import pub
from meshtastic.serial_interface import SerialInterface
from meshtastic.tcp_interface import TCPInterface
from typing import Dict, List, Tuple
import threading

# Connection Configuration
CONNECTION_TYPE = "tcp"  # Options: "tcp" or "serial"
NODE_IP = "192.168.1.20"  # Replace with your Meshtastic node's IP address
SERIAL_PORT = "/dev/ttyUSB0"  # Replace with your serial port
CHANNEL_INDEX = 0  # Replace with your channel index
STATS_FILE = "trivia_stats.json"  # File to store statistics

# Questions Database
QUESTIONS = [
    # Science & Nature (30 questions)
    ("Chemical symbol for gold?", "au"),
    ("Which planet is closest to the sun?", "mercury"),
    ("What element has atomic number 1?", "hydrogen"),
    ("Chemical symbol for silver?", "ag"),
    ("Which metal is liquid at room temperature?", "mercury"),
    ("What gas do plants absorb from the air?", "co2"),
    ("Largest planet in our solar system?", "jupiter"),
    ("Chemical symbol for iron?", "fe"),
    ("Number of bones in human body?", "206"),
    ("Hardest natural material?", "diamond"),
    ("What's the closest star to Earth?", "sun"),
    ("Chemical symbol for sodium?", "na"),
    ("What's the speed of light in km/s?", "300000"),
    ("Number of teeth in adult human?", "32"),
    ("Chemical symbol for oxygen?", "o"),
    ("Earth's largest ocean?", "pacific"),
    ("Human body's largest organ?", "skin"),
    ("Number of chromosomes in humans?", "46"),
    ("Most abundant gas in Earth's atmosphere?", "nitrogen"),
    ("Symbol for helium?", "he"),
    ("Number of planets in our solar system?", "8"),
    ("Fastest land animal?", "cheetah"),
    ("Chemical symbol for potassium?", "k"),
    ("Largest mammal?", "blue whale"),
    ("What covers 71% of Earth's surface?", "water"),
    ("Symbol for carbon?", "c"),
    ("Most abundant element in universe?", "hydrogen"),
    ("Temperature in Celsius where water boils?", "100"),
    ("Number of elements in periodic table?", "118"),
    ("What type of animal is a dolphin?", "mammal"),

    # History (30 questions)
    ("What year did World War II end?", "1945"),
    ("Surname of first US president?", "washington"),
    ("Year America gained independence?", "1776"),
    ("Who painted the Mona Lisa?", "da vinci"),
    ("In what year did Titanic sink?", "1912"),
    ("Which empire built the pyramids?", "egyptian"),
    ("Year World War I began?", "1914"),
    ("Who was the first man on moon?", "armstrong"),
    ("What year did Berlin Wall fall?", "1989"),
    ("Who was ancient Egypt's boy king?", "tutankhamun"),
    ("Year Columbus reached Americas?", "1492"),
    ("Which country invented paper?", "china"),
    ("Year of French Revolution?", "1789"),
    ("Who wrote Romeo and Juliet?", "shakespeare"),
    ("First civilization in history?", "sumer"),
    ("Year of Russian Revolution?", "1917"),
    ("Who built Great Wall of China?", "qin"),
    ("Year America Civil War ended?", "1865"),
    ("First Emperor of Rome?", "augustus"),
    ("Who painted Sistine Chapel?", "michelangelo"),
    ("Year of American moon landing?", "1969"),
    ("Which empire built Machu Picchu?", "inca"),
    ("Who invented telephone?", "bell"),
    ("Year printing press invented?", "1440"),
    ("Who discovered gravity?", "newton"),
    ("First European to reach India by sea?", "gama"),
    ("Who was first female pharaoh?", "hatshepsut"),
    ("Year electricity discovered?", "1752"),
    ("Who invented light bulb?", "edison"),
    ("Year internet was invented?", "1969"),

    # Geography (30 questions)
    ("Capital of Japan?", "tokyo"),
    ("Largest country by area?", "russia"),
    ("Capital of France?", "paris"),
    ("How many continents are there?", "7"),
    ("Longest river in world?", "nile"),
    ("Capital of Italy?", "rome"),
    ("Largest desert?", "sahara"),
    ("Capital of China?", "beijing"),
    ("Highest mountain?", "everest"),
    ("Capital of Brazil?", "brasilia"),
    ("Number of oceans?", "5"),
    ("Capital of Egypt?", "cairo"),
    ("Largest rainforest?", "amazon"),
    ("Capital of Spain?", "madrid"),
    ("Smallest continent?", "australia"),
    ("Capital of Russia?", "moscow"),
    ("Longest wall in world?", "great wall"),
    ("Capital of India?", "delhi"),
    ("Deepest ocean?", "pacific"),
    ("Capital of Mexico?", "mexico city"),
    ("Largest island?", "greenland"),
    ("Capital of Canada?", "ottawa"),
    ("Highest waterfall?", "angel falls"),
    ("Capital of Germany?", "berlin"),
    ("Largest bay?", "bengal"),
    ("Capital of Argentina?", "buenos aires"),
    ("Longest mountain range?", "andes"),
    ("Capital of Australia?", "canberra"),
    ("Largest lake?", "caspian"),
    ("Capital of Greece?", "athens"),

    # Math & Numbers (30 questions)
    ("Square root of 144?", "12"),
    ("How many degrees in a circle?", "360"),
    ("25% of 200?", "50"),
    ("7 x 8?", "56"),
    ("Square root of 81?", "9"),
    ("15 + 26?", "41"),
    ("100 ÷ 4?", "25"),
    ("5 squared?", "25"),
    ("12 x 12?", "144"),
    ("1000 - 750?", "250"),
    ("6 x 7?", "42"),
    ("Square root of 25?", "5"),
    ("18 + 23?", "41"),
    ("200 ÷ 8?", "25"),
    ("4 cubed?", "64"),
    ("9 x 9?", "81"),
    ("150 - 75?", "75"),
    ("3 x 15?", "45"),
    ("Square root of 16?", "4"),
    ("27 + 14?", "41"),
    ("120 ÷ 6?", "20"),
    ("7 squared?", "49"),
    ("8 x 8?", "64"),
    ("90 - 45?", "45"),
    ("5 x 12?", "60"),
    ("Square root of 100?", "10"),
    ("33 + 17?", "50"),
    ("160 ÷ 4?", "40"),
    ("6 squared?", "36"),
    ("11 x 11?", "121"),

    # General Knowledge (30 questions)
    ("Number of weeks in a year?", "52"),
    ("How many minutes in an hour?", "60"),
    ("Number of cards in standard deck?", "52"),
    ("How many strings on guitar?", "6"),
    ("Number of players in soccer team?", "11"),
    ("Days in February in leap year?", "29"),
    ("Number of notes in musical scale?", "7"),
    ("How many legs does spider have?", "8"),
    ("Number of colors in rainbow?", "7"),
    ("How many days in December?", "31"),
    ("Number of tentacles on octopus?", "8"),
    ("How many seconds in minute?", "60"),
    ("Number of dots on dice?", "21"),
    ("How many teeth does adult cat have?", "30"),
    ("Number of squares on chess board?", "64"),
    ("How many hours in day?", "24"),
    ("Number of keys on piano?", "88"),
    ("How many days in September?", "30"),
    ("Number of primary colors?", "3"),
    ("How many months start with J?", "3"),
    ("Number of faces on cube?", "6"),
    ("How many days in lunar month?", "28"),
    ("Number of letters in alphabet?", "26"),
    ("How many cents in dollar?", "100"),
    ("Number of sides in pentagon?", "5"),
    ("How many quarts in gallon?", "4"),
    ("Number of lines in haiku?", "3"),
    ("How many days in June?", "30"),
    ("Number of wheels on tricycle?", "3"),
    ("How many cups in quart?", "4")
]

class TriviaBot:
    def __init__(self):
        self.channel_index = CHANNEL_INDEX
        self.interface = None
        self.stats_file = STATS_FILE
        self.connected = False
        self.reconnect_interval = 10  # seconds between reconnection attempts
        self.should_run = True  # Control flag for monitoring thread
        
        self.connect()
            
        self.active_questions: Dict[str, Tuple[str, str, float]] = {}
        self.playing_users: set = set()
        
        # Load saved statistics
        self.user_stats = self.load_stats()
        print(f"Loaded statistics for {len(self.user_stats)} players")
        
        print("Subscribing to message events...")
        pub.subscribe(self.on_receive, "meshtastic.receive")
        print("Subscription complete")
        
        self.questions = QUESTIONS
        
        # Start connection monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_connection, daemon=True)
        self.monitor_thread.start()

    def connect(self) -> bool:
        """Attempt to connect to the Meshtastic device"""
        try:
            if self.interface:
                try:
                    self.interface.close()
                except:
                    pass
                    
            if CONNECTION_TYPE.lower() == "tcp":
                print(f"Connecting via TCP to {NODE_IP}...")
                self.interface = TCPInterface(hostname=NODE_IP)
            else:
                print(f"Connecting via Serial to {SERIAL_PORT}...")
                self.interface = SerialInterface(SERIAL_PORT)
                
            # Wait a moment for the interface to initialize
            time.sleep(2)
            self.connected = True
            print("Connection established successfully")
            return True
            
        except Exception as e:
            print(f"Error connecting to device: {e}")
            self.connected = False
            return False

    def monitor_connection(self):
        """Monitor connection and attempt reconnection if needed"""
        while self.should_run:
            try:
                if not self.connected:
                    print("Connection lost, attempting to reconnect...")
                    if self.connect():
                        print("Reconnection successful")
                        # Resubscribe to messages
                        pub.subscribe(self.on_receive, "meshtastic.receive")
                    else:
                        print(f"Reconnection failed, waiting {self.reconnect_interval} seconds...")
                        time.sleep(self.reconnect_interval)
                time.sleep(1)
            except Exception as e:
                print(f"Error in connection monitor: {e}")
                self.connected = False
                time.sleep(self.reconnect_interval)

    def load_stats(self) -> Dict:
        """Load statistics from file"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            else:
                print("No existing stats file found, starting fresh")
                return {}
        except Exception as e:
            print(f"Error loading stats: {e}")
            print("Starting with fresh stats")
            return {}

    def save_stats(self):
        """Save statistics to file"""
        try:
            # Create a backup of the current file if it exists
            if os.path.exists(self.stats_file):
                backup_file = f"{self.stats_file}.backup"
                os.replace(self.stats_file, backup_file)
            
            # Save current stats
            with open(self.stats_file, 'w') as f:
                json.dump(self.user_stats, f, indent=2)
            print("Statistics saved successfully")
            
            # Remove backup if save was successful
            if os.path.exists(f"{self.stats_file}.backup"):
                os.remove(f"{self.stats_file}.backup")
                
        except Exception as e:
            print(f"Error saving stats: {e}")
            # If there was an error and we have a backup, restore it
            if os.path.exists(f"{self.stats_file}.backup"):
                os.replace(f"{self.stats_file}.backup", self.stats_file)
                print("Restored stats from backup")

    def get_random_question(self) -> Tuple[str, str]:
        """Return a random question and its answer"""
        print("Getting random question...")
        return random.choice(self.questions)

    def get_node_num(self, node_id: str) -> int:
        """Convert node ID string to number"""
        try:
            if not node_id:  # Check for None or empty string
                print(f"Invalid node ID: {node_id}")
                return None
                
            if node_id.startswith('!'):
                return int(node_id[1:], 16)
            return int(node_id, 16)
        except ValueError:
            print(f"Could not convert node ID to number: {node_id}")
            return None
        except Exception as e:
            print(f"Error processing node ID {node_id}: {e}")
            return None

    def send_message(self, message: str, to_node: str):
        """Send a message to a specific node"""
        try:
            if not self.connected:
                print("Cannot send message: Not connected")
                return
                
            if not to_node:  # Check for None or empty string
                print("Cannot send message: Invalid node ID (None)")
                return
                
            print(f"Sending message to {to_node}: {message}")
            node_num = self.get_node_num(to_node)
            if node_num is None:
                print(f"Invalid node ID format: {to_node}")
                return
                
            print(f"Converting node ID {to_node} to number: {node_num}")
            self.interface.sendText(message, node_num, channelIndex=self.channel_index)
            print("Message sent successfully")
        except Exception as e:
            print(f"Error sending message: {e}")
            self.connected = False
            import traceback
            print(traceback.format_exc())

    def handle_quit(self, node_id: str):
        """Handle user quitting the game"""
        if not node_id:  # Check for None or empty string
            return

        # Remove active question if exists
        if node_id in self.active_questions:
            del self.active_questions[node_id]  # Remove active question without counting it

        # Remove from playing users set
        self.playing_users.discard(node_id)

        # Update last played timestamp in stats if user exists
        if node_id in self.user_stats:
            self.user_stats[node_id]["last_played"] = datetime.now().isoformat()
            self.save_stats()

        # Send goodbye message
        self.send_message("Thanks for playing! Send any message to start a new game.", node_id)

        print(f"Player {node_id} has quit the game")

    def send_new_question(self, node_id: str):
        """Send a new random question to a node"""
        if not node_id:  # Check for None or empty string
            return

        print(f"Sending new question to {node_id}")
        question, answer = self.get_random_question()
        self.active_questions[node_id] = (question, answer, time.time())
        self.playing_users.add(node_id)  # Mark user as playing
        self.send_message(f"{question} (30 seconds to answer! Send 'X' to quit, 'L' for stats)", node_id)

        # Start timer thread
        threading.Timer(30.0, self.check_timeout, args=[node_id, question, answer]).start()

    def check_timeout(self, node_id: str, question: str, answer: str):
        """Check if a question has timed out"""
        if not node_id:  # Check for None or empty string
            return

        if node_id in self.active_questions:
            current_question, current_answer, timestamp = self.active_questions[node_id]
            if current_question == question and current_answer == answer:
                self.send_message("Time's up! The correct answer was: " + answer, node_id)
                self.update_stats(node_id, False, 30.0)
                del self.active_questions[node_id]

    def check_answer(self, node_id: str, answer: str) -> bool:
        """Check if the answer is correct for the active question"""
        if not node_id:  # Check for None or empty string
            return False

        if node_id in self.active_questions:
            question, correct_answer, timestamp = self.active_questions[node_id]
            current_time = time.time()

            # Check if within 30-second time limit
            if current_time - timestamp <= 30:
                if answer.lower().strip() == correct_answer.lower():
                    response_time = current_time - timestamp
                    self.update_stats(node_id, True, response_time)
                    return True
            else:
                # Time expired
                self.send_message("Time's up! The correct answer was: " + correct_answer, node_id)
                self.update_stats(node_id, False, 30.0)

            del self.active_questions[node_id]
        return False

    def update_stats(self, node_id: str, correct: bool, response_time: float):
        """Update user statistics"""
        if not node_id:  # Check for None or empty string
            return

        if node_id not in self.user_stats:
            self.user_stats[node_id] = {
                "total_answered": 0,
                "correct_answers": 0,
                "total_time": 0,
                "fastest_time": float('inf'),
                "first_seen": datetime.now().isoformat(),
                "last_played": datetime.now().isoformat()
            }

        stats = self.user_stats[node_id]
        stats["total_answered"] += 1
        stats["last_played"] = datetime.now().isoformat()

        if correct:
            stats["correct_answers"] += 1
            stats["total_time"] += response_time
            stats["fastest_time"] = min(stats["fastest_time"], response_time)

        # Save after each update
        self.save_stats()

    def get_leaderboard(self) -> str:
        """Get top 5 players sorted by correct answers and time"""
        if not self.user_stats:
            return "No players yet!"

        # Convert stats to list of tuples for sorting
        player_stats = []
        for node_id, stats in self.user_stats.items():
            if stats["correct_answers"] > 0:  # Only include players who have correct answers
                avg_time = stats["total_time"] / stats["correct_answers"]
                player_stats.append((
                    node_id,
                    stats["correct_answers"],
                    stats["total_answered"],
                    avg_time
                ))

        # Sort by correct answers (descending) and average time (ascending)
        player_stats.sort(key=lambda x: (-x[1], x[3]))

        # Format top 5 leaderboard
        leaderboard = "🏆 Top Players 🏆\n"
        for i, (node_id, correct, total, avg_time) in enumerate(player_stats[:5], 1):
            leaderboard += f"{i}. {node_id}: {correct}/{total} correct (avg {avg_time:.1f}s)\n"

        return leaderboard

    def get_stats(self, node_id: str) -> str:
        """Get formatted statistics for a node"""
        if not node_id:  # Check for None or empty string
            return "Invalid node ID"

        if node_id in self.user_stats:
            stats = self.user_stats[node_id]
            correct = stats["correct_answers"]
            total = stats["total_answered"]
            avg_time = stats["total_time"] / correct if correct > 0 else 0
            if stats["fastest_time"] == float('inf'):
                fastest = 0
            else:
                fastest = stats["fastest_time"]

            # Get player's rank
            player_position = self.get_player_rank(node_id)
            rank_str = f" (Rank: #{player_position})" if player_position else ""

            # Calculate days played
            first_seen = datetime.fromisoformat(stats["first_seen"])
            last_played = datetime.fromisoformat(stats["last_played"])
            days_playing = (last_played - first_seen).days

            # Get leaderboard
            leaderboard = self.get_leaderboard()

            return (f"Your Stats{rank_str}: {correct}/{total} correct answers\n"
                   f"Avg time: {avg_time:.1f}s\n"
                   f"Best time: {fastest:.1f}s\n"
                   f"Days playing: {days_playing}\n"
                   f"First seen: {first_seen.strftime('%Y-%m-%d')}\n\n"
                   f"{leaderboard}")
        return "No statistics available yet."

    def get_player_rank(self, node_id: str) -> int:
        """Get player's rank based on correct answers and time"""
        if not node_id or node_id not in self.user_stats:  # Check for None or empty string
            return 0

        player_stats = []
        for nid, stats in self.user_stats.items():
            if stats["correct_answers"] > 0:
                avg_time = stats["total_time"] / stats["correct_answers"]
                player_stats.append((
                    nid,
                    stats["correct_answers"],
                    avg_time
                ))

        # Sort by correct answers (descending) and average time (ascending)
        player_stats.sort(key=lambda x: (-x[1], x[2]))

        # Find player's position
        for i, (nid, _, _) in enumerate(player_stats, 1):
            if nid == node_id:
                return i
        return 0

    def on_receive(self, packet, interface):
        """Handle incoming messages"""
        try:
            # print(f"\nReceived packet: {packet}")

            if 'decoded' in packet and packet['decoded'].get('portnum') == 'TEXT_MESSAGE_APP':
                print("Processing text message...")
                message = packet['decoded']['payload'].decode('utf-8').strip()

                # Get from_node with better error handling
                from_node = packet.get('fromId')
                if not from_node:  # Check for None or empty string
                    print("Warning: Received message without valid fromId")
                    return

                print(f"Message from {from_node}: {message}")

                # Handle 'X' command to quit
                if message.upper() == 'X':
                    print("Quit command received")
                    self.handle_quit(from_node)
                    return

                # Handle 'L' command for statistics
                if message.upper() == 'L':
                    print("Stats request received")
                    stats = self.get_stats(from_node)
                    self.send_message(stats, from_node)
                    return

                # Check if there's an active question for this node
                if from_node in self.active_questions:
                    print(f"Active question found for node {from_node}")
                    if self.check_answer(from_node, message):
                        self.send_message("Correct! Well done!", from_node)
                        # Wait a moment before sending new question
                        threading.Timer(2.0, self.send_new_question, args=[from_node]).start()
                    else:
                        self.send_message("Sorry, that's incorrect!", from_node)
                        # Send a new question after incorrect answer
                        threading.Timer(2.0, self.send_new_question, args=[from_node]).start()
                else:
                    # Send welcome message for new game
                    welcome_msg = ("Welcome to Trivia! Send 'X' to quit anytime, 'L' to see statistics. "
                                "Here's your first question...")
                    self.send_message(welcome_msg, from_node)
                    time.sleep(1)  # Brief pause before first question
                    print(f"No active question for node {from_node}, sending new question")
                    self.send_new_question(from_node)

        except Exception as e:
            print(f"Error processing message: {e}")
            import traceback
            print(traceback.format_exc())

    def cleanup(self):
        """Cleanup resources before shutdown"""
        self.should_run = False  # Stop the monitoring thread
        if self.interface:
            try:
                self.interface.close()
            except:
                pass

def main():
    bot = None
    try:
        print("Initializing TriviaBot...")
        bot = TriviaBot()
        print("Trivia bot is running...")
        print(f"Using {'TCP' if CONNECTION_TYPE.lower() == 'tcp' else 'Serial'} connection")
        print(f"Questions loaded: {len(QUESTIONS)}")
        print(f"Stats file: {STATS_FILE}")

        if bot.interface:
            try:
                my_info = bot.interface.getMyNodeInfo()
                print(f"Our node ID: {my_info.get('num', 'Unknown')}")
            except Exception as e:
                print(f"Warning: Could not get node info: {e}")

        print("Waiting for messages...")

        while True:
            try:
                time.sleep(1)
            except Exception as e:
                print(f"Error in sleep: {e}")

    except KeyboardInterrupt:
        print("\nShutting down trivia bot...")
    except Exception as e:
        print(f"Error in main loop: {e}")
        import traceback
        print(traceback.format_exc())
    finally:
        if bot:
            print("Cleaning up...")
            bot.cleanup()
            print("Cleanup complete")

if __name__ == "__main__":
    main()
