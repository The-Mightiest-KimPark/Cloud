import sys
import logging
import pymysql

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
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        bodys = json.loads(event['body'])
        # 식재료 종류 삽입
        for body in bodys:
            refri_number = body['refri_number']
            name = body['name']
            count = body['count']
            reg_date = body['reg_date']
            reg_time = body['reg_time']
            sql = f"insert into NOW_GROCERY values(0, {refri_number}, {name}, {count}, {reg_date}, {reg_time}, false)"
            cur.execute(sql)
            conn.commit()
        conn.close()
        return {
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "http://jmtgr.s3-website-us-east-1.amazonaws.com",
                # "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Credentials": "true"
            },
            "statusCode":200,
            "body":True
            }