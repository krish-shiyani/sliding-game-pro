# 🧩 Pro Slider: Leaderboard Edition

A modern, sleek 15-puzzle sliding tile game developed in Python using the standard `turtle` graphics library. Features interactive mouse and keyboard controls, customizable difficulty modes, a guaranteed-solvable shuffle algorithm, and a persistent local leaderboard.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Game Objective & Rules](#game-objective--rules)
- [Difficulty Levels](#difficulty-levels)
- [Controls](#controls)
- [Installation & Setup](#installation--setup)
- [How to Play](#how-to-play)
- [Project Structure](#project-structure)
- [Code Architecture](#code-architecture)
- [Customization](#customization)
- [Leaderboard System](#leaderboard-system)
- [Troubleshooting](#troubleshooting)
- [Author & Credits](#author--credits)

---

## 🌟 Overview

The **15-Puzzle** is a classic sliding puzzle consisting of a 4×4 frame of numbered square tiles in random order, with one tile missing. The object of the puzzle is to place the tiles in order by making sliding moves that use the empty space.

**Sliding Game Pro** enhances the classic experience with:
- A modern dark-mode aesthetic with neon teal accents.
- Responsive graphical interface built with Python's built-in `turtle` module.
- Zero external third-party dependencies required.
- Robust state management with automated score tracking and leaderboard persistence.

---

## ✨ Key Features

- **🎯 Guaranteed Solvable Boards**: Rather than arbitrary permutation (which has a 50% chance of being mathematically unsolvable), the game shuffles backwards from the solved state using valid adjacent tile swaps.
- **🎮 Hybrid Controls**: Move tiles with intuitive **mouse clicks** or keyboard **arrow keys**.
- **📊 Real-time HUD**: Track your move count and current difficulty dynamically on screen.
- **🏆 Persistent Multi-Difficulty Leaderboard**: High scores (Player Name, Moves, Duration in Seconds, Difficulty) are automatically recorded in `leaderboard_multi.json`.
- **🥇 Top-5 High Score Display**: Filtered by difficulty and ranked primarily by lowest move count, then fastest time.
- **🎨 Modern Dark Palette**: Designed with a polished cyberpunk/dark UI palette (`#1A1A1D`, `#4E4E50`, `#66FCF1`).
- **⚡ Lightweight & Pure Python**: Runs out of the box using standard libraries (`turtle`, `random`, `time`, `json`, `os`).

---

## 🎯 Game Objective & Rules

Arrange the tiles sequentially from **1 to 15**, starting at the top-left corner and ending with the empty space at the bottom-right corner.

### Solved State Layout
```text
┌────┬────┬────┬────┐
│  1 │  2 │  3 │  4 │
├────┼────┼────┼────┤
│  5 │  6 │  7 │  8 │
├────┼────┼────┼────┤
│  9 │ 10 │ 11 │ 12 │
├────┼────┼────┼────┤
│ 13 │ 14 │ 15 │ [ ]│
└────┴────┴────┴────┘
```

- Only tiles horizontally or vertically adjacent to the empty slot can be slid into the empty slot.
- Diagonal movements are not permitted.

---

## 🎚️ Difficulty Levels

When starting the game, you can select one of three preset difficulties:

| Difficulty | Shuffle Steps | Description | Recommended For |
|:-----------|:-------------:|:------------|:----------------|
| **Easy**   | 15 steps      | Gentle scramble close to solved state | Beginners / Warm-up |
| **Medium** | 60 steps      | Moderate complexity | Balanced challenge |
| **Hard**   | 150 steps     | Deeply scrambled board | Experienced puzzle solvers |

---

## 🕹️ Controls

| Action | Input | Description |
|:-------|:------|:------------|
| **Click Tile** | `Left Mouse Click` | Click on any tile adjacent to the empty space to slide it. |
| **Slide Up** | `↑` (Up Arrow) | Moves the tile **below** the empty space **up** into it. |
| **Slide Down** | `↓` (Down Arrow) | Moves the tile **above** the empty space **down** into it. |
| **Slide Left** | `←` (Left Arrow) | Moves the tile to the **right** of the empty space **left** into it. |
| **Slide Right** | `→` (Right Arrow) | Moves the tile to the **left** of the empty space **right** into it. |
| **Restart / Menu** | `R` key | Returns to the difficulty menu and lets you re-enter your player name. |

---

## 💻 Installation & Setup

### Prerequisites
- **Python 3.6+** installed on your system.
- Standard Tkinter library (required for Python's `turtle` module).

> [!NOTE]
> On most Windows and macOS Python installations, Tkinter is bundled by default. On Linux (Ubuntu/Debian), you may need to install `python3-tk` if not already installed:
> ```bash
> sudo apt-get update && sudo apt-get install python3-tk
> ```

### Clone Repository
```bash
git clone https://github.com/krish-shiyani/sliding-game-pro.git
cd sliding-game-pro
```

---

## 🚀 How to Play

1. **Launch the game**:
   ```bash
   python3 slider1.py
   ```
2. **Enter your name**: A prompt window will appear asking for your name (defaults to "Guest" if left blank).
3. **Select difficulty**: Click on `Easy`, `Medium`, or `Hard` button on the main screen.
4. **Solve the puzzle**: Slide the tiles using mouse clicks or the arrow keys.
5. **View high score**: When completed, your stats will be recorded to the leaderboard and the Top 5 scores for that difficulty will be shown.
6. **Play again**: Press `R` at any time to return to the main menu.

---

## 📁 Project Structure

```text
sliding-game-pro/
├── README.md                 # Project documentation
├── slider1.py                # Main game source code (GUI, game loop, logic)
└── leaderboard_multi.json    # JSON storage for high scores
```

---

## 🏗️ Code Architecture

The entire game logic is contained in [slider1.py](file:///home/krish-shiyani/Desktop/Code/webDev/sliding-game-pro/slider1.py) inside the `SlidingPuzzle` class:

### Core Methods Breakdown

| Method | Role |
|:-------|:-----|
| `__init__()` | Sets up screen dimensions, turtle canvas, event listeners for mouse and keys, and launches the menu. |
| `show_menu()` | Prompts the user for their name via a dialog box and renders the difficulty selection screen. |
| `draw_menu()` | Draws the clickable interactive difficulty buttons (`Easy`, `Medium`, `Hard`). |
| `setup_game(diff_name, steps)` | Generates the 4x4 matrix, executes random valid walk moves to guarantee solvability, and records start time. |
| `handle_click(x, y)` | Maps mouse canvas coordinates to grid `(row, col)` or menu button bounds. |
| `move_by_key(key)` | Handles keyboard arrow inputs, calculating the adjacent tile to swap with the empty space. |
| `perform_move(r, c)` | Swaps target tile coordinates with empty space, increments move count, checks for win, and redraws the board. |
| `check_win()` | Checks if flattened board matches `[1, 2, ..., 15, 0]`. Triggers `save_score()` upon victory. |
| `save_score()` | Appends the player's run to `leaderboard_multi.json` and sorts entries by `moves ASC`, then `time ASC`. |
| `draw_leaderboard()` | Filters top 5 records for the current difficulty and displays them on the victory screen. |
| `draw_tile(row, col, value)` | Uses turtle stamping to draw rounded square tiles and write numerical labels. |
| `draw_everything()` | Refreshes canvas with current HUD (mode, moves), all tiles, and win overlay when solved. |

---

## 🎨 Customization

You can easily customize game appearance and behavior by modifying the constants at the top of [slider1.py](file:///home/krish-shiyani/Desktop/Code/webDev/sliding-game-pro/slider1.py):

```python
# Screen and Grid Dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GRID_SIZE = 4       # Grid size (4x4)
TILE_SIZE = 110     # Size of each square tile
GAP = 8             # Spacing between tiles
BOARD_OFFSET_Y = -100

# Color Scheme
COLORS = {
    "bg": "#1A1A1D",      # Window background color
    "tile": "#4E4E50",    # Numbered tile color
    "text": "#66FCF1",    # Neon accent & text color
    "empty": "#1A1A1D",   # Empty slot color
    "accent": "#C5C6C7",  # Border & secondary text
    "win": "#45A29E",     # Victory message color
    "btn": "#1F2833"      # Button background
}
```

---

## 🏆 Leaderboard System

High scores are saved locally in `leaderboard_multi.json`.

### Sample JSON Entry:
```json
[
  {
    "name": "kishna",
    "moves": 31,
    "time": 25,
    "difficulty": "Easy"
  }
]
```

- **Sorting Criteria**:
  1. `moves`: Primary sorting key (fewer moves rank higher).
  2. `time`: Secondary sorting key (less time in seconds breaks ties).
- **Filter**: Only entries matching the played difficulty level are displayed on the victory screen.

---

## ❓ Troubleshooting

### 1. `_tkinter.TclError: no display name and no $DISPLAY environment variable`
If running on a headless Linux server or via SSH, `turtle` requires an X11 graphical display. Run the game from a desktop terminal or configure X11 forwarding (`ssh -X`).

### 2. `ModuleNotFoundError: No module named '_tkinter'`
On Ubuntu/Debian, install the Tkinter package:
```bash
sudo apt update && sudo apt install python3-tk
```
On Fedora:
```bash
sudo dnf install python3-tkinter
```
On Arch Linux:
```bash
sudo pacman -S tk
```

---

## 👤 Author & Credits

- **Author**: Krish Shiyani
- **Repository**: [sliding-game-pro](https://github.com/krish-shiyani/sliding-game-pro)
- **License**: Open Source for educational and personal use.