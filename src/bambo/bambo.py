import re
import json

class Bambo:
    def __init__(self, client, bambo_role=None, roles=None, tools=None, agents=None, model=None):
        if bambo_role is None:
            bambo_role = self.get_role()
        else:
            pass
        self.roles_info = ""
        for key, value in roles.items():
            self.roles_info += f"@{key}: {value}\n"
        self.tools = {}
        self.tool_describe = []
        for key, value in tools.items():
            self.tools[key] = value["obj"]
            self.tool_describe.append(f"{key}: {value['describe']}\n")
        self.role = bambo_role.replace(r"{roles}", self.roles_info).replace(r"{tools}", "".join(self.tool_describe))
        self.agents = agents
        self.llm_client = client
        self.model = model

    def get_role(self):
        with open(
            r"./src/bambo/bambo_role.txt",
            "r",
            encoding="utf-8",
        ) as f:
            job_describe = f.read()
        return job_describe

    async def agent_run(self, agent_name, agent_job):
        pass

    async def params_extract(self, params_content):
        stack = 0
        params_content = params_content.strip()
        if params_content[0] != "{":
            raise Exception("params_content extract error, can not be parsed to json")
        json_end = 0
        for index, char in enumerate(params_content):
            if char == "{":
                stack += 1
            elif char == "}":
                stack -= 1
            if stack == 0:
                json_end = index + 1
                break
        return json.loads(params_content[:json_end+1])
    
    async def tool_run(self, tool_message):
        function_name, function_params = tool_message.split(":", 1)
        function_params_json = await self.params_extract(function_params)
        need_params = await self.tools[function_name](params_format=True)
        extract_params = {}
        for param in need_params:
            extract_params[param] = function_params_json[param]
        result = await self.tools[function_name](**extract_params)
        return result

    async def execute(self, qeury):
        prompt = self.role.replace("{prompt}", qeury).strip()
        messages = [{"role": "user", "content": prompt}]
        result = self.llm_client.chat.completions.create(
                model=self.model,  # 请填写您要调用的模型名称
                messages=messages,
                stream=True
            )
        all_answer = ""
        tool_messages = ""
        tool_Flag = False
        for chunk in result:
            all_answer += chunk.choices[0].delta.content
            if tool_Flag:
                tool_messages += chunk.choices[0].delta.content
                if "=>@" in tool_messages:
                    tool_messages == tool_messages.split("=>@")[0]
                    break
                continue
            if ":" in chunk.choices[0].delta.content and "=>$" in all_answer:
                tool_Flag = True
                tool_messages += chunk.choices[0].delta.content
                yield ": "
                continue
            yield chunk.choices[0].delta.content
        if tool_Flag:
            tool_messages = all_answer.split("=>$")[-1]
            result = await self.tool_run(tool_message=tool_messages)
            for item in str(result+"\n"):
                yield item
            query = qeury + "\n" + "已经执行内容:" + all_answer + "\n" + "工具执行结果:" + result
            async for item in self.execute(qeury=query):
                yield item
        # result = result.choices[0].message.content
        # print("agent_result:", result)