# 1. 要用安徽那边的测试环境 的vin。
# 2. vin和userId，要保证匹配。
import requests

"""
vin
HVWTDMER8PA000448  8711c8c8-56a0-48bf-a255-3fa28e9ad902
HVWTDMERZPA000396  93f167b8-393d-4f65-9de0-a23c987da630
HVWTDMER6PA000450  2682fead-d5ad-40e4-baac-872d4c387af1
"""

# 中国地区服务器的接口地址
url = "https://cardata.sandbox.cn.vcf.apps.vwautocloud.cn/vehicles/{vin}/charging/status"

# 假设你有一个有效的VIN
vin = "HVWTDMER6PA000450"
# vin = "HVWTDMER8PA000448"
# vin = "HVWTDMERZPA000396"
# vin = "HVWTDMER6PA000450"

# 请求头中需要提供User-ID，这里假设为一个有效的用户ID
headers = {
    "Authorization": "Bearer eyJraWQiOiI3OThkNzA5NC1lNTljLTQwMDQtODE4OC1iZjdjMTdkYzlkZGIiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyZWEwN2E5Ni02NTdhLTQ1ZTAtYjVjNy0yZGM0ZWFjZmZmOGFAYXBwc192dy1kaWxhYl9jb20iLCJhdWQiOiIyZWEwN2E5Ni02NTdhLTQ1ZTAtYjVjNy0yZGM0ZWFjZmZmOGFAYXBwc192dy1kaWxhYl9jb20iLCJhYXQiOiJpZGVudGl0eWtpdCIsImlzcyI6Imh0dHBzOi8vaWRlbnRpdHktc2FuZGJveC52d2dyb3VwLmlvIiwianR0IjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzE1NzQ4NDA4LCJpYXQiOjE3MTU3NDQ4MDgsImxlZSI6WyJWV19BTkhVSSJdLCJqdGkiOiJkNzg4YjY2My1kY2M5LTRmMjktYWI2ZC0zMGZiYWIxNjQwZWUifQ.ryms35kNDY3rOjSp17wD0GdMAmaGsfVnJWnmjoMT9_bw_0guJ-966oP-AYuNPYDV0fJGXoZ7ZTW_IA4AhtIU_9VniYgcrjdzDtjyQch8YfWbvIGo49DzRVPROv1dvutInnUPmIuSbQuuzwvc1OpjY5Y1U6loN_JuzM60odOtKLZa-ldQeXq3DKp0KbQJ-41rnwi-gnlu7q4VK_DSp8FDgPcvUCBsUD9LnejeGjS8F2be7GBvhACbyxSBUHLioBxismUo_Xi3OZ--vZ48wz5HEjdVKi9M-sPZ2Tdb3mei_atYlZJThKc7EjsLybc6kC_76X3ls0KJwAKN1eud-1jG5tFyoKfK_jBQI50-FlG-ia23aZh-EQg5KLbhk_VBcW-a1IUyxQD1-eiF6a0Cv0P5TO_Y-AcmPZCFMpcQPpYflgPo4v2kpgmB0B1rkG0T_l6zApbhQmvZzumusOKwI7B0ndKs2OcIf9loyYAm74YCnHE6iWZNGcnZL91ejLUAZoBfKKiNBQGXEpt64HDoj6eUjrTw49RLgEuCKmGsHJwsQ2aiYlkyJNFm3w1mEgcobguA7bfSCFjezlFZo50NsWUL02York8aCuO_jkUXHhwooMWHRVBlLlj7Dvb-OV581Ye6QHcKUMgLAqr7sooA9BiGvpVh3x3DK_lx207YESvQ7zQ",
    "User-ID": "2682fead-d5ad-40e4-baac-872d4c387af1",
    # "User-ID": "8711c8c8-56a0-48bf-a255-3fa28e9ad902",
    # "User-ID": "93f167b8-393d-4f65-9de0-a23c987da630",
    # "User-ID": "2682fead-d5ad-40e4-baac-872d4c387af1",
}

try:
    # 发起GET请求
    response = requests.get(url.format(vin=vin), headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        # 请求成功，打印响应内容
        print("请求成功:")
        print(response.json())
    else:
        # 请求失败，打印状态码和错误信息
        print("请求失败，状态码:", response.status_code)
        print("错误信息:", response.text)
except Exception as e:
    # 发生异常，打印异常信息
    print("发生异常:", str(e))




