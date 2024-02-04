from databricks import sql
import logging

logging.getLogger("twg_databricks.sql").setLevel(logging.DEBUG)
logging.basicConfig(filename="results.log",
                    level=logging.DEBUG)

connection = sql.connect(
                            server_hostname="adb-2515004071041721.1.databricks.azure.cn",
                            http_path="/sql/1.0/warehouses/07194f39c23cde02",
                            access_token="dapi9aefab090c8d18b7619235656a43b0ef")

cursor = connection.cursor()
cursor.execute("SELECT * from range(10)")
result = cursor.fetchall()

for row in result:
    logging.debug(row)

cursor.close()
connection.close()

