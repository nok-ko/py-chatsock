import logging

# Echo bot – sends back every message you send it.

logger = logging.getLogger(__name__)
class EchoBot():
	def __init__(self, sio):
		self.sio = sio

	async def send_chat(self, msg, to=None):
		logger.info(f"[CHAT] echoBot: {msg}")
		return await self.sio.emit('chat', ('echoBot', msg), to=to)
	
	async def on_chat(self, sid, msg):
		async with self.sio.session(sid) as session:
			echo_enabled = session.get('echo', False)
			# We would normally get this value like session['echo'],
			# but it might be undefined and raise a KeyError.

			# session.get(key, value) sidesteps the issue: if there isn't a
			# key like 'echo' in `session`, it evaluates to False.

			if msg.strip() == "!echo":
				# Turn False to True, and True to False.
				session['echo'] = not echo_enabled

				logger.info(f"Echo now {session['echo']} for {session.get('nick'), sid}")

				await self.sio.emit('serverchat', 
					f"echo toggled.", to=sid)
				# Return early to avoid echoing `!echo`
				return

			if echo_enabled:
				await self.send_chat(str(msg))

def create(sio):
	logger.info("Initializing EchoBot.")
	return EchoBot(sio)