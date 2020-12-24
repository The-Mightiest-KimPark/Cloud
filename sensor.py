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



# 센서값 저장, 화재감지 시 문자발송
# 받는 값 : fridge_number, name, value, reg_date
# 작성자 : snchoi
def lambda_handler(event, context):
    conn = pymysql.connect(host=endpoint, port=port, db=database_name, user=username,
                passwd=password, charset='utf8')
    operation = event['httpMethod']
    if operation == 'POST':
        # 받아온 데이터
        print('event : ', event)
        body = json.loads(event['body'])
        print('body : ', body)
        fridge_number = body['fridge_number']
        print('fridge_number : ', fridge_number)
        name = body['name']
        value = body['value']
        reg_date = body['reg_date']
        
        # 냉장고 번호 이용해 사용자 이메일 가져오기
        conn.commit()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        
        sql_email = f"select email from REFRIGERATOR where fridge_number = '{fridge_number}'"
        cur.execute(sql_email)
        email = cur.fetchone()['email']
        
        
        # 불꽃 센서 작동시 문자메세지 보내기
        if name == 'flame' and value <= 50:
            
            sql_fire = f"select guardian_phone_number, name, guardian_name from USER_INFO where email = '{email}'"
            cur.execute(sql_fire)
            result = cur.fetchone()

            guardian_phone_number = result['guardian_phone_number']
            user_name = result['name']
            guardian_name = result['guardian_name']
            
            # SNS 문자 보내는 로직 
            # Create an SNS client
            client = boto3.client(
                "sns",
                aws_access_key_id="AKIAXLGYXNODVELA6FE2",
                aws_secret_access_key="0nCGogPxjZyEIZC+qQKsDQbEO+uyLFkDfhXTMmrm",
                region_name="us-east-1"
            )
            
            # Send your sms message.
            client.publish(
                PhoneNumber="+82"+guardian_phone_number,
                Message=f"{guardian_name}님!! {reg_date} 시각 {user_name}님의 집에  화재가 감지되었습니다."
            )
        
        # 이전 센서값 삭제
        sql_sensor = f"delete from SENSOR where email='{email}' AND name='{name}'"
        cur.execute(sql_sensor)
        conn.commit()

        
        # 센서값 저장
        sql_sensor = f"insert into SENSOR values(0, '{email}', '{name}', {value}, '{reg_date}')"
        cur.execute(sql_sensor)
        conn.commit()
        
        cur.close()
        conn.close()
        
        
        return {
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                # "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Credentials": "true"
                },
            "statusCode":200,
            "body":True
            }