# 发送邮件
import smtplib  # smtp服务器， (smtp：轻量级邮件发送协议)
from email.mime.text import MIMEText  # 邮件文本

content = '这是一封测试邮件方式02'

message = MIMEText(content, 'plain', 'utf-8')  # 内容，文本，编码

message['Subject'] = '邮件自动发送'
message['To'] = 'bq07140@163.com'
message['From'] = 'zhonggong_test@163.com'

smtp = smtplib.SMTP_SSL('smtp.163.com', 994)

smtp.login('zhonggong_test@163.com', 'zhonggong0311')
smtp.sendmail('zhonggong_test@163.com', ['bq07140@163.com'], message.as_string())
smtp.close()


