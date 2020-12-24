import sys
import logging
import pymysql
import boto3
import json
import datetime

endpoint = 'themightiestkpk.c9jl6xhdt5hy.us-east-1.rds.amazonaws.com'
username = 'admin'
password = 'themightiestkpk1'
database_name = 'themightiestkpk'
port = 3306

logger = logging.getLogger()
logger.setLevel(logging.INFO)

connection = pymysql.connect(host=endpoint, port=port, db=database_name, user=username,
                passwd=password, charset='utf8')

# 회원 사진 등록/수(multipart로 받은 파일 S3에 올리고 디비에 url저장하기)            
# 받는 값 : email, multipart file
# 만든이 : snchoi
s3 = boto3.client('s3')
def lambda_handler(event, context):
    # S3 정보 세팅
    # 이메일, 멀티파트 파일, 파일이름 받기
    # body = event['body']
    # email = body['email']
    # file = body['file']
    # fileName = body['fileName']
    
    # # S3에 이미지 올리기
    # bucket = 'themightiestpkpuserprofile'
    # fullFileName = f'{email}/{fileName}.PNG'
    # s3.put_object(Bucket=bucket, Key=fullFileName, Body=file)
    
    # img_url = f'https://themightiestpkpuserprofile.s3.amazonaws.com/{fullFileName}'
    
    # print('Put Complete')
    
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
    
    # # 해당 email에 해당하는 사용자 데이터 베이스에 이미지 url 저장
    # cursor = connection.cursor(pymysql.cursors.DictCursor)
    # query = f"update USER_INFO set img_url = '{img_url}' where email = '{email}')"
    # result = cursor.execute(query)
    # if result:
    #     connection.commit()
    #     return {
    #         "headers": {
    #         "Content-Type": "application/json",
    #         "Access-Control-Allow-Origin": "http://jmtgr.s3-website-us-east-1.amazonaws.com",
    #         "Access-Control-Allow-Headers": "Content-Type",
    #         "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
    #         "Access-Control-Allow-Credentials": "true"
    #         },
    #         "statusCode":200,
    #         "body":True
    #     }
    # return {
    #     "statusCode":400,
    #     "body": False
    # }