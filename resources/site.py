from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models.site import SiteModel


class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}


class Site(Resource):
    def get(self, url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()

        return {'message': 'Site not found'}, 404

    @jwt_required
    def post(self, url):
        if SiteModel.find_site(url):
            return {"message": f'The site {url} already exists'}, 400
        try:
            site = SiteModel(url)
            site.save_site()
            return site.json()
        except Exception as error:
            return {'message': error}

    @jwt_required
    def delete(self, url):
        site = SiteModel.find_site(url)
        if site:
            try:
                site = SiteModel(url)
                site.delete_site()
                return {'message', "site deleted"}
            except Exception as error:
                return {'message': error}

        return {'message': 'Site not found'}
