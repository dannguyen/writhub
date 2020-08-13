
class WrithubException(Exception):
    pass

class WrithubValueError(WrithubException):
    pass

class WrithubIOError(WrithubValueError):
    pass
