"""
This is the main script. Some variables are defined and the main window is created.
"""

from gui import Tic_Tac_Toe


# Defining vairables
size_of_board = 1200
symbol_size = (size_of_board / 3) *0.6 / 2
symbol_thickness =25
symbol_x_color = '#EE4035'
symbol_o_color = '#0492CF'
green_color = '#7BC043'


game = Tic_Tac_Toe(size_of_board, symbol_size, symbol_thickness, symbol_x_color, symbol_o_color, green_color)
game.mainloop()