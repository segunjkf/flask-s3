from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
import boto3
import logging
from botocore.exceptions import ClientError
from filter import datetimeformat, file_type

Client = boto3.client("s3")
response = Client.list_buckets()

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'secret'
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files')
def files():
    s3_resource = boto3.resource('s3')
    buckets = s3_resource.Bucket("zeitgeist-operations")
    summaries = buckets.objects.all()

    return render_template('files.html', buckets=buckets, files=summaries)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    s3_resource = boto3.resource('s3')
    buckets = s3_resource.Bucket("zeitgeist-operations")
    buckets.Object(file.filename).put(Body=file)
    flash('File was successfully uploaded')
    return redirect(url_for('files'))

if __name__ == '__main__':
    app.debug   
    app.run()

