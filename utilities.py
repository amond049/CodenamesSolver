# Importing the necessary modules
import sys
import tkinter as tk
from tkinter import ttk


# Creating the window
window = tk.Tk()
window.title("Codenames Board")
window.geometry('400x700')
window.resizable(False, False)

# The outer colour of the location card
outer_colour = ""

# The current colour being played
current_colour = ""

# This list will contain all the boards that have an outer colour of the one selected by the user
current_outer_board = []

# This list will contain the resultant boards after the user has indicated which colour cards are where
remaining_boards = []
# Creating a map between the colour in the text file and the appropriate background colour for the button
colour_dict = {"a": "#21272d", "b": "#085c88", "r": "#ba2710", "w": "#c6b394", "d": "#dec8a8"}



def print_value(*args):
    """
    This function will load the current_outer_board with all possible configurations of the outer colour chosen to avoid importing
    unnecessary configurations
    :param args: *args
    :return: None
    """
    global current_outer_board
    global remaining_boards
    global outer_colour

    outer_colour = text_variable.get()
    if outer_colour == "Blue":
        load_boards('outer_blue.txt')
        current_outer_board = outer_blue_boards
        remaining_boards = outer_blue_boards
        global current_colour
        current_colour = 'b'
    else:
        load_boards('outer_red.txt')
        current_outer_board = outer_red_boards
        remaining_boards = outer_red_boards
        current_colour = 'r'



def combo_box_read_only():
    """
    This function is just to create the necessary labels the user can click on to select the outer colour, change
    the colour currently being played and view hints when they get below a specific threshold of board possibilities
    :return: None
    """
    colour_chosen.config(state='disabled')

    for toggleButton in buttons:
        toggleButton.config(state='normal')

    colour_options_label_text = tk.StringVar()
    colour_options_label_text.set("You can select the colours here: ")
    colour_options_label = tk.Label(window, textvariable=colour_options_label_text)

    hint_label_text = tk.StringVar()
    hint_label_text.set("Once the possible number of boards start to reduce, \nyou will begin to see hints below indicating where the "
                        "next \ncorrect placement of your coloured card should be: ")
    hint_label = tk.Label(window, textvariable=hint_label_text)

    colour_options_label.place(x=10, y=510)
    hint_label.place(x=40, y=550)
    blue_button.config(width=2, height=1)
    red_button.config(width=2, height=1)
    bystander_button.config(width=2, height=1)

    blue_button.place(x=220, y=510)
    red_button.place(x=250, y=510)
    bystander_button.place(x=280, y=510)
    return ""


def change_colour(colour):
    """
    Utility function to change the colour of the background when a button is pressed
    :param colour: String, one of the values in the colour_dict dictionary
    :return:
    """
    global current_colour
    current_colour = colour


# Creating the label for the dropdown list
text_variable = tk.StringVar()
colour_chosen = ttk.Combobox(window, textvariable=text_variable)

# Creating the dropdown list
colour_chosen['values'] = ('Blue', 'Red')
colour_chosen.place(x=10,y=475)
text_variable.trace('w', print_value)

# Creating the confirm button
confirm_button = tk.Button()
confirm_button.config(text='Confirm', command=lambda: combo_box_read_only())
confirm_button.place(x=175, y=470)

# Creating the buttons for each colour
blue_button = tk.Button()
blue_button.config(bg=colour_dict['b'], width=1, height=1, command=lambda: change_colour("b"))

red_button = tk.Button()
red_button.config(bg=colour_dict['r'], width=1, height=1, command=lambda: change_colour("r"))

bystander_button = tk.Button()
bystander_button.config(bg=colour_dict['w'], width=1, height=1, command=lambda: change_colour("w"))


# List of buttons that will represent the configuration of the current playing board
buttons = []
outer_red_boards = []
outer_blue_boards = []

def rotate_90(original):
    """
    Because each board layout is in the shape of a square, there are 4 degrees of rotation, thus 4 configurations per card. To account for this
    we need to allow each configuration to be rotated. This function will rotate and map the placements to the correct rotated spots
    :param original: The original configuration of the board
    :return: The board after a 90 degree turn
    """
    copy_of_original = original[:]
    rotated_board = [None] * 25

    for index in range(25):
        # There are different equations for each row of the board
        if index <= 4:
            rotated_board[5 * index + 4] = copy_of_original[index]
        elif index in range(5, 10):
            rotated_board[5 * index - 22] = copy_of_original[index]
        elif index in range(10, 15):
            rotated_board[5 * index - 48] = copy_of_original[index]
        elif index in range(15, 20):
            rotated_board[5 * index - 74] = copy_of_original[index]
        else:
            rotated_board[5 * index - 100] = copy_of_original[index]
    return rotated_board


def load_boards(file_name):
    """
    Loading all the possible boards
    :param file_name: Name of the file to get the configurations from
    :return: None
    """
    outer_red_file = open(file_name, 'r')
    for line in outer_red_file:
        line_as_array = line.split(",")

        # Stripping the last line in the character of the newline (\n) character
        if "\n" in line_as_array[-1]:
            line_as_array[-1] = line_as_array[-1][0]

        # ROTATING 90 DEGREES CW (OR 270 CCW)
        board_after_90 = rotate_90(line_as_array)

        # ROTATING 180 DEGREES CW
        board_after_180 = rotate_90(board_after_90)

        # ROTATING 270 DEGREES CW (OR 90 DEGREES CCW)
        board_after_270 = rotate_90(board_after_180)

        # Loading the appropriate lists depending on the filename that was passed
        if file_name == 'outer_red.txt':
            outer_red_boards.append(line_as_array)
            outer_red_boards.append(board_after_90)
            outer_red_boards.append(board_after_180)
            outer_red_boards.append(board_after_270)
        else:
            outer_blue_boards.append(line_as_array)
            outer_blue_boards.append(board_after_90)
            outer_blue_boards.append(board_after_180)
            outer_blue_boards.append(board_after_270)


def check_for_win(possible_boards):
    """
    This function is only triggered when there is less than or equal to 5 possible boards, either displays hints when there are <= 5 possibilities
    or paints the board once there is only 1 possibility left for the configuration
    :return:
    """
    global outer_colour

    # This function works only if the person using the tool goes first. If the player is second, you can use the hints as a way of
    # learning which squares to avoid
    local_outer_colour = outer_colour
    if len(possible_boards) in range(2, 6):
        # To allow for hints, a dictionary is used to measure how often the colour shows up in each spot in the different boards for the chosen colour
        place_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0,
                      15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0}


        for each_possible_board in possible_boards:
            for cell in range(len(each_possible_board)):
                if each_possible_board[cell] == local_outer_colour[0].lower():
                    place_dict[cell] += 1

        # Checking to make sure that the most probable next spot is not already covered
        most_likely_button = -1
        while True:
            most_likely_button = max(zip(place_dict.values(), place_dict.keys()))[1]
            if buttons[most_likely_button].cget('bg') != colour_dict['d']:
                del place_dict[most_likely_button]
            else:
                break

        hint_label_text.set("The most likely place your next \ncard will be at position: " + str(most_likely_button) +
                            " For reference's sake, \nthe top left most button is button 0, the bottom \nright most button is button 24. ")
    elif len(possible_boards) == 1:
        # Should set the buttons to no longer do anything and then set the background colour of each button to
        # the correct colour according to the template (for lack of a better word)
        for i in range(25):
            buttons[i].config(bg=colour_dict[possible_boards[0][i]])
        pass
    else:
        pass

def calculate_boards(number):
    """
    Given the button that was just clicked upon, find all boards that have that specific colour in that exact position among all of the remaining boards
    :param number: The index of the button in the board list
    :return:
    """
    global remaining_boards
    temp_boards = []

    # This is so that you can't go over the same button twice. If you make a mistake, unfortunate, time to restart
    buttons[number].config(state='disabled')
    for board in remaining_boards:
        if board[number] == current_colour:
            temp_boards.append(board)

    # Should not be possible to get to 0 boards unless the user messed up in some way
    if len(temp_boards) == 0:
        print("I don't know how you've ended up in this situation, this should be impossible. Congrats, I guess. ")
        sys.exit()
    remaining_boards = temp_boards

    buttons[number].config(bg=colour_dict[current_colour])
    check_for_win(remaining_boards)


# Creating the board
for i in range(25):
    button = tk.Button()
    buttons.append(button)
    # Have now generated all possible boards, colouring each button the default colour of the card
    button.config(bg=colour_dict["d"])
    button.config(height=5, width=10, command=lambda buttonNumber = i: calculate_boards(buttonNumber), state='disabled')
    button.grid(row=i // 5, column=i % 5)

# Creating some necessary labels and placing them on the screen
outer_colour_label_text = tk.StringVar()
outer_colour_label_text.set("Enter the outer colour: ")
outer_colour_label = tk.Label(window, textvariable=outer_colour_label_text)
outer_colour_label.place(x=10, y=440)

hint_label_text = tk.StringVar()
hint_label_text.set("")
hint_label = tk.Label(window, textvariable=hint_label_text)
hint_label.place(x=60, y=625)
window.mainloop()

