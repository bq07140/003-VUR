"""
    插入少量数据（数千行）
    对于大量数据，应先将数据上传到云存储，然后执行COPY INTO命令。
"""
from databricks import sql
import pandas as pd
import json
from datetime import datetime
import pytz

# 设置显示所有列的选项
pd.set_option('display.max_columns', None)

# 指定 CSV 文件路径
csv_file_path = "./export.csv"

# 使用 pandas 读取 CSV 文件
df = pd.read_csv(csv_file_path, header=None)
# print(df)


# 定义函数来提取字段
def extract_fields(row):
    # print(row)
    try:
        data = json.loads(row)
        return {
            "userId": data["userId"],
            "vehicleId": data["vehicleId"],

            "schemaId": data["schemaId"],
            "userMessageId": data["userMessageId"],
            "useCaseIds": json.dumps(data["useCaseIds"]),

            "name": data["payload"]["name"],
            "value": data["payload"]["value"],
            "timestamp": data["payload"]["timestamp"],

            "containerMsgId": data["payload"]["containerMsgId"],
            "orderId": data["payload"]["orderId"],
            "containerId": data["payload"]["containerId"],
            "containerMsgCount": data["payload"]["containerMsgCount"],
        }
    except Exception as e:
        print(f"Error extracting fields: {e}")
        return None


# 应用函数并创建新列
df["extracted_fields"] = df[0].apply(extract_fields)
# 将提取的字段展开为独立的列
df = pd.concat([df, df["extracted_fields"].apply(pd.Series)], axis=1)

# 删除原始列和中间列
df = df.drop([0, "extracted_fields"], axis=1)

# 新增 inserttime 字段，类型为当前北京时间字符串
beijing_time = datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")
df["inserttime"] = beijing_time

# 新增 timestamp_to_datetime 字段，根据 timestamp 字段的时间戳转化为北京时间字符串类型
df["timestamp_to_datetime"] = pd.to_datetime(df["timestamp"], unit='ms', origin='unix')
df["timestamp_to_datetime"] = df["timestamp_to_datetime"].dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai').dt.strftime("%Y-%m-%d %H:%M:%S")

# 新增 date_id 字段，为日期类型，取当天的北京日期
beijing_date = datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d")
df["date_id"] = beijing_date

# output_csv_path = "./cx5_ods_gdc_daily905.csv"
# df.to_csv(output_csv_path, index=False)

# print(df)

conn = sql.connect(
    server_hostname="adb-2515004071041721.1.databricks.azure.cn",
    http_path="/sql/1.0/warehouses/07194f39c23cde02",
    access_token="dapi27116197bf3636c59422a74de3e768ab")

cursor = conn.cursor()

for userId, vehicleId, schemaId, userMessageId, useCaseIds, name, value, timestamp, containerMsgId, orderId, containerId, containerMsgCount, inserttime, timestamp_to_datetime, date_id in df.itertuples(
        index=False):
    # 将 useCaseIds 字段值放入单引号中，确保 SQL 中的字符串格式正确
    values = f"('{userId}', '{vehicleId}', '{schemaId}', '{userMessageId}', '{useCaseIds}', '{name}', '{value}', " \
             f"{timestamp}, '{containerMsgId}', '{orderId}', '{containerId}', {containerMsgCount}, " \
             f"'{inserttime}', '{timestamp_to_datetime}', '{date_id}')"

    sql = """
            INSERT INTO `hive_metastore`.`default`.`cx5_ods_gdc_daily905`
            (userId, vehicleId, schemaId, userMessageId, useCaseIds, name, value, timestamp, containerMsgId, orderId,
            containerId, containerMsgCount, inserttime, timestamp_to_datetime, date_id)
            VALUES {0}
        """.format(values)

    print(sql)

    cursor.execute(sql)


# 关闭游标和数据库连接
cursor.close()
conn.close()
