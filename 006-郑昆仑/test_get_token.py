"""
使用前先安装requests和pytest
"""
# congding=uft-8
import requests
import time
import pytest


# case1获取token成功

class Test_Get_Token:
    def setup_method(self):
        print("新测试场景开始")

    def teardown_method(self):
        print("新测试场景结束")

    url = 'http://10.41.3.224/tdr-tdreport-gst-web/gst/get-token'
    headers = {
        'Content-Type': 'application/json'
    }

    # def test_get_token_sucess(self):
    #     body = {
    #         'clientId': 'cariad387a8124d87af4f4',
    #         'clientSecret': 'c931d180bdb3ab2f02a21498e39f2de'
    #     }
    #     r = requests.get(url=self.url, params=body, headers=self.headers)
    #
    #     print('测试获取token成功')
    #     print(r.content)
    #     print(r.text)
    #     print(r.status_code)
    #     assert r.status_code == 200
    #     assert "200" in r.text
    #     print('----------------')
    #     time.sleep(3)

    # # case2无请求头获取token成功
    # def test_get_token_headerless(self):
    #     body = {
    #         'clientId': 'cariad387a8124d87af4f4',
    #         'clientSecret': 'c931d180bdb3ab2f02a21498e39f2de3'
    #     }
    #     r = requests.get(url=self.url, params=body)
    #
    #     print('测试无请求头获取token成功')
    #     print(r.status_code)
    #     assert r.status_code == 200
    #     assert "200" in r.text
    #     print('----------------')
    #     time.sleep(3)
    #
    # # case3 clienId缺失
    # def test_get_token_clienId_less(self):
    #     body = {
    #         'clientSecret': 'c931d180bdb3ab2f02a21498e39f2de3'
    #     }
    #     r = requests.get(url=self.url, data=body, headers=self.headers)
    #     print('测试clienId缺失请求失败')
    #     print(r.status_code)
    #     assert r.status_code == 200
    #     assert "80001" in r.text
    #     print('----------------')
    #     time.sleep(3)
    #
    # # case4 clientSecret缺失
    # def test_get_token_clientSecret_less(self):
    #     body = {
    #         'clientId': 'cariad387a8124d87af4f4'
    #     }
    #     r = requests.get(url=self.url, data=body, headers=self.headers)
    #
    #     print('测试clientSecret缺失请求失败')
    #     #   print(r.content)
    #     print(r.status_code)
    #     assert r.status_code == 200
    #     #   assert "80002" in r.text
    #     print('----------------')
    #     time.sleep(3)
    #
    # time.sleep(5)
    #
    # # case5 clienId值为空
    # def test_get_token_clientId_nondata(self):
    #     body = {
    #         'clientId': '',
    #         'clientSecret': 'c931d180bdb3ab2f02a21498e39f2de3'
    #     }
    #     r = requests.get(url=self.url, data=body, headers=self.headers)
    #
    #     print('测试clienId值为空请求失败')
    #     print(r.content)
    #     print(r.status_code)
    #     assert r.status_code == 200
    #     assert "80001" in r.text
    #     print('----------------')
    #     time.sleep(3)
    #
    # time.sleep(5)
    #
    # # case6 clientSecret值为空
    # def test_get_token_clientSecret_nondata(self):
    #     body = {
    #         'clientId': 'cariad387a8124d87af4f4',
    #         'clientSecret': ''
    #     }
    #     r = requests.get(url=self.url, data=body, headers=self.headers)
    #
    #     print('clientSecret值为空请求失败')
    #     print(r.content)
    #     print(r.status_code)
    #     assert r.status_code == 200
    #     #   assert "80002" in r.text
    #     print('----------------')
    #     time.sleep(3)
    #
    # time.sleep(5)
    #
    # # case7 入参clienId值超长
    # def test_get_token_clienId_overlength(self):
    #     body = {
    #         'clientId': 'cariad387a8124d87af4f4123',
    #         'clientSecret': 'c931d180bdb3ab2f02a21498e39f2de3'
    #     }
    #     r = requests.get(url=self.url, data=body)
    #
    #     print('请求入参clienId值超长请求失败')
    #     print(r.content)
    #     print(r.status_code)
    #     assert r.status_code == 200
    #     #   assert "80003" in r.text
    #     print('----------------')
    #     time.sleep(3)
    #
    # time.sleep(5)
    #
    # # case8 入参clientSecret值超长
    # def test_get_token_clientSecret_overlength(self):
    #     body = {
    #         'clientId': 'cariad387a8124d87af4f4',
    #         'clientSecret': 'c931d180bdb3ab2f02a21498e39f2de3123'
    #     }
    #     r = requests.get(url=self.url, data=body)
    #     print('请求入参clientSecret值超长请求失败')
    #     print(r.content)
    #     print(r.status_code)
    #     assert r.status_code == 200
    #     #   assert "80005" in r.text
    #     print('----------------')
    #     time.sleep(3)
    #
    # time.sleep(5)
    #
    # # case9 入参clienId值超短
    # def test_get_token_clienId_short(self):
    #     body = {
    #         'clientId': 'cariad387a8124d87af4f',
    #         'clientSecret': 'c931d180bdb3ab2f02a21498e39f2de3'
    #     }
    #     r = requests.get(url=self.url, data=body, headers=self.headers)
    #     print('请求入参clienId值超短请求失败')
    #     print(r.content)
    #     print(r.status_code)
    #     assert r.status_code == 200
    #     #   assert "8003" in r.text
    #     print('----------------')
    #     time.sleep(3)
    #
    # time.sleep(5)

    # case10 入参clientSecret值超短
    def test_get_token_clientSecret_short(self):
        body = {
            'clientId': 'cariad387a8124d87af4f4',
            'clientSecret': 'c931d180bdb3ab2f02a21498e39f2de'
        }
        # r = requests.get(url=self.url, data=body)
        r = requests.get(url=self.url, params=body, headers=self.headers)

        print('测试请求入参clientSecret值超短请求失败')
        print(r.content)
        print(r.text, type(r.text))
        print(r.status_code)
        assert r.status_code == 200
        assert "80005" in r.text
        print('----------------')

    time.sleep(5)


if __name__ == '__main__':
    pytest.main(['-s', '-v'])
