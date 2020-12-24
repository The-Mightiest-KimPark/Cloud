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
        # 현재 식재료에 해당하는 추천 레시 삽입
        for body in bodys:
            refri_number = body['refri_number']
            name = body['name']
            ingredient = body['ingredient']
            ingredient_name = body['ingredient_name']
            seasoning = body['seasoning']
            seasoning_name = body['seasoning_name']
            howto = body['howto']
            purpose = body['purpose']
            sql1 = f"insert into NOW_RECIPE values(0, {refri_number}, {name}, {ingredient}, {ingredient_name}, {seasoning}, {seasoning_name}, {howto})"
            cur.execute(sql1)
            conn.commit()
            
            sql2 = f"insert into NOW_RECIPE values(0, {refri_number}, {name}, {ingredient}, {ingredient_name}, {seasoning}, {seasoning_name}, {howto}, {purpose})"
            cur.execute(sql2)
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