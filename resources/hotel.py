from flask_restful import Resource, reqparse

from models.hotel import HotelModel


class Hoteis(Resource):
    def get(self):
        return {'Hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    # os argumentos recebidos vão ser uma requestparses
    argumentos = reqparse.RequestParser()
    # argumentos que queremos receber do json recebido
    argumentos.add_argument('nome', type=str, required=True, help="The filnds 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="The filnds 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria', type=float, required=True, help="The filnds 'diaria' cannot be left blank")
    argumentos.add_argument('cidade', type=str, required=True, help="The filnds 'cidade' cannot be left blank")

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

        try:
            hotel_obj.save_hotel()
            return hotel_obj.json()
        except Exception as err:
            return {'message': f'Erro ao salvar os dados {err}'}

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()

        # atualizar hotel se for encontrado
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)

            try:
                hotel_encontrado.save_hotel()
                return hotel_encontrado.json(), 200
            except Exception as err:
                return {'message': f'Erro ao atualizar os dados {err}'}, 500

        # Salvar novo hotel
        hotel_new = HotelModel(hotel_id, **dados)
        try:
            hotel_new.save_hotel()
            return hotel_new.json(), 201
        except Exception as err:
            return {'message': f'Erro ao salvar os dados {err}'}, 500

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
                return {'message': f"Hotel '{hotel_id}' deleted."}
            except Exception as err:
                return {'message': f'Erro ao Deletar os dados {err}'}

        return {'message': f"Hotel '{hotel_id}' not found."}, 404
