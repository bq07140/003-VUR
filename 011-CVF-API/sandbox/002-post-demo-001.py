import requests

url = "https://identity-sandbox.vwgroup.io/oidc/v1/token"


data = {
    "grant_type": "client_credentials",
    "client_id": "2ea07a96-657a-45e0-b5c7-2dc4eacfff8a@apps_vw-dilab_com",
    "client_secret": "a972a286b5fbd6cf2d1fcb04404e612e5db0e23904c52b31a2d4a51513feb29c"
}

try:
    response = requests.post(url, data=data)
    response.raise_for_status()  # 检查请求是否成功
    print(response.json())  # 输出响应的 JSON 数据
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")




