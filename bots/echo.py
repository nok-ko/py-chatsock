from .bot import Bot
import logging

# Echo bot – sends back every message you send it.
#TODO: Better variable names
class EchoBot(Bot):
	def __init__(self, sio):
		super().__init__(sio, "echoBot")

	# async def send_chat(self, msg, to=None):
	# 	self.logger.info(f"[CHAT] echoBot: {msg}")
	# 	return await self.sio.emit('chat', ('echoBot', msg), to=to)
	
	async def on_chat(self, sid, msg, session):
		echo_enabled = session.get('echo', False)
		# We would normally get this value like session['echo'],
		# but it might be undefined and raise a KeyError.

		# session.get(key, False) sidesteps the issue: if there isn't a
		# key like 'echo' in `session`, it evaluates to False.

		if msg.strip() == "!echo":
			# Turn False to True, and True to False.
			session['echo'] = not echo_enabled

			self.logger.info(f"Echo now {session['echo']} for {session.get('nick'), sid}")

			await self.send_serverchat(f"echo toggled.", to=sid)
			# Return early to avoid echoing `!echo`
			return

		if echo_enabled:
			# If the user has echo on, send their message back to them.
			await self.send_chat(str(msg))

bot = EchoBot