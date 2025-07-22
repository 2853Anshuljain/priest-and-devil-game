import tkinter as tk
from tkinter import messagebox
import time
from collections import deque

class GameState:
    def __init__(self):
        self.p_left = 3
        self.d_left = 3
        self.p_right = 0
        self.d_right = 0
        self.boat = 'left'  # 'left' or 'right'
        self.boat_passengers = []
        self.history = []

    def is_valid(self):
        if (self.p_left > 0 and self.p_left < self.d_left):
            return False
        if (self.p_right > 0 and self.p_right < self.d_right):
            return False
        return True

    def move_boat(self):
        # Save current state for undo
        self.history.append((self.p_left, self.d_left, self.p_right, self.d_right, self.boat, list(self.boat_passengers)))

        for char in self.boat_passengers:
            if self.boat == 'left':
                if char == 'P':
                    self.p_left -= 1
                    self.p_right += 1
                else:
                    self.d_left -= 1
                    self.d_right += 1
            else:
                if char == 'P':
                    self.p_right -= 1
                    self.p_left += 1
                else:
                    self.d_right -= 1
                    self.d_left += 1

        self.boat = 'right' if self.boat == 'left' else 'left'
        self.boat_passengers = []
        return self.is_valid()

    def undo(self):
        if self.history:
            self.p_left, self.d_left, self.p_right, self.d_right, self.boat, self.boat_passengers = self.history.pop()
            return True
        return False

    def game_won(self):
        return self.p_left == 0 and self.d_left == 0

    def get_state_tuple(self):
        return (self.p_left, self.d_left, self.p_right, self.d_right, self.boat)

    def set_from_tuple(self, state):
        self.p_left, self.d_left, self.p_right, self.d_right, self.boat = state
        self.boat_passengers = []

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Priests and Devils")
        self.canvas = tk.Canvas(root, width=800, height=450, bg="lightblue")
        self.canvas.pack()
        self.state = GameState()
        self.step_count = 0
        self.start_time = time.time()

        self.info_label = tk.Label(root, text="Step: 0    Time: 0s", font=("Arial", 14))
        self.info_label.pack(pady=5)

        self.draw_scene()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.buttons = {}
        for i in range(3):
            self.buttons[f"P{i}_L"] = tk.Button(self.button_frame, text=f"Priest {i+1} (L)", command=lambda i=i: self.select_passenger('P', 'left', i))
            self.buttons[f"D{i}_L"] = tk.Button(self.button_frame, text=f"Devil {i+1} (L)", command=lambda i=i: self.select_passenger('D', 'left', i))
            self.buttons[f"P{i}_R"] = tk.Button(self.button_frame, text=f"Priest {i+1} (R)", command=lambda i=i: self.select_passenger('P', 'right', i))
            self.buttons[f"D{i}_R"] = tk.Button(self.button_frame, text=f"Devil {i+1} (R)", command=lambda i=i: self.select_passenger('D', 'right', i))

        for btn in self.buttons.values():
            btn.pack(side=tk.LEFT, padx=2)

        self.move_button = tk.Button(root, text="Move Boat", command=self.move_boat)
        self.move_button.pack(pady=5)

        self.undo_button = tk.Button(root, text="Undo", command=self.undo_move)
        self.undo_button.pack(pady=5)

        self.solve_button = tk.Button(root, text="Auto Solve (BFS)", command=self.auto_solve)
        self.solve_button.pack(pady=5)

    def select_passenger(self, char_type, side, idx):
        if self.state.boat != side:
            messagebox.showinfo("Invalid", f"Boat is on the {self.state.boat} side!")
            return
        if len(self.state.boat_passengers) >= 2:
            messagebox.showinfo("Full Boat", "Boat can only carry 2 characters!")
            return
        key = f"{char_type}{idx}_{side[0].upper()}"
        if self.buttons[key]['state'] == tk.DISABLED:
            messagebox.showinfo("Unavailable", f"{char_type} {idx+1} is not available on {side} side!")
            return
        self.state.boat_passengers.append(char_type)
        self.buttons[key]['state'] = tk.DISABLED
        self.draw_scene()

    def move_boat(self):
        if len(self.state.boat_passengers) == 0:
            messagebox.showinfo("Empty Boat", "Select at least one character to move!")
            return

        if not self.state.move_boat():
            self.draw_scene()
            self.update_info()
            messagebox.showerror("Game Over", "Priests got eaten by Devils! You lose!")
            self.root.quit()
        elif self.state.game_won():
            self.step_count += 1
            self.draw_scene()
            self.update_info()
            messagebox.showinfo("Victory", f"All priests and devils crossed safely in {self.step_count} steps and {int(time.time() - self.start_time)} seconds!")
            self.root.quit()
        else:
            self.step_count += 1
            self.update_buttons()
            self.draw_scene()
            self.update_info()

    def undo_move(self):
        if self.state.undo():
            self.step_count = max(0, self.step_count - 1)
            self.update_buttons()
            self.draw_scene()
            self.update_info()
        else:
            messagebox.showinfo("Undo", "No more moves to undo!")

    def update_info(self):
        elapsed = int(time.time() - self.start_time)
        self.info_label.config(text=f"Step: {self.step_count}    Time: {elapsed}s")

    def update_buttons(self):
        for key, btn in self.buttons.items():
            btn['state'] = tk.NORMAL

    def draw_scene(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 300, 800, 450, fill="green")
        self.canvas.create_rectangle(370, 260, 430, 300, fill="blue")  # river

        # Boat
        boat_x = 150 if self.state.boat == 'left' else 650
        self.canvas.create_rectangle(boat_x - 40, 260, boat_x + 40, 300, fill="black")
        for i, passenger in enumerate(self.state.boat_passengers):
            color = "white" if passenger == 'P' else "red"
            self.canvas.create_oval(boat_x - 30 + i*30, 230, boat_x - 10 + i*30, 250, fill=color)

        # Left side
        for i in range(self.state.p_left):
            self.canvas.create_oval(50 + i * 30, 200, 70 + i * 30, 220, fill="white")
        for i in range(self.state.d_left):
            self.canvas.create_oval(50 + i * 30, 230, 70 + i * 30, 250, fill="red")

        # Right side
        for i in range(self.state.p_right):
            self.canvas.create_oval(700 - i * 30, 200, 720 - i * 30, 220, fill="white")
        for i in range(self.state.d_right):
            self.canvas.create_oval(700 - i * 30, 230, 720 - i * 30, 250, fill="red")

    def auto_solve(self):
        visited = set()
        queue = deque()
        parent = {}

        init = self.state.get_state_tuple()
        queue.append(init)
        visited.add(init)
        parent[init] = None

        while queue:
            curr = queue.popleft()
            p_left, d_left, p_right, d_right, boat = curr

            for move in [(1,0), (2,0), (0,1), (0,2), (1,1)]:
                new_p_left, new_d_left, new_p_right, new_d_right = p_left, d_left, p_right, d_right
                if boat == 'left':
                    if move[0] > p_left or move[1] > d_left:
                        continue
                    new_p_left -= move[0]
                    new_d_left -= move[1]
                    new_p_right += move[0]
                    new_d_right += move[1]
                    new_boat = 'right'
                else:
                    if move[0] > p_right or move[1] > d_right:
                        continue
                    new_p_left += move[0]
                    new_d_left += move[1]
                    new_p_right -= move[0]
                    new_d_right -= move[1]
                    new_boat = 'left'

                new_state = (new_p_left, new_d_left, new_p_right, new_d_right, new_boat)

                if (new_p_left >= 0 and new_p_right >= 0 and new_d_left >= 0 and new_d_right >= 0 and
                    (new_p_left == 0 or new_p_left >= new_d_left) and
                    (new_p_right == 0 or new_p_right >= new_d_right) and
                    new_state not in visited):
                    queue.append(new_state)
                    visited.add(new_state)
                    parent[new_state] = curr

                    if new_p_left == 0 and new_d_left == 0:
                        path = []
                        while new_state:
                            path.append(new_state)
                            new_state = parent[new_state]
                        path.reverse()

                        for state in path[1:]:
                            self.state.set_from_tuple(state)
                            self.step_count += 1
                            self.draw_scene()
                            self.update_info()
                            self.root.update()
                            time.sleep(0.5)
                        messagebox.showinfo("Auto Solved", f"Solved in {self.step_count} steps and {int(time.time() - self.start_time)} seconds!")
                        return

if __name__ == '__main__':
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()
