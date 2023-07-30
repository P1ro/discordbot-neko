from dataclasses import dataclass
import random
from typing import List, Optional

@dataclass
class Rules:
    max_interval: Optional[int]
    min_interval: Optional[int]
    depends_on: Optional[str] = None
    message_to_answer: Optional[str] = None
    commands_to_avoid: Optional[List[str]] = None
    time_to_avoid: Optional[int] = None
    
    def get_next_interval(self):
        if self.max_interval == None or self.min_interval == None:
            raise ValueError('Rules are missing max and min interval')
        
        return random.random() * (self.max_interval - self.min_interval) + self.min_interval
    
    def is_in_message_condition(self, message: str) -> bool:
        if self.message_to_answer == None:
            return False
    
        return self.message_to_answer in message