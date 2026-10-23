from uuid import UUID

from domain.service.auth_service import AuthService


class UserAuthenticator():

    def __init__(self, service: AuthService):
        self.service = service


    def authenticate(self, authorization: str | None) -> UUID | None:

        if authorization is None:
            return None

        parts = authorization.split(" ", 1)

        if parts[0].lower() == "basic" and len(parts) == 2 and len(parts[1]) != 0:
            return self.service.authenticate(parts[1])
        else:
            return None
        


        