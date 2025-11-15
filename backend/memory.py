'''
Memory Manager - Handles context and state management
'''
from typing import Dict, List, Any
from datetime import datetime
from loguru import logger

class MemoryManager:
    '''Manages short-term and long-term memory for the MCP system'''

    def __init__(self):
        '''Initialize memory systems'''
        self.short_term = []  # Recent conversation
        self.long_term = {}   # Persistent facts
        self.max_short_term = 10

        logger.info("💾 Memory manager initialized")

    def add_message(self, role: str, content: str):
        '''Add message to short-term memory'''
        self.short_term.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Keep only recent messages
        if len(self.short_term) > self.max_short_term:
            self.short_term = self.short_term[-self.max_short_term:]

    def get_context(self) -> Dict[str, Any]:
        '''Get current context for request processing'''
        return {
            "recent_messages": self.short_term[-5:],
            "facts": self.long_term
        }

    def store_fact(self, key: str, value: Any):
        '''Store a persistent fact'''
        self.long_term[key] = value
        logger.info(f"📝 Stored: {key}")

    def recall(self, key: str) -> Any:
        '''Recall a stored fact'''
        return self.long_term.get(key)

    def clear_short_term(self):
        '''Clear short-term memory'''
        self.short_term = []
        logger.info("🧹 Short-term memory cleared")
