# Bambo
Bambo is a new proxy framework. Compared with mainstream frameworks, it is more lightweight and flexible and can handle various load tasks.

![Bambo_structure](https://github.com/user-attachments/assets/360e9b32-43fc-4b61-956b-5eac579add12)

# USE
1. pip install {packages}. 
- pip install -r requirements.txt  
- (This project uses deepseek as an example. openai needs to be installed.)
2. Define all tools you want to use in the tools directory or other path. The custom function needs to be asynchronous, the parameter passed must include **params_format**, and the default value is False. The **params_format** parameter must be checked at the beginning of the function body. If True, all other parameters that must be passed are returned as a list to verify that the extracted parameters meet the function call requirements when tool_call is used.
3. You need to define the llm you want to call in the llm_cient.py file, including the **model** and **client** parameters.
4. You can then create your own test scripts in the examples folder. In the script, you need to define the /*roles*/ and /*tools*/ that your scenario needs. Bambo's instantiated object is then initialized and query is passed into the object's execute interface, and Bambo starts the execution logic.

- Note:
/*When initializing the Bambo example, in the tools parameters, each tool must be configured with describe and object. describe is the description of the current tool, and what parameters need to be extracted when calling the current tool. object is the function object of the current tool.*/

### Example
```python
import asyncio
from src.bambo import Bambo
from src.llm_client import client, model
from src.tools.code_execute import code_execute
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
async for item in bambo.execute(qeury=query):
    print(item, end="", flush=True)
```

### Note
1. You can redefine your **bambo-role** and pass it in when instantiating the Bambo object to override the default value.


# CASES
##  NotebookLM
- describe: Based on Bambo, notebooklm has achieved a similar effect, which can summarize the main content of the file in the form of an interview conversation with the incoming text. However, there is no TTS related logic in this project, so it can only be converted to text in the form of dialogue. If readers want to implement TTS, they can add corresponding code in the test script.
```
python examples/notebooklm.py
```
- query:"请根据以下参考信息回答问题：\n{reference}\n\n问题：以采访对话形式介绍一下这篇文章的内容，至少5论对话。"
- answer:
  ![notetbook](https://github.com/user-attachments/assets/3cc6a966-3b57-4527-90d1-91edfdb77729)

## PaperRecommend
- The paper recommend tool is an agent for recommending papers every day, which retrieves some of the latest papers at the moment, summarizes them by category, and recommends them according to the user's research direction.
```
python examples/paper_recommend.py
```
- query:
"""
1、请首先搜索最新的10篇论文；
2、然后对这些论文进行分类，类别列表为['LLM','RAG','Agent','多模态','音频','计算机视觉','其它']，分类结果按照{论文标题：类别}的形式输出;
3、对分类后的论文按照类别进行总结，并且给出当前类别有哪些文件，总结结果按照{类别1：类别1多篇论文的总结。类别1的所有参考论文标题。}的形式输出；
4、我的研究方向是['LLM','RAG','Agent','多模态'],请根据我的研究方向，推荐一些相关的论文，推荐结果按照{论文标题：类别、论文链接、摘要的总结}的形式输出；
"""
- answer
```
https://x.com/i/status/1866480838394745075
https://www.bilibili.com/video/BV1ajqCYrEVa/?vd_source=63fa380f22166ecfe2ab8b828b77344d
```

##  MultiRoles
- describe: Multi-role scenarios are implemented based on Bambo for building agent-based team-based scenarios. This project constructs a college entrance examination consulting group, including experts from different majors, who can provide professional responses to students' questions from different majors.
```
python examples/multi_roles.py
```
- query:"我是高考生，现在想要选专业，但是不知道选什么专业。请你介绍一下金融、法律和计算机三个专业分别有什么优点和缺点。"
- answer:
![multi_roles](https://github.com/user-attachments/assets/151758eb-0dcc-4872-8807-5a2cc226e07b)



## CodeExpert
- describe: CodeExpert is a code expert based on the Bambo framework who can answer questions about code and execute code.
```
python examples/code_expert.py
```
- query:"请帮我生成一段选择排序的代码，调用代码执行器运行生成的代码，基于结果分析一下选择排序的特点"
- answer:
![code_expert](https://github.com/user-attachments/assets/e6f54290-3418-47dc-bf93-71515df1ce28)


# Participate
Bambo is currently in its initial stage, more functions will be integrated in the future, and we look forward to more partners joining in. If you would like to work with the author to improve this project, please contact lby15356@gmail.com
