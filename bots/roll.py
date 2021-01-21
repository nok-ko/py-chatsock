import random
from .bot import Bot

class RollBot(Bot):
	# RollBot()
	def __init__(self, socket_io):
		super().__init__(socket_io, "rollBot")

	async def on_chat_message(self, sid, msg, session):
		# first two words matter, the rest doesn't
		words = msg.strip().split(' ', 2)
		# '!roll' alone shouldn't work
		if words[0] != '!roll':
			return
		
		if len(words) <= 1:
			return
		
		cmd = words[0]
		# words[1] is guaranteed to exist because of the if
		if 'd' in words[1]:
			dice = words[1].split('d') 
			dice_amt = dice[0]
			try:
				dice_sides = int(dice[1])
			except ValueError:
				print('Error!')
				return
			result = random.randint(1, int(dice[1]))
			await self.send_chat(f"Rolling... {result}!")

bot = RollBot