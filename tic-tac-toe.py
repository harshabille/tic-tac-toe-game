from tkinter import *
import numpy as np

size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 15
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'
BG_COLOR = '#F1F2B5'
LINE_COLOR = '#6A0572'
WIN_COLOR = '#FFD700'
ANIMATION_SPEED = 10

class Tic_Tac_Toe():
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board, bg=BG_COLOR)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board, width=symbol_thickness, fill=LINE_COLOR)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3, width=symbol_thickness, fill=LINE_COLOR)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        for radius in range(0, int(symbol_size), ANIMATION_SPEED):
            self.canvas.create_oval(grid_position[0] - radius, grid_position[1] - radius,
                                    grid_position[0] + radius, grid_position[1] + radius, width=symbol_thickness,
                                    outline=symbol_O_color)
            self.window.update()
            self.canvas.delete('oval')
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        for i in range(0, int(2 * symbol_size), ANIMATION_SPEED):
            self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                    grid_position[0] - symbol_size + i, grid_position[1] - symbol_size + i, width=symbol_thickness,
                                    fill=symbol_X_color)
            self.canvas.create_line(grid_position[0] + symbol_size, grid_position[1] - symbol_size,
                                    grid_position[0] + symbol_size - i, grid_position[1] - symbol_size + i, width=symbol_thickness,
                                    fill=symbol_X_color)
            self.window.update()
            self.canvas.delete('line')
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    def display_gameover(self):
        if self.X_wins:
            self.X_score += 1
            text = 'Player 1 (X) Wins!'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Player 2 (O) Wins!'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'It\'s a Tie!'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 4, font="Helvetica 50 bold", fill=color, text=text, tags="result")

        score_text = 'Scores'
        self.canvas.create_text(size_of_board / 2, 2 * size_of_board / 4, font="Helvetica 40 bold", fill=Green_color, text=score_text, tags="result")

        score_text = f'Player 1 (X): {self.X_score}\nPlayer 2 (O): {self.O_score}\nTie: {self.tie_score}'
        self.canvas.create_text(size_of_board / 2, 2.5 * size_of_board / 4, font="Helvetica 30 bold", fill=Green_color, text=score_text, tags="result")
        
        countdown_text = 'Restarting in 5 seconds...'
        self.canvas.create_text(size_of_board / 2, 3.5 * size_of_board / 4, font="Helvetica 20 bold", fill="gray", text=countdown_text, tags="result")

        self.reset_board = True
        self.window.after(1000, self.update_countdown, 4)

    def update_countdown(self, count):
        if count >= 0:
            countdown_text = f'Restarting in {count} seconds...'
            self.canvas.delete("countdown")
            self.canvas.create_text(size_of_board / 2, 3.5 * size_of_board / 4, font="Helvetica 20 bold", fill="gray", text=countdown_text, tags="countdown")
            self.window.after(1000, self.update_countdown, count - 1)
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0]][logical_position[1]] != 0

    def is_winner(self, player):
        player = -1 if player == 'X' else 1
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True
        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True
        return False

    def is_tie(self):
        return not any(0 in row for row in self.board_status)

    def is_gameover(self):
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')
        if not self.O_wins:
            self.tie = self.is_tie()
        return self.X_wins or self.O_wins or self.tie

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_X_turns = not self.player_X_turns
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not self.player_X_turns
            if self.is_gameover():
                self.display_gameover()
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

game_instance = Tic_Tac_Toe()
game_instance.mainloop()
