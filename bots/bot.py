import logging

class Bot():
	"""A chatbot that can process incoming chat messages and send its own chat messages back.

	Attributes:
		logger (logging.Logger): the logger associated with this bot.
			Its name will be the `name` argument given to __init__.
		socketio (socketio.AsyncServer): the SocketIO server used by the bot to send messages.
		name (str): the bot's name. Used in log messages, and in the message-sending functions by default.


	"""
	def __init__(self, socketio, name):
		"""Constructor method. Mainly sets up logging.

		Args:
			socketio (socketio.AsyncServer): The SocketIO server used internally by the bot to send messages.
			name (str): The name of this chatbot – used in the logging functions and when sending chat messages.
		"""
		name = name or self.__class__.__name__ # decent fallback name
		self.logger = logging.getLogger(name)
		self.logger.setLevel(logging.INFO)

		# Sanity check: is the name okay, has the bot started?
		self.logger.info(f"Initializing {name}.")

		self.socketio = socketio
		self.name = name

	def log_info(self, message):
		return self.logger.info(message)

	def log_warn(self, message):
		return self.logger.warn(message)

	def log_error(self, message):
		return self.logger.error(message)

	async def send_event(self, event_name, data, to=None, log=None):
		"""Sends a SocketIO event.

		Args:
			event_name (str): The name of the event.

			data (Any): The data to send along with the event.

			to (str, optional): The recipient of the message.
				This can be set to the session ID of a client to address only that client, or to any custom room created by the application to address all the clients in that room.

				If this argument is omitted, the event is broadcasted to all connected clients.

			log (str, optional): What to log for this function. If None, logs `data`.
				Defaults to None, logging `data` was sent.

		Returns:
			None
		"""
		to_string = ""
		if to is not None:
			to_string = f" to={to}"

		if log is None:
			log = data

		# E.g: [CHAT to=someSID] exampleBot: Hello there!
		self.log_info(f"[{event_name.upper()}{to_string}] {self.name}: {log}")

		return await self.socketio.emit(event_name, data, to=to)

	async def send_chat(self, message, to=None, from_=None):
		"""Send a chat message, optionally to a specific client or room.

		Args:
			message (str): The message to be sent.
				Will accept any type, but only strings are displayed reliably.

			to (str, optional): The recipient of the message.
				Can be a user’s session ID or a room ID.
				Defaults to None, broadcasting to every connected client.
			to (str, optional): The sender of the message.
				Just a string, can be anything.
				If set to None, defaults to self.name.
		Returns:
			None
		"""
		from_ = from_ or self.name # If from_ is None, set to the bot's name.
		return await self.send_event('chat', (from_, message), to=to, log=message)

	async def send_serverchat(self, message, to=None):
		"""Send a chat message as “the server,” optionally to a specific client or room.

		Args:
			message (str): The message to be sent.
				Will accept any type, but only strings are displayed reliably.

			to (str, optional): The recipient of the message.
				Can be a user’s session ID or a room ID.
				Defaults to None, broadcasting to every connected client.
		Returns:
			None
		"""
		return await self.send_event('serverchat', message, to=to, log=message)

	async def on_chat_message(self, session_id, message, session):
		"""Callback method: this is called every time a message arrives on the server.

		The default on_chat_message method does nothing. Bots do not have to implement this method (e.g. a bot may instead send a message every time an event happens, without reacting to any other chat messages.)

		Args:
			session_id (str): The session ID of the client who sent this message.
			message (str): The message itself. Can be an empty string.
			session ([type]): The session dictionary associated with the client.

				`session` be used for storing data related to a particular user. (E.g: have they used a command before, are they allowed to do a certain action, etc.)

				The data is not persistent across restarts of the server or disconnections: the session dictionary will not save between restarts of the server, and reconnecting users will have different Session IDs.
		"""
		pass