from fastapi import status


class BaseError(Exception):
    msg: str
    code: int


class NotFoundError(BaseError):
    def __init__(self, msg: str):
        self.msg = msg
        self.code = status.HTTP_404_NOT_FOUND

    def __repr__(self):
        return self.msg


class WrongFormatError(BaseError):
    def __init__(self, msg: str):
        self.msg = msg
        self.code = status.HTTP_400_BAD_REQUEST

    def __repr__(self):
        return self.msg


class AlreadyExistsError(BaseError):
    def __init__(self, msg: str):
        self.msg = msg
        self.code = status.HTTP_409_CONFLICT

    def __repr__(self):
        return self.msg
