"""
Unit tests for Memory Manager
"""
import pytest
from memory import MemoryManager


class TestMemoryManager:
    """Test Memory Manager functionality"""
    
    def test_initialization(self):
        """Test memory manager initialization"""
        memory = MemoryManager(max_context_length=5)
        assert memory.max_context_length == 5
        assert len(memory.context) == 0
    
    def test_add_message(self):
        """Test adding messages to context"""
        memory = MemoryManager(max_context_length=5)
        memory.add_message("user", "Hello")
        memory.add_message("assistant", "Hi there")
        
        assert len(memory.context) == 2
        assert memory.context[0]["role"] == "user"
        assert memory.context[0]["content"] == "Hello"
        assert memory.context[1]["role"] == "assistant"
        assert memory.context[1]["content"] == "Hi there"
    
    def test_max_context_length(self):
        """Test context length limit"""
        memory = MemoryManager(max_context_length=3)
        
        for i in range(5):
            memory.add_message("user", f"Message {i}")
        
        # Should only keep last 3 messages
        assert len(memory.context) == 3
        assert memory.context[0]["content"] == "Message 2"
        assert memory.context[-1]["content"] == "Message 4"
    
    def test_get_context(self):
        """Test retrieving context"""
        memory = MemoryManager()
        memory.add_message("user", "Test message")
        
        context = memory.get_context()
        assert isinstance(context, list)
        assert len(context) == 1
        assert context[0]["content"] == "Test message"
    
    def test_clear_context(self):
        """Test clearing context"""
        memory = MemoryManager()
        memory.add_message("user", "Message 1")
        memory.add_message("user", "Message 2")
        
        assert len(memory.context) == 2
        
        memory.clear()
        assert len(memory.context) == 0
    
    def test_context_contains_timestamp(self):
        """Test that messages have timestamps"""
        memory = MemoryManager()
        memory.add_message("user", "Test")
        
        assert "timestamp" in memory.context[0]
        assert memory.context[0]["timestamp"] is not None
