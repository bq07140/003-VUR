import pandas as pd
import json

# 设置显示所有列的选项
pd.set_option('display.max_columns', None)

# 指定 CSV 文件路径
csv_file_path = "export.csv"
# 指定保存的 CSV 文件路径
output_excel_file = "./processed_data02.xlsx"

# 使用 pandas 读取 CSV 文件
df = pd.read_csv(csv_file_path, header=0)
print(df.columns)

# 对 'name' 和 'value' 列进行联合去重
df = df.drop_duplicates(subset=['name', 'value'])
# 对 'name' 字段进行排序
df = df.sort_values(by='name')


# 打印结果
# print(df)

# 保存处理后的数据框为 Excel 文件
df.to_excel(output_excel_file, index=False)



