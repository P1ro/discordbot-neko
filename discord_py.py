import asyncio
from cmath import log
from typing import Callable
from command import Command
from discord_handler import DiscordHandler
from discord.ext import tasks
import discord

from message import Message

class DiscordPy(DiscordHandler):
    
    token: str
    logic_fun: Callable
    on_message_fun: Callable
    channel_id: int
    
    def __init__(self) -> None:
        super().__init__()
    
    def connect(self, logic_fun, on_message_fun, token, channel_id: int):
        self.token = token
        self.logic_fun = logic_fun
        self.on_message_fun = on_message_fun
        self.channel_id = channel_id
        
        self.client = MyClient(
            channel_id=channel_id, 
            logic_fun=logic_fun, 
            on_message_fun=on_message_fun)
        self.client.run(token)
        
    def execute(self, command: Command):
        asyncio.get_running_loop().create_task(
            self.client.execute_message(command.command))
        
    def disconnect(self):
        self.client.close()
    

class MyClient(discord.Client):
    channel_id: str
    logic_fun: Callable
    on_message_fun: Callable

    intents = discord.Intents.default()
    intents.messages = True
    intents.guilds = True
    intents.reactions = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.intents
        self.channel_id = kwargs['channel_id']
        self.logic_fun = kwargs['logic_fun']
        self.on_message_fun = kwargs['on_message_fun']

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        print('Starting')
        self.my_background_task.start()
        
        
    async def execute_message(self, message: str):
        channel = self.get_channel(self.channel_id)
        await channel.send(message)

    @tasks.loop(seconds=1)
    async def my_background_task(self):
        channel = self.get_channel(self.channel_id)  # channel ID goes here
        
        message = [message async for message in channel.history(limit=1)][0]
        if len(message.embeds) == 0: 
            message = Message(message.content)
        else:    
            message = Message(
                str(message.embeds[0].title) + '\n'
                + str(message.embeds[0].description) + '\n'
                + str("\n".join(field.value for field in message.embeds[0].fields))
                )
        
        self.logic_fun()
        self.on_message_fun(message)
        

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

if __name__ == '__main__':
    
    client = MyClient(channel_id=989529457704918298)
    client.run('HIDDEN')
