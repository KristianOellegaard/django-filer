#-*- coding: utf-8 -*-
import os
import mimetypes
from django.utils.encoding import smart_str

class ServerBase(object):
    def __init__(self, *args, **kwargs):
        pass
    
    def get_mimetype(self, path):
        return mimetypes.guess_type(path)[0] or 'application/octet-stream'
    
    def default_headers(self, **kwargs):
        self.save_as_header(**kwargs)
        self.size_header(**kwargs)
    def save_as_header(self, response, **kwargs):
        '''
        * if save_as is False the header will not be added
        * if save_as is a filename, it will be used in the header
        * if save_as is None the filename will be determined from the file path
        '''
        save_as = kwargs.get('save_as', None)
        if save_as == False:
            return
        file = kwargs.get('file', None)
        filename = None
        if save_as:
            filename = save_as
        else:
            filename = os.path.basename(file.path)
        response['Content-Disposition'] = smart_str(u'attachment; filename=%s' % filename)
    def size_header(self, response, **kwargs):
        size = kwargs.get('size', None)
        file = kwargs.get('file', None)
        if size:
            response['Content-Length'] = size
        elif file and file.size is not None:
            response['Content-Length'] = file.size