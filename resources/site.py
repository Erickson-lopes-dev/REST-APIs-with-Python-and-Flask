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
            return {"message": "The site '{}' already exists."}, 400 # bad request
        site = SiteModel(url)
        try:
            site.save_site()
        except Exception as error:
            return {'message': f'An internal error ocurred trying to create a new site. {error}'}, 500
        return site.json()

    @jwt_required
    def delete(self, url):
        site = SiteModel.find_site(url)
        if site:
            site.delete_site()
            return {'message': 'Site deleted.'}
        return {'message': 'Site not found.'}, 404
