import datetime
import time
from typing import List, Optional

from command import Command
from discord_handler import DiscordHandler
from discord_py import DiscordPy
from message import Message
from config import TOKEN, CHANNEL_ID, COMMANDS

class Executor:
    
    start_time: int
    commands: List[Command]
    discord: DiscordHandler
    last_message: Optional[Message] = None
    
    def __init__(self) -> None:
        self.start_time = int(time.time())
        self.discord = DiscordPy()
        self.commands = []
    
    def start(self):
        self.commands = [Command(**command) for command in COMMANDS]
        self.discord.connect(
            self.execute_logic,
            self.on_message_received,
            TOKEN,
            CHANNEL_ID)           
    
    def execute_logic(self):
        execution_time = self._get_execution_time()
        command_list = self._get_sorted_command_list()
        dependent_commands = [command for command in command_list if command.is_dependent()]    
        commands_to_avoid = [command for command in command_list if command.is_of_type(Command.COMMAND_AVOID_OVERLAP)]
        
        for command in command_list:
            if command.should_execute(execution_time):
                if not command.must_be_avoided(commands_to_avoid):
                    self.discord.execute(command)
                else:
                    print(f'Command {command.command} avoided')
                if (command.is_of_type(Command.COMMAND_SCHEDULED)
                        or command.is_of_type(Command.COMMAND_AVOID_OVERLAP)):
                    command.update_next_execution(execution_time)
                elif command.is_of_type(Command.COMMAND_DEPENDENT):
                    command.erase_next_execution()
                for dependent_command in dependent_commands:
                    if dependent_command.depends_on(command):
                        dependent_command.update_next_execution(execution_time)
            
        
    def on_message_received(self, message: Message):
        if not (self.last_message and self.last_message.is_same_as(message)):
            print(f'Message received: {datetime.datetime.now().isoformat()} {message.content}')
            self.last_message = message
        #print(message.content)
        for command in self.commands:
            if command.is_of_type(Command.COMMAND_ANSWER):
                if command.meet_condition(message.get_content()):
                    self.discord.execute(command)
    
    def _get_execution_time(self) -> int:
        return int(time.time()) - self.start_time
    
    def _get_command_list(self) -> List[Command]:
        return self.commands
    
    def _get_sorted_command_list(self) -> List[Command]:
        return sorted(
            self._get_command_list(), 
            key=lambda command: command.get_priority())
    