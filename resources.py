import boto3

# credentials
S3_BUCKET = 'upload-with-flask'
S3_KEY = ''
S3_SECRET = ''


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
