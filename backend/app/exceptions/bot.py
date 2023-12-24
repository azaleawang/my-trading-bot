from .commons import BadRequest

class BotNameInvalid(BadRequest):
    DETAIL = "名稱只能包含英文、數字、底線、減號"


class BotNameExisted(BadRequest):
    DETAIL = "名稱重複，請重新命名！"
    
    
class BotNameTooLong(BadRequest):
    DETAIL = "名稱長度必須介於1到20個字元之間"
    