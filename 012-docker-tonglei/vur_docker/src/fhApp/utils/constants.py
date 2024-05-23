# -*- coding: utf-8 -*-
# 常量模块


# VHR--告警配置信息
MESSAGEID_LI = {
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


# messageId --- 指标名称的映射
MESSAGEID_TO_NAME = {
    # 1. =============VHR指标
    # 电池温度
    "battery_temp": ["BMS_RtmWarnTZelleDiff_XIX_BMS_28_XIX_E3V_EVCANFD",
                     "BMS_RtmWarnTZelleMax_XIX_BMS_28_XIX_E3V_EVCANFD",
                     "BMS_RtmWarnTZelleMin_XIX_BMS_28_XIX_E3V_EVCANFD"],
    # 绝缘电阻
    "insulation_resist": ["BMS_IsoFehler_XIX_BMS_11_XIX_E3V_ACANFD"],
    # 电池碰撞/进水检测
    "battery_collision_waterDetect": ["BMS_Fehler_Notabschaltung_Crash_XIX_BMS_20_XIX_E3V_EVCANFD"],
    # 电池管理
    "battery_management": ["BMS_RtmWarnZelleZustand_XIX_BMS_28_XIX_E3V_EVCANFD"],
    # 充放电电压
    "charging_discharging_voltage": ["BMS_RtmWarnUPackMax_XIX_BMS_28_XIX_E3V_EVCANFD",
                                     "BMS_RtmWarnUPackMin_XIX_BMS_28_XIX_E3V_EVCANFD",
                                     "BMS_RtmWarnUZelleMax_XIX_BMS_28_XIX_E3V_EVCANFD",
                                     "BMS_RtmWarnUZelleMin_XIX_BMS_28_XIX_E3V_EVCANFD"],
    # 自动除雾
    "automatic_defog": ["FSH_Status_XIX_Klima_16_XIX_E3V_EVCANFD"],
    "b_call": ["bCall_active_XIX_TM_01_XIX_E3V_FASCANFD1"],
    "e_call": ["EA_eCall_Anf_XIX_EA_04_XIX_HCP4_CANFD03"],
    # "i_call": ["iCall_active_XIX_TM_01_XIX_E3V_K2CANFD"],  # 暂时不用
    # 盲区检测
    "blind_spot_detect": ["ACC_Blindheit_erkannt_XIX_ACC_18_XIX_E3V_ACANFD"],
    # 制动盘
    "brake_disc": ["BCM_Bremsbelag_Sensor_CND_XIX_SAM_01_XIX_E3V_KCAN",
                   "BCM_Bremsbelag_Sensor_Rdw_XIX_SAM_01_XIX_E3V_KCAN",
                   "BCM_Bremsbelag_Sensor_XIX_BCM_01_XIX_E3V_KCAN",
                   "BCM_Bremsbelag_Sensor_NAR_XIX_SAM_01_XIX_E3V_KCAN"],
    # 雨刮水
    "wiper_water": ["Wischer_vorne_defekt_XIX_Wischer_01_XIX_E3V_KCAN"],
    # 冷却液
    "coolant": ["BCM_Kuehlmittel_Sensor_XIX_BCM_01_XIX_E3V_KCAN",
                "BCM_Kuehlmittel_Sensor_02_XIX_BCM_01_XIX_E3V_KCAN"],

}