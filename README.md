# priest-and-devil-game
DSA and python project
# Priests and Devils River Crossing Puzzle (Python with Tkinter)

This is a **Python** implementation of the classic **Priests and Devils** (also known as **Missionaries and Cannibals**) river crossing puzzle with an interactive **Tkinter-based GUI**.

## 🎮 Gameplay Rules

* You start with **3 Priests** and **3 Devils** on the left side of the river.
* A boat can carry **at most 2 people** at a time.
* At no point on either riverbank can the number of devils exceed the number of priests (if any priests are present), or the priests will be eaten!
* Safely move all characters to the right side.

## 🛠 Features

* 🚤 Smooth **animated boat and character movement**.
* ⏱ **Step counter** and **timer**.
* ↩️ **Undo** last move functionality.
* 🤖 **BFS Solver** for hint or auto-solve.
* 🔊 Sound effects:

  * Boat rowing
  * Win sound when puzzle is solved
  * Lose sound if priests are eaten
* 📜 Move history tracker

## 🧠 DSA Concepts Used

* `stack` — Undo functionality
* `queue` — BFS Solver (shortest path to win)
* `State` class — Encapsulation of each game state
* State transition graph modeling

## 🔧 Installation

### Requirements

* Python 3.8+
* Tkinter (comes with standard Python)
* Pygame (for sound effects)

### Installing Dependencies

```bash
pip install pygame
```

### Run the Game

```bash
python main.py
```

## 📁 Project Structure

```
.
├── assets/
│   ├── priest.png
│   ├── devil.png
│   ├── boat.png
│   ├── background.jpg
│   └── sounds/
│       ├── row.wav
│       ├── win.wav
│       └── lose.wav
├── main.py
├── state.py
├── solver.py
├── utils.py
└── README.md
```

## 👨‍💻 Author

**Anshul Jain**
4rd Year Mechanical Engineering @ NIT Srinagar
Data Structures & Algorithms | ML Enthusiast

## 📝 License


---

> If you like this project, give it a ⭐ on GitHub!
