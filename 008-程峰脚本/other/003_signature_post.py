import logging
import hashlib
import hmac
import base64
from datetime import datetime
import requests
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SVWHmacSignatureUtil:
    HMAC_SHA256_ALGORITHM = "HmacSHA256"

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        if not client_id.strip() or not client_secret.strip():
            raise ValueError("参数 clientId 和 clientSecret 不能为空")
        try:
            self.mac = hmac.new(client_secret.encode(), digestmod=hashlib.sha256)
        except Exception as e:
            logger.error(f"初始化 SVWHmacSignatureUtil 失败: {e}")

    @classmethod
    def getInstance(cls, client_id, secret_key):
        return cls(client_id, secret_key)

    def signature(self, method, uri, host, date, nonce):
        sign_string = f"{method}{uri}\nhost={host}\nx-client-id={self.client_id}\nx-date={date}\nx-nonce={nonce}"
        logger.info("签名前内容:\n" + sign_string)
        self.mac.update(sign_string.encode())
        signature = self.digest()
        logger.info("签名后内容:\n" + signature)
        return signature

    def digest(self):
        return base64.b64encode(self.mac.digest()).decode('ascii')

#
# # 示例用法
# client_id = "vwa-vur-sit"
# client_secret = "i0JCJj3DgsBiasMjdN4Em5eXhaSwqlG9"
#
# util = SVWHmacSignatureUtil.getInstance(client_id, client_secret)
# method = "POST"
# uri = "/ezia/vwasp-sit/mos/DPL/v1/activeUser"
# host = "api.dev.maezia.com"
# date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
# nonce = "your_nonce"
# signature = util.signature(method, uri, host, date, nonce)
# print("Signature:", signature)


# 1. 主函数
def main(uri, body):
    # "vwa-vur-prod": "yCyvfOtqlc5MGeLGrQqsR6bL5QaxTNHQ",
    # "vwa-vur-uat": "yw7c3vpXPxwRd84G6cgHfPBqI3M2uDv7",
    # "vwa-vur-sit": "i0JCJj3DgsBiasMjdN4Em5eXhaSwqlG9",  #

    client_id = "vwa-vur-sit"
    client_secret = "i0JCJj3DgsBiasMjdN4Em5eXhaSwqlG9"

    util = SVWHmacSignatureUtil(client_id, client_secret)

    method = "POST"
    # host = "ingress-sit.ma"  # http://ingress-sit.ma  003
    host = "api.dev.maezia.com"  # http://ingress-sit.ma  003
    # date = "Mon, 13 Apr 2020 10:22:50 GMT"  # 现在时间
    # 获取当前时间
    now = datetime.utcnow()
    # 将当前时间格式化为指定格式
    date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    # print(date)
    nonce = "random_nonce"

    uri_signature = util.signature(method, uri, host, date, nonce)
    print("uri_signature:", uri_signature)
    
    # body_signature = util.digest(body)
    # print("body_signature:", body_signature)

    return uri_signature, date, client_id, nonce, host
    # return uri_signature, date, client_id, nonce, body_signature, host


if __name__ == "__main__":

    # SIT:
    # https://api.dev.maezia.com/ezia/vwasp-sit/mos/DPL/v1/primaryUser
    # https://api.dev.maezia.com/ezia/vwasp-sit/mos/DPL/v1/activeUser

    # UAT:
    # https://api-uat.maezia.com/ezia/vwasp-uat/mos/DPL/v1/primaryUser
    # https://api-uat.maezia.com/ezia/vwasp-uat/mos/DPL/v1/activeUser

    # VWA-UAT:
    # https://external-uat.ci.volkswagen-anhui.com/mos/DPL/v1/primaryUser
    # https://external-uat.ci.volkswagen-anhui.com/mos/DPL/v1/activeUser

    # # 1.1 uri签名
    # uri = "/vwasp-sit-vur-service-dbr/DPL/v1/activeUser"  # 获取活跃用户切换信息
    # # uri = "/vwasp-sit-vur-service-dbr/DPL/v1/primaryUser"  # 主用户

    uri = "/ezia/vwasp-sit/mos/DPL/v1/activeUser"  # 活跃用户
    # uri = "/ezia/vwasp-uat/mos/DPL/v1/activeUser"  # 活跃用户
    # uri = "/mos/DPL/v1/activeUser"  # 活跃用户

    # uri = "/ezia/vwasp-sit/mos/DPL/v1/primaryUser"  # 主用户
    # uri = "/ezia/vwasp-uat/mos/DPL/v1/primaryUser"  # 主用户
    # uri = "/mos/DPL/v1/primaryUser"  # 主用户

    # 1.2 body签名
    vin_li = ['HVWTDMER6PA000450', 'LAVTDMERZAA000050']
    body = json.dumps(vin_li)

    uri_signature, date, client_id, nonce, host = main(uri, body)
    # uri_signature, date, client_id, nonce, body_signature, host = main(uri, body)

    # # 2. url拼接
    # url = 'http://ingress-sit.ma' + uri  # 活跃用户

    url = 'https://api.dev.maezia.com' + uri  # 主用户
    # url = 'https://api-uat.maezia.com' + uri  # 主用户
    # url = 'https://external-uat.ci.volkswagen-anhui.com' + uri  # 主用户

    print(url)

    # # 3. header
    # headers = {
    #     "accept": "*/*",
    #     "Content-Type": "application/json",
    #     'Host': host,
    #     'X-Digest': body_signature,
    #     'X-Signature': uri_signature,
    #     'X-Client-Id': client_id,
    #     'Uri': url,
    #     'X-Nonce': nonce,
    #     'X-Date': date,
    #     'X-Method': 'POST'
    # }
    #
    # response = requests.post(url, headers=headers, data=body)
    #
    # if response.status_code == 200:
    #     print("请求成功:")
    #     print(response.text)
    # else:
    #     print("请求失败:", response.status_code)
    #     print(response.text)