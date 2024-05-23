import requests

"""
Approval：  IDK: https://identity-sandbox.vwgroup.io/oidc/v1/token
            Consent: https://consent-sandbox.vwgroup.io
Live:   IDK: https://identity.idk.vwautocloud.cn/oidc/v1/token
        Consent: https://consent.apps.cn.vwapps.io
"""


url = "https://identity.idk.vwautocloud.cn/oidc/v1/token"


data = {
    "grant_type": "client_credentials",
    "client_id": "a75bab52-033c-4fd7-ad9a-1b42fcd4ed13@apps_vw-dilab_com",
    "client_secret": "49a9e71ebedec93952c907465ea9c852339b5a2a64831911ee7ba0fe5476c08b"
}

try:
    response = requests.post(url, data=data)
    response.raise_for_status()  # 检查请求是否成功
    print(response.json())  # 输出响应的 JSON 数据
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")





