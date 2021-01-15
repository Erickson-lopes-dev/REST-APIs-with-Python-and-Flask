from flask_restful import Resource, reqparse

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 423.34,
        'cidade': 'Rio'
    },
    {
        'hotel_id': 'Paladins',
        'nome': 'Cundi Hotel',
        'estrelas': 3.7,
        'diaria': 200.00,
        'cidade': 'Rio'
    },
    {
        'hotel_id': 'Fiulad',
        'nome': 'GUloia Hotel',
        'estrelas': 1.5,
        'diaria': 54,
        'cidade': 'Montes Claros'
    }
]


class Hoteis(Resource):
    def get(self):
        return {'Hoteis': hoteis}


class Hotel(Resource):
    def get(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return {'message': 'hotel not found'}

    def post(self, hotel_id):
        # os argumentos recebidos vão ser uma requestparses
        argumentos = reqparse.RequestParser()
        # argumentos que queremos receber do json recebido
        argumentos.add_argument('nome')
        argumentos.add_argument('estrelas')
        argumentos.add_argument('diaria')
        argumentos.add_argument('cidade')
        # construtor dos dados
        dados = argumentos.parse_args()
        # exibe os dados recebidos
        # print(dados)
        novo_hotel = {
            'hotel_id': hotel_id, **dados
        }
        hoteis.append(novo_hotel)

        print(novo_hotel)
        return novo_hotel, 200

    def put(self, hotel_id):
        pass

    def delete(self, hotel_id):
        pass
