from .commons import BadRequest, PermissionDenied

class EmailExisted(BadRequest):
    DETAIL = "Email already registered!"
    
class LoginFailed(PermissionDenied):
    DETAIL = "Incorrect email or password"