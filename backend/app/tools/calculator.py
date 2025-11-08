"""Calculator tool for mathematical expressions."""
from typing import Optional
from langchain.tools import BaseTool
from pydantic import Field
import re


class CalculatorTool(BaseTool):
    """
    A simple calculator tool that evaluates mathematical expressions.
    Supports basic arithmetic: +, -, *, /, **, ()
    """
    
    name: str = "calculator"
    description: str = (
        "Useful for performing mathematical calculations. "
        "Input should be a valid mathematical expression like '5+3' or '10*2'. "
        "Supports +, -, *, /, ** (power), and parentheses."
    )
    
    def _run(self, query: str) -> str:
        """
        Execute the calculator tool.
        
        Args:
            query: Mathematical expression as a string
            
        Returns:
            Result of the calculation or error message
        """
        try:
            # Clean the input
            query = query.strip()
            
            # Security: Only allow numbers, operators, spaces, and parentheses
            if not re.match(r'^[\d\s+\-*/.()]+$', query):
                return "Error: Invalid characters in expression. Only numbers and operators (+, -, *, /, **) are allowed."
            
            # Evaluate the expression safely
            # Using eval with restricted globals/locals for safety
            result = eval(query, {"__builtins__": {}}, {})
            
            return f"The result of {query} is {result}"
            
        except ZeroDivisionError:
            return "Error: Division by zero is not allowed."
        except SyntaxError:
            return "Error: Invalid mathematical expression. Please check your syntax."
        except Exception as e:
            return f"Error calculating '{query}': {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the tool (calls sync version)."""
        return self._run(query)

