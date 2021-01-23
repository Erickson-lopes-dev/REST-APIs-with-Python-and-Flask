from sql_alchemy import banco


class SiteModel(banco.Model):
    __tablename__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    # criando uma relação entre as tabelas
    hoteis = banco.relationship('HotelModel')  # lista de objs hoteis

    def __init__(self, url):
        self.url = url

    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json for hotel in self.hoteis]  # self.hoteis -> esta dentro do self recebido do obj
        }

    @classmethod
    def find_site(cls, url):
        site = cls.query.filter_by(url=url).first()  # SELECT * FROM hoteis WHERE hotel_id = hotel_id
        if site:
            return site
        return None

    def save_site(self):
        # adiciona o obj no banco
        banco.session.add(self)
        banco.session.commit()

    def delete_site(self):
        # Deletar todos os hoteis relacionados
        [hotel.delete_hotel()for hotel in self.hoteis]
        # Deleta o site
        banco.session.delete(self)
        banco.session.commit()
