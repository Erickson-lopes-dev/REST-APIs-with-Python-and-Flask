from flask_restful import Resource, reqparse

from models.usuario import UserModel


# /usuarios/{user_id}
class User(Resource):
    # os argumentos recebidos vão ser uma requestparses
    argumentos = reqparse.RequestParser()
    # argumentos que queremos receber do json recebido
    argumentos.add_argument('login', type=str, required=True, help="The filnds 'Login' cannot be left blank")
    argumentos.add_argument('senha', type=str, required=True, help="The filnds 'Senha' cannot be left blank")

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404

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
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help='O campo login nao pode ser deixado em branco')
        atributos.add_argument('senha', type=str, required=True, help='O campo senha nao pode ser deixado em branco')
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message', f"User {dados['login']} already exists"}

        user = UserModel(**dados)

        user.save_user()
        return {'message': 'User cread successefully'}, 201
