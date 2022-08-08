import logging
import os
import datetime
import random
import requests
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

    if cmd == "welcome":
        welcome_command(request, cmd, params, say, logger)
    elif cmd == "time":
        time_command(request, cmd, params, say, logger)
    elif cmd == "weather":
        weather_command(request, cmd, params, say, logger)
    elif cmd == "help":
        help_command(request, cmd, params, say, logger)
    elif cmd == "sleep":
        sleep_command(request, cmd, params, say, logger)
    elif cmd == "lofi":
        lofi_command(request, cmd, params, say, logger)
    else:
        say("It was a really fascinating request: " + request)

# Welcome command
def welcome_command(request, cmd, params, say, logger):
    say(
        '''
        Hi, my name is Richie, and I am always here to help you :)
        
        Make your day better with the following commands:
        @Happy dog
            1) welcome - to see the welcome message 🙃
            2) time - to get the current date and time 🕓
            3) weather - to get the weather over the world ☀️
            4) help - to get help by emphasizing the problem ✋
            5) sleep - to get the remaining time until the healthy scheduled time to sleep 🌙
            6) lofi - to listen to beats for relaxation, working, or studying 💫

        Enjoy this beautiful day and call me when you need me 🐕
        '''
    )

# Time command
def time_command(request, cmd, params, say, logger):
    # get current time
    current_time = datetime.datetime.now()
    
    say("Date: " + str(current_time.day) + "/" + str(current_time.month) + "/" + str(current_time.year) + "\n" +
    "Time: " + str(current_time.hour) + ":" + str(current_time.minute) + ":" + str(current_time.second))

# Weather command
def weather_command(request, cmd, params, say, logger):
    api_key = "4256b3de394a56a86ee35e43af6f5c2e"
    #city = "San Jose"

    data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={params}&units=metric&APPID={api_key}"
    )

    say(
        "In " + params + "\n" +
        "Weather: " + str(data.json().get('weather')[0].get('main')) + "\n" +
        "Temperature: " + str(data.json().get('main')['temp']) + "°C" + "\n" +
        "Min/Max Temperature: " + str(data.json().get('main')['temp_min']) + "°C/" + str(data.json().get('main')['temp_max']) + "°C" + "\n" +
        "Humidity: " + str(data.json().get('main')['humidity']) + "%" + "\n" +
        "Wind: " + str(data.json().get('wind')['speed']) + "km/h"
    )

# Help command
def help_command(request, cmd, params, say, logger):
    say("❗ ❗ ❗" + "Need help with: " + params + "❗ ❗ ❗")

# Sleep command
def sleep_command(request, cmd, params, say, logger):
    # get current time
    current_time = datetime.datetime.now()

    # calculate time to sleep
    sleep_hour = 22 - current_time.hour
    sleep_minute = 60 - current_time.minute

    say("In " + str(sleep_hour) + " hours and " + str(sleep_minute) + " minutes will be the best time for you to fall asleep.")

# Lofi command
def lofi_command(request, cmd, params, say, logger):
    lofi_links_list = [
        "https://www.youtube.com/watch?v=lTRiuFIWV54",
        "https://www.youtube.com/watch?v=wAPCSnAhhC8&t=2817s",
        "https://www.youtube.com/watch?v=BTYAsjAVa3I",
        "https://www.youtube.com/watch?v=EtD7_8kCMHA",
        "https://www.youtube.com/watch?v=sUwD3GRPJos",
        "https://www.youtube.com/watch?v=SEzAoQJZOhc",
        "https://www.youtube.com/watch?v=7NOSDKb0HlU",
        "https://www.youtube.com/watch?v=kgx4WGK0oNU",
        "https://www.youtube.com/watch?v=e_e1WMNFiHc",
        "https://www.youtube.com/watch?v=rUxyKA_-grg",
        "https://www.youtube.com/watch?v=n61ULEU7CO0&t=3018s",
        "https://www.youtube.com/watch?v=f02mOEt11OQ&t=19s"
    ]
    
    say(random.choice(lofi_links_list))

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()