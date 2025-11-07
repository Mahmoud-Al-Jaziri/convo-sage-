"""Mock LLM for testing without OpenAI API."""
from typing import Any, List, Optional
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun


class MockLLM(LLM):
    """
    Mock LLM that simulates responses without calling OpenAI.
    
    Perfect for testing and development when you don't have API credits.
    """
    
    responses: List[str] = [
        "Hello! I'm a helpful AI assistant for ZUS Coffee. How can I help you today?",
        "I'd be happy to help you with that!",
        "That's a great question. Let me assist you with information about ZUS Coffee.",
        "I can help you find ZUS Coffee outlets, learn about our products, or answer any questions you have.",
    ]
    response_index: int = 0
    
    @property
    def _llm_type(self) -> str:
        """Return identifier for this LLM."""
        return "mock"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        Simulate LLM response.
        
        Args:
            prompt: The prompt to respond to
            stop: Stop sequences (ignored in mock)
            run_manager: Callback manager (ignored in mock)
            
        Returns:
            Mock response
        """
        # Extract just the current human message (last line after "Human:")
        lines = prompt.split('\n')
        current_input = ""
        for i in range(len(lines)-1, -1, -1):
            if lines[i].strip().startswith("Human:"):
                current_input = lines[i].replace("Human:", "").strip()
                break
        
        # If we couldn't extract, use last non-empty line
        if not current_input:
            for line in reversed(lines):
                if line.strip() and not line.strip().startswith("AI:"):
                    current_input = line.strip()
                    break
        
        current_lower = current_input.lower()
        prompt_lower = prompt.lower()
        
        # Memory check - if CURRENT input asks about name
        if "what" in current_lower and ("name" in current_lower or "my name" in current_lower):
            # Look in HISTORY (prompt) for the name
            if "my name is sarah" in prompt_lower or "i'm sarah" in prompt_lower:
                return "Your name is Sarah! I remember you mentioned that."
            elif "my name is alex" in prompt_lower or "i'm alex" in prompt_lower:
                return "Your name is Alex! I remember you mentioned that."
            elif "my name is john" in prompt_lower or "i'm john" in prompt_lower:
                return "Your name is John! I remember you mentioned that."
            else:
                return "I don't recall you mentioning your name. What is it?"
        
        # Product questions - check CURRENT input
        if "product" in current_lower or "drinkware" in current_lower or "tumbler" in current_lower:
            return "ZUS Coffee offers a range of high-quality drinkware including insulated tumblers, bottles, and mugs. They're perfect for keeping your drinks hot or cold!"
        
        # Outlet questions
        if "outlet" in current_lower or "location" in current_lower or "store" in current_lower:
            return "ZUS Coffee has outlets across Malaysia, particularly in Kuala Lumpur and Selangor. I can help you find specific locations!"
        
        # Calculation requests
        if any(op in current_lower for op in ["calculate", "+", "-", "*", "/"]) or ("what" in current_lower and "is" in current_lower and any(c.isdigit() for c in current_input)):
            if "5+3" in current_input or "5 + 3" in current_input:
                return "The calculation 5 + 3 equals 8."
            elif "10*2" in current_input or "10 * 2" in current_input:
                return "The calculation 10 * 2 equals 20."
            else:
                return "I can help you with calculations. What would you like me to calculate?"
        
        # Check for name introduction (anywhere in message)
        import re
        if "my name is" in current_lower or "i'm" in current_lower or "i am" in current_lower:
            # Extract name
            name_match = re.search(r"(?:my name is|i'?m|i am)\s+(\w+)", current_input, re.IGNORECASE)
            if name_match:
                name = name_match.group(1).capitalize()
                return f"Hello {name}! Nice to meet you. I'll remember your name. How can I help you today?"
        
        # Greeting responses
        if any(greeting in current_lower for greeting in ["hello", "hi", "hey"]):
            return "Hello! I'm a helpful AI assistant for ZUS Coffee. How can I help you today?"
        
        # Default response - cycle through responses
        response = self.responses[self.response_index % len(self.responses)]
        self.response_index += 1
        return response
    
    @property
    def _identifying_params(self) -> dict:
        """Return identifying parameters."""
        return {"model": "mock-llm"}

