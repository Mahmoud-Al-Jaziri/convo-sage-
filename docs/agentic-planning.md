# Agentic Planning & Tool Calling

This document explains how ConvoSage implements agentic behavior with tool calling using the ReAct pattern.

## Overview

The agent can **decide** whether to:
1. **Respond directly** (normal conversation)
2. **Use a tool** (e.g., calculator for math)
3. **Ask for clarification** (when ambiguous)

## Architecture

```
User Message
     |
     v
 ToolAgent
     |
     ├──> Pattern Detection
     |    ├─ Calculation keywords? ("calculate", "compute", "what is")
     |    └─ Math expression found? (regex: numbers + operators)
     |
     ├──> Tool Dispatch
     |    └─ CalculatorTool._run(expression)
     |
     └──> Conversation
          └─ ConversationAgent (normal LLM response)
```

## Decision Flow

### Step 1: Intent Detection
The agent analyzes the user's message for:
- **Calculation keywords**: "calculate", "compute", "what is", "solve"
- **Mathematical expressions**: Regex pattern matching `\d+[\s]*[+\-*/]+[\s]*\d+`

### Step 2: Tool Selection
If a calculation is detected:
- Extract the mathematical expression
- Call `CalculatorTool`
- Return formatted result

Otherwise:
- Use `ConversationAgent` for normal dialogue

### Step 3: Memory Management
All interactions (both tool calls and conversations) are saved to memory, maintaining context across turns.

## Implementation

### ToolAgent (Simple Pattern-Based)
For the mock LLM, we use a simple pattern-based dispatcher:

```python
async def _simple_tool_dispatch(self, message: str) -> str:
    # Detect calculation intent
    calc_keywords = ["calculate", "compute", "what is", "solve"]
    has_calc_keyword = any(kw in message.lower() for kw in calc_keywords)
    
    # Find math expressions
    math_pattern = r'([\d\s+\-*/().]+)'
    math_matches = re.findall(math_pattern, message)
    
    if has_calc_keyword and math_expression_found:
        # Use calculator tool
        return calculator._run(expression)
    else:
        # Use conversation agent
        return conversation_agent.process_message(message)
```

### ReAct Agent (Full Implementation)
With a real LLM (GPT-3.5/4), we use LangChain's ReAct agent:

```python
from langchain.agents import create_react_agent, AgentExecutor

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    handle_parsing_errors=True
)
```

The ReAct pattern allows the LLM to:
1. **Think**: Reason about what to do
2. **Act**: Use a tool if needed
3. **Observe**: See the tool's output
4. **Respond**: Provide a final answer

## Calculator Tool

### Tool Definition
```python
class CalculatorTool(BaseTool):
    name = "calculator"
    description = (
        "Useful for performing mathematical calculations. "
        "Input should be a valid mathematical expression."
    )
    
    def _run(self, query: str) -> str:
        # Validate and evaluate expression
        result = eval(query, {"__builtins__": {}}, {})
        return f"The result of {query} is {result}"
```

### Security
- Input validation with regex (only numbers and operators)
- Restricted `eval()` with no builtins
- Error handling for division by zero, syntax errors

## Example Interactions

### Example 1: Calculation Request
```
User: "Calculate 5+3"
Agent: Detects "calculate" keyword + "5+3" expression
      → Calls CalculatorTool("5+3")
      → Returns "The result of 5+3 is 8"
```

### Example 2: Normal Conversation
```
User: "What products does ZUS Coffee have?"
Agent: No calculation keywords or math expression
      → Calls ConversationAgent
      → Returns conversational response about products
```

### Example 3: Mixed Conversation
```
User: "Hi! My name is Alex."
Agent: → Conversational response

User: "Can you calculate 10*2?"
Agent: → Calculator tool returns "20"

User: "What's my name?"
Agent: → Uses memory, responds "Your name is Alex!"
```

## Testing

We test three key behaviors:

1. **Tool Invocation**: Agent correctly uses calculator for math
   ```python
   def test_calculator_request():
       response = chat("Calculate 5+3")
       assert "8" in response
   ```

2. **Conversation Preservation**: Normal chat still works
   ```python
   def test_normal_conversation():
       response = chat("Hello!")
       assert response is conversational (not calculation)
   ```

3. **Context Switching**: Can alternate between tools and conversation
   ```python
   def test_mixed_conversation():
       chat("Hi! I'm Bob")
       chat("Calculate 7+5")  # Uses tool
       chat("What's my name?")  # Uses memory
   ```

## Configuration

Toggle between mock and real LLM in `config.py`:

```python
USE_MOCK_LLM: bool = True  # False for GPT-3.5/4
```

Mock LLM uses simple pattern matching, while real LLM uses full ReAct reasoning.

