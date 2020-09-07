import arrow
import os
import mimetypes


def datetimeformat(date_str: str) -> str:
    """
    Return reader friendly time display

    :return: time format as string
    """
    dt = arrow.get(date_str)
    return dt.humanize()


def file_type(key: str) -> str:
    """
    Return file extension to MIME types

    :return: file extension MIME type as string
    """
    # extract file extension in file name string
    file_info = os.path.splitext(key)
    file_extension = file_info[1].lower()
    try:
        return mimetypes.types_map[file_extension]
    except KeyError:
        return 'Unknown'
