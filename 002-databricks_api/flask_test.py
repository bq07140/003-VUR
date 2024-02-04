import logging
from flask import Flask, jsonify, request

logging.getLogger("response_aggr_dbr_api.py").setLevel(logging.DEBUG)
logging.basicConfig(filename="response_aggr_dbr_api.log", level=logging.ERROR)

app = Flask(__name__)


# http://127.0.0.1:5000/index
@app.route('/index')
def vdaa_gdc():

    response = {
        'code': 200,
        'msg': 'Success',
        'data': {}
    }

    return jsonify(response)


if __name__ == '__main__':
    # print(app.url_map)
    app.run(host='0.0.0.0', debug=True, port=9092)









