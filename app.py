from flask import Flask, render_template, request, redirect, url_for, flash, Response
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
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file is None:
        flash('Please select a file to upload')
        return redirect(url_for('files'))

    if file and allowed_file(file.filename):
        s3_resource = boto3.resource('s3')
        buckets = s3_resource.Bucket("zeitgeist-operations")
        try:
            buckets.Object(file.filename).put(Body=file)
            flash('File was successfully uploaded')
            return redirect(url_for('files'))
        except Exception as e:
            flash('An error occurred while uploading the file: {}'.format(e))
            return redirect(url_for('files'))
    else:
        flash('File type not allowed')
        return redirect(url_for('files'))

@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    s3_resource = boto3.resource('s3')
    buckets = s3_resource.Bucket("zeitgeist-operations")
    buckets.Object(key).delete()

    flash('File deleted successfully')
    return redirect(url_for('files'))

@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']

    s3_resource = boto3.resource('s3')
    buckets = s3_resource.Bucket("zeitgeist-operations")

    file_obj = buckets.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )


if __name__ == '__main__':
    app.debug   
    app.run()