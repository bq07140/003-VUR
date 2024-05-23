import hashlib
import hmac
import base64
import logging
import requests
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SVWHmacSignatureUtil:
    HMAC_SHA256_ALGORITHM = "HmacSHA256"

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        if not client_id or not client_secret:
            raise ValueError("clientId和clientSecret不能为空")
        self.mac = hmac.new(client_secret.encode(), digestmod=hashlib.sha256)

    @classmethod
    def getInstance(cls, client_id, secret_key):
        return cls(client_id, secret_key)

    def signature(self, method, uri, host, date, nonce):
        sign_string = "\n".join(
            [method + uri, f"host={host}", f"x-client-id={self.client_id}", f"x-date={date}", f"x-nonce={nonce}"])
        logger.info("签名前内容:\n" + sign_string)
        signature = self.digest(sign_string)
        logger.info("签名后内容:\n" + signature)
        return signature

    # def digest(self, body):
    #     byte_val = self.mac.copy().update(body.encode())
    #     return base64.b64encode(byte_val.digest()).decode("ascii")

    def digest(self, body):
        byte_val = self.mac.copy()
        byte_val.update(body.encode())
        return base64.b64encode(byte_val.digest()).decode("ascii")


# 1. 主函数
def main(uri):
    # "vwa-vur-prod": "yCyvfOtqlc5MGeLGrQqsR6bL5QaxTNHQ",
    # "vwa-vur-uat": "yw7c3vpXPxwRd84G6cgHfPBqI3M2uDv7",
    # "vwa-vur-sit": "i0JCJj3DgsBiasMjdN4Em5eXhaSwqlG9",  #

    client_id = "vwa-vur-sit"
    client_secret = "i0JCJj3DgsBiasMjdN4Em5eXhaSwqlG9"
    util = SVWHmacSignatureUtil(client_id, client_secret)
    method = "GET"
    # uri = "/vwasp-sit-vur-service-dbr/DPL/v1/activeUser"  # 获取活跃用户切换信息
    host = "ingress-sit.ma"  # http://ingress-sit.ma
    # date = "Mon, 13 Apr 2020 10:22:50 GMT"  # 现在时间
    # 获取当前时间
    now = datetime.utcnow()
    # 将当前时间格式化为指定格式
    date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    # print(date)
    nonce = "random_nonce"
    signature = util.signature(method, uri, host, date, nonce)
    print("Signature:", signature)

    return signature, date, client_id, nonce


if __name__ == "__main__":

    # 1. 获取签名
    uri = "/vwasp-sit-vur-service-dbr/DPL/v1/activeUser?"  # 获取活跃用户切换信息
    signature, date, client_id, nonce = main(uri)

    # 2. url拼接
    url = 'http://ingress-sit.ma' + uri  # 活跃用户
    print(url)
    # vinList=1&vinList=2
    vin_li = ['HVWTDMER6PA000450', 'LAVTDMERZAA000050']
    vin_str = ['vinList=' + str(i) for i in vin_li]
    vin_str_join = "&".join(vin_str)
    url += vin_str_join
    print(url)

    # 3. header
    headers = {
        'Host': 'ingress-sit.ma',
        'X-Signature': signature,
        'X-Client-Id': client_id,
        'X-Nonce': nonce,
        'X-Date': date,
        'X-Method': 'GET'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("请求成功:")
        print(response.text)
    else:
        print("请求失败:", response.status_code)
        print(response.text)







