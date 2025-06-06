class AppException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class UserNotFound(AppException):
    def __init__(self, message):
        super().__init__(f"User error: {message}", 404)

class Unauthorized(AppException):
    def __init__(self, message, status):
        super().__init__(f"Unauthorized: {message}", status)

class EventNotFound(AppException):
    def __init__(self, message, status=404):
        super().__init__(f"Event error: {message}", status)

class ModelException(AppException):
    def __init__(self, message, status):
        super().__init__(f"Model exception error: {message}", status)
