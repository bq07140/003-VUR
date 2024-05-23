import mysql.connector

cnx = mysql.connector.connect(
            user="tanwg",
            password="pass@1234",
            host="vur-python_demo-mysql.mysql.database.chinacloudapi.cn",
            port=3306,
            database="vur_db",
            # ssl_ca="{ca-cert filename}",
            # ssl_disabled=False
        )

# 使用连接创建游标对象
cursor = cnx.cursor()

# 执行查询
cursor.execute("SHOW TABLES")  # sql语句

# 获取查询结果
tables = cursor.fetchall()

# 打印所有表名
for table in tables:
    print(table[0])

# 关闭游标和连接
cursor.close()
cnx.close()













