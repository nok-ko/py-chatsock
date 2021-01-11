import argparse
import importlib
import logging
import os
import pathlib
import random
import sys
import socketio
from aiohttp import web

#TODO: Better variable names

sio = socketio.AsyncServer() # sio - the SocketIO Server
app = web.Application()
sio.attach(app)

logger = logging.getLogger(__name__) # Log stuff using logging, rather than print()

@sio.event
async def connect(sid, environ):
    logger.info(f'[CONN] client {sid} connected.')

    # Ask for a nickname when connecting.
    await sio.emit('nick-please', room=sid)


@sio.on('nick-please')
async def on_change_nick(sid, data):
    logger.info(f'[NICK] client {sid} changing nick to {data}.')
    async with sio.session(sid) as session:
        #TODO: Validate the nickname before setting it.
        session['nick'] = data
        
        # Broadcast a new-nick message. 
        # '' is the old nickname, an empty string, which will produce a special
        # join message.
        await sio.emit('new-nick', ('', data))
        return True # acknowledgement
        # True if the nick is good.
        # TODO: Should emit an error string if it isn't.

@sio.on('chat')
async def on_chat_message(sid, msg):

    # Here, session is read-only and will not update if we change it.
    session = await sio.get_session(sid)
    logger.info(f"[CHAT] {session['nick']}: {msg}")

    await sio.emit('chat', (session['nick'], str(msg)))

    for bot in bot_modules:
        # We allow bots without an on_chat method, hence getattr.
        async with sio.session(sid) as session:
            await bot.on_chat(sid, msg, session)

@sio.event
def disconnect(sid):
    logger.info(f'[DCON] client {sid} disconnected.')

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

    # Get command-line arguments, so we can specify the port 
    # the HTTP server should use.
    parser = argparse.ArgumentParser(description="An HTTP/WebSockets chat server!")

    parser.add_argument("port", type=int, help="The port number that the server should use.")

    # Log level command-line argument
    levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    parser.add_argument('--log-level', default='INFO', choices=levels)

    args = parser.parse_args()


    # Settting up the loggers

    # Use the command-line argument for log level.
    logger.setLevel(args.log_level)

    # Log everything, including debug events, to a file log.
    # mode="w" overwrites the log between runs, instad of appending.
    fh = logging.FileHandler('debug.log', mode="w")
    fh.setLevel(logging.DEBUG) # Capture everything in the file log...

    # But only INFO or higher-level messages in the console log.
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setLevel(logging.INFO) 
    
    # Use the handlers we just set up:
    logging.basicConfig(
    format='%(levelname)s:%(name)s: %(message)s', 
    handlers=[
        stdout,
        fh
    ]
    )

    # Look through the `bots` directory and load every python module.
    bot_modules = []
    for filename in os.listdir(pathlib.Path.cwd().joinpath("bots")):
        # *Not at all* a reliable check for python files. Good enough, however.
        if ".py" in filename and filename != 'bot.py': 
            bot_module = importlib.import_module(f"bots.{filename[:-3]}")
            
            # If the bot has a logger associated with it, set the level to
            # the main log level.
            bot_logger = getattr(bot_module, 'logger', None)
            if bot_logger:
                bot_logger.setLevel(args.log_level)

            # Each bot must have a `create()` function that accepts the SocketIO
            # server instance as an argument.
            bot_class = getattr(bot_module, 'bot')
            if bot_class:
                bot = bot_class(sio)
                bot_modules.append(bot)
            else:
                logger.error(f"Bot in {filename} has no `bot` variable!")

    web.run_app(app, port=args.port)