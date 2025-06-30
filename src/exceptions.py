from fastapi import status


class NotFoundError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        self.code = status.HTTP_404_NOT_FOUND
    
    def __repr__(self):
        return self.msg
    

class WrongFormatError(ValueError):
    def __init__(self, msg: str):
        self.msg = msg
        self.code = status.HTTP_400_BAD_REQUEST
    
    def __repr__(self):
        return self.msg