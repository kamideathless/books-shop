class NotFoundError(Exception):
    def __init__(self, detail: str = "Не найдено"):
        self.detail = detail
        super().__init__(detail)


class AlreadyExistsError(Exception):
    def __init__(self, detail: str = "Уже существует"):
        self.detail = detail
        super().__init__(detail)


class AuthError(Exception):
    def __init__(self, detail: str = "Неправильный логин или пароль"):
        self.detail = detail
        super().__init__(detail)


class WrongTokenType(Exception):
    def __init__(self, detail: str = "Неправильный тип токена"):
        self.detail = detail
        super().__init__(detail)


class TokenExpired(Exception):
    def __init__(self, detail: str = "Срок действия токена истек"):
        self.detail = detail
        super().__init__(detail)


class InvalidToken(Exception):
    def __init__(self, detail: str = "Токен неправильный"):
        self.detail = detail
        super().__init__(detail)
