from databricks import sql
import json
import pandas as pd

# connection = sql.connect(
#     server_hostname="adb-2515004071041721.1.databricks.azure.cn",
#     http_path="/sql/1.0/warehouses/07194f39c23cde02",
#     access_token="dapideac683303ce305bcf4971b955c39bbf")

# cursor = connection.cursor()


connection = sql.connect(
    server_hostname="adb-4179350563878772.0.databricks.azure.cn",
    http_path="/sql/1.0/warehouses/7f680d3f5fdd0653",
    access_token="dapi3dc9c4a7c889fa66c637fa385415147a")

cursor = connection.cursor()



# cursor.execute("""
#                 SELECT
#     t1.name,
#     t1.count_name,
#     t2.time01,
#     t2.time02
# FROM
#     (SELECT
#         NAME,
#         COUNT(*) AS count_name
#     FROM
#         cx5_ods_gdc_daily
#     WHERE
#         timestamp_to_datetime BETWEEN '2024-04-16 10:15:00' AND '2024-04-16 11:35:00'
#             AND vin = 'LAVB7ZER2P1200019'
#             AND name IN ('BMS_Fehler_Notabschaltung_Crash' , 'BMS_RtmWarnTZelleDiff' , 'BMS_RtmWarnTZelleMax' , 'BMS_RtmWarnTZelleMin' , 'BMS_IsoFehler' , 'BMS_RtmWarnZelleZustand' , 'BMS_RtmWarnUPackMax' , 'BMS_RtmWarnUPackMin' , 'BMS_RtmWarnUZelleMax' , 'BMS_RtmWarnUZelleMin' , 'FSH_Status' , 'bCall_active' , 'iCall_active' , 'AB_Anforderung_eCall' , 'ACC_Blindheit_erkannt' , 'BCM_Bremsbelag_Sensor_CND' , 'BCM_Bremsbelag_Sensor_Rdw' , 'BCM_Bremsbelag_Sensor' , 'BCM_Bremsbelag_Sensor_NAR' , 'BCM_Waschwasser_Sensor' , 'BCM_Kuehlmittel_Sensor')
#     GROUP BY `name`) AS t1
#         JOIN
#     (SELECT
#         name,
#             ROUND(AVG(a.time01)) AS time01,
#             ROUND(AVG(a.time02)) AS time02
#     FROM
#         (SELECT
#         *,
#             TIMESTAMPDIFF(SECOND, timestamp_to_datetime, ingest_timestamp_to_datetime) time01,
#             TIMESTAMPDIFF(SECOND, timestamp_to_datetime, inserttime) time02
#     FROM
#         cx5_ods_gdc_daily
#     WHERE
#         timestamp_to_datetime BETWEEN '2024-04-16 10:15:00' AND '2024-04-16 11:35:00'
#             AND vin = 'LAVB7ZER2P1200019'
#             AND name IN ('BMS_Fehler_Notabschaltung_Crash' , 'BMS_RtmWarnTZelleDiff' , 'BMS_RtmWarnTZelleMax' , 'BMS_RtmWarnTZelleMin' , 'BMS_IsoFehler' , 'BMS_RtmWarnZelleZustand' , 'BMS_RtmWarnUPackMax' , 'BMS_RtmWarnUPackMin' , 'BMS_RtmWarnUZelleMax' , 'BMS_RtmWarnUZelleMin' , 'FSH_Status' , 'bCall_active' , 'iCall_active' , 'AB_Anforderung_eCall' , 'ACC_Blindheit_erkannt' , 'BCM_Bremsbelag_Sensor_CND' , 'BCM_Bremsbelag_Sensor_Rdw' , 'BCM_Bremsbelag_Sensor' , 'BCM_Bremsbelag_Sensor_NAR' , 'BCM_Waschwasser_Sensor' , 'BCM_Kuehlmittel_Sensor')) AS a
#     GROUP BY `name`) AS t2 ON t1.name = t2.name
#     ORDER BY t1.name;
#             """)

# cursor.execute("""
#                 select vin,name,value,unit,timestamp_to_datetime,ingest_timestamp_to_datetime,inserttime, raw_data
#                 from cx5_ods_gdc_daily
#                 where
#                 value='Fehler'
#                 and timestamp_to_datetime >= '2024-04-16 00:00:00'
#                 AND timestamp_to_datetime <= '2024-04-16 23:59:59'
#                 limit  100;
#             """)

# cursor.execute("""
#             select vin,name,value,unit,timestamp_to_datetime,ingest_timestamp_to_datetime,inserttime
#             from ods_gdc_daily
#             where date_id='2024-05-11'
#             order by timestamp_to_datetime desc;
#         """)

# LAVB8ZER6P1200117、LAVB8ZER1P1200090、LAVB7ZER3P1200028
cursor.execute("""
                    SELECT NAME, *
                    FROM
                        ods_gdc_daily
                    WHERE
                        date_id='2024-05-16'
                        AND vin IN ('LAVB8ZER6P1200117', 'LAVB8ZER1P1200090', 'LAVB7ZER3P1200028')
                        AND NAME IN (
                            'AB_Anforderung_eCall',
                            'ACC_Blindheit_erkannt',
                            'ACC_Status_ACC',
                            'BCM_Bremsbelag_Sensor',
                            'BCM_Bremsbelag_Sensor_CND',
                            'BCM_Bremsbelag_Sensor_NAR',
                            'BCM_Bremsbelag_Sensor_Rdw',
                            'BCM_Kuehlmittel_Sensor',
                            'BCM_Waschwasser_Sensor',
                            'BMS_Fehler_Notabschaltung_Crash',
                            'BMS_IsoFehler',
                            'BMS_RtmWarnTZelleDiff',
                            'BMS_RtmWarnTZelleMax',
                            'BMS_RtmWarnTZelleMin',
                            'BMS_RtmWarnUPackMax',
                            'BMS_RtmWarnUPackMin',
                            'BMS_RtmWarnUZelleMax',
                            'BMS_RtmWarnUZelleMin',
                            'BMS_RtmWarnZelleZustand',
                            'FSH_Status',
                            'bCall_active',
                            'ESP_Laengsbeschl',
                            'ESP_Querbeschleunigung',
                            'TA_ACC_Sollstatus',
                            'KBI_Kilometerstand',
                            'BMS_Verbrauch',
                            'BMS_Nutzbare_EntladeEnergie',
                            'BMS_UBE',
                            'EM1_Verbrauch',
                            'EM2_Verbrauch',
                            'MO_Verbrauch_EM_Ges',
                            'BMS_Ladezustand',
                            'BMS_Spannung',
                            'BMS_Strom',
                            'BMS_Ladevorgang_aktiv',
                            'clamp 15 status',
                            'ESP_v_Signal',
                            'RDR1_Blindheit_erkannt'
                        )
        """)


ret = cursor.fetchall()
# 转换为Pandas DataFrame
df = pd.DataFrame(ret, columns=[col[0] for col in cursor.description])

# 保存到Excel表格
df.to_excel('0516-data.xlsx', index=False)

# ret = [line.asDict() for line in ret]

# print(len(ret))
# for line in ret:
#     print(line)
#     dic = json.loads(line['value'])
#     name = dic['payload']['name']
#     pay_value = dic['payload']['value']
#     print(name, pay_value)

cursor.close()
connection.close()
