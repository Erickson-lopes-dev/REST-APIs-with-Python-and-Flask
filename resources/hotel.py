from flask_restful import Resource, reqparse

from models.hotel import HotelModel

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
    # os argumentos recebidos vão ser uma requestparses
    argumentos = reqparse.RequestParser()
    # argumentos que queremos receber do json recebido
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'hotel not found'}, 404

    def post(self, hotel_id):
        # Cerificando se o id do hotel existe
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'hotel id >{hotel_id}< already exists'}, 400  # bed requets

        dados = Hotel.argumentos.parse_args()
        # exibe os dados recebidos
        # print(dados)
        hotel_obj = HotelModel(hotel_id, **dados)

        hotel_obj.save_hotel()

        return hotel_obj.json()

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()

        hotel_obj = HotelModel(hotel_id, **dados)

        novo_hotel = hotel_obj.json()

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200

        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted'}
