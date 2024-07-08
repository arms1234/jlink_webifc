


class PageError(Exception):
    def __init__(self, msg, errno = 0):    
        self.errno = errno
        self.errmsg = msg


