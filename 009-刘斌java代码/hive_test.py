from databricks import sql
import os

connection = sql.connect(
    server_hostname="adb-4179350563878772.0.databricks.azure.cn",
    http_path="/sql/1.0/warehouses/7f680d3f5fdd0653",
    access_token="dapie354cc12765aae3ed91dfc98d63dcdcb")

cursor = connection.cursor()

cursor.execute("SELECT * from cx5_chr_data")
print(cursor.fetchall())

cursor.close()
connection.close()
