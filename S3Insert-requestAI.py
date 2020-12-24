import sys
import logging
import pymysql
import requests
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



def lambda_handler(event, context):
    connection = pymysql.connect(host=endpoint, port=port, db=database_name, user=username,
                passwd=password, charset='utf8')
    
    # S3 이미지 정보 가져오기
    s3_client = boto3.client('s3',
            region_name = 'us-east-1',
            aws_access_key_id = 'AKIAS4NQIUJ45YMBYCX3',
            aws_secret_access_key = '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')
    s3_resource = boto3.resource('s3',
            region_name = 'us-east-1',
            aws_access_key_id = 'AKIAS4NQIUJ45YMBYCX3',
            aws_secret_access_key = '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')
    bucket_name = 'themightiestkpk1'
    my_bucket = s3_resource.Bucket(bucket_name)
    
    for file in my_bucket.objects.all():
        params = {'Bucket': bucket_name, 'Key': file.key}
        
        # 사진 URL
        url = s3_client.generate_presigned_url('get_object', params)
        # 파일 이름
        fridge_number = (file.key).split('.')[0]
        # 저장 시간
        reg_date = str(file.last_modified(timezone('Asia/Seoul')))
        
        if fridge_number == event['fridge_number']:
            # AI 호출
            data = {
            "url": url,
            "fridge_number" : fridge_number,
            "reg_date" : event['reg_date']
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            data = json.dumps(data)
            print(data)
            res = requests.post('http://3.92.44.79/api/ai-img-grocery/', data=data, headers=headers)
            print(res)
    
        