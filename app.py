from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_bootstrap import Bootstrap
import requests

from resources import get_bucket
from validators import validate_extension
from filters import datetimeformat, file_type

app = Flask(__name__)
app.secret_key = 'secret'

# load bootstrap extension
Bootstrap(app)

# load filters for data
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type


@app.route('/')
def index():
    """
    Render index page
    """
    # get bucket summary from bucket
    my_bucket = get_bucket()
    summaries = my_bucket.objects.all()

    # get image labels from lambda function
    res = requests.get("https://0f3kzkdn93.execute-api.us-east-2.amazonaws.com/prod")
    labels = res.json()['body']

    # render files.html
    return render_template('index.html', my_bucket=my_bucket, files=summaries, labels=labels)


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
