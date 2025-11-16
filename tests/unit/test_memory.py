"""
Unit tests for Memory Manager
"""
import pytest
from memory import MemoryManager


class TestMemoryManager:
    """Test Memory Manager functionality"""
    
    def test_initialization(self):
        """Test memory manager initialization"""
        memory = MemoryManager()
        assert memory.max_short_term == 10
        assert len(memory.short_term) == 0
        assert isinstance(memory.long_term, dict)
    
    def test_add_message(self):
        """Test adding messages to context"""
        memory = MemoryManager()
        memory.add_message("user", "Hello")
        memory.add_message("assistant", "Hi there")
        
        assert len(memory.short_term) == 2
        assert memory.short_term[0]["role"] == "user"
        assert memory.short_term[0]["content"] == "Hello"
        assert memory.short_term[1]["role"] == "assistant"
        assert memory.short_term[1]["content"] == "Hi there"
    
    def test_max_context_length(self):
        """Test context length limit"""
        memory = MemoryManager()
        
        # Add 15 messages (more than max of 10)
        for i in range(15):
            memory.add_message("user", f"Message {i}")
        
        # Should only keep last 10 messages
        assert len(memory.short_term) == 10
        assert memory.short_term[0]["content"] == "Message 5"
        assert memory.short_term[-1]["content"] == "Message 14"
    
    def test_get_context(self):
        """Test retrieving context"""
        memory = MemoryManager()
        memory.add_message("user", "Test message")
        
        context = memory.get_context()
        assert isinstance(context, dict)
        assert "recent_messages" in context
        assert "facts" in context
        assert len(context["recent_messages"]) == 1
        assert context["recent_messages"][0]["content"] == "Test message"
    
    def test_clear_context(self):
        """Test clearing short-term context"""
        memory = MemoryManager()
        memory.add_message("user", "Message 1")
        memory.add_message("user", "Message 2")
        
        assert len(memory.short_term) == 2
        
        memory.clear_short_term()
        assert len(memory.short_term) == 0
    
    def test_context_contains_timestamp(self):
        """Test that messages have timestamps"""
        memory = MemoryManager()
        memory.add_message("user", "Test")
        
        assert "timestamp" in memory.short_term[0]
        assert memory.short_term[0]["timestamp"] is not None
    
    def test_store_and_recall_fact(self):
        """Test storing and recalling long-term facts"""
        memory = MemoryManager()
        memory.store_fact("user_name", "Alice")
        memory.store_fact("user_preference", "dark_mode")
        
        assert memory.recall("user_name") == "Alice"
        assert memory.recall("user_preference") == "dark_mode"
        assert memory.recall("nonexistent") is None
    
    def test_recent_messages_limit(self):
        """Test that get_context returns only last 5 messages"""
        memory = MemoryManager()
        
        # Add 10 messages
        for i in range(10):
            memory.add_message("user", f"Message {i}")
        
        context = memory.get_context()
        # Should return only last 5
        assert len(context["recent_messages"]) == 5
        assert context["recent_messages"][0]["content"] == "Message 5"
