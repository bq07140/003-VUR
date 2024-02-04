from datetime import datetime
# timestamp = 1704254271
# timestamp = 1704254277
# timestamp = 1704273913
timestamp = 1704273936


# # # 将毫秒转换为秒
# timestamp = 1703494137040
# # # timestamp = 1702272208012
# timestamp = timestamp / 1000

dt_object = datetime.fromtimestamp(timestamp)

print(dt_object)






