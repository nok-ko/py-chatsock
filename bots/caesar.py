from string import ascii_lowercase as alphabet
from .bot import Bot
import logging

# Caesar bot – caesar-shifts messages 
# by X characters, called with !rotX

#TODO: Better variable names

def shift_by(cleartext, shift):
	"""Performs a Caesar shift on the cleartext string provided.
	Returns the shifted string.
	`cleartext` – must be a string or collection of characters, the input text.
	`shift` – must be an integer, the amount to shift the text.
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
	def __init__(self, sio):
		super().__init__(sio, "caesarBot")

	async def on_chat_messageself, sid, msg, session):
		# async with self.sio.session(sid) as session:
		# Split up the message into !rotX and the remaining text
		words = msg.strip().split(' ', 1)

		# Accept !rot13, !rot22, !rot-20, etc.
		if words[0][:4] == '!rot':
			self.logger.info(words)
			try:
				shift = int(words[0][4:])
			except ValueError:
				self.logger.warning(f"[CAESAR] caesarBot rejected command {words}")
				await self.send_chat("Usage: “!rotX <text>,” where X is an integer without spaces or commas.")
				return
			cleartext = words[1]
			await self.send_chat(shift_by(cleartext, shift))

bot = CaesarBot