import pandas as pd
import json
from datetime import datetime

# 设置显示所有列的选项
pd.set_option('display.max_columns', None)

# 指定 CSV 文件路径
# csv_file_path = "export.csv"
csv_file_path = "export (7).csv"

# 指定保存的 CSV 文件路径
# 获取当前时间戳
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

output_excel_file = f"./processed_data_{timestamp}.xlsx"
# print(output_excel_file)

# 使用 pandas 读取 CSV 文件
df = pd.read_csv(csv_file_path, header=0)
print(df.columns)

# # 对 'name' 和 'value' 列进行联合去重
df = df.drop_duplicates(subset=['name', 'value'])
# df = df.drop_duplicates(subset=['name'])
# 对 'name' 字段进行排序
# df = df.sort_values(by='name')
df = df.sort_values(by='timestamp_to_datetime')
# df = df.sort_values(by='inserttime')


# 打印结果
# print(df)

# 保存处理后的数据框为 Excel 文件
df.to_excel(output_excel_file, index=False)



