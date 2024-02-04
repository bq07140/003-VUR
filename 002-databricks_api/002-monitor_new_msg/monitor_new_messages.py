import logging
from databricks import sql
from datetime import datetime
import smtplib  # 发送邮件 smtp服务器， (smtp：轻量级邮件发送协议)
from email.mime.text import MIMEText  # 邮件文本

logging.getLogger("response_aggr_dbr_api.py").setLevel(logging.DEBUG)
logging.basicConfig(filename="../response_aggr_dbr_api.log", level=logging.ERROR)

TOTAL_LINE = 86


class QueryDatabricks(object):

    def __init__(self):
        self.conn = sql.connect(
            server_hostname="adb-2515004071041721.1.databricks.azure.cn",
            http_path="/sql/1.0/warehouses/07194f39c23cde02",
            access_token="dapi27116197bf3636c59422a74de3e768ab")

        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def timestamp_to_str(self, timestamp):

        dt_object = datetime.utcfromtimestamp(timestamp)
        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')

        return formatted_time

    # 发送邮件通知
    def send_msg_to_email(self, new_total):

        content = 'kafka 中有了新的数据, 原来有{0}条数据，现在有{1}'.format(TOTAL_LINE, new_total)
        print(content)

        message = MIMEText(content, 'plain', 'utf-8')  # 内容，文本，编码

        message['Subject'] = 'kafka主题有了新的消息，请注意查收'
        message['To'] = 'bq07140@163.com'
        message['From'] = 'zhonggong_test@163.com'

        smtp = smtplib.SMTP_SSL('smtp.163.com', 994)

        smtp.login('zhonggong_test@163.com', 'zhonggong0311')
        smtp.sendmail('zhonggong_test@163.com', ['bq07140@163.com', 'hurunpu@qq.com', 'wengang.tan@gausscode.com'],
                      message.as_string())
        # smtp.sendmail('zhonggong_test@163.com', ['bq07140@163.com', 'wengang.tan@gausscode.com'], message.as_string())
        smtp.close()

    def monitor_kafka_new_msgs(self):

        try:
            sql = """
                    SELECT count(*) as new_total
                    from hive_metastore.default.cx5_ods_gdc_original001 
                  """

            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            ret = [line.asDict() for line in ret]
            new_total = ret[0]['new_total']
            print(new_total)

            # 有新的数据写入，发送邮件
            if new_total > TOTAL_LINE:
                self.send_msg_to_email(new_total)

        except Exception as e:
            print(str(e))

        return ret


if __name__ == '__main__':
    monitor = QueryDatabricks()

    monitor.monitor_kafka_new_msgs()
