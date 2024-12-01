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
    query = "我是高考生，现在想要选专业，但是不知道选什么专业。请你介绍一下金融、法律和计算机三个专业分别有什么优点和缺点。"
    # query = "炒股的时候什么时候买进比较好？"
    # query = "请介绍一下主流的数组排序算法的优缺点。"
    async for item in bambo.execute(qeury=query):
        print(item, end="", flush=True)


if __name__ == "__main__":
    # TODO: Add a command line interface
    asyncio.run(main())
