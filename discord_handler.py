from abc import ABC

from command import Command

class DiscordHandler(ABC):
    
    def connect(self, logic_fun, on_message_fun, token, intents, channel_id: int):
        pass
    
    def execute(self, command: Command):
        pass
    
    def disconnect(self):
        pass
    