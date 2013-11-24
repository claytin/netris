from curses import wrapper


optionNames = ["Port", "Names", "Levels", "Sync Levels", "Speed", "Rounds", "Width", "Height", "Next", "Pause", "Sync Pause", "Loss"]
optionStatus = [13337, True, False, False, 500, 3, 10, 20, True, True, True, "Score"]
options = [optionNames, optionStatus]

selected = 0

def main(stdscr):
	stdscr.clear()
	stdscr.refresh()

	for index in range(len(options[0])):
		stdscr.addstr(options[0][index])
		stdscr.move(stdscr.getyx()[0], 14);
		stdscr.addstr( ": (" + str(options[1][index]) + ")\n");
	stdscr.getkey()

wrapper(main)