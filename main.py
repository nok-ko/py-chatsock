from aiohttp import web
import socketio, random, os, asyncio, importlib, pathlib
import asyncio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

@sio.event
async def connect(sid, environ):
    print('connect ', sid)
    print(await sio.get_session(sid))
    async with sio.session(sid) as session:
        session['test'] = True
        session['nick'] = "test_user"
    print(await sio.get_session(sid))

    await sio.emit('nick-please', room=sid)


@sio.on('nick-please')
async def on_change_nick(sid, data):
    print(f"changing nick to {data}")
    async with sio.session(sid) as session:
        #TODO: Validate the nickname before setting it.
        session['nick'] = data
        await sio.emit('new-nick', ('', data))
        return True # acknowledgement
        # True if the nick is good.
        # Should emit an error string if it isn't.

@sio.on('chat')
async def on_chat_message(sid, msg):
    async with sio.session(sid) as session:
        print(f"message from {session['nick']}", msg)

        await sio.emit('chat', (session['nick'], str(msg)))

        for bot in bot_modules:
            await bot.on_chat(sio, sid, session, msg)
        
        

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

# Serve static files (stylesheets, JS, etc.)
app.router.add_static('/static/', 'static')

# Serve index.html without the filename in the URL
# Function receives 1 argument, but we don't need it, hence the underscore.
def index(_):
    return web.FileResponse('./static/index.html')
app.router.add_get('/', index)

# Code in this “__main__ guard” will only run if this file is launched from the console, 
# rather than imported as a library in another Python file.
if __name__ == '__main__':

    # Look through the `bots` directory and load every python module.
    bot_modules = []
    for filename in os.listdir(pathlib.Path.cwd().joinpath("bots")):
        if filename not in ("__pycache__"):
            bot_modules.append(importlib.import_module(f"bots.{filename[:-3]}"))

    web.run_app(app)