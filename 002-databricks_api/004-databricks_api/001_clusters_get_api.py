"""
curl --request GET "https://${DATABRICKS_HOST}/api/2.0/clusters/get" \
     --header "Authorization: Bearer ${DATABRICKS_TOKEN}" \
     --data '{ "cluster_id": "1234-567890-a12bcde3" }'
"""
import requests

DATABRICKS_HOST = "https://adb-3637957763693437.17.azuredatabricks.net"
DATABRICKS_TOKEN = "dapidea5ec1a19c80899b0b7872d61da5c60-2"
CLUSTER_ID = "1016-093945-mu381tjr"

headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}"
}
url = f"{DATABRICKS_HOST}/api/2.0/clusters/get"

response = requests.get(
                        url,
                        headers=headers,
                        params={
                                "cluster_id": CLUSTER_ID
                                }
                        )

print(response.status_code)
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Failed to fetch cluster information")
