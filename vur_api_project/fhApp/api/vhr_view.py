# -*- coding: utf-8 -*-
import logging
from flask import request, jsonify
from . import api
from fhApp.utils.vhr_worker_fun import DataGenerator
from fhApp.utils.dbr_worker_fun import QueryDatabricks


# http://127.0.0.1:8000/vhr/produce_one_mock_data?userId=393b4915-8a1a-43c9-a5e1-2710057fdf8b&vin=b9487cfbc0c74499a970d5d08d2878c1&messageId=battery_temp&flag=0
@api.route('vhr/produce_one_mock_data')
def produce_one_mock_data():
    userId = request.args.get('userId')
    vin = request.args.get('vin')
    messageId = request.args.get('messageId')
    flag = request.args.get('flag', '1')

    response = {
        'code': 200,
        'msg': 'Success',
        'data': ""
    }

    if all([userId, vin, messageId, flag]):

        try:
            data_generator = DataGenerator()

            try:
                data = data_generator.generate_data(userId, vin, messageId, flag)

                data_generator.send_to_kafka(data)
                ret = "%s : message sent successfully" % messageId

            except Exception as e:
                print(str(e))
                ret = str(e)

            data_generator.producer.close()

            response['data'] = ret

        except Exception as e:
            logging.error(str(e))
            response['code'] = 500
            response['msg'] = str(e)

    else:
        msg = 'Bad Request: Missing required parameters'
        response['code'] = 400
        response['msg'] = msg
        logging.error(msg)

    return jsonify(response)


# http://127.0.0.1:8000/vhr/vdaa_gdc?userId=393b4915-8a1a-43c9-a5e1-2710057fdf8b&vin=b9487cfbc0c74499a970d5d08d2878c1
# http://127.0.0.1:8000/vhr/vdaa_gdc?vin=b9487cfbc0c74499a970d5d08d2878c1
@api.route('vhr/vdaa_gdc')
def vdaa_gdc():
    vin = request.args.get('vin')

    response = {
        'code': 200,
        'msg': 'Success',
        'data': {}
    }

    if vin:
        try:
            databricks = QueryDatabricks()
            ret = databricks.vdaa_gdc(vin)
            response['data']['warningLights'] = ret
            databricks.close_db()  # 关闭连接
        except Exception as e:
            logging.error(str(e))
            response['code'] = 500
            response['msg'] = str(e)

    else:
        msg = 'Bad Request: Missing required parameters'
        response['code'] = 400
        response['msg'] = msg
        logging.error(msg)

    return jsonify(response)


