#!/bin/env python3
# Copyright (c) Anand Krishnamoorthi
# Licensed under the MIT License.

# Lenth of the solution word.
WORD_LENGTH = 5

# Check whether a word is valid.
def is_valid(word):
    # The word must be of desired length.
    if len(word) != WORD_LENGTH:
        return False

    # The word should not contain non alphabet characters.
    # E.g: ' , " 6
    if not word.isalpha():
        return False

    # Ignore words that contain foregin characters.
    if not word.isascii():
        return False

    # Otherwise, it is a valid word.
    return True

# Use the import statement to import a module so that we can use its
# functionality.
import sys

# If '--is-valid <word>' is passed as the arguments to the program,
# check whether the given word is valid.
if len(sys.argv) == 3 and sys.argv[1] == '--is-valid':
    word = sys.argv[2]
    b = is_valid(word)
    print("valid" if b else "invalid")
    sys.exit(0)

# Words are maintained in a plain-text file. Each line in the file
# consists of a word. There are two files. For each game, a word is
# randomly selected from the solution words file. The player can make
# guesses using words from either file.
SOLUTION_WORDS_FILE = './solution_words.txt'
GUESS_WORDS_FILE = './guess_words.txt'

# Define a function to read all words from a file.
def load_words(words_file):
    # Create an empty list. We will use this list to store the words.
    words = []

    # Use the `with open` to open given file. The file will be
    # automatically closed at the end of this block.
    with open(words_file, 'r') as f:
        # readlines function reads the entire file and returns
        # all the lines as a list. Iterate through the list.
        for line in f.readlines():
            # Remove any leading and trailing spaces in the line.
            line = line.strip()

            # If the line starts with #, treat it as a comment and ignore it.
            # Make sure to handle empty lines.
            if len(line) > 0 and line[0] == '#':
                continue

            # The line is a word.
            word = line

            # Ignore invalid words
            if not is_valid(word):
                continue

            # Convert the word to upper case and add it to list of words.
            # By converting to uppercase every where, we need to deal with
            # only one case of letters.
            words.append(word.upper())

    # Return list of words to caller.
    return words

# Load both sets of words. Sort them alphabetically.
solution_words = sorted(load_words(SOLUTION_WORDS_FILE))
guess_words    = sorted(load_words(GUESS_WORDS_FILE))

# Create a set of all words. A set is much faster than a list of checking whether
# a given word exists in the set. First add guess words to the set.
# Then update the set with solution words.
all_words = set(guess_words)
all_words.update(solution_words)

# If '--print-solution-words' is passed as the 1st argument to the program,
# we will print all the solution words.
if len(sys.argv) == 2 and sys.argv[1] == '--print-solution-words':
    print(solution_words)
    sys.exit(0)

# Similarly, if '--print-guess-words' is passed as the 1st argument, we will
# print all the guess words.
if len(sys.argv) == 2 and sys.argv[1] == '--print-guess-words':
    print(guess_words)
    sys.exit(0)

# Handle '--print-all-words' too.
if len(sys.argv) == 2 and sys.argv[1] == '--print-all-words':
    print(all_words)
    sys.exit(0)

# Each letter in a guess can have 3 results.
# The result is correct, if the letter is found in the same location in the
# solution. The result is misplaced, if the letter is found in the solution
# but at a different location. The result is wrong, it the letter is not
# found in the solution.
CORRECT   = 'green'
MISPLACED = 'orange'
INCORRECT = 'gray'

# The following is a function to grade an a guess.
def grade_guess(guess, solution):
    # Create a list to hold the result for each letter.
    # By default, assign no grade to each letter.
    grades = [None] * WORD_LENGTH

    # First look for all correct letters.
    for i in range(0, WORD_LENGTH):
        if guess[i] == solution[i]:
            grades[i] = CORRECT
            # Remove character from solution since it is matched.
            solution = solution[:i] + ' ' + solution[i+1:]

    # Now find misplaced letters.
    for i in range(0, WORD_LENGTH):
        if grades[i] != CORRECT:
            # Get current letter.
            ch = guess[i]
            # Find the position of the character in the solution
            pos = solution.find(ch)

            # The find function will return -1 if the character is not found in
            # a string. Otherwise it will return the position of the first
            # occurance of the character.
            if pos != -1:
                # If the character exists in the solution, then it is misplaced.
                grades[i] = MISPLACED
                # Remove the character from the solution by marking it
                # as '*' so that it will not be found again.
                # The original solution is not modified; a copy is created.
                solution = solution[:pos] + ' ' + solution[pos+1:]
            else:
                # The character does not exist in the solution.
                grades[i] = INCORRECT

    return grades

# If '--grade guess solution' is supplied in the command line, then grade the
# guess and print the grades.
# Example: --grade haven never
#          --grade steel never
if len(sys.argv) == 4 and sys.argv[1] == '--grade':
    guess = sys.argv[2]
    solution = sys.argv[3]
    grades = grade_guess(guess, solution)
    print(grades)
    sys.exit(0)

# The `random` module provides function to select (sample) a value randomly.
import random

# It is good practice to `seed` the random module so that the selections are
# truly random. The seed the random module, we use the os module to generate
# 512 random bytes.
import os
seed_value = os.urandom(512)
random.seed(seed_value)

# If --seed is supplied, then print the seed value.
if len(sys.argv) == 2 and sys.argv[1] == '--seed':
    print(seed_value)
    sys.exit(0)

# If --random is supplied, then print a random value.
if len(sys.argv) == 2 and sys.argv[1] == '--seed':
    print(seed_value)
    sys.exit(0)

# The number of allowed attempts is one more than word length
NUM_ATTEMPTS = 1 + WORD_LENGTH

# Here is the textual version of the game
def textual_game():
    # Select a word at random
    solution = random.choice(solution_words)

    # Initially all the letters for 'A' to 'Z' are assumed to be possible
    # in the solution.
    possible_letters = [chr(ch) for ch in range(ord('A'), ord('Z')+1)]

    # Repeat the following NUM_ATTEMPT times
    attempt = 0
    while attempt < NUM_ATTEMPTS:
        # Get a guess from the player.
        # Read a line form the standard input
        print('Enter guess: ', end='', flush=True)
        line = sys.stdin.readline()

        # Remove white space and capitalize.
        guess = line.strip().upper()

        # Ensure that the guess is a valid word.
        if not is_valid(guess):
            print('Invalid input. Reenter.')
            continue

        # Check whether the guess is in allowed words.
        if not guess in all_words:
            print('Not a word. Reenter.')
            continue

        # Grade the guess
        grades = grade_guess(guess, solution)

        # If all the letters are correct, then the player has won.
        if grades == [CORRECT] * WORD_LENGTH:
            print('!!! YOU WON !!!')
            return

        # If not all guesses are correct, print the grades.
        print(grades)

        # Print letters that can be used.
        for i, ch in enumerate(guess):
            if grades[i] == INCORRECT:
                # Remove, incorrect letters from list of possible letters
                possible_letters = [c for c in possible_letters if c != ch]

        print('Possible letters: %s' % str(possible_letters))
        # Next attempt
        attempt += 1

    # If all the attempts have failed, then the player has lost.
    print('!!! YOU LOST !!!')
    print('The word was %s' % solution)


# If --play is supplied, then do one textual game.
if len(sys.argv) == 2 and sys.argv[1] == '--play':
    textual_game()
    sys.exit(0)

# The curses module is used to create terminal-based applications.
from curses import *
import curses

# A curses application is a function that is passed to curses.wrapper.
# The wrapper performs necessary initialization, creates a screen and calls app
# with the screen. The wrapper also takes care of any necessary cleanup.
def app(screen):
    # In curses, for each character a color pair (foreground and background
    # colors) can be specified. The color pair must first be registered.

    # Create color pairs for correct, misplaced and incorrect letters.
    init_pair(1, COLOR_BLACK, COLOR_GREEN)
    init_pair(2, COLOR_BLACK, COLOR_YELLOW)
    init_pair(3, COLOR_BLACK, COLOR_WHITE)

    # Create a map of colors. Each key in the table is the grade of a letter.
    # The value is the color pair and boldness for the character.
    colors = {
        CORRECT   : color_pair(1) + A_BOLD,
        MISPLACED : color_pair(2) + A_BOLD,
        INCORRECT : color_pair(3)
    }

    # Draw winner message
    def draw_you_won(row, col):
        screen.addstr(row, col + 3, ' CONGRATS! ', colors[CORRECT])
        screen.addstr(row+1, col + 4, 'YOU WON!', colors[CORRECT])
        screen.refresh()

    # If --you-won is supplied draw a guess on the screen
    if len(sys.argv) == 2 and sys.argv[1] == '--you-won':
        draw_you_won(5, 10)
        napms(1000)
        sys.exit(0)

    # Draw lost message
    def draw_you_lost(row, col, solution):
        screen.addstr(row, col + 3, ' SORRY, YOU LOST! ', colors[INCORRECT])
        screen.addstr(row+1, col + 5, 'ANSWER: ', colors[INCORRECT])
        screen.addstr(row+1, col + 12, solution, colors[CORRECT])
        screen.refresh()

    # If --you-lost is supplied draw a guess on the screen
    if len(sys.argv) == 2 and sys.argv[1] == '--you-lost':
        draw_you_lost(5, 10, 'TERML')
        napms(1000*3)
        sys.exit(0)

    # The following function displays a guess at a given row and column on the
    # screen.
    def draw_guess(row, col, guess, grades):
        # Iterate through each letter in the guess and its grade.
        for ch, g in zip(guess, grades):
            # Call addstr to display the letter with appropriate color.
            screen.addstr(row, col-1, ' ' + ch + ' ', colors[g])
            col += 3
            screen.refresh()
            # Wait for sometime
            napms(100)

    # If --draw-guess is supplied draw a guess on the screen
    if len(sys.argv) == 2 and sys.argv[1] == '--draw-guess':
        solution = random.choice(solution_words)
        guess    = random.choice(guess_words)
        grades   = grade_guess(guess, solution)
        draw_guess(5, 10, guess, grades)
        screen.refresh()
        napms(1000)
        sys.exit(0)

    # Read a character at a given row and column
    def read_char(row, col):
        while True:
            # Read a character at location.
            key = screen.getch(row, col)

            # Convert the key code to a character.
            try:
                ch = chr(key)
                # Check if character is valid. The character must be valid
                # English alphabet.
                if ch.isalpha() and ch.isascii():
                    return ch.upper()

                # Return '\b' for backspace
                if ch in [chr(8), chr(KEY_BACKSPACE)]:
                    return '\b'

            except:
                # Ignore key
                pass

    # If --read-char is supplied read a valid character at given location.
    if len(sys.argv) == 2 and sys.argv[1] == '--read-char':
        # Read a character.
        ch = read_char(5, 10)
        # Display the character and refresh the screen.
        screen.addstr(5, 10, ch)
        screen.refresh()
        # Wait for a bit.
        napms(1000)
        sys.exit(0)

    # The following function reads a guess at a given row and column
    def read_guess(row, col):
        # Save the starting column
        start_col = col

        # Initialize guess to empty string.
        guess = ''

        # Loop forever
        while True:
            # Read a character at location.
            ch = read_char(row, col)
            if ch == '\b':
                # Backspace pressed.
                if col > start_col:
                    # Move to previous character's location and erase it by
                    # writing space characters.
                    col -= 3
                    screen.addstr(row, col, '  ')
                    # Remove character from guess
                    guess = guess[:-1]
            else:
                # The character is valid. Add it to the guess.
                guess += ch

                # Draw the character.
                screen.addstr(row, col-1, ' ' + ch + ' ')

                # Move to next character.
                col += 3

                # Check if all the characters in the guess have been read.
                if len(guess) == WORD_LENGTH:
                    # Check if the guess is valid.
                    if guess in all_words:
                        return guess

                    # The guess is not a valid word.
                    # Erase the guess.
                    guess = ''
                    col = start_col
                    screen.addstr(row, col, '   ' * WORD_LENGTH)

    # If --read-guess is supplied, read a guess and grade it.
    if len(sys.argv) == 2 and sys.argv[1] == '--read-guess':
        solution = random.choice(solution_words)
        guess    = read_guess(5, 10)
        grades   = grade_guess(guess, solution)
        draw_guess(5, 10, guess, grades)
        screen.refresh()
        napms(1000)
        sys.exit(0)

    # A key in the keyboard can be in 4 states.
    # The character  has not been used in any guesses so far:
    KEY_UNUSED    = 0
    # The character does not exist in the solution:
    KEY_INCORRECT = 1
    # The character is misplaced:
    KEY_MISPLACED = 2
    # The character is placed correctly:
    KEY_CORRECT   = 4

    # Create colors for unused and hidden characters in the keyboard
    init_pair(4, COLOR_BLACK, COLOR_WHITE)
    init_pair(5, COLOR_BLACK, COLOR_BLACK)

    # Create a table of possible colors for keyboard keys.
    key_colors_table = {
        KEY_UNUSED    : color_pair(4),
        KEY_INCORRECT : color_pair(5),
        KEY_MISPLACED : colors[MISPLACED],
        KEY_CORRECT   : colors[CORRECT]
    }

    # Draw the keyboard at given location using the color table for each key.
    def draw_keyboard(row, start_col, key_colors):
        # Define strings corresponding to each row in the keyboard.
        key_rows = [
            'QWERTYUIOP',
            'ASDFGHJKL',
            'ZXCVBNM'
        ]

        for key_row in key_rows:
            col = start_col
            # Loop through each character in the key row
            for ch in key_row:
                screen.addstr(row, col, ' ' + ch + ' ', key_colors[ch])
                col += 3

            # Offset the next row to the right
            start_col += 2
            row += 1

        # Refresh the screen
        screen.refresh()


    # If --draw-keyboard is supplied, display the keyboard
    if len(sys.argv) == 2 and sys.argv[1] == '--draw-keyboard':
        # Create a table of colors
        key_colors = {}
        # Assign colors randomly
        for ch in range(ord('A'), ord('Z')+1):
            key_colors[chr(ch)] = random.sample(
                list(key_colors_table.values()), 1)[0]
        draw_keyboard(5, 10, key_colors)
        # Wait for a bit.
        napms(1000 * 3)
        sys.exit(0)

    # Update the keyboard based on the grades
    def update_keyboard(guess, grades, key_colors):
        # First mark all correct and incorrect keys
        for ch,g in zip(guess, grades):
            if g == CORRECT:
                key_colors[ch] = key_colors_table[KEY_CORRECT]
            elif g == INCORRECT:
                key_colors[ch] = key_colors_table[KEY_INCORRECT]

        # Mark keys that are misplaced. If a key is correct as well as
        # misplaced, it will thus be marked as misplaced.
        for ch,g in zip(guess, grades):
            if g == MISPLACED:
                key_colors[ch] = key_colors_table[KEY_MISPLACED]


    init_pair(8, COLOR_MAGENTA, COLOR_BLACK)
    LINE_COLOR = color_pair(8)

    def draw_hline(row, col, length, start_ch, end_ch):
        for c in range(col+1, col+length):
            screen.addch(row, c, curses.ACS_HLINE, LINE_COLOR)
        screen.addch(row, col, start_ch, LINE_COLOR)
        screen.addch(row, col+length, end_ch, LINE_COLOR)

    # If --draw-hline is supplied, draw some horizontal lines
    if len(sys.argv) == 2 and sys.argv[1] == '--draw-hline':
        draw_hline(5, 10, 20, curses.ACS_ULCORNER, curses.ACS_URCORNER)
        draw_hline(6, 10, 20, curses.ACS_LTEE, curses.ACS_RTEE)
        draw_hline(7, 10, 20, curses.ACS_LLCORNER, curses.ACS_LRCORNER)
        screen.refresh()
        napms(1000 * 3)
        sys.exit(0)

    def draw_vline(row, col, length):
        for r in range(row, row+length):
            screen.addch(r, col, curses.ACS_VLINE, LINE_COLOR)

    # If --draw-hline is supplied, draw some horizontal lines
    if len(sys.argv) == 2 and sys.argv[1] == '--draw-vline':
        draw_hline(5, 10, 20, curses.ACS_LTEE, curses.ACS_RTEE)
        draw_hline(7, 10, 20, curses.ACS_LTEE, curses.ACS_RTEE)
        screen.refresh()
        napms(1000 * 3)
        sys.exit(0)

    # Wordinal game
    def wordinal(solution=None):
        # Start a bit away form the top and left of the terminal window.
        START_ROW = 2
        START_COL = 25

        # Clear the screen
        screen.clear()

        # Draw the title.
        screen.addstr(START_ROW, START_COL+0, ' W O R ', colors[CORRECT])
        screen.addstr(START_ROW, START_COL+7, ' D I N ', colors[MISPLACED])
        screen.addstr(START_ROW, START_COL+14, ' A L ', key_colors_table[KEY_UNUSED])

        # Initialize the keyboard colors
        key_colors = {}
        for ch in range(ord('A'), ord('Z') + 1):
            key_colors[chr(ch)] = key_colors_table[KEY_UNUSED]

        # Draw the keyboard
        KEYBOARD_ROW = START_ROW + 2 + WORD_LENGTH + 4
        KEYBOARD_COL = START_COL - 5
        draw_keyboard(KEYBOARD_ROW, KEYBOARD_COL, key_colors)

        STATUS_ROW = KEYBOARD_ROW + 4
        STATUS_COL = START_COL - 2

        if True:
            # Draw top line
            BOX_TOP = START_ROW - 1
            BOX_LEFT = START_COL - 6
            BOX_WIDTH = 31
            BOX_HEIGHT = 18

            # Draw left and right sides.
            draw_vline(BOX_TOP + 1, BOX_LEFT, BOX_HEIGHT)
            draw_vline(BOX_TOP + 1, BOX_LEFT + BOX_WIDTH, BOX_HEIGHT)

            # Draw top side
            draw_hline(BOX_TOP, BOX_LEFT, BOX_WIDTH,
                       curses.ACS_ULCORNER, curses.ACS_URCORNER)

            # Draw line after title
            draw_hline(BOX_TOP + 2, BOX_LEFT, BOX_WIDTH,
                       curses.ACS_LTEE, curses.ACS_RTEE)

            # Draw line after play area
            draw_hline(KEYBOARD_ROW - 1, BOX_LEFT, BOX_WIDTH,
                       curses.ACS_LTEE, curses.ACS_RTEE)

            # Draw line after keyboard area
            draw_hline(KEYBOARD_ROW + 3, BOX_LEFT, BOX_WIDTH,
                       curses.ACS_LTEE, curses.ACS_RTEE)

            # Draw bottom side.
            draw_hline(BOX_TOP + BOX_HEIGHT, BOX_LEFT, BOX_WIDTH,
                       curses.ACS_LLCORNER, curses.ACS_LRCORNER)

        # Refresh the screen
        screen.refresh()

        # Choose a randome solution word.
        if not solution:
            solution = random.choice(solution_words)

        row = START_ROW + 3
        col = START_COL + 3
        for i in range(0, NUM_ATTEMPTS):
            # Read a guess from the player.
            guess = read_guess(row, col)

            # Grade the guess and draw it.
            grades = grade_guess(guess, solution)
            draw_guess(row, col, guess, grades)

            # Update and draw the keyboard.
            update_keyboard(guess, grades, key_colors)
            draw_keyboard(KEYBOARD_ROW, KEYBOARD_COL, key_colors)

            # Check if the player has won
            if grades == [CORRECT] * WORD_LENGTH:
                draw_you_won(STATUS_ROW, STATUS_COL + 3)
                return

            # Move to next row.
            row += 1

        draw_you_lost(STATUS_ROW, STATUS_COL, solution)

    try:
        while True:
            # Play one game
            wordinal()

            # Get a key to continue
            key = screen.getch()

            # Quit if requested.
            if key in ['Q']:
                break
    except:
        pass

# Launch application using wrapper.
wrapper(app)
