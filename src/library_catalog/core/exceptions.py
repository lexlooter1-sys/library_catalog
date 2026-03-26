from fastapi import HTTPException

class AppException(HTTPException):
    def __init__(self, message: str ='', status_code: int = 400):
        super().__init__(status_code=status_code, detail=message)

class NotFoundException(HTTPException):
    def __init__(self, resource=None, identifier=None):
        message = f'Resource {resource} with identifier {identifier} not found'
        super().__init__(status_code=404, detail=message)