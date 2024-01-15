"""
Here the GUI class is implemented.
"""
import tkinter as tk
import numpy as np


class Tic_Tac_Toe():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self, size_of_board, symbol_size, symbol_thickness, symbol_x_color, symbol_o_color, green_color):
        self.symbol_size = symbol_size
        self.size_of_board = size_of_board
        self.symbol_thickness = symbol_thickness
        self.symbol_x_color = symbol_x_color
        self.symbol_o_color = symbol_o_color
        self.green_color = green_color
        
        
        self.window = tk.Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = tk.Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_x_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_x_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.x_wins = False
        self.o_wins = False
        
        self.x_score = 0
        self.o_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * self.size_of_board / 3, 0, (i + 1) * self.size_of_board / 3, self.size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * self.size_of_board / 3, self.size_of_board, (i + 1) * self.size_of_board / 3)

    def play_again(self):
        self.initialize_board()
        self.player_x_starts = not self.player_x_starts
        self.player_x_turns = self.player_x_starts
        self.board_status = np.zeros(shape=(3, 3))

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        # Adjust the bounding box to account for the symbol_thickness
        offset = self.symbol_thickness / 2
        self.canvas.create_oval(
            grid_position[0] - self.symbol_size + offset, 
            grid_position[1] - self.symbol_size + offset,
            grid_position[0] + self.symbol_size - offset, 
            grid_position[1] + self.symbol_size - offset,
            width=self.symbol_thickness, 
            outline=self.symbol_o_color
        )

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        # Adjust the start and end points to account for the symbol_thickness
        offset = self.symbol_thickness / 2
        self.canvas.create_line(grid_position[0] - self.symbol_size + offset, grid_position[1] - self.symbol_size + offset,
                                grid_position[0] + self.symbol_size - offset, grid_position[1] + self.symbol_size - offset,
                                width=self.symbol_thickness, fill=self.symbol_x_color)
        self.canvas.create_line(grid_position[0] - self.symbol_size + offset, grid_position[1] + self.symbol_size - offset,
                                grid_position[0] + self.symbol_size - offset, grid_position[1] - self.symbol_size + offset,
                                width=self.symbol_thickness, fill=self.symbol_x_color)



    def display_gameover(self):

        if self.x_wins:
            self.x_score += 1
            text = 'Winner: Player 1 (X)'
            color = self.symbol_x_color
        elif self.o_wins:
            self.o_score += 1
            text = 'Winner: Player 2 (O)'
            color = self.symbol_o_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(self.size_of_board / 2, self.size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(self.size_of_board / 2, 5 * self.size_of_board / 8, font="cmr 40 bold", fill=self.green_color,
                                text=score_text)

        score_text = 'Player 1 (X) : ' + str(self.x_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.o_score) + '\n'
        score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(self.size_of_board / 2, 3 * self.size_of_board / 4, font="cmr 30 bold", fill=self.green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(self.size_of_board / 2, 15 * self.size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (self.size_of_board / 3) * logical_position + self.size_of_board / 6


    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (self.size_of_board / 3), dtype=int)


    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True


    def is_winner(self, player):

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False


    def is_tie(self):

        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie


    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.x_wins = self.is_winner('X')
        if not self.x_wins:
            self.o_wins = self.is_winner('O')

        if not self.o_wins:
            self.tie = self.is_tie()

        gameover = self.x_wins or self.o_wins or self.tie

        if self.x_wins:
            print('X wins')
        if self.o_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return gameover


    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.player_x_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_x_turns = not self.player_x_turns
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_x_turns = not self.player_x_turns

            # Check if game is concluded
            if self.is_gameover():
                self.display_gameover()
                # print('Done')
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False
            