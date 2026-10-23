from domain.model.sign_up_request import SignUpRequest
from domain.service.auth_service import AuthService
from domain.service.user_service import UserService
from uuid import uuid4, UUID

import base64
from binascii import Error

from domain.model.user import User

from werkzeug.security import generate_password_hash, check_password_hash

class AuthServiceImpl(AuthService):

    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    def sign_up(self, request: SignUpRequest) -> bool:
        login = request.login
        password = request.password

        existing_user = self.user_service.get_by_login(login)
        if existing_user is not None:
            return False
        
        password_hash = generate_password_hash(password)

        new_user = User(
            id = uuid4(),
            login=request.login,
            password = password_hash
        )

        self.user_service.create_user(new_user)

        return True

        

    
    def authenticate(self, encoded_credentials: str) -> UUID | None:
        
        
        try:
            decoded_bytes = base64.b64decode(encoded_credentials, validate=True)
            decoded_string = decoded_bytes.decode("utf-8")

            login, password = decoded_string.split(":", 1)

            user = self.user_service.get_by_login(login)
        except (Error, UnicodeDecodeError, ValueError): 
            return None
        
        if user is None:
            return None
        
        is_valid = check_password_hash(user.password, password)

        if is_valid:
            return user.id
        else: 
            return None
