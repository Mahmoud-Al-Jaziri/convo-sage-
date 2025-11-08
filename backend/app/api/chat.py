"""Chat endpoint for conversational AI."""
from fastapi import APIRouter, HTTPException
from app.models.chat_models import ChatRequest, ChatResponse
from app.agents.memory_store import memory_store
from app.agents.tool_agent import ToolAgent

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint with conversation memory.
    
    Maintains context across multiple turns of conversation using LangChain memory.
    
    Args:
        request: ChatRequest with message and optional session_id
        
    Returns:
        ChatResponse with AI response and session_id
        
    Raises:
        HTTPException: If there's an error processing the message
    """
    try:
        # Get or create session
        session_id, memory = memory_store.get_or_create_session(request.session_id)
        
        # Create tool agent for this session (with calculator support)
        agent = ToolAgent(memory)
        
        # Process message
        ai_response = await agent.process_message(request.message)
        
        # Save to memory store
        memory_store.save_conversation(session_id, request.message, ai_response)
        
        # Return response
        return ChatResponse(
            response=ai_response,
            session_id=session_id
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your message. Please try again."
        )


@router.get("/history/{session_id}")
async def get_history(session_id: str):
    """
    Get conversation history for a session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Conversation history
    """
    history = memory_store.get_conversation_history(session_id)
    session_info = memory_store.get_session_info(session_id)
    
    if not history and not session_info:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "history": history,
        "metadata": session_info
    }


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a conversation session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Success message
    """
    memory_store.delete_session(session_id)
    return {"message": f"Session {session_id} deleted successfully"}


@router.get("/stats")
async def get_stats():
    """
    Get statistics about active sessions.
    
    Returns:
        Session statistics
    """
    return {
        "active_sessions": memory_store.active_sessions
    }

