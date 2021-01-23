from flask import Flask
from flask.json import jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from resources.hotel import Hoteis, Hotel
from resources.site import Sites, Site
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'NaoContApRaNinguem123'  # secret key para aplicação
app.config['JWT_BLACKLIST_ENABLED'] = True  # ativar a blacklist do jwt para invalidar tokens
api = Api(app)

# vai cuidar de toda parte de autenticação do sistema
jwt = JWTManager(app)


@app.before_first_request
def cria_banco():
    banco.create_all()


# especificar que a função irá verificar se existe ou não o token na blacklist
@jwt.token_in_blacklist_loader
def verificar_blacklist(token):
    # verifica se esta dentro do set da Blacklist
    return token['jti'] in BLACKLIST


# regoar o acesso / regar / se estiver na blacklist esta invalidado, vai fazer o seguinte :
@jwt.revoked_token_loader
def token_de_acesso_invalidade():
    # retorna a mensagem convertendo o dicionario para json
    return jsonify({'message': 'You have been logged out'}), 401 # Não autorizado


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuario/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/site/<string:url>')

if __name__ == '__main__':
    from sql_alchemy import banco

    banco.init_app(app)
    app.run(debug=True)
