##### 1.1 月度报告数据
    
##### 简要描述

- 根据参数条件，返回表aggr_dbr_monthly中，月度报告数据

##### 请求URL
- ` http://39.99.143.169:5000/dbr/aggr_dbr_monthly?month_id=2023-10&page=1&num=1000 `

##### 请求方式 
- GET 

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|month_id     |是  |string | 月份    |
|page     |是  |string | 页码    |
|num     |是  |string | 每页数量    |


##### 返回示例 

``` 
{
    "code": 200,
	"totalnum": 90000,
    "totalpage": 90
     "data": [
                {
                    "acc_activate_cnt": 152133,
                    "acceleration_cnt": 0,
                    "charging_cnt": 977,
                    "deceleration_cnt": 0,
                    "electrical_consumptions": 32706.959999999766,
                    "high_charging_cnt": 0,
                    "low_charging_cnt": 0,
                    "mileage": 953,
                    "month_date": "2023-10",
                    "month_id": "2023-10",
                    "sharp_turn_cnt": 976,
                    "userId": "393b4915-8a1a-43c9-a5e1-2710057fdf8b",
                    "vin": "b9487cfbc0c74499a970d5d08d2878c1"
                 },
                ...
            ],
     "msg": "Success"
 }
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|totalnum |int   |数据总数  |
|totalpage |int   |总页数  |
|acc_activate_cnt |int   |激活次数  |
|acceleration_cnt |int   |加速次数  |
|charging_cnt |int   |充电次数  |
|deceleration_cnt |int   |减速次数  |
|electrical_consumptions |float   |电能消耗  |
|high_charging_cnt |int   |高电量充电次数  |
|low_charging_cnt |int   |低电量充电次数  |
|mileage |int   |里程  |
|month_date |string   |月份日期  |
|month_id |string   |月份标识  |
|sharp_turn_cnt |int   |急转次数  |
|userId |string   |用户ID  |
|vin |string   |车辆识别号码（VIN码）  |





##### 1.2 日报数据接口

##### 简要描述

- 根据参数条件，返回表aggr_dbr__daily中，mileage大于200的数据。

##### 请求URL
- ` http://39.99.143.169:5000/dbr/aggr_dbr_daily?day_id=2023-10-16&page=1&num=1000 `

##### 请求方式 
- GET 

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|day_id     |是  |string | 日期    |
|page     |是  |string | 页码    |
|num     |是  |string | 每页数量    |


##### 返回示例 

``` 
{
 "code": 200,
 "totalnum": 90000,
 "totalpage": 90
 "data": [
            {
                "acc_activate_cnt": 0,
                "acceleration_cnt": 0,
                "charging_cnt": 0,
                "day_id": "2023-10-16",
                "deceleration_cnt": 0,
                "electrical_consumptions": 619.92,
                "high_charging_cnt": 0,
                "low_charging_cnt": 0,
                "mileage": 8484,
                "report_date": "2023-10-16",
                "sharp_turn_cnt": 0,
                "userId": "393b4915-8a1a-43c9-a5e1-2710057fdf8b",
                "vin": "b9487cfbc0c74499a970d5d08d2878c1"
             },
            ...
        ],
 "msg": "Success"
 }
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|totalnum |int   |数据总数  |
|totalpage |int   |总页数  |
|acc_activate_cnt |int   |激活次数  |
|acceleration_cnt |int   |加速次数  |
|charging_cnt |int   |充电次数  |
|day_id |string   |日期标识  |
|deceleration_cnt |int   |减速次数  |
|electrical_consumptions |float   |电能消耗  |
|high_charging_cnt |int   |高电量充电次数  |
|low_charging_cnt |int   |低电量充电次数  |
|mileage |int   |里程  |
|report_date |string   |报告日期  |
|sharp_turn_cnt |int   |急转次数  |
|userId |string   |用户ID  |
|vin |string   |车辆识别号码（VIN码）  |






##### 1.3 生成一条dbr mock数据
    
##### 简要描述

- 根据参数指标，生成一条dbr mock数据，发送到kafka。

##### 请求URL
- ` http://39.99.143.169:5000/dbr/send_dbr_m39.99.143.169ock_data?userId=393b4915-8a1a-43c9-a5e1-2710057fdf8b&vin=b9487cfbc0c74499a970d5d08d2878c1&messageId=acc_activate_cnt&day_id=2023-12-06`

##### 请求方式 
- GET 

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|userId |是  |string |用户id   |
|vin |是  |string |车辆vin    |
|messageId     |是  |string | 告警项标识    |
|day_id     |是  |string | 指定日期（默认日期为昨天）    |

##### 返回示例 

``` 
{
  "code": 200,
  "data": "acc_activate_cnt : message sent successfully",
  "msg": "Success"
}
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|code |int   |响应码  |
|data |string   |发送成功或者报错信息  |
|msg |string   |提示信息  |


##### 备注 
messageId 取值情况如下：
	# ACC启动次数
	"acc_activate_cnt",
	# 快充次数
	"charging_cnt",
	# 低充电次数
	"low_charging",
	# 高充电次数
	"high_charging",
	#里程
	"mileage"




##### 2.1 生成一条vhr的mock数据
    
##### 简要描述

- 根据参数指标，生成一条mock数据，发送到kafka。

##### 请求URL
- ` http://39.99.143.169:5000/vhr/produce_one_mock_data?userId=393b4915-8a1a-43c9-a5e1-2710057fdf8b&vin=b9487cfbc0c74499a970d5d08d2878c1&messageId=battery_temp&flag=0`

##### 请求方式 
- GET 

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|userId |是  |string |用户id   |
|vin |是  |string |车辆vin    |
|messageId     |是  |string | 告警项标识    |
|flag     |否  |string | flag=1置为异常，flag=0置为正常(不传，默认flag=1)    |


##### 返回示例 

``` 
{
  "code": 200,
  "data": "BMS_Fehler_Notabschaltung_Crash_XIX_BMS_20_XIX_E3V_EVCANFD : message sent successfully",
  "msg": "Success"
}
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|code |int   |响应码  |
|data |string   |发送成功或者报错信息  |
|msg |string   |提示信息  |


##### 备注 
messageId 取值情况如下：
    # 电池温度
    "battery_temp",
    # 绝缘电阻
    "insulation_resist",
    # 电池碰撞/进水检测
    "battery_collision_waterDetect",
    # 电池管理
    "battery_management",
    # 充放电电压
    "charging_discharging_voltage",
    # 自动除雾
    "automatic_defog",
    "b_call",
    "e_call",
    # "i_call": ["iCall_active_XIX_TM_01_XIX_E3V_K2CANFD"],  # 暂时不用
    # 盲区检测
    "blind_spot_detect",
    # 制动盘
    "brake_disc",
    # 雨刮水
    "wiper_water",
    # 冷却液
    "coolant",







##### 2.2 返回车辆最新警告信息
    
##### 简要描述

- 根据vin， 返回车辆最新警告信息。

##### 请求URL
- ` http://39.107.107.149:5000/vhr/vdaa_gdc?vin=b9487cfbc0c74499a970d5d08d2878c1 `

##### 请求方式 
- GET 

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|userId |是  |string |用户id   |
|vin |是  |string |车辆vin    |


##### 返回示例 

``` 
{
  "code": 200,
  "data": {
    "warningLights": [
      {
        "iconColor": "Yellow",
        "messageId": "battery_collision_waterDetect",
        "timeOfOccurrence": "2023-10-27 01:59:59",
        "warningLightTextCn": "故障：电池碰撞/进水检测",
        "warningLightTextEn": "Error: Please check battery collision or waterDetect!"
      },
      {
        "iconColor":  "",
        "messageId": "battery_temp",
        "timeOfOccurrence": "2023-10-27 01:59:59",
        "warningLightTextCn": "",
        "warningLightTextEn": ""
      },
      {
        "iconColor":  "",
        "messageId": "insulation_resist",
        "timeOfOccurrence": "2023-10-27 01:59:59",
        "warningLightTextCn": "",
        "warningLightTextEn": ""
      },
      ...
    ]
  },
  "msg": "Success"
}
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|code |int   |响应码  |
|data |dict   |响应数据  |
|warningLights |list   |警告信息列表  |
|iconColor |string   |告警颜色(没有异常则为空)  |
|messageId |string   |告警项标识  |
|timeOfOccurrence |datetime   |发生时间  |
|warningLightTextCn |string   |告警中文信息(没有异常则为空)   |
|warningLightTextEn |string   |告警英文信息(没有异常则为空)   |
|msg |string   |提示信息  |


##### 备注1：
``` 
# 1.告警项中/英文信息说明
{
    "battery_temp": {
                      "warningLightTextCn": "故障：电池温度",
                      "warningLightTextEn": "Error: Please check battery temperature!",
                  },
    "insulation_resist": {
                      "warningLightTextCn": "故障：绝缘电阻",
                      "warningLightTextEn": "Error: Please check insulation resist!",
                  },
    "battery_collision_waterDetect": {
                      "warningLightTextCn": "故障：电池碰撞/进水检测",
                      "warningLightTextEn": "Error: Please check battery collision or waterDetect!",
                  },
    "battery_management": {
                      "warningLightTextCn": "故障：电池管理",
                      "warningLightTextEn": "Error: Please check battery management!",
                  },
    "charging_discharging_voltage": {
                      "warningLightTextCn": "故障：充放电电压",
                      "warningLightTextEn": "Error: Please check charing and discharging voltage!",
                  },
    "automatic_defog": {
                      "warningLightTextCn": "故障：自动除雾",
                      "warningLightTextEn": "Error: Please check automatic defog!",
                  },
    "b_call": {
                      "warningLightTextCn": "故障：Bcall",  # 紧急呼叫
                      "warningLightTextEn": "Error: Please check Bcall!",
                  },
	"i_call": {
                      "warningLightTextCn": "故障：Icall",  # 紧急呼叫
                      "warningLightTextEn": "Error: Please check Icall!",
                  },
    "e_call": {
                    "warningLightTextCn": "故障：Ecall",  # 紧急呼叫
                    "warningLightTextEn": "Error: Please check Ecall!",
                },
    "blind_spot_detect": {
                    "warningLightTextCn": "故障：盲区检测",
                    "warningLightTextEn": "Error: Please check blind spot detect!",
                },
    "brake_disc": {
                    "warningLightTextCn": "故障：制动盘",
                    "warningLightTextEn": "Error: Please check brake disc!",
                },
    "wiper_water": {
                    "warningLightTextCn": "故障：雨刮水",
                    "warningLightTextEn": "Error: Please check wiper water!",
                },
    "coolant": {
                    "warningLightTextCn": "故障：冷却液",
                    "warningLightTextEn": "Error: Please check coolant!",
                },
}

# 2.响应码说明
{
'code':1001,  # 数据库无数据；
'code':1002,  # 查询异常无数据(无响应)；
'code':200,  # 有数据
}
```












