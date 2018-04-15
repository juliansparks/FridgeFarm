from flask import request
from app.rest.apis import classproperty, token_required, user_from_token
from flask_restplus import Resource, fields, Namespace
from app.models import Fridge, Item

from app.typing import ViewResponse

api = Namespace('fridges', description='Fridge related operations')


class ApiModels:
    """ A collection of API models used to parse json """

    @classproperty
    def item_payload(cls):
        return api.model(
            'Item payload model', {
                'name':
                fields.String(description='Item name'),
                'description':
                fields.String(description='Fridge description'),
                'quantity':
                fields.Integer(description='Quantity of this item'),
                'expiration':
                fields.DateTime(
                    description='Expiration date of this item',
                    attribute='experation'),
            })

    @classproperty
    def item(cls):
        return api.inherit(
            'Item',
            cls.item_payload, {
                'item_id':
                fields.Integer(
                    description='Unique of identifier of an item',
                    attribute='id'),
                'created':
                fields.DateTime(description='Item creation date'),
            })

    @classproperty
    def fridge_payload(cls):
        return api.model(
            'Fridge payload model', {
                'name': fields.String(description='Fridge name'),
                'description': fields.String(description='Fridge description'),
            })

    @classproperty
    def fridge(cls):
        return api.inherit(
            'Fridge',
            cls.fridge_payload, {
                'fridge_id':
                fields.Integer(
                    description='Unique identifier of a fridge',
                    attribute='id'),
                'items':
                fields.List(fields.Nested(ApiModels.item)),
                'created':
                fields.DateTime(description='Fridge creation date'),
            })


@api.doc(security='apikey')
@api.route('/')
class CreateFridgeResource(Resource):

    @token_required
    @api.expect(ApiModels.fridge_payload, validate=True)
    @api.marshal_with(ApiModels.fridge)
    def post(self) -> ViewResponse:
        """ Create a new fridge """
        data = request.json
        fridge = Fridge(
            name=data['name'],
            description=data['description'],
            user_id=user_from_token().id)
        fridge.save()
        return fridge


@api.doc(security='apikey')
@api.route('/mine')
class CurrentUsersFridgeResource(Resource):

    @token_required
    @api.marshal_with(ApiModels.fridge)
    def get(self) -> ViewResponse:
        """ Get a list of this user's fridges """
        return Fridge.owned_by(user_from_token())


@api.doc(security='apikey')
@api.route('/<int:fridge_id>')
class FridgeResource(Resource):

    @token_required
    @api.marshal_with(ApiModels.fridge)
    def get(self, fridge_id: int) -> str:
        """ Get a fridge by its id """
        fridge = Fridge.by_id(fridge_id)
        return fridge

    @token_required
    @api.expect(ApiModels.fridge_payload, validate=True)
    @api.marshal_with(ApiModels.fridge)
    def patch(self, fridge_id: int) -> str:
        """ Update a fridge """
        fridge = Fridge.by_id(fridge_id)
        data = request.json
        fridge.update(data)
        return fridge

    @token_required
    @api.expect(ApiModels.item_payload, validate=True)
    @api.marshal_with(ApiModels.item)
    def post(self, fridge_id):
        """ Create an item and add it to this fridge """
        fridge = Fridge.by_id(fridge_id)
        if fridge.user_id is not user_from_token().id:
            return {'message': 'Unauthorized'}, 401
        data = request.json
        fridge.add_item(
            name=data['name'],
            description=data['description'],
            quantity=data['quantity'],
            expiration=data['expiration'])
        return fridge


@api.doc(security='apikey')
@api.route('/<int:fridge_id>/items/<int:item_id>')
class ItemResource(Resource):

    @token_required
    @api.marshal_with(ApiModels.item)
    def get(self, fridge_id: int, item_id: int) -> ViewResponse:
        """ Get an item by id """
        fridge = Fridge.by_id(fridge_id)
        item = Item.by_id(item_id)

        if item not in fridge:
            return {
                'message': f'Item ({item_id}) is not in fridge ({fridge_id})'
            }, 404

        return item

    @token_required
    @api.expect(ApiModels.item_payload, validate=True)
    @api.marshal_with(ApiModels.item)
    def patch(self, fridge_id: int, item_id: int) -> ViewResponse:
        """ Update an item by it's id """
        fridge = Fridge.by_id(fridge_id)
        item = Item.by_id(item_id)

        if item not in fridge:
            return {
                'message': f'Item ({item_id}) is not in fridge ({fridge_id})'
            }, 404

        data = request.json
        data.items()
        item.update(data)
        return item
