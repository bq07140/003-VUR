"""
    插入少量数据（数千行）
    对于大量数据，应先将数据上传到云存储，然后执行COPY INTO命令。
"""
from databricks import sql

with sql.connect(
        server_hostname="adb-2515004071041721.1.databricks.azure.cn",
        http_path="/sql/1.0/warehouses/07194f39c23cde02",
        access_token="dapi9aefab090c8d18b7619235656a43b0ef") as connection:

    with connection.cursor() as cursor:

        cursor.execute("CREATE TABLE IF NOT EXISTS squares (x int, x_squared int)")

        squares = [(i, i * i) for i in range(100)]
        values = ",".join([f"({x}, {y})" for (x, y) in squares])

        cursor.execute(f"INSERT INTO squares VALUES {values}")

        cursor.execute("SELECT * FROM squares LIMIT 10")

        result = cursor.fetchall()
        for row in result:
            print(row)
