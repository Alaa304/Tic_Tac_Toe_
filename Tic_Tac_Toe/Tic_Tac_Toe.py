import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg="black")

        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"  

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root, bg="black")
        frame.pack()

        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text="", font=("Arial", 40), width=5, height=2,
                                command=lambda row=i, col=j: self.click(row, col),
                                bg="black", fg="white", activebackground="gray")
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn

       
        reset_btn = tk.Button(self.root, text="Restart", font=("Arial", 20),
                              command=self.reset_game,
                              bg="gray", fg="white", activebackground="white")
        reset_btn.pack(pady=10)

    def click(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            color = "purple" if self.current_player == "X" else "yellow"
            self.buttons[row][col].config(text=self.current_player, fg=color)

            winner = self.check_winner()
            if winner:
                self.disable_buttons()
                messagebox.showinfo("Game Over", f"{winner} wins!")
            elif self.is_full():
                messagebox.showinfo("Game Over", "It's a tie!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O":
                    self.root.after(500, self.computer_move)

    def computer_move(self):
        best_score = -float("inf")
        move = None

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(False, -float("inf"), float("inf"))
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        move = (i, j)

        if move:
            self.click(move[0], move[1])

    def minimax(self, is_max, alpha, beta):
        winner = self.check_winner()
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif self.is_full():
            return 0

        if is_max:
            max_eval = -float("inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        eval = self.minimax(False, alpha, beta)
                        self.board[i][j] = ""
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float("inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        eval = self.minimax(True, alpha, beta)
                        self.board[i][j] = ""
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def check_winner(self):
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] != "":
                return b[i][0]
            if b[0][i] == b[1][i] == b[2][i] != "":
                return b[0][i]

        if b[0][0] == b[1][1] == b[2][2] != "":
            return b[0][0]
        if b[0][2] == b[1][1] == b[2][0] != "":
            return b[0][2]
        return None

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell == "":
                    return False
        return True

    def disable_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state=tk.DISABLED)

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state=tk.NORMAL, fg="white")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
