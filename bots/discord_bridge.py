import asyncio
import discord

from .bot import Bot

class DiscordBridgeBot(Bot):
	def __init__(self, socket_io):

		# Briefly block the thread to read the token.
		# It's okay because __init__ is called before
		# the main loop starts.
		# TODO: Error handling
		with open('bots/discord.secret') as token_file:
			self.token = token_file.readline()

		super().__init__(socket_io, None)

		self.client = discord.Client()
		self.listening_to = set() # Set of discord.Channel

		@self.client.event
		async def on_ready():
			await self.send_chat("Logged into Discord!")

		@self.client.event
		async def on_message(message):
			if message.content == "!chatsock listen":
				if message.channel not in self.listening_to:
					self.listening_to.add(message.channel)
					await message.channel.send("Now listening to this channel.")
					return
				else:
					self.listening_to.remove(message.channel)
					await message.channel.send("No longer listening to this channel.")
					return

			
			if message.channel in self.listening_to:
				await self.send_chat(message.content, from_=f"[DISCORD {message.author.name}]")

	async def on_chat_message(self, session_id, message, session):
		if message == "!login":
			async def login_task():
				await self.send_chat("Logging in...")
				await self.client.login(self.token)
				await self.client.connect()

			loop = asyncio.get_event_loop()
			loop.create_task(login_task())
		if message == "!status":
			if self.client.user is None:
				await self.send_chat("Not logged into Discord.")
			else:
				await self.send_chat(f"{self.client.user}")
		
		for channel in self.listening_to:
			await channel.send(message)




bot = DiscordBridgeBot