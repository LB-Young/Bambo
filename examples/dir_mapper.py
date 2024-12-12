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
    tools = {
        "code_execute": {
            "describe": "代码执行器,参数{'code'：'待执行的代码'},如果代码有多个请合并成一个。",
            "object": code_execute,
        }
    }
    bambo = Bambo(
        client=client,
        bambo_role=None,
        roles=roles,
        tools=tools,
        agents=None,
        model=model,
    )
    query = "请帮我生成一段选择排序的代码，调用代码执行器运行生成的代码，基于结果分析一下选择排序的特点"
    async for item in bambo.execute(query=query):
        print(item, end="", flush=True)



if __name__ == "__main__":
    # TODO: Add a command line interface
    asyncio.run(main())
