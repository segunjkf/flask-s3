import arrow
import mimetypes
import os

additional_file_types = {
    '.tfsate': 'terraform/state'
}

def datetimeformat(date_str):
    dt = arrow.get(date_str)
    return dt.humanize()

def file_type(key):
    file_info = os.path.splitext(key)
    file_extension = file_info[1]
    try:
        return mimetypes.types_map.get(file_extension, 'application/octet-stream')
    except KeyError:
        file_type = 'Unknown'
        if file_info[0].startswith('.') and file_extension == '':
            filetype = 'text'
        if file_extension in additional_file_types.keys(): 
           filetype = additional_file_types[file_extension]   
        return filetype

        