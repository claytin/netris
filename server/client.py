import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

class client(tornado.websocket.WebSocketHandler):
	pass

clients = []

class WSHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		global clients

		clients.append(self)
		print("new connection" + str(clients))
		self.write_message("ntr")

	def on_message(self, message):
		print("message received: " + message)
		self.write_message(u"You said: " + message)

	def on_close(self):
		print('connection closed')
		clients.remove(self)


application = tornado.web.Application([
	(r'/ws', WSHandler),
])

http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(13337)