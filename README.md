# 🛒Monster Arena Game

![Badge](https://img.shields.io/badge/status-active-brightgreen)

## Project Description

A fully playable game made in Python, using the pygame library. The game is an arena type 
based game where you have to survive each round by defeating enemies. 
The project is originally from a youtube course video for learning Python, by making 5 
different games, made by a youtuber named Clear Code. Here is a link to this course: 
https://www.youtube.com/watch?v=8OMghdHP-zs&pp=0gcJCfcAhR29_xXO 
The base game was very simple and did not include the round system or the skills upgrade system.
I managed to add those features and it fundamentally improved my knowledge of Python.

## 🚀 Features 

Based on the provided code, "Monster Arena" has the following key features:

#1. Core Gameplay
-Wave-Based Combat: The game consists of multiple rounds where players must survive against waves of enemies.
-Enemy Types: Different enemy types include bats, blobs, and skeletons, each with unique health and attack properties.
-Shooting Mechanics: The player can shoot bullets at enemies using a gun.
-Round Progression: Players progress through rounds, facing increasing enemy difficulty.

#2. Player Mechanics
-Health System: The player has a health bar, and getting hit by enemies reduces health.
-Upgradable Skills: Players can upgrade attributes like:
-Damage (costs 500 coins)
-Health (costs 750 coins)
-Running Speed (costs 250 coins)
-Shooting Speed (costs 500 coins)
-Coin Collection: Players earn coins by defeating enemies and can use them for upgrades.
-Immortality Mode: The game starts with temporary invincibility.

#3. Enemy System
-Enemy Spawning: Enemies spawn at predefined locations.
-Enemy Attack: Enemies inflict damage upon collision with the player.
-Death & Rewards: Enemies drop rewards upon defeat.

#4. UI & Visuals
-Health Bar: Displays the player’s current health.
-Coin Counter: Keeps track of collected coins.
-Round Timer: Shows time left in the current round.
-Welcome Screen: A starting screen before the game begins.
-Win & Death Screens: Displays appropriate screens depending on whether the player wins or loses.

#5. Sound & Music
-Background Music: Continuous music plays during gameplay.
-Sound Effects:
-Shooting
-Enemy impacts
-Damage received
-Coin collection
-Winning and losing sounds

#6. Game Progression & Difficulty
-Multiple Rounds: Players advance through five rounds.
-Increasing Challenge: Enemy count and difficulty increase in later rounds.
-Custom Events: The game has timers for spawning enemies and tracking round durations.

#7. Environment & World
-Tile-Based Map: The game loads a 2D tile-based world using Tiled (.tmx) maps.
-Collision System: Players and enemies collide with obstacles.
-Spawn Points: Enemies appear at pre-defined spawn locations.

#8. Game Over Conditions
-Win Condition: Survive all rounds to win.
-Lose Condition: If the player’s health reaches zero, the game ends.

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Retr0647/monster-arena-game.git
   ```
2. Navigate to the project directory:
   ```bash
   cd monster-arena-game
   ```
3. Need to have Python and pygame installed beforehand.
  
3. Open `main.py` in a code editor or just by clicking it.

## 📄 Documentation
Detailed documentation for all Python functions and project structure can be found in the **`docs/`** folder.

## 🎯 Usage
Explore the interactive elemnts of the game by playing it fully. The project serves as a great reference for structuring a 
a fully playable and interactive game as well as the possibilites of the pygame library. It is also a great showcase of Python
classes and object-oriented programming.

## 📜 License
This project is open-source and available under the **MIT License**.

# Contact

For any questions, feel free to reach out via [GitHub Issues](https://github.com/your-username/monster-arena-game/issues) or kuba@eskrytka.net.pl.

