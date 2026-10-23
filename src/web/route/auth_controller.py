from flask import Blueprint, request

from domain.model.sign_up_request import SignUpRequest

from domain.service.auth_service import AuthService



def create_auth_blueprint(service: AuthService) -> Blueprint:
    auth_blueprint = Blueprint('auth', __name__)

    @auth_blueprint.post("/auth/signup")
    def auth_sign_up():


        data = request.get_json(silent=True)

        if data is None or not isinstance(data, dict):
            return{
                "message": "Некорректное тело запроса"
            }, 400
        
        if "login" not in data or "password" not in data:
            return{
                "message": "Некорректный запрос (отсутствует логин или пароль)"
            }, 400
        
        
        if not isinstance(data["login"], str) or not isinstance(data["password"], str):
            return{
                "message": "Некорректное тело запроса"
            }, 400
             

        user = SignUpRequest(
            login=data["login"],
            password=data["password"]
        )

        result = service.sign_up(user)

        if result:
            return{
                "message": "Пользователь зарегистрирован"
            }, 201
        else:
            return{
                "message": "Логин уже занят"
            },409
        






    @auth_blueprint.post("/auth/login")
    def auth_login():

        authorization = request.headers.get("Authorization")

        if authorization is None:
            return{
                "message": "Ошибка заголовка Authorization"
            }, 401, {
                    "WWW-Authenticate": 'Basic realm="TicTacToe"'
                }

        parts = authorization.split(" ", 1)

        if len(parts) != 2 or parts[1] == "" or parts[0].lower() != "basic":
            return{
                "message": "Ошибка заголовка Authorization"
            }, 401, {
                    "WWW-Authenticate": 'Basic realm="TicTacToe"'
                }

        base_string = parts[1]
        user_id = service.authenticate(base_string)

        if user_id is None:
            return{
                "message": "Неверные учётные данные"
            }, 401, {
                    "WWW-Authenticate": 'Basic realm="TicTacToe"'
                }
        else:
            return{
                "user_id": str(user_id)
            }, 200




    return auth_blueprint



