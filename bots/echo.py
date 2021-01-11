from .bot import Bot
import logging

# Echo bot – sends back every message you send it.
#TODO: Better variable names
class EchoBot(Bot):
	"""A bot that sends the user's messages back to them.

	Attributes:
	count (int): A count of the echo messages that have been sent so far.
	"""
	def __init__(self, sio):
		"""Initialize the EchoBot. Counter starts at 0."""		
		super().__init__(sio, "echoBot")
		self.count = 0 # Counter: increments every time we send an echo message.

	async def on_chat_message(self, sid, msg, session):
		echo_enabled = session.get('echo', False)
		# We would normally get this value like session['echo'],
		# but it might be undefined and raise a KeyError.

		# session.get(key, False) sidesteps the issue: if there isn't a
		# key like 'echo' in `session`, it evaluates to False.

		if msg.strip() == "!echo":
			# Turn False to True, and True to False.
			session['echo'] = not echo_enabled

			self.log_info(f"Echo now {session['echo']} for {session.get('nick'), sid}")

			await self.send_serverchat(f"echo toggled.", to=sid)
			# Return early to avoid echoing `!echo`
			return

		if msg.strip() == "!echo info":
			self.log_info(f"Reporting echo info for {session.get('nick'), sid}")
			await self.send_serverchat(f"{self.count} echoes sent.", to=sid)
			return

		if echo_enabled:
			# If the user has echo on, send their message back to them.
			await self.send_chat(str(msg))
			# Increment the counter.
			self.count = self.count + 1

bot = EchoBot