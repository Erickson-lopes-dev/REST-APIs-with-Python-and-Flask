from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from models.usuario import UserModel

# os argumentos recebidos vão ser uma requestparses
argumentos = reqparse.RequestParser()
# argumentos que queremos receber do json recebido
argumentos.add_argument('login', type=str, required=True, help="The filnds 'Login' cannot be left blank")
argumentos.add_argument('senha', type=str, required=True, help="The filnds 'Senha' cannot be left blank")


# /usuarios/{user_id}
class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
                return {'message': f"User '{user}' deleted."}
            except Exception as err:
                return {'message': f'Erro ao Deletar os dados {err}'}

        return {'message': f"User '{user}' not found."}, 404


class UserRegister(Resource):
    # /cadastro
    # usuario tera que ter acesso com token a aplicação para registrar um usuário
    def post(self):
        dados = argumentos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists.".format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created successfully!'}, 201  # Created


class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = argumentos.parse_args()

        user = UserModel.find_by_login(dados['login'])
        # comparar duas str seguramente
        if user and safe_str_cmp(user.senha, dados['senha']):
            # cria um token de acesso para o usuário
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200

        return {'message': 'The username or password is incorrect.'}, 401  # nao autorizado
