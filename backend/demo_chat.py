"""Interactive demo to test the chatbot with Mock LLM.

Run this to see how the agent handles different types of queries:
- Outlet searches (Text2SQL)
- Product searches (RAG)
- Calculations
- Normal conversation

Usage:
    python demo_chat.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.agents.tool_agent import ToolAgent
from app.agents.memory_store import memory_store


async def interactive_demo():
    """Interactive chat demo."""
    
    # Create a session
    session_id, memory = memory_store.get_or_create_session()
    
    # Create agent
    agent = ToolAgent(memory)
    
    print("\n" + "="*60)
    print("🎭 ConvoSage Interactive Demo (Mock LLM)")
    print("="*60)
    print("\nTry asking about:")
    print("  🏪 Outlets: 'Where are outlets in KL?'")
    print("  🥤 Products: 'What tumblers do you have?'")
    print("  🔢 Math: 'Calculate 25 * 4'")
    print("  💬 Chat: 'Hi, my name is Sarah'")
    print("\nType 'quit' or 'exit' to stop\n")
    print("="*60 + "\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            # Process message
            response = await agent.process_message(user_input)
            
            # Print response
            print(f"\n🤖 Bot: {response}\n")
            print("-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


async def quick_demo():
    """Quick demo with pre-set questions."""
    
    # Create a session
    session_id, memory = memory_store.get_or_create_session()
    
    # Create agent
    agent = ToolAgent(memory)
    
    print("\n" + "="*60)
    print("🎭 ConvoSage Quick Demo (Mock LLM)")
    print("="*60 + "\n")
    
    # Test questions
    questions = [
        "Where are the outlets in Petaling Jaya?",
        "Which outlets have drive-through?",
        "What tumblers do you have?",
        "Calculate 79 + 45",
        "Hi, my name is Alex",
        "What's my name?",
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. You: {question}")
        response = await agent.process_message(question)
        
        # Truncate long responses for readability
        if len(response) > 300:
            print(f"🤖 Bot: {response[:300]}...\n   [truncated, full response is {len(response)} chars]")
        else:
            print(f"🤖 Bot: {response}")
        
        print("-" * 60)
    
    print("\n✅ Demo complete!")
    print("\nRun with --interactive flag for interactive mode:")
    print("   python demo_chat.py --interactive\n")


if __name__ == "__main__":
    if "--interactive" in sys.argv or "-i" in sys.argv:
        asyncio.run(interactive_demo())
    else:
        asyncio.run(quick_demo())

