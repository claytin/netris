from curses import wrapper
import curses
import math

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import threading


optionNames = ["Port", "Names", "Levels", "Sync Levels", "Speed", "Rounds", "Width", "Height", "Next", "Pause", "Sync Pause", "Loss", "ghost"]
optionStatus = [13337, True, False, False, 500, 3, 10, 20, True, True, True, "score", True]
options = [optionNames, optionStatus]

connectedPlayers = ["tst", "tst2", "tst3"]

buttons = ["apply", "kick", "add", "start", "stop", "pause", "restart", "end", "broadcast", "quit"]
#buttonKeys = ['a', 'k', 'd', 's', 't', 'p', 'r', 'e', 'b', 'q']

selected = 0

#windows
global optionsWindow

def main(stdscr):
	global selected
	global optionsWindow

	curses.curs_set(0)
	stdscr.clear()

	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)	#green check
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)	#red other data
	curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)	#blue title
	curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)	#yellow selected
	curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLACK)	#background greyed out stuff (remember to bold)

	stdscr.refresh()

	#create options window
	optionsWindow = curses.newwin(stdscr.getmaxyx()[0] - 3 - 1, 30, 0, 0)
	optionsWindow.box(0, 0)
	drawOptionsWindow(optionsWindow, False)
	optionsWindow.refresh();

	#create actions window
	actionsWindow = curses.newwin(3, stdscr.getmaxyx()[1], stdscr.getmaxyx()[0] - 3 - 1, 0)
	actionsWindow.box(0, 0)
	drawActionsWindow(actionsWindow)
	actionsWindow.refresh()

	#create players window
	playersWindow = curses.newwin(int(math.floor((stdscr.getmaxyx()[0] - 3 - 1) / 2)), stdscr.getmaxyx()[1] - 30, 0, 30)
	playersWindow.box(0, 0)
	drawPlayersWindow(playersWindow)
	playersWindow.refresh()

	#create waiting players window
	waitingPlayersWindow = curses.newwin(stdscr.getmaxyx()[0] - playersWindow.getmaxyx()[0] - 4, 43,
		playersWindow.getmaxyx()[0], playersWindow.getbegyx()[1])
	waitingPlayersWindow.box(0, 0)
	drawWaitingPlayersWindow(waitingPlayersWindow)
	waitingPlayersWindow.refresh()

	#create output window
	outputWindow = curses.newwin(stdscr.getmaxyx()[0] - playersWindow.getmaxyx()[0] - 4, stdscr.getmaxyx()[1] - waitingPlayersWindow.getmaxyx()[1] - 30,
		playersWindow.getmaxyx()[0], playersWindow.getbegyx()[1] + 43)
	drawOutput(outputWindow)
	outputWindow.refresh()

	stdscr.move(stdscr.getmaxyx()[0] - 1, 0)
	stdscr.clrtoeol()
	stdscr.addstr(">");

	while True:
		key = stdscr.getch()

		stdscr.addstr(stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1 - len(str(key)), str(key) + "");
		stdscr.refresh()

		if key >= 258 and key <= 261:
			if key == 259:
				moveSelected(0)
			elif key == 261:
				moveSelected(1)
			elif key == 258:
				moveSelected(2)
			elif key == 260:
				moveSelected(3)
			drawOptionsWindow(optionsWindow, False)
			optionsWindow.refresh()
			drawActionsWindow(actionsWindow)
			actionsWindow.refresh()
		elif key == 410:			
			#check if stuff will fit
			pass
		elif key == 10:
			selectOption()
			drawOptionsWindow(optionsWindow, False)
			optionsWindow.refresh()
			drawActionsWindow(actionsWindow)
			actionsWindow.refresh()
		elif key == 113:
			quit()
			return

def quit():
	pass

def drawOutput(outputWindow, outputString = ""):
	outputWindow.box(0, 0)
	outputWindow.move(0, 2)
	outputWindow.addstr("Output", curses.color_pair(3) | curses.A_BOLD)

def drawWaitingPlayersWindow(waitingPlayersWindow):
	for index in range(len(connectedPlayers)):
		waitingPlayersWindow.move(1 + index, 1)
		waitingPlayersWindow.addstr(connectedPlayers[index] + "\t(add/kick)" + "\n")

	waitingPlayersWindow.box(0, 0)
	waitingPlayersWindow.move(0, 2)
	waitingPlayersWindow.addstr("Waiting", curses.color_pair(3) | curses.A_BOLD);

def drawPlayersWindow(playersWindow):
	playersWindow.move(0, 2)
	playersWindow.addstr("Game", curses.color_pair(3) | curses.A_BOLD);

def drawActionsWindow(actionsWindow):
	actionsWindow.move(1, 1)
	for index in range(len(buttons)):
		if index + len(options[0]) == selected:
			actionsWindow.addstr(buttons[index], curses.color_pair(4) | curses.A_BOLD | curses.A_UNDERLINE)
		else:
			actionsWindow.addstr(buttons[index])

		actionsWindow.addstr("    ");

	actionsWindow.box(0, 0)
	actionsWindow.move(0, 2)
	actionsWindow.addstr("Actions", curses.color_pair(3) | curses.A_BOLD)

redraw = 0
def drawOptionsWindow(optionsWindow, enterval):
	global selected
	global redraw

	enterValX = 0
	enterValY = 0

	optionsWindow.clear()

	optionsWindow.move(1, 1);
	for index in range(len(options[0])):
		optionsWindow.move(index + 1, 1);
		#	optionsWindow.addstr(str(index) + ") " + options[0][index], curses.A_REVERSE)
		#else:
		
		if selected == index:
			optionsWindow.addstr(options[0][index], curses.color_pair(4) | curses.A_UNDERLINE | curses.A_BOLD)
		else:
			optionsWindow.addstr(options[0][index])

		optionsWindow.move(index + 1, 16);
		optionsWindow.addstr( ": (")
		if selected == index:	
			if type(options[1][index]) is bool:
				if options[1][index]:
					optionsWindow.addstr("*", curses.color_pair(4) | curses.A_BOLD | curses.A_UNDERLINE)
				elif not options[1][index]:
					optionsWindow.addstr("-", curses.color_pair(4) | curses.A_BOLD | curses.A_UNDERLINE)
			else:
				if enterval:
					enterValX = optionsWindow.getyx()[1]
					enterValY = optionsWindow.getyx()[0]
					optionsWindow.addstr(str(options[1][index]), curses.color_pair(5) | curses.A_BOLD)
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

	optionsWindow.box(0, 0)
	optionsWindow.move(0, 2);
	redraw += 1
	optionsWindow.addstr("Options (" + str(selected) + ", " + str(enterValX) + ", " + str(enterValY) + ")", curses.color_pair(3) | curses.A_BOLD);

	#its kinda eh... but it works
	if enterval:
		newval = ""
		optionsWindow.refresh()
		curses.curs_set(1)
		optionsWindow.move(enterValY, enterValX)
		while True:
			key = optionsWindow.getch()
			if key == 10:
				break
			elif key == 127:
				newval = newval[:-1]
				optionsWindow.addch(optionsWindow.getyx()[0], optionsWindow.getyx()[1] - 1, ' ')
			elif optionsWindow.getyx()[1] < optionsWindow.getmaxyx()[1] - 2 and (key >= 32 and key <= 126):
				if type(options[1][selected]) == int:
					if key >= 48 and key <= 57:
						newval = newval + str(unichr(key))
				else:
					newval = newval + str(unichr(key))
			optionsWindow.move(enterValY, enterValX - 1)
			optionsWindow.addstr("(" + newval)
			optionsWindow.refresh()
		if newval == "":
			return

		if type(options[1][selected]) == int:
			options[1][selected] = int(newval) 
		else:
			options[1][selected] = newval

def selectOption():
	global selected
	global options

	if selected < len(options[0]):
		if type(options[1][selected]) == bool:
			options[1][selected] = not options[1][selected]
		elif type(options[1][selected]) == int or type(options[1][selected]) == str:
			global optionsWindow
			drawOptionsWindow(optionsWindow, True)
		

def moveSelected(direction):	#yeah... this could be better... but eh, it works
	#0=up, 1=right, 2=down, 3=left
	global selected

	if selected <= len(options[0]) - 1:
		if direction == 0 and selected >= 1:
			selected = selected - 1
		elif direction == 2 and selected <= len(options[0]):
			selected = selected + 1
	elif selected > len(options[0]) - 1:
		if (direction == 1 or direction == 2) and selected < len(options[0]) + len(buttons) - 1:
			selected = selected + 1
		if direction == 3 and selected > len(options[0]):
			selected = selected - 1
		if direction == 0:
			selected = len(options[0]) - 1

#for multi threading the server
class ClientHandler(threading.Thread):
	def run(self):
		tornado.ioloop.IOLoop.instance().start()

class WSHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print("new connection")

	def on_message(self, message):
		print("message received: " + message)
		self.write_message(u"You said: " + message)

	def on_close(self):
		print('connection closed')

application = tornado.web.Application([
	(r'/ws', WSHandler),
])

http_server = tornado.httpserver.HTTPServer(application)

#http_server.listen(13337)
#
#serverThread = ClientHandler()
#serverThread.start()

#start everything by calling main with the curses wrapper
wrapper(main)