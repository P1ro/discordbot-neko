import asyncio
from typing import Callable
from discord.ext import tasks
import discord
from message import Message
from command import Command

class DiscordPy(discord.Client):
    def __init__(self, logic_fun: Callable, on_message_fun: Callable, token: str, channel_id: int):
        super().__init__()
        self.logic_fun = logic_fun
        self.on_message_fun = on_message_fun
        self.channel_id = channel_id
        self.token = token

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        print('Starting')
        self.my_background_task.start()

    async def execute_message(self, message: str):
        channel = self.get_channel(self.channel_id)
        if not channel:
            print(f"Channel with ID {self.channel_id} not found. Make sure the bot is in the server and the channel exists.")
            return

        await channel.send(message)

    @tasks.loop(seconds=1)
    async def my_background_task(self):
        channel = self.get_channel(self.channel_id)
        if not channel:
            print(f"Channel with ID {self.channel_id} not found. Make sure the bot is in the server and the channel exists.")
            return

        message = [message async for message in channel.history(limit=1)]
        if not message:
            print("No messages found in the channel.")
            return

        message = message[0]
        if len(message.embeds) == 0:
            message_obj = Message(message.content)
        else:
            message_obj = Message(
                str(message.embeds[0].title) + '\n'
                + str(message.embeds[0].description) + '\n'
                + str("\n".join(field.value for field in message.embeds[0].fields))
            )

        self.logic_fun()
        self.on_message_fun(message_obj)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

    def execute(self, command: Command):
        asyncio.get_running_loop().create_task(
            self.execute_message(command.command)
        )

    def disconnect(self):
        self.my_background_task.cancel()
        asyncio.get_event_loop().run_until_complete(self.logout())

if __name__ == '__main__':
    def logic_function():
        print("Logic function called.")

    def on_message_function(message):
        print(f"Received message: {message}")

    client = DiscordPy(logic_fun=logic_function, on_message_fun=on_message_function, token='MTEzNTAyMjc5MjQyNTg2NTI5Ng.Gw1voT.S7MDjReB-R-B6soRgfF1RyoiHiuWodDxyQIjL0', channel_id=989529457704452198)
    client.run(client.token)


    #client = DiscordPy(logic_fun=logic_function, on_message_fun=on_message_function, token='MTEzNTAyMjc5MjQyNTg2NTI5Ng.Gw1voT.S7MDjReB-R-B6soRgfF1RyoiHiuWodDxyQIjL0', channel_id=955667648845316146)
    #client.run(client.token)
