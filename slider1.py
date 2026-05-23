import turtle
import random
import time
import json
import os

# --- CONSTANTS ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GRID_SIZE = 4
TILE_SIZE = 110
GAP = 8
BOARD_OFFSET_Y = -100
LB_FILE = "leaderboard_multi.json"

COLORS = {
    "bg": "#1A1A1D",
    "tile": "#4E4E50",
    "text": "#66FCF1",
    "empty": "#1A1A1D",
    "accent": "#C5C6C7",
    "win": "#45A29E",
    "btn": "#1F2833"
}

class SlidingPuzzle:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.title("Pro Slider: Leaderboard Edition")
        self.screen.bgcolor(COLORS["bg"])
        self.screen.tracer(0)

        self.player_name = ""
        self.difficulty = "Medium"
        self.shuffle_steps = 60
        self.moves = 0
        self.start_time = 0
        self.board = []
        self.empty_pos = (3, 3)
        self.is_won = False
        self.in_menu = True
        
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.penup()
        
        # Difficulty Button Areas: (x_min, x_max, y_min, y_max, label, steps)
        self.buttons = [
            (-100, 100, 40, 90, "Easy", 15),
            (-100, 100, -30, 20, "Medium", 60),
            (-100, 100, -100, -50, "Hard", 150)
        ]

        self.show_menu()
        
        # Controls
        self.screen.onclick(self.handle_click)
        self.screen.onkey(lambda: self.move_by_key("Up"), "Up")
        self.screen.onkey(lambda: self.move_by_key("Down"), "Down")
        self.screen.onkey(lambda: self.move_by_key("Left"), "Left")
        self.screen.onkey(lambda: self.move_by_key("Right"), "Right")
        self.screen.onkey(self.show_menu, "r")
        self.screen.listen()
        
        self.screen.mainloop()

    def show_menu(self):
        self.in_menu = True
        self.is_won = False
        self.pen.clear()
        
        # Get Name
        self.player_name = self.screen.textinput("Name", "Enter your name:") or "Guest"
        self.screen.listen() # Re-focus after input
        
        self.draw_menu()

    def draw_menu(self):
        self.pen.clear()
        self.pen.color(COLORS["text"])
        self.pen.goto(0, 150)
        self.pen.write("SELECT DIFFICULTY", align="center", font=("Arial", 24, "bold"))
        
        for x1, x2, y1, y2, label, _ in self.buttons:
            # Draw Button Box
            self.pen.goto(x1, y1)
            self.pen.pendown()
            self.pen.color(COLORS["accent"])
            for _ in range(2):
                self.pen.forward(x2-x1)
                self.pen.left(90)
                self.pen.forward(y2-y1)
                self.pen.left(90)
            self.pen.penup()
            
            # Button Label
            self.pen.goto((x1+x2)/2, y1 + 10)
            self.pen.write(label, align="center", font=("Arial", 16, "bold"))
            
        self.screen.update()

    def setup_game(self, diff_name, steps):
        self.in_menu = False
        self.difficulty = diff_name
        self.shuffle_steps = steps
        self.moves = 0
        self.is_won = False
        self.start_time = time.time()
        
        # Reset Board
        nums = list(range(1, 16)) + [0]
        self.board = [nums[i:i+4] for i in range(0, 16, 4)]
        self.empty_pos = (3, 3)
        
        # Shuffle
        for _ in range(self.shuffle_steps):
            r, c = self.empty_pos
            adj = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
            valid = [(nr, nc) for nr, nc in adj if 0 <= nr < 4 and 0 <= nc < 4]
            tr, tc = random.choice(valid)
            self.board[r][c], self.board[tr][tc] = self.board[tr][tc], self.board[r][c]
            self.empty_pos = (tr, tc)
        
        self.draw_everything()

    def move_by_key(self, key):
        if self.is_won or self.in_menu: return
        r, c = self.empty_pos
        
        # Determine which tile wants to move into the empty spot
        target_r, target_c = r, c
        if key == "Up": target_r = r + 1
        elif key == "Down": target_r = r - 1
        elif key == "Left": target_c = c + 1
        elif key == "Right": target_c = c - 1
        
        if 0 <= target_r < 4 and 0 <= target_c < 4:
            self.perform_move(target_r, target_c)

    def handle_click(self, x, y):
        if self.in_menu:
            for x1, x2, y1, y2, label, steps in self.buttons:
                if x1 < x < x2 and y1 < y < y2:
                    self.setup_game(label, steps)
            return

        if self.is_won: return
        
        # Grid detection for mouse clicks
        start_x = -((GRID_SIZE * TILE_SIZE) / 2)
        start_y = ((GRID_SIZE * TILE_SIZE) / 2) + BOARD_OFFSET_Y
        col, row = int((x - start_x) // TILE_SIZE), int((start_y - y) // TILE_SIZE)
        
        if 0 <= row < 4 and 0 <= col < 4:
            er, ec = self.empty_pos
            if abs(row - er) + abs(col - ec) == 1:
                self.perform_move(row, col)

    def perform_move(self, r, c):
        er, ec = self.empty_pos
        self.board[er][ec], self.board[r][c] = self.board[r][c], self.board[er][ec]
        self.empty_pos = (r, c)
        self.moves += 1
        self.check_win()
        self.draw_everything()

    def check_win(self):
        flat = [val for row in self.board for val in row]
        if flat == list(range(1, 16)) + [0]:
            self.is_won = True
            self.save_score()

    def save_score(self):
        duration = int(time.time() - self.start_time)
        new_entry = {"name": self.player_name, "moves": self.moves, "time": duration, "difficulty": self.difficulty}
        
        scores = []
        if os.path.exists(LB_FILE):
            with open(LB_FILE, "r") as f: scores = json.load(f)
        
        scores.append(new_entry)
        # Sort by moves then time
        scores.sort(key=lambda x: (x["moves"], x["time"]))
        with open(LB_FILE, "w") as f: json.dump(scores, f)

    def draw_leaderboard(self):
        self.pen.clear()
        self.pen.color("white")
        self.pen.goto(0, 50)
        self.pen.write(f"--- {self.difficulty.upper()} LEADERBOARD ---", align="center", font=("Arial", 16, "bold"))
        
        if os.path.exists(LB_FILE):
            with open(LB_FILE, "r") as f: 
                all_scores = json.load(f)
            
            # Filter only current difficulty
            filtered = [s for s in all_scores if s.get("difficulty") == self.difficulty][:5]
            
            y_pos = 10
            for i, s in enumerate(filtered):
                y_pos -= 25
                self.pen.goto(0, y_pos)
                color = COLORS["text"] if s["name"] == self.player_name else "white"
                self.pen.color(color)
                self.pen.write(f"#{i+1} {s['name'][:10]:<10} {s['moves']} moves", align="center", font=("Courier", 12, "normal"))

    def draw_tile(self, row, col, value):
        start_x = -((GRID_SIZE * TILE_SIZE) / 2) + (TILE_SIZE / 2)
        start_y = ((GRID_SIZE * TILE_SIZE) / 2) - (TILE_SIZE / 2) + BOARD_OFFSET_Y
        x, y = start_x + (col * TILE_SIZE), start_y - (row * TILE_SIZE)
        
        self.pen.goto(x, y)
        self.pen.shape("square")
        self.pen.shapesize((TILE_SIZE - GAP) / 20)
        self.pen.color(COLORS["tile"] if value != 0 else COLORS["empty"])
        self.pen.stamp()
        
        if value != 0:
            self.pen.color(COLORS["text"])
            self.pen.goto(x, y - 18)
            self.pen.write(value, align="center", font=("Arial", 22, "bold"))

    def draw_everything(self):
        if self.in_menu: return
        self.pen.clear()
        
        # HUD
        self.pen.color(COLORS["text"])
        self.pen.goto(-260, 320)
        self.pen.write(f"Mode: {self.difficulty}", align="left", font=("Arial", 14, "bold"))
        self.pen.goto(260, 320)
        self.pen.write(f"Moves: {self.moves}", align="right", font=("Arial", 14, "bold"))
        
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.draw_tile(r, c, self.board[r][c])
        
        if self.is_won:
            self.pen.goto(0, 100)
            self.pen.color(COLORS["win"])
            self.pen.write("SOLVED!", align="center", font=("Arial", 30, "bold"))
            self.draw_leaderboard()
            self.pen.color("white")
            self.pen.goto(0, -350)
            self.pen.write("Press 'R' to return to menu", align="center", font=("Arial", 12, "italic"))
            
        self.screen.update()

if __name__ == "__main__":
    SlidingPuzzle()
