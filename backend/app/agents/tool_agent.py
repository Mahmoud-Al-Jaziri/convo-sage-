"""ReAct agent with tool calling capabilities."""
from typing import List, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import BaseTool
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain import hub

from app.config import settings
from app.agents.mock_llm import MockLLM
from app.tools.calculator import CalculatorTool
from app.tools.product_search import ProductSearchTool


class ToolAgent:
    """
    Agent with tool-calling capabilities using ReAct pattern.
    Can decide when to use tools vs. respond directly.
    """
    
    def __init__(self, memory: ConversationBufferMemory, tools: Optional[List[BaseTool]] = None):
        """
        Initialize the tool agent.
        
        Args:
            memory: Conversation memory
            tools: List of tools available to the agent
        """
        self.memory = memory
        
        # Initialize LLM (mock or real)
        if settings.USE_MOCK_LLM:
            self.llm = MockLLM()
            print("🎭 Using Mock LLM with tools (simplified)")
        else:
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                api_key=settings.OPENAI_API_KEY
            )
            print("🤖 Using OpenAI GPT-3.5-turbo with tools")
        
        # Initialize tools
        self.tools = tools or [CalculatorTool(), ProductSearchTool()]
        
        # For mock LLM, we'll use a simple pattern matcher instead of full ReAct
        # In production with real LLM, we'd use create_react_agent
        self.use_simple_agent = settings.USE_MOCK_LLM
        
        if not self.use_simple_agent:
            # Create ReAct agent with tools (for real LLM)
            try:
                prompt = hub.pull("hwchase17/react")
                self.agent = create_react_agent(self.llm, self.tools, prompt)
                self.agent_executor = AgentExecutor(
                    agent=self.agent,
                    tools=self.tools,
                    memory=self.memory,
                    verbose=False,
                    handle_parsing_errors=True
                )
            except Exception as e:
                print(f"Warning: Could not create ReAct agent: {e}")
                self.use_simple_agent = True
    
    async def process_message(self, message: str) -> str:
        """
        Process a message with tool calling capability.
        
        Args:
            message: User's input message
            
        Returns:
            Agent's response
        """
        try:
            if self.use_simple_agent:
                # Simple pattern-based tool calling for mock LLM
                return await self._simple_tool_dispatch(message)
            else:
                # Use full ReAct agent for real LLM
                response = await self.agent_executor.ainvoke({"input": message})
                return response["output"]
                
        except Exception as e:
            print(f"Error in tool agent: {e}")
            return "I apologize, but I encountered an error processing your request. Please try again."
    
    async def _simple_tool_dispatch(self, message: str) -> str:
        """
        Simple tool dispatcher for mock LLM.
        Detects tool requests: calculations, product search, etc.
        """
        import re
        
        message_lower = message.lower()
        
        # Check for product search requests
        product_keywords = ["product", "tumbler", "bottle", "cup", "mug", "drinkware", 
                           "buy", "purchase", "price", "available", "stock"]
        has_product_keyword = any(kw in message_lower for kw in product_keywords)
        
        if has_product_keyword:
            # Use product search tool
            for tool in self.tools:
                if tool.name == "product_search":
                    result = tool._run(message)
                    return result
        
        # Check if this is a calculation request
        calc_keywords = ["calculate", "compute", "what is", "solve"]
        has_calc_keyword = any(kw in message_lower for kw in calc_keywords)
        
        # Look for mathematical expressions (including parentheses)
        math_pattern = r'([\d\s+\-*/().]+)'
        # Find all potential math expressions
        potential_matches = re.findall(math_pattern, message)
        
        # Find the longest valid math expression
        math_match = None
        longest_expr = ""
        for match in potential_matches:
            cleaned = match.strip()
            # Check if it contains operators and numbers
            if re.search(r'\d', cleaned) and re.search(r'[+\-*/]', cleaned):
                if len(cleaned) > len(longest_expr):
                    longest_expr = cleaned
                    math_match = True
        
        if (has_calc_keyword or math_match) and longest_expr:
            # Use the longest expression found
            expression = longest_expr.replace(" ", "")
            
            # Use calculator tool
            calculator = CalculatorTool()
            result = calculator._run(expression)
            
            # Save to memory manually (since we're not using ConversationChain)
            self.memory.save_context(
                {"input": message},
                {"output": result}
            )
            
            return result
        else:
            # No tool needed, use conversation LLM
            from app.agents.conversation_agent import ConversationAgent
            conv_agent = ConversationAgent(self.memory)
            return await conv_agent.process_message(message)

