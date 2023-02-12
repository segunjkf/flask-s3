import boto3
from botocore.exceptions import ClientError
from flask import session, flash, redirect, url_for


def get_bucket():
    s3_resource = boto3.resource('s3')
    if 'bucket' in session:
        bucket = session['bucket']
    else:
        flash("Bucket is not available")
        return redirect(url_for('/'))   
    return s3_resource.Bucket(bucket)

def list_buckets():
    client = boto3.client('s3')
    return client.list_buckets().get('Buckets')
