import pandas as pd
import json

# 设置显示所有列的选项
pd.set_option('display.max_columns', None)

# 指定 CSV 文件路径
csv_file_path = "export_001.csv"
# 指定保存的 CSV 文件路径
output_excel_file = "./processed_data.xlsx"

# 使用 pandas 读取 CSV 文件
df = pd.read_csv(csv_file_path, header=None)
# print(df)


# 定义函数来提取字段
def extract_fields(row):
    try:
        data = json.loads(row)
        return {
            "userId": data["userId"],
            "vehicleId": data["vehicleId"],
            "name": data["payload"]["name"],
            "value": data["payload"]["value"],
            "timestamp": data["payload"]["timestamp"]
        }
    except Exception as e:
        print(f"Error extracting fields: {e}")
        return None


# 应用函数并创建新列
df["extracted_fields"] = df[0].apply(extract_fields)
# 将提取的字段展开为独立的列
df = pd.concat([df, df["extracted_fields"].apply(pd.Series)], axis=1)

# 删除原始列和中间列
# df = df.drop([0, "extracted_fields", "timestamp"], axis=1)
df = df.drop([0, "extracted_fields"], axis=1)
print(df)

















# # # 对 'name' 和 'value' 列进行联合去重
# # df_unique_names_values = df.drop_duplicates(subset=['name', 'value'])
# #
# # # 对 'name' 字段进行排序
# # df_sorted = df_unique_names_values.sort_values(by='name')
#
#
# # # 打印结果
# # print(df_sorted)
# #
# # # 保存处理后的数据框为 Excel 文件
# # df_sorted.to_excel(output_excel_file, index=False)
#
#
