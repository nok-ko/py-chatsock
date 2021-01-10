# Echo bot – sends back every message you send it.

async def on_chat(sio, sid, session, msg):
	# We would normally get this value like session['echo'],
	# but it might be undefined and raise a KeyError.

	# session.get(key, value) sidesteps the issue: if there isn't a
	# key like 'echo' in `session`, it evaluates to False.

	echo_enabled = session.get('echo', False)

	if msg.strip() == "!echo":
		# Turn False to True, and True to False.
		session['echo'] = not echo_enabled

		await sio.emit('serverchat', 
			f"echo toggled.")
		# Return early to avoid echoing `!echo`
		return

	if echo_enabled:
		await sio.emit('chat', ('echoBot', str(msg)))