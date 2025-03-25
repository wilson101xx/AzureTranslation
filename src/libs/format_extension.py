def get_format_from_extension(source_ext):
    format_mapping = {
        '.txt': "text/plain",
        '.txv': "text/tab-separated-values",
        '.tab': "text/tab-separated-values",
        '.csv': "text/csv",
        '.html': "text/html",
        '.htm': "text/html",
        '.mthml': "message/rfc822@application/x-mimearchive@multipart/related",
        '.mthm': "message/rfc822@application/x-mimearchive@multipart/related",
        '.pptx': "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        '.xlsx': "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        '.docx': "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        '.msg': "application/vnd.ms-outlook",
        '.xlf': "application/xliff+xml",
        '.xliff': "application/xliff+xml"
    }
    return format_mapping.get(source_ext, None)