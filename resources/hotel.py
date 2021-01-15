from flask_restful import Resource

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


class Hotel(Resource):
    def get(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel

    def post(self, hotel_id):
        pass

    def put(self, hotel_id):
        pass

    def delete(self, hotel_id):
        pass
