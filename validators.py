def validate_extension(filename: str) -> bool:
    """
    Validate file extension

    :param filename: file name as string
    :return: True if extension is allowed
    """
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions