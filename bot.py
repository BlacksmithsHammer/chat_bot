from sys import argv
from time import sleep

from origamibot import OrigamiBot as Bot
from origamibot.listener import Listener

import requests
import freecurrencyapi

class BotsCommands:
    def __init__(self, bot: Bot):  # Can initialize however you like
        self.bot = bot
        self.cclient = freecurrencyapi.Client("fca_live_G3DdF4IEQVFyQPH1UqBYO0BJ0PMW2RB4jrkdiBzR")

    def weather(self, message, city: str):
        response = requests.get(f"http://api.weatherapi.com/v1/current.json?key=263480053f73422fa5893539230412&q={city}&aqi=no")
        if response.status_code == 400:
            self.bot.send_message(
                message.chat.id,
                "400 | Error. Might no matching location found."
            )
            return
        
        temp_c = response.json()['current']['temp_c']
        self.bot.send_message(
            message.chat.id,
            str(temp_c)
        )

    def currency(self, message, fromc: str, toc: str):
        cresult = self.cclient.latest(base_currency=fromc, currencies=[toc])
        currency = cresult['data'][toc]
        self.bot.send_message(
            message.chat.id,
            f"{fromc}: {currency} {toc}"
        )
        
        

    def start(self, message):   # /start command
        self.bot.send_message(
            message.chat.id,
            'Hello user!\nThis is an example bot.')

    def echo(self, message, value: str):  # /echo [value: str] command
        self.bot.send_message(
            message.chat.id,
            value
            )

    def add(self, message, a: float, b: float):  # /add [a: float] [b: float]
        self.bot.send_message(
            message.chat.id,
            str(a + b)
            )

    def _not_a_command(self):   # This method not considered a command
        print('I am not a command')


class MessageListener(Listener):  # Event listener must inherit Listener
    def __init__(self, bot):
        self.bot = bot
        self.m_count = 0

    def on_message(self, message):   # called on every message
        self.m_count += 1
        print(f'Total messages: {self.m_count}')

    def on_command_failure(self, message, err=None):  # When command fails
        if err is None:
            self.bot.send_message(message.chat.id,
                                  'Command failed to bind arguments!')
        else:
            self.bot.send_message(message.chat.id,
                                  f'Error')
            print(err)


if __name__ == '__main__':
    token = '5511513570:AAGnBWyRqebgkfbGiTTcdZEtUwEBI1QBhFc'
    # token = (argv[1] if len(argv) > 1 else input('Enter bot token: '))
    bot = Bot(token)   # Create instance of OrigamiBot class

    # Add an event listener
    bot.add_listener(MessageListener(bot))

    # Add a command holder
    bot.add_commands(BotsCommands(bot))

    # We can add as many command holders
    # and event listeners as we like

    bot.start()   # start bot's threads
    while True:
        sleep(1)
        # Can also do some useful work i main thread
        # Like autoposting to channels for example