import boto3
import logging
from botocore.exceptions import ClientError
from pprint import pprint


def get_bucket():
    s3_resource = boto3.resource('s3')
    return s3_resource.Bucket("zeitgeist-operations")

def list_buckets():
    client = boto3.client('s3')
    return client.list_buckets().get('Buckets')
