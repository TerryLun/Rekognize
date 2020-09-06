from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_bootstrap import Bootstrap
import boto3
from filters import datetimeformat, file_type

# credentials
S3_BUCKET = 'upload-with-flask'
S3_KEY = 'AKIA3LV4Y2GSU2CHQCGL'
S3_SECRET = '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'

app = Flask(__name__)
app.secret_key = 'secret'

# load bootstrap extention
Bootstrap(app)

# load filters for data
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type


def get_s3_resource():
    """
    Return s3 service resource

    :return: s3 service resource
    """
    if S3_KEY and S3_SECRET:
        return boto3.resource("s3", aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)
    else:
        return boto3.resource('s3')


def get_bucket():
    """
    Return the s3 bucket

    :return: s3 bucket
    """
    s3_resource = get_s3_resource()
    return s3_resource.Bucket(S3_BUCKET)


@app.route('/')
def index():
    """
    Files route

    docs: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/collections.html
    """
    # get bucket summary from bucket
    my_bucket = get_bucket()
    summaries = my_bucket.objects.all()
    tags = {}
    counter = 0
    for f in summaries:
        tags[f.key] = str(counter)
        counter += 1
    print(tags)
    # render files.html
    return render_template('index.html', my_bucket=my_bucket, files=summaries, tags=tags)


def validate_extension(filename: str) -> bool:
    """
    Validate file extension

    :param filename: file name as string
    :return: True if extension is allowed
    """
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/upload', methods=['post'])
def upload():
    """
    Upload image
    """
    try:
        file = request.files['file']
    except:
        pass
    else:
        # check file extension
        if validate_extension(file.filename):
            # upload user file to bucket
            my_bucket = get_bucket()
            my_bucket.Object(file.filename).put(Body=file)

            # flash message
            flash('File uploaded successfully')
        else:
            flash('Only .jpg, .jpeg and .png are allowed')
    finally:
        return redirect(url_for('index'))


@app.route('/delete', methods=['post'])
def delete():
    """
    Delete image
    """
    # get key from hidden value
    key = request.form['key']

    # delete file in bucket using key
    my_bucket = get_bucket()
    my_bucket.Object(key).delete()

    # flash message
    flash('File deleted successfully')

    return redirect(url_for('index'))


@app.route('/download', methods=['post'])
def download():
    """
    Download image
    """
    # get key from hidden value
    key = request.form['key']

    # get file in bucket using key
    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()

    # download file
    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={'content-Disposition': f'attachment;filename={key}'}
    )


if __name__ == '__main__':
    app.run(debug=True)
