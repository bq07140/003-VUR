import requests

url_token = "https://login.partner.microsoftonline.cn/a12a82ff-eb68-4d6d-b3c7-c4fb2d2220e5/oauth2/v2.0/token"
payload = {
    'client_id': '17362fa4-6e13-41b2-866d-f27553296e4e',
    'client_secret': 'C9bUCN6~9jFl0kNyDnCt_Th4p_zv01cY.5',
    'scope': 'api://china-apr-vwacv-a72-apim-backend-sp/.default',
    'grant_type': 'client_credentials'
}
response = requests.post(url_token, data=payload)
access_token = response.json()["access_token"]
print("Access Token:", access_token)


# url_vin = "https://apr-vwacv-a72-apim.vwcloud.cn/vehicles/api/registration/vehicle/39ec0be958624d86ade8f50e16064ff5/uuid?api-version=2020-07-01"
url_vin = "https://apr-vwacv-a72-apim.vwcloud.cn/vehicles/api/registration/vehicle/46e7e2f9ef3845628ea2bb8738fb6f51/uuid?api-version=2020-07-01"
headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Authorization': 'bearer ' + access_token
}
response = requests.get(url_vin, headers=headers)
print(response.text)
print(type(response.text))

if response.text:
    data = response.json()
    print("API Response:", data)





