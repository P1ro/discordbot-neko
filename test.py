import time
import discord

CHANNEL_ID = 989529457704452198

class MyClient(discord.Client):
    
    async def on_ready(self):
        print('Logged on as', self.user)
        channel = self.get_channel(CHANNEL_ID)
        await channel.send('!crime')
        time.sleep(5)
        messages = [message async for message in channel.history(limit=1)]
        for message in messages:
            print(message)
            print(message.author)
            print(message.content)
            print(message.created_at)
            print(message.mentions)
            if len(message.embeds) > 0:
                print(message.embeds[0].description)
                print(message.embeds[0].title)
                print(message.embeds[0].footer)
            if len(message.components) > 0:
                print(message.components[0])
                await message.components[0].children[0].click()
            
        
        
client = MyClient()
client.run('MzE1NzY0MjQzMjM0MjkxNzEy.GO2-o_.lwJfmqfJfQ-1edh1kRt72UObosJFg8eY8L0XG0')