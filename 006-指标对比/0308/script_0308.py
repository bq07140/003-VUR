import pandas as pd

# 读取CSV文件
df = pd.read_csv('./export (5).csv')

# 按name字段进行分组
grouped_df = df.groupby('name')

ret_data = {}


# 定义自定义函数来处理每个组的数据
def process_group(group):
    # BMS_Ladezustand    BMS_Nutzbare_EntladeEnergie   BMS_Verbrauch  BV1_FS_0_Haltelinie_Gierwinkel
    # print('---------111111111111111')
    data_li = []
    value_li = []
    name = group.name

    if name in ['BMS_Ladezustand', 'BMS_Nutzbare_EntladeEnergie', 'BMS_Verbrauch', 'Speed displayed']:

        for index, row in group.iterrows():
            value = float(row['value'])
            value_li.append(value)
        data_li.append(min(value_li))
        data_li.append(max(value_li))

        # 转为整形
        if name in ['BMS_Nutzbare_EntladeEnergie', 'Speed displayed']:
            data_li = [int(i) for i in data_li]

    elif name == 'BV1_FS_0_Haltelinie_Gierwinkel':
        for index, row in group.iterrows():
            try:
                value = float(row['value'])
                value_li.append(value)
            except Exception as e:
                data_li.append(row['value'])

        data_li.append(min(value_li))
        data_li.append(max(value_li))
    else:
        for index, row in group.iterrows():
            value = row['value']
            data_li.append(value)

    ret_data[name] = data_li


# 遍历每个分组中的每一行数据
grouped_df.apply(process_group)
print(ret_data)


