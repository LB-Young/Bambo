import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import asyncio
from src.bambo import Bambo
from src.llm_client import client, model
from src.tools.code_execute import code_execute


async def main():
    roles = {
        "finance_expert": "金融专家",
        "law_expert": "法律专家",
        "medical_expert": "医疗专家",
        "computer_expert": "计算机专家",
    }
    tools = {}
    bambo = Bambo(
        client=client,
        bambo_role=None,
        roles=roles,
        tools=tools,
        agents=None,
        model=model,
    )
    messages = []
    
    # Add default initial question about team experts
    default_question = "介绍一下你们团队的专家吧。"
    messages.append({"role": "user", "content": default_question})
    
    # Get initial response about team experts
    response = ""
    async for item in bambo.execute(messages=messages):
        print(item, end="", flush=True)
        response += item
    
    # Add assistant's response to messages for context
    messages.append({"role": "assistant", "content": response})
    
    while True:
        # Get user input
        query = input("\nPlease enter your question (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
            
        # Add user's query to messages
        messages.append({"role": "user", "content": query})
        
        # Collect assistant's response
        response = ""
        async for item in bambo.execute(messages=messages):
            print(item, end="", flush=True)
            response += item
            
        # Add assistant's response to messages for context
        messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    # TODO: Add a command line interface
    asyncio.run(main())
