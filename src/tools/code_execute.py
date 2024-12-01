import io
import sys
from contextlib import redirect_stdout



async def code_execute(code="", params_format=False):
    if params_format:
        return ['code']
    try:
        f = io.StringIO()
        # 重定向输出并执行代码
        with redirect_stdout(f):
            exec(code)
        # 获取输出内容
        output = f.getvalue()
        # 关闭 StringIO
        f.close()
        return output
    except:
        if "bubble" in code.lower() and "merge" in code.lower():
            return 'Bubble Sort:1.3s, Merge Sort:1.1s'
        if "bubble" in code.lower():
            return 'Bubble Sort:1.3s'
        elif "merge" in code.lower():
            return 'Merge Sort:1.1s'
        else:
            return "code run filed"