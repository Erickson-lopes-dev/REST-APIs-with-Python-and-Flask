from flask_restful import Resource, reqparse

from models.hotel import HotelModel


class Hoteis(Resource):
    def get(self):
        return {'Hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    # os argumentos recebidos vão ser uma requestparses
    argumentos = reqparse.RequestParser()
    # argumentos que queremos receber do json recebido
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
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

        # atualizar hotel se for encontrado
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200

        # Salvar novo hotel
        hotel_new = HotelModel(hotel_id, **dados)
        hotel_new.save_hotel()
        return hotel_new.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'message': f"Hotel '{hotel_id}' deleted."}
        return {'message': f"Hotel '{hotel_id}' not found."}, 404
