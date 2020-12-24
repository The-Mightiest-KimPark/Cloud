import sys
import logging
import pymysql
import boto3

s3 = boto3.resource('s3',
                region_name = 'us-east-1',
                aws_access_key_id = 'AKIAS4NQIUJ4WC3TUPHZ',
                aws_secret_access_key = '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')

def lambda_handler(event, context): 
    result_list = [] 
    for bucket in s3.buckets.all(): 
        print(bucket)
        
