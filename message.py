from __future__ import annotations

class Message:
    content: str
    
    def __init__(self, message: str) -> None:
        self.content = message
        
    def get_content(self):
        return self.content
    
    def is_same_as(self, message: Message) -> bool:
        return self.content == message.content