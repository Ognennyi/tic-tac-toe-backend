from abc import ABC, abstractmethod
from domain.model.sign_up_request import SignUpRequest

from uuid import UUID

class AuthService(ABC):

    @abstractmethod
    def sign_up(self, request: SignUpRequest) -> bool:
        pass

    @abstractmethod
    def authenticate(self, encoded_credentials: str) -> UUID | None:
        pass