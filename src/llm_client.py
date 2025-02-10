# from zhipuai import ZhipuAI
from openai import OpenAI
from groq import Groq
from together import Together

import json

def load_api_key(platform):
    with open(r"/Users/liubaoyang/Documents/windows/api_key.json", "r", encoding="utf-8") as f:
        api_dict = json.load(f)
    return api_dict.get(platform, None)

# 智谱AI
# client = ZhipuAI(api_key=load_api_key("zhipu"))
# model="glm-4-plus"


# Deepseek
# client = OpenAI(
#     api_key=load_api_key("deepseek"),
#     base_url="https://api.deepseek.com",
# )
# model = "deepseek-chat"

# Deepseek （阿里云）
client = OpenAI(
    api_key=load_api_key("aliyun"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
model = "deepseek-v3"
# model = "deepseek-r1"

# Groq
# client = Groq(
#     api_key=load_api_key("groq")
# )
# model = "llama3-8b-8192"



# Together
# client = Together(api_key=load_api_key("together"))
# model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"