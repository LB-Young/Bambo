import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import asyncio
from src.bambo import Bambo
from src.llm_client import client, model
from src.tools.code_execute import code_execute
from src.tools.paper_search import paper_search

async def main():
    roles = {
        "paper_classification_expert": "论文分类专家",
        "paper_summary_expert": "论文总结专家",
        "paper_recommend_expert": "论文推荐专家",
    }
    tools = {
        "code_execute": {
            "describe": "代码执行器,参数{'code'：'待执行的代码'},如果代码有多个请合并成一个。",
            "obj": code_execute,
        },
        "paper_search":{
            "obj":paper_search,
            "describe":"搜索最新的论文，需要参数{'nums':需要读取的论文数目}",
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
    query = """
1、请首先搜索最新的10篇论文；
2、然后对这些论文进行分类，类别列表为['LLM','RAG','Agent','多模态','音频','计算机视觉','其它']，分类结果按照{论文标题：类别}的形式输出;
3、对分类后的论文按照类别进行总结，并且给出当前类别有哪些文件，总结结果按照{类别1：类别1多篇论文的总结。类别1的所有参考论文标题。}的形式输出；
4、我的研究方向是['LLM','RAG','Agent','多模态'],请根据我的研究方向，推荐一些相关的论文，推荐结果按照{论文标题：类别、论文链接、摘要的总结}的形式输出；
"""
    async for item in bambo.execute(qeury=query):
        print(item, end="", flush=True)



if __name__ == "__main__":
    # TODO: Add a command line interface
    asyncio.run(main())
