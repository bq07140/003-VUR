from databricks import sql
import json

connection = sql.connect(
    server_hostname="adb-2515004071041721.1.databricks.azure.cn",
    http_path="/sql/1.0/warehouses/07194f39c23cde02",
    access_token="dapideac683303ce305bcf4971b955c39bbf")

cursor = connection.cursor()

cursor.execute("SELECT value FROM cx5_original_data WHERE value LIKE '%LWI_Lenkradw_Geschw%';")

ret = cursor.fetchall()
ret = [line.asDict() for line in ret]

print(len(ret))
for line in ret:
    dic = json.loads(line['value'])
    name = dic['payload']['name']
    pay_value = dic['payload']['value']
    print(name, pay_value)

cursor.close()
connection.close()








