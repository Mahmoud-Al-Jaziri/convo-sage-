"""In-memory storage for conversation sessions."""
from typing import Dict, Optional
from langchain.memory import ConversationBufferMemory
from datetime import datetime
import uuid


class MemoryStore:
    """
    Manages conversation memory for multiple sessions.
    
    Uses in-memory storage (dict) for simplicity.
    In production, this would use Redis or a database.
    """
    
    def __init__(self):
        """Initialize the memory store."""
        self._sessions: Dict[str, ConversationBufferMemory] = {}
        self._session_metadata: Dict[str, dict] = {}
    
        
        """
        Get existing session memory or create a new one.
        
        Args:
            session_id: Optional session ID. If None, creates a new session.
            
        Returns:
            Tuple of (session_id, memory)
        """
        if session_id is None:
            session_id = self._generate_session_id()
        
        if session_id not in self._sessions:
            # Create new memory for this session
            memory = ConversationBufferMemory(
                memory_key="history",
                input_key="input"
            )
            self._sessions[session_id] = memory
            self._session_metadata[session_id] = {
                "created_at": datetime.utcnow(),
                "message_count": 0
            }
        
        return session_id, self._sessions[session_id]
    
    def save_conversation(self, session_id: str, user_message: str, ai_response: str):
        """
        Save a conversation turn to memory.
        
        Args:
            session_id: Session identifier
            user_message: User's message
            ai_response: AI's response
        """
        if session_id in self._sessions:
            memory = self._sessions[session_id]
            memory.save_context(
                {"input": user_message},
                {"output": ai_response}
            )
            # Update metadata
            self._session_metadata[session_id]["message_count"] += 1
            self._session_metadata[session_id]["updated_at"] = datetime.utcnow()
    
    def get_conversation_history(self, session_id: str) -> list:
        """
        Get conversation history for a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of message dictionaries
        """
        if session_id not in self._sessions:
            return []
        
        memory = self._sessions[session_id]
        history = memory.load_memory_variables({})
        
        # Get the history string and parse it
        if "history" in history:
            history_text = history["history"]
            # Simple parsing - in production you'd want more robust parsing
            return [{"history": history_text}]
        
        return []
    
    def clear_session(self, session_id: str):
        """
        Clear a session's memory.
        
        Args:
            session_id: Session identifier
        """
        if session_id in self._sessions:
            self._sessions[session_id].clear()
            self._session_metadata[session_id]["message_count"] = 0
    
    def delete_session(self, session_id: str):
        """
        Delete a session entirely.
        
        Args:
            session_id: Session identifier
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
        if session_id in self._session_metadata:
            del self._session_metadata[session_id]
    
    def get_session_info(self, session_id: str) -> Optional[dict]:
        """
        Get metadata about a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session metadata or None if not found
        """
        return self._session_metadata.get(session_id)
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        return f"session_{uuid.uuid4().hex[:16]}"
    
    @property
    def active_sessions(self) -> int:
        """Get count of active sessions."""
        return len(self._sessions)


# Global instance
memory_store = MemoryStore()

