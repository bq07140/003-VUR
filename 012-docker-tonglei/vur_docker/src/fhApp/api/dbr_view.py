# -*- coding: utf-8 -*-
# import logging
from flask import request, jsonify
from . import api
from fhApp.utils.dbr_worker_fun import QueryDatabricks, DbrDataGenerator
from datetime import datetime, timedelta


# http://127.0.0.1:5000/dbr/aggr_dbr_monthly?month_id=2024-02&page=1&num=100
@api.route('dbr/aggr_dbr_monthly')
def aggr_dbr_monthly():
    month_id = request.args.get('month_id')
    page = request.args.get('page', '1')  # 默认第1页
    num = request.args.get('num', '10000')  # 默认1万条

    response = {
        'code': 200,
        'msg': 'Success',
        'data': []
    }

    if all([month_id, page, num]):
        try:
            databricks = QueryDatabricks()
            ret, totalnum, totalpage = databricks.aggr_dbr_monthly(month_id, int(page), int(num))
            response['data'] = ret
            response['totalnum'] = totalnum
            response['totalpage'] = totalpage
            databricks.close_db()  # 关闭连接
        except Exception as e:
            # logging.error(str(e))
            print(e)
            response['code'] = 500
            response['msg'] = str(e)

    else:
        msg = 'Bad Request: Missing required parameters'
        response['code'] = 400
        response['msg'] = msg
        print(msg)
        # logging.error(msg)

    return jsonify(response)


# http://127.0.0.1:5000/dbr/aggr_dbr_daily?day_id=2024-03-18&page=1&num=100
@api.route('dbr/aggr_dbr_daily')
def aggr_dbr_daily():
    day_id = request.args.get('day_id')
    page = request.args.get('page', '1')  # 默认第1页
    num = request.args.get('num', '10000')  # 默认1万条

    response = {
        'code': 200,
        'msg': 'Success',
        'data': []
    }

    if all([day_id, page, num]):

        try:
            databricks = QueryDatabricks()
            ret, totalnum, totalpage = databricks.aggr_dbr_daily(day_id, int(page), int(num))
            response['data'] = ret
            response['totalnum'] = totalnum
            response['totalpage'] = totalpage
            databricks.close_db()  # 关闭连接
        except Exception as e:
            # logging.error(str(e))
            print(e)
            response['code'] = 500
            response['msg'] = str(e)

    else:
        msg = 'Bad Request: Missing required parameters'
        response['code'] = 400
        response['msg'] = msg
        # logging.error(msg)
        print(msg)

    return jsonify(response)


# http://127.0.0.1:8000/dbr/send_dbr_mock_data?userId=393b4915-8a1a-43c9-a5e1-2710057fdf8b&vin=b9487cfbc0c74499a970d5d08d2878c1&messageId=acc_activate_cnt&day_id=2023-12-06
# http://127.0.0.1:8000/dbr/send_dbr_mock_data?userId=393b4915-8a1a-43c9-a5e1-2710057fdf8b&vin=b9487cfbc0c74499a970d5d08d2878c1&messageId=charging_cnt&day_id=2023-12-06
# http://127.0.0.1:8000/dbr/send_dbr_mock_data?userId=393b4915-8a1a-43c9-a5e1-2710057fdf8b&vin=b9487cfbc0c74499a970d5d08d2878c1&messageId=low_charging&day_id=2023-12-06
# http://127.0.0.1:8000/dbr/send_dbr_mock_data?userId=393b4915-8a1a-43c9-a5e1-2710057fdf8b&vin=b9487cfbc0c74499a970d5d08d2878c1&messageId=high_charging&day_id=2023-12-06
# http://127.0.0.1:8000/dbr/send_dbr_mock_data?userId=393b4915-8a1a-43c9-a5e1-2710057fdf8b&vin=b9487cfbc0c74499a970d5d08d2878c1&messageId=mileage&day_id=2023-12-06
@api.route('dbr/send_dbr_mock_data')
def send_dbr_mock_data():

    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    userId = request.args.get('userId')
    vin = request.args.get('vin')
    messageId = request.args.get('messageId')
    day_id = request.args.get('day_id', yesterday)

    response = {
        'code': 200,
        'msg': 'Success',
        'data': ""
    }

    if all([userId, vin, messageId, day_id]):

        try:
            # 给kafka发送一条数据
            data_generator = DbrDataGenerator()
            timestamp = int(data_generator.get_timestamp(day_id))

            try:
                data_li = []
                # 1. ACC启动次数
                if messageId == "acc_activate_cnt":
                    name = "ACC_Anfahren_XIX_ACC_18_XIX_E3V_FASCANFD1"
                    data_li = data_generator.dbr_general_send_fun(userId, vin, name, timestamp)

                # 2. 快充次数
                elif messageId == "charging_cnt":
                    name = "BMS_DC_Ladeprofil_Wechsel_XIX_BMS_26_XIX_E3V_EVCANFD"
                    data_li = data_generator.dbr_general_send_fun(userId, vin, name, timestamp)

                # 3. 低电量充电次数   low_charging  current_charge
                elif messageId == "low_charging":
                    name = "BMS_IstModus_XIX_BMS_20_XIX_E3V_EVCANFD"
                    data_li = data_generator.low_charging(userId, vin, name, timestamp)

                # 4. 高电量充电次数   high_charging  current_charge
                elif messageId == "high_charging":
                    name = "BMS_IstModus_XIX_BMS_20_XIX_E3V_EVCANFD"
                    data_li = data_generator.high_charging(userId, vin, name, timestamp)

                # 5. 里程   mileage
                elif messageId == "mileage":
                    name = "someip_drivingstatistics_1_3.0_field_distances_notifier_49184"
                    data_li = data_generator.mileage(userId, vin, name, timestamp)

                else:
                    ret = "%s is not exist" % messageId
                    print(ret)

                if data_li:
                    print(data_li)
                    for data in data_li:
                        data_generator.send_to_kafka(data)
                        ret = "%s : message sent successfully" % messageId

            except Exception as e:
                print(str(e))
                ret = str(e)

            data_generator.producer.close()

            response['data'] = ret

        except Exception as e:
            # logging.error(str(e))
            print(e)
            response['code'] = 500
            response['msg'] = str(e)

    else:
        msg = 'Bad Request: Missing required parameters'
        response['code'] = 400
        response['msg'] = msg
        # logging.error(msg)
        print(msg)

    return jsonify(response)












