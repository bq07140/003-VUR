from databricks import sql

with sql.connect(
        server_hostname="adb-2515004071041721.1.databricks.azure.cn",
        http_path="/sql/1.0/warehouses/07194f39c23cde02",
        access_token="dapi9aefab090c8d18b7619235656a43b0ef") as connection:

    with connection.cursor() as cursor:
        cursor.columns(schema_name="default", table_name="squares")
        print(cursor.fetchall())



