from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaia': 423.34,
        'cidade': 'Rio'
    },
    {
        'hotel_id': 'Paladins',
        'nome': 'Cundi Hotel',
        'estrelas': 3.7,
        'diaia': 200.00,
        'cidade': 'Rio'
    },
    {
        'hotel_id': 'Fiulad',
        'nome': 'GUloia Hotel',
        'estrelas': 1.5,
        'diaia': 54,
        'cidade': 'Montes Claros'
    }
]


class Hoteis(Resource):
    def get(self):
        return {'Hoteis': hoteis}


api.add_resource(Hoteis, '/hoteis')

if __name__ == '__main__':
    app.run(debug=True)
