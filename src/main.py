from wordle_bot import wordle_bot
import numpy as np

import time
import curses
from curses import textpad


# making bot instance
bot = wordle_bot()

# setting up the bot
bot.setup()
top = bot.getTop()
#print(top)

# entropy of word in current wordlist
#print(bot.entropy('tares'))

# finding matches
#frame = (np.asarray([0, 0, 1, 1, 0]), 'weary')
# all words in the wordlist that match the frame
#match = bot.filter(frame)
#print(match)


# terminal gui (this is soooooo annoying)

menu = ['Play', 'Exit']

def print_menu(stdscr, selected):
	stdscr.clear()

	h, w = stdscr.getmaxyx()

	for i, row in enumerate(menu):
		x = w//2 - len(row)//2
		y = h//2 - len(menu)//2 + i
		if i == selected:
			stdscr.attron(curses.color_pair(1))
			stdscr.addstr(y, x, row)
			stdscr.attroff(curses.color_pair(1))
		else:
			stdscr.addstr(y, x, row)

	stdscr.refresh()

def print_board(stdscr, row, col):

	sh, sw = stdscr.getmaxyx()
	h, w = 3, 3
	box = [[h, w], [sh-h, sw-w]]

	width_start = sw//2-1
	height_start = sh//4

	textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

	current_pos = [height_start, width_start-1]
	letters = []

	backspace = False

	while 1:
		key = stdscr.getch()

		# exit midword
		if chr(key) == ':':
			key = stdscr.getch()
			if chr(key) == 'e':
				return

		elif key == curses.KEY_ENTER or key in [10, 13]:
			if current_pos[1] - width_start == 0:
				if current_pos[0] - height_start == -1:
					continue
				current_pos[0] -= 1
				current_pos[1] = width_start + 4
			else:
				current_pos[1] -= 1

			letters = letters[:-1]
			backspace = True

		if not backspace:
			if current_pos[1] - width_start == 4:
				if current_pos[0] - height_start == 5:
					return
				current_pos[0] += 1
				current_pos[1] = width_start
			else:
				current_pos[1] += 1
			letters.append([current_pos[0], current_pos[1], key])

		for y, x, c in letters:
			stdscr.addstr(y, x, chr(c))

		backspace = False

		stdscr.refresh()




def main(stdscr):
	curses.curs_set(0)
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

	h, w = stdscr.getmaxyx()
	row_idx = 0
	print_menu(stdscr, row_idx)

	while 1:
		key = stdscr.getch()
		stdscr.clear()

		if key == curses.KEY_UP:
			row_idx = (row_idx - 1) % len(menu)
		elif key == curses.KEY_DOWN:
			row_idx = (row_idx + 1) % len(menu)
		elif key == curses.KEY_ENTER or key in [10, 13]:
			#stdscr.addstr(0, 0, "You pressed {}".format(menu[row_idx]))
			#stdscr.refresh()

			if row_idx == len(menu)-1:
				return
			else:
				text = "Wordle Bot"
				x = w//2 - len(text)//2
				y = h//32
				stdscr.addstr(y, x, "Wordle Bot")
				print_board(stdscr, 0, 0)
				stdscr.refresh()
			# return back to main menu loop
			#stdscr.getch()

		print_menu(stdscr, row_idx)

		stdscr.refresh()

curses.wrapper(main)