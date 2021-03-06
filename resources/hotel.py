from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
import sqlite3

from models.site import SiteModel
from resources.filtros import normalize_path_params, consulta_sem_cidade, consulta_com_cidade

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        # Criando conexao com o banco
        connection = sqlite3.connect('banco.db')
        cursos = connection.cursor()

        dados = path_params.parse_args()
        # recebe toda chave se o valor que nao for nulo/None
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        # se não for retornado nada irá retornar os parametros default
        parametros = normalize_path_params(**dados_validos)

        # cidade = parametros.get('cidade')  # Verifica se existe
        if not parametros.get('cidade'):
            # envolve os itens em uma tupla
            tupla = tuple([parametros[chave] for chave in parametros])

            # realiza a consulta passando os valores na tupla
            resultado = cursos.execute(consulta_sem_cidade, tupla)

        else:
            # envolve os itens em uma tupla
            tupla = tuple([parametros[chave] for chave in parametros])

            # realiza a consulta passando os valores na tupla
            resultado = cursos.execute(consulta_com_cidade, tupla)

        hoteis = []

        for linha in resultado:
            # para cada linha do restuldado será gerado um dicionario com os dados recebido
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4],
                'site_id': linha[5],
            })

        return {'hoteis': hoteis}


class Hotel(Resource):
    # os argumentos recebidos vão ser uma requestparses
    argumentos = reqparse.RequestParser()
    # argumentos que queremos receber do json recebido
    argumentos.add_argument('nome', type=str, required=True, help="The filnds 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="The filnds 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria', type=float, required=True, help="The filnds 'diaria' cannot be left blank")
    argumentos.add_argument('cidade', type=str, required=True, help="The filnds 'cidade' cannot be left blank")
    argumentos.add_argument('site_id', type=int, required=True, help="The filnds 'Site' cannot be left blank")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'hotel not found'}, 404

    @jwt_required
    def post(self, hotel_id):
        # Cerificando se o id do hotel existe
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'hotel id >{hotel_id}< already exists'}, 400  # bed requets

        dados = Hotel.argumentos.parse_args()
        hotel_obj = HotelModel(hotel_id, **dados)

        if not SiteModel.find_by_id(dados.get('site_id')):
            return {"message": 'O hotel precisa estar associado a um site'}
        try:
            hotel_obj.save_hotel()
            return hotel_obj.json()
        except Exception as err:
            return {'message': f'Erro ao salvar os dados {err}'}

    @jwt_required
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

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
                return {'message': f"Hotel '{hotel_id}' deleted."}
            except Exception as err:
                return {'message': f'Erro ao Deletar os dados {err}'}

        return {'message': f"Hotel '{hotel_id}' not found."}, 404
