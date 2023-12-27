from .commons import BadRequest, PermissionDenied

class BotNameInvalid(BadRequest):
    DETAIL = "名稱只能包含英文、數字、底線、減號"


class BotNameExisted(BadRequest):
    DETAIL = "名稱重複，請重新命名！"
    
    
class BotNameLengthError(BadRequest):
    DETAIL = "名稱長度必須介於3到20個字元之間"
    
    
class BotUnauthorized(PermissionDenied):
    DETAIL = "您沒有權限操作此機器人"
    

class BotNotFound(BadRequest):
    DETAIL = "找不到此機器人"
    