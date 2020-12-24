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

# 모션 센서 ON상태 > 설정기간동안 작동 없을 시 이메일 보내기
# 작성자 : snchoi
def lambda_handler(event, context):
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    # 외출모드  안해논 사람들 이메일, 설정기간 조회 
    sql_users = "SELECT email, motion_period FROM REFRIGERATOR where outing_mode = 0  and email is not null;"
    cur.execute(sql_users)
    user_infos = cur.fetchall()
    
    
    
    # 현재시간, 최근 감지 시간 비교하여 설정기간보다 텀이 길면 메세지 발송
    for user_info in user_infos:
        email = user_info['email']
        motion_period = user_info['motion_period']
        
        sql_user = f"SELECT name, guardian_phone_number, guardian_name FROM USER_INFO where email = '{email}'"
        cur.execute(sql_user)
        user = cur.fetchone()
        name = user['name']
        guardian_phone_number = user['guardian_phone_number']
        guardian_name = user['guardian_name']
        print('name : ', name)
        print('guardian_phone_number : ', guardian_phone_number)
        
        sql_motion_latest = f"SELECT reg_date FROM SENSOR WHERE email = '{email}' and name = 'motion' ORDER BY reg_date DESC limit 1"
        result = cur.execute(sql_motion_latest)
        print('result :',  result)
        
        if result:
            latest_date = cur.fetchone()['reg_date'] # 최근 감지 시간
            now_date = datetime.datetime.now() # 현재 시간
            
            days = (now_date - latest_date).days
            print('days : ', days)
            print('motion_period : ', motion_period)
            # 설정 기간과 비교
            if days >= motion_period:
                
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
                    Message=f"{guardian_name}님 현재 {name}님의 움직임이 {days}일간 감지되지 않았습니다."
                )
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