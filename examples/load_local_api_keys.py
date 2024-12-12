import json

def load_local_api_keys(platform):
    """
    读取本地json文件中的API密钥
    """
    try:
        with open(r"C:\Users\86187\Desktop\api_key.json", "r", encoding="utf-8") as f:
            api_keys = json.load(f)
        return api_keys[platform]
    except Exception as e:
        raise Exception(f"读取API密钥文件失败: {str(e)}")

if __name__ == "__main__":
    keys = load_local_api_keys()
    print(keys)