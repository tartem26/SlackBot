import logging
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Logging levels
logging.basicConfig(level=logging.INFO)

load_dotenv()

# read the environment variables
SLACK_BOT_TOKEN = os.environ["bot_user_oauth_token"]
SLACK_APP_TOKEN = os.environ["socket_mode_token"]

app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def mention_handler(body, context, payload, options, say, event, logger):
    request = payload['blocks'][0]['elements'][0]['elements'][1]['text']
    # logger.info(request)
    res = request.lstrip().split(' ', 1)
    logger.info(res)
    cmd = res[0].strip().lower()
    if len(res) > 1:
        params = res[1].lstrip()
    else:
        params = ""
    logger.info(cmd)
    logger.info('------')

    if cmd == "help":
        command1(request, cmd, params, say, logger)
    elif cmd == "sleep":
        command2(request, cmd, params, say, logger)
    else:
        say("It was a really fascinating request: " + request)


def command1(request, cmd, params, say, logger):
    say("command1: " + params)

def command2(request, cmd, params, say, logger):
    say("command2: " + params)


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()