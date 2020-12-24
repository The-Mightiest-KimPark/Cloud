import sys
import logging
import pymysql
import json
import datetime
import boto3

endpoint = 'themightiestkpk.c9jl6xhdt5hy.us-east-1.rds.amazonaws.com'
username = 'admin'
password = 'themightiestkpk1'
database_name = 'themightiestkpk'
port = 3306

logger = logging.getLogger()
logger.setLevel(logging.INFO)

conn = pymysql.connect(host=endpoint, port=port, db=database_name, user=username,
                passwd=password, charset='utf8')

def lambda_handler(event, context):
    # client = boto3.client('sns', region_name='us-east-1')
    # response = client.publish(
    #     TopicArn = 'arn:aws:sns:us-east-1:198475031161:TheMightiestKPK-SNS',
    #     Message = '테스트입니당'
    # )
    
    # client.publish(
    #     Message = '테스트입니당',
    #     PhoneNumber="+821074948977"
    # )
    
    
    # Create an SNS client
    client = boto3.client(
        "sns",
        aws_access_key_id="AKIAS4NQIUJ4WC3TUPHZ",
        aws_secret_access_key="lOX/mNiARytQovTR16zPr0zA4WUU/gckLCpeyNwe",
        region_name="us-east-1"
    )
    
    # Send your sms message.
    client.publish(
        PhoneNumber="+8201074948977",
        Message="Hello World!"
    )