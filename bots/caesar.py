from string import ascii_lowercase as alphabet
from .bot import Bot
import logging

# Caesar bot – caesar-shifts messages 
# by X characters, called with !rotX

#TODO: Better variable names

def shift_by(cleartext, shift):
	"""Perform a Caesar shift on the cleartext string provided.
	If characters in the string are not in the English alphabet,
	it skips them, keeping them as they are in the original message.

	Args:
		cleartext (str): The input text.
		shift (int): The amount to shift the text.

	Returns:
		str: The shifted text
	"""
	shift = shift % 26
	shifted = alphabet[shift:] + alphabet[:shift]

	ciphertext = ""
	cleartext = cleartext.lower()
	for character in cleartext:
		if character in alphabet:
			position = alphabet.index(character)
			character = shifted[position]
		ciphertext = ciphertext + character

	return ciphertext

class CaesarBot(Bot):
	"""Caesar-shifts messages. Called with "!rotX <text>," where X is some integer."""
	def __init__(self, socket_io):
		"""The constructor for the bot.

		Args:
			socket_io (socketio.AsyncServer): The SocketIO server used internally by the bot to send messages.
		"""
		super().__init__(socket_io, "caesarBot")

	async def on_chat_message(self, sid, msg, session):
		# async with self.sio.session(sid) as session:
		# Split up the message into !rotX and the remaining text
		words = msg.strip().split(' ', 1)

		# Accept !rot13, !rot22, !rot-20, etc.
		if words[0][:4] == '!rot':
			self.log_info(words)
			try:
				shift = int(words[0][4:])
			except ValueError:
				self.log_warn(f"[CAESAR] caesarBot rejected command {words}")
				await self.send_chat("Usage: “!rotX <text>,” where X is an integer without spaces or commas.")
				return
			cleartext = words[1]
			await self.send_chat(shift_by(cleartext, shift))

bot = CaesarBot