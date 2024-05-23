import requests
import json
import hashlib
import hmac
import base64
import time
import uuid
from datetime import datetime, timedelta
from urllib.parse import urlparse


class HmacSignatureUtil:
    HMAC_SHA256_ALGORITHM = "HmacSHA256"

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        if not client_id.strip() or not client_secret.strip():
            raise ValueError("Parameters clientId and clientSecret cannot be empty.")
        self.client_secret = client_secret.encode()

    @staticmethod
    def get_instance(client_id, secret_key):
        return HmacSignatureUtil(client_id, secret_key)

    def signature(self, method, uri, host=None, date=None, nonce=None):
        if host and date and nonce:
            sign_string = f"{method}{uri}\nhost={host}\nx-client-id={self.client_id}\nx-date={date}\nx-nonce={nonce}"
        else:
            sign_string = f"{method}{uri}\nx-client-id={self.client_id}"
        print("签名前内容:", sign_string)
        signature = self.digest(sign_string)
        print("签名后内容:", signature)
        return signature

    def digest(self, body):
        mac_copy = hmac.new(self.client_secret, digestmod=hashlib.sha256)
        mac_copy.update(body.encode())
        byte_val = mac_copy.digest()
        return base64.b64encode(byte_val).decode("ascii")


def request_user(body, url):

    id_secret_li = [
                    {
                        "client_id": "vwa-vur-sit",
                        "client_secret": "i0JCJj3DgsBiasMjdN4Em5eXhaSwqlG9"
                    },
                    # {
                    #     "client_id": "vwa-vur-prod",
                    #     "client_secret": "yCyvfOtqlc5MGeLGrQqsR6bL5QaxTNHQ"
                    # },
                    # {
                    #     "client_id": "vwa-vur-uat",
                    #     "client_secret": "yw7c3vpXPxwRd84G6cgHfPBqI3M2uDv7"
                    # }
                ]

    client_id = id_secret_li[0]["client_id"]
    client_secret = id_secret_li[0]["client_secret"]

    date_str = datetime.utcnow().strftime("%a %d %b %Y %H:%M:%S GMT")
    # print("date:", date_str)
    nonce = str(uuid.uuid4())
    method = "POST"

    parsed_url = urlparse(url)
    host = parsed_url.netloc
    uri = parsed_url.path

    # 2. 实例化，调用签名函数
    instance = HmacSignatureUtil.get_instance(client_id, client_secret)
    uri_signature = instance.signature(method, uri, host, date_str, nonce)
    body_signature = instance.digest(body)

    headers = {
        "Content-Type": "application/json",
        "host": host,
        "x-signature": uri_signature,
        "x-client-id": client_id,
        "uri": url,
        "x-date": date_str,
        "x-nonce": nonce,
        "Accept-Language": "zh_CN",
        "x-digest": body_signature,
        "x-method": method
    }

    # 3. 发起请求
    response = requests.post(url, headers=headers, data=body, timeout=30)

    if response.status_code == 200:
        print("请求成功:")
        print(response.text)
        data = json.loads(response.text)['data']
    else:
        print("请求失败:", response.status_code)
        print(response.text)
        data = []
    # print(data)
    return data


if __name__ == "__main__":

    # 1. 准备参数
    # vin = ["HVWTDMER6PA000450", "LAVTDMERZAA000050"]
    vin = ['LAVB8ZER6P1200117', 'HVWB8ZER4P1200188', 'LAVB7ZER2P1200019', 'LAVB7ZER6P1200038', 'LAVB7ZER3P1200028', 'LAVB8ZER1P1200090', 'HVWB8ZER8P1200209']
    # vin = ['LAVB8ZER6P1200117']
    body = json.dumps(vin)

    # SIT:
    url = "https://api.dev.maezia.com/ezia/vwasp-sit/mos/DPL/v1/primaryUser"
    # url = "https://api.dev.maezia.com/ezia/vwasp-sit/mos/DPL/v1/activeUser"

    # UAT:
    # url = "https://api-uat.maezia.com/ezia/vwasp-uat/mos/DPL/v1/primaryUser"
    # url = "https://api-uat.maezia.com/ezia/vwasp-uat/mos/DPL/v1/activeUser"

    # VWA-UAT:
    # url = "https://external-uat.ci.volkswagen-anhui.com/mos/DPL/v1/primaryUser"
    # url = "https://external-uat.ci.volkswagen-anhui.com/mos/DPL/v1/activeUser"

    pri_user_data = request_user(body, url)
    print(pri_user_data)









