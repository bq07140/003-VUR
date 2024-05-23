from databricks import sql
import json
import pandas as pd

connection = sql.connect(
    server_hostname="adb-2515004071041721.1.databricks.azure.cn",
    http_path="/sql/1.0/warehouses/07194f39c23cde02",
    access_token="dapideac683303ce305bcf4971b955c39bbf")

cursor = connection.cursor()

sql = """
        select vin,name,value,timestamp_to_datetime from cx5_ods_gdc_daily905_vin  
        where date_id='2024-03-21' order by timestamp_to_datetime desc;
        """
cursor.execute(sql)

ret = cursor.fetchall()
# 转换为Pandas DataFrame
df = pd.DataFrame(ret, columns=[col[0] for col in cursor.description])

# 保存到Excel表格
df.to_excel('0321-data.xlsx', index=False)

# ret = [line.asDict() for line in ret]

# print(len(ret))
# for line in ret:
#     print(line)
#     dic = json.loads(line['value'])
#     name = dic['payload']['name']
#     pay_value = dic['payload']['value']
#     print(name, pay_value)

cursor.close()
connection.close()








