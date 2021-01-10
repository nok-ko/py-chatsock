from string import ascii_lowercase as alphabet
import logging

# Caesar bot – caesar-shifts messages 
# by X characters, called with !rotX

logger = logging.getLogger(__name__)

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

class CaesarBot():
	def __init__(self, sio):
		self.logger = logger
		self.sio = sio

	async def send_chat(self, msg, to=None):
		logger.info(f"[CHAT] 'caesarBot': {msg}")
		return await self.sio.emit('chat', ('caesarBot', msg), to=to)

	async def on_chat(self, sid, msg):
		async with self.sio.session(sid) as session:
			words = msg.strip().split(' ')
			if words[0][:4] == '!rot':
				logger.info(words)
				try:
					shift = int(words[0][4:])
				except ValueError:
					logger.warning(f"[CAESAR] caesarBot rejected command {words}")
					await self.send_chat("Usage: “!rotX <text>,” where X is an integer without spaces or commas.")
					return
				cleartext = ' '.join(words[1:])
				await self.send_chat(shift_by(cleartext, shift))
		
def create(sio):
	logger.info("Initializing CaesarBot.")
	return CaesarBot(sio)