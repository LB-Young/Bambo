import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import asyncio
from src.bambo import Bambo
from src.llm_client import client, model
from src.tools.code_execute import code_execute


async def main():
    roles = {
        "host": "采访记者",
        "expert": "专家",
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

    with open(r"C:\Users\86187\Desktop\test.txt", "r", encoding="utf-8") as f:
        reference = f.read()
    query = f"请根据以下参考信息回答问题：\n{reference}\n\n问题：以采访对话形式介绍一下这篇文章的内容，至少5论对话。"
    async for item in bambo.execute(qeury=query):
        print(item, end="", flush=True)


if __name__ == "__main__":
    # TODO: Add a command line interface
    asyncio.run(main())
