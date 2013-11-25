from curses import wrapper
import curses
import math

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web


optionNames = ["Port", "Names", "Levels", "Sync Levels", "Speed", "Rounds", "Width", "Height", "Next", "Pause", "Sync Pause", "Loss", "ghost"]
optionStatus = [13337, True, False, False, 500, 3, 10, 20, True, True, True, "score", True]
options = [optionNames, optionStatus]

connectedPlayers = ["tst", "tst2", "tst3"]

buttons = ["apply", "kick", "add", "start", "pause", "restart", "end", "say"]

selected = 0

def main(stdscr):
	global selected

	curses.curs_set(0)
	stdscr.clear()

	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)	#green check
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)	#red other data
	curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)	#blue title
	curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)	#yellow selected

	stdscr.refresh()

	#create options window
	optionsWindow = curses.newwin(stdscr.getmaxyx()[0] - 3 - 1, 30, 0, 0)
	optionsWindow.box(0, 0)
	drawOptionsWindow(optionsWindow)
	optionsWindow.refresh();

	#create actions window
	actionsWindow = curses.newwin(3, stdscr.getmaxyx()[1], stdscr.getmaxyx()[0] - 3 - 1, 0)
	actionsWindow.box(0, 0)
	drawActionsWindow(actionsWindow)
	actionsWindow.refresh()

	#create players window
	playersWindow = curses.newwin(math.floor((stdscr.getmaxyx()[0] - 3 - 1) / 2), stdscr.getmaxyx()[1] - 30, 0, 30)
	playersWindow.box(0, 0)
	drawPlayersWindow(playersWindow)
	playersWindow.refresh()

	#create waiting players window
	waitingPlayersWindow = curses.newwin(stdscr.getmaxyx()[0] - playersWindow.getmaxyx()[0] - 4, stdscr.getmaxyx()[1] - 30, playersWindow.getmaxyx()[0], playersWindow.getbegyx()[1])
	waitingPlayersWindow.box(0, 0)
	drawWaitingPlayersWindow(waitingPlayersWindow)
	waitingPlayersWindow.refresh()

	stdscr.move(stdscr.getmaxyx()[0] - 1, 0)
	stdscr.clrtoeol()
	stdscr.addstr(">");

	while True:
		key = stdscr.getkey()
		if key == "KEY_UP" or key == "KEY_DOWN" or key == "KEY_RIGHT" or key == "KEY_LEFT":
			if key == "KEY_UP":
				moveSelected(0)
			elif key == "KEY_RIGHT":
				moveSelected(1)
			elif key == "KEY_DOWN":
				moveSelected(2)
			elif key == "KEY_LEFT":
				moveSelected(3)
			drawOptionsWindow(optionsWindow)
			optionsWindow.refresh()
			drawActionsWindow(actionsWindow)
			actionsWindow.refresh()
		elif key == "KEY_RESIZE":
			#check if stuff will fit
			pass
		elif key == "KEY_ENTER":
			selectOption()
			drawOptionsWindow(optionsWindow)
			optionsWindow.refresh()
			drawActionsWindow(actionsWindow)
			actionsWindow.refresh()


def drawWaitingPlayersWindow(waitingPlayersWindow):
	waitingPlayersWindow.move(0, 2)
	waitingPlayersWindow.addstr("Waiting", curses.color_pair(3) | curses.A_BOLD);
	for index in range(len(connectedPlayers)):
		waitingPlayersWindow.move(1 + index, 1)
		waitingPlayersWindow.addstr(connectedPlayers[index] + "\t: (add  -  kick  -  ban)" + "\n")

def drawPlayersWindow(playersWindow):
	playersWindow.move(0, 2)
	playersWindow.addstr("Players", curses.color_pair(3) | curses.A_BOLD);

def drawActionsWindow(actionsWindow):
	actionsWindow.move(0, 2)
	actionsWindow.addstr("Actions", curses.color_pair(3) | curses.A_BOLD)
	actionsWindow.move(1, 1)
	for index in range(len(buttons)):
		if index + 12 == selected:
			actionsWindow.addstr(buttons[index], curses.color_pair(4) | curses.A_BOLD | curses.A_UNDERLINE)
		else:
			actionsWindow.addstr(buttons[index])

		actionsWindow.addstr("    ");


def drawOptionsWindow(optionsWindow):
	global selected

	optionsWindow.move(0, 2);
	optionsWindow.addstr("Options (" + str(selected) + ")", curses.color_pair(3) | curses.A_BOLD);
	optionsWindow.move(1, 1);
	for index in range(len(options[0])):
		optionsWindow.move(index + 1, 1);
		#if selected == index:
		#	optionsWindow.addstr(str(index) + ") " + options[0][index], curses.A_REVERSE)
		#else:
		optionsWindow.addstr(str(index) + ") " + options[0][index])
		optionsWindow.move(index + 1, 16);
		optionsWindow.addstr( ": (")
		if selected == index:
			if type(options[1][index]) is bool:
				if options[1][index]:
					optionsWindow.addstr("*", curses.color_pair(4) | curses.A_BOLD | curses.A_UNDERLINE)
				elif not options[1][index]:
					optionsWindow.addstr("-", curses.color_pair(4) | curses.A_BOLD | curses.A_UNDERLINE)
			else:
				optionsWindow.addstr(str(options[1][index]), curses.color_pair(4) | curses.A_BOLD | curses.A_UNDERLINE)
			optionsWindow.addstr(")");
		else:
			if type(options[1][index]) is bool:
				if options[1][index]:
					optionsWindow.addstr("*", curses.color_pair(1))
				elif not options[1][index]:
					optionsWindow.addstr(" ")
			else:
				optionsWindow.addstr(str(options[1][index]), curses.color_pair(2) | curses.A_BOLD)
			optionsWindow.addstr(")")

def selectOption():
	global selected
	global options

	if selected == 0:
		pass
	elif selected == 1:
		pass


def moveSelected(direction):	#yeah... this could be better... but eh, it works
	#0=up, 1=right, 2=down, 3=left
	global selected

	if selected <= 11:
		if direction == 0 and selected >= 1:
			selected = selected - 1
		elif direction == 2 and selected <= 11:
			selected = selected + 1
	elif selected > 11:
		if direction == 1 and selected < 12 + 7:
			selected = selected + 1
		if direction == 3 and selected > 12:
			selected = selected - 1
		if direction == 0:
			selected = 11

class ClientHandler():
	def run():
		pass

wrapper(main)