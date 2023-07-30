from __future__ import annotations
from typing import Dict, List
from rules import Rules

class Command:
    COMMAND_SCHEDULED = 0
    COMMAND_DEPENDENT = 1
    COMMAND_ANSWER = 2
    COMMAND_AVOID_OVERLAP = 3
    EXECUTION_TIME_NOT_SET = -1
    
    command: str
    rules: Rules
    next_execution: int
    last_execution:int
    
    def __init__(self, command: str, rules: Dict[str, str]) -> None:
        self.command = command
        self.rules = Rules(**rules)
        self.next_execution = Command.EXECUTION_TIME_NOT_SET
        if (self.is_of_type(Command.COMMAND_SCHEDULED) 
                or self.is_of_type(Command.COMMAND_AVOID_OVERLAP)):
            self.update_next_execution(0)
        self.last_execution = Command.EXECUTION_TIME_NOT_SET
    
    def _get_command_type(self) -> int:
        if self.rules.message_to_answer:
            return Command.COMMAND_ANSWER
        if self.rules.max_interval != None and self.rules.min_interval != None:
            if self.rules.depends_on:
                return Command.COMMAND_DEPENDENT
            elif self.rules.commands_to_avoid != None and self.rules.time_to_avoid != None:
                return Command.COMMAND_AVOID_OVERLAP
            return Command.COMMAND_SCHEDULED
        raise ValueError('The Command is missing some parameters in its rules')
    
    def is_of_type(self, command_type: int) -> bool:
        return self._get_command_type() == command_type
            
    def should_execute(self, current_time: int) -> bool:
        if (self.is_of_type(Command.COMMAND_SCHEDULED)
                or self.is_of_type(Command.COMMAND_AVOID_OVERLAP)):
            return current_time >= self.next_execution
        elif self.is_of_type(Command.COMMAND_DEPENDENT) and self.next_execution > 0:
            return current_time >= self.next_execution
        return False
    
    def update_next_execution(self, current_time: int) -> None:
        if self.is_of_type(Command.COMMAND_ANSWER):
            raise ValueError('The Command is an answer command and cannot be scheduled')
        
        self.last_execution = current_time
        self.next_execution = current_time + self.rules.get_next_interval() 
    
    def is_dependent(self) -> bool:
        return self.rules.depends_on != None
    
    def depends_on (self, command) -> bool:
        if not self.is_dependent():
            return False
        
        return self.rules.depends_on == command.command
    
    def erase_next_execution(self) -> None:
        self.next_execution = Command.EXECUTION_TIME_NOT_SET
        
    def meet_condition(self, message: str) -> bool:
        return self.rules.is_in_message_condition(message)
    
    def get_priority(self) -> bool:
        if self.is_of_type(Command.COMMAND_AVOID_OVERLAP):
            return 1
        return 2
    
    def get_commands_to_avoid(self) -> List[str]:
        if self.rules.commands_to_avoid == None:
            return []
        
        return self.rules.commands_to_avoid
    
    def must_be_avoided(self, commands_to_avoid: List[Command]) -> bool:
        for command in commands_to_avoid:
            if self.is_in_commands_to_avoid(command):
                return (command.is_after_avoidable_command(self.next_execution)
                        or command.is_before_avoidable_command(self.next_execution))
        return False
    
    def is_after_avoidable_command(self, next_execution: int) -> bool:
        return self.last_execution + self.rules.time_to_avoid >= next_execution 
    
    def is_before_avoidable_command(self, next_execution: int) -> bool:
        return self.next_execution - self.rules.time_to_avoid <= next_execution
    
    def is_in_commands_to_avoid(self, command: Command) -> bool:
        return self.command in command.get_commands_to_avoid()