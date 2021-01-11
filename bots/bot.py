import logging

class Bot():
	def __init__(self, socketio, name):
		self.logger = logging.getLogger(name)
		self.logger.setLevel(logging.INFO)
		self.logger.info(f"Initializing {name}.")
		self.socketio = socketio
		self.name = name

	async def send_event(self, event_name, data, to=None):
		return await self.socketio.emit(event_name, data, to=to)

	async def send_chat(self, message, to=None):
		self.logger.info(f"[CHAT] {self.name}: {message}")
		return await self.send_event('chat', (self.name, message), to=to)
	
	async def send_serverchat(self, message, to=None):
		self.logger.info(f"[SERVERCHAT]: {message}")
		return await self.send_event('serverchat', message, to=to)

	async def on_chat_messageself, session_id, message, session):
		pass