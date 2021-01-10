# Caesar bot – caesar-shifts messages 
# by X characters, called with !rotX

from string import ascii_lowercase as alphabet

def shift_by(cleartext, shift):
	shifted = alphabet[shift:] + alphabet[:shift]
	
	ciphertext = ""
	cleartext = cleartext.lower()
	for character in cleartext:
		if character in alphabet:
			position = alphabet.index(character)
			character = shifted[position]
		ciphertext = ciphertext + character
	
	return ciphertext

async def on_chat(sio, sid, session, msg):
	words = msg.strip().split(' ')
	if words[0][:4] == '!rot':
		print(words)
		try:
			shift = int(words[0][4:])
		except ValueError:
			print(f"caesarBot rejected command {words}")
			return
		cleartext = ' '.join(words[1:])
		await sio.emit('chat', 
			('caesarBot', shift_by(cleartext, shift))
		)
		