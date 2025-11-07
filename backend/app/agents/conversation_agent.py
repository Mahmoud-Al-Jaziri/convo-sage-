"""Conversation agent with LangChain and OpenAI."""
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from app.config import settings
from app.agents.mock_llm import MockLLM


class ConversationAgent:
    """LangChain conversation agent with memory."""
    
    def __init__(self, memory: ConversationBufferMemory):
        """Initialize the agent with memory."""
        self.memory = memory
        
        # Use mock LLM for testing or real OpenAI when you have credits
        if settings.USE_MOCK_LLM:
            self.llm = MockLLM()
            print("🎭 Using Mock LLM (no API calls)")
        else:
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                api_key=settings.OPENAI_API_KEY
            )
            print("🤖 Using OpenAI GPT-3.5-turbo")
        
        # Create conversation chain with memory
        # ConversationChain uses default prompt that works with chat_history
        self.chain = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=False
        )
    
    async def process_message(self, message: str) -> str:
        """Process user message and return AI response."""
        try:
            # Use predict method which is simpler than invoke
            response = self.chain.predict(input=message)
            return response
        except Exception as e:
            print(f"Error in conversation agent: {e}")
            return "I apologize, but I'm having trouble processing your message. Please try again."
