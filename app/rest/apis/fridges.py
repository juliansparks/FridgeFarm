from flask import request
from app.rest.apis import classproperty, token_required
from flask_restplus import Resource, fields, Namespace
from app.models import Fridge, Item

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
@api.route('/<int:fridge_id>')
class FridgeResource(Resource):

    @token_required
    @api.marshal_with(ApiModels.fridge)
    def get(self, fridge_id: int) -> str:
        fridge = Fridge.by_id(fridge_id)
        return fridge

    @token_required
    @api.expect(ApiModels.fridge_payload, validate=True)
    @api.marshal_with(ApiModels.fridge)
    def patch(self, fridge_id: int) -> str:
        fridge = Fridge.by_id(fridge_id)
        data = request.json
        print(data.items())
        fridge.update(data)
        return fridge


@api.doc(security='apikey')
@api.route('/<int:fridge_id>/items/<int:item_id>')
class ItemResource(Resource):

    @token_required
    @api.marshal_with(ApiModels.item)
    def get(self, fridge_id: int, item_id: int) -> str:
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
    def patch(self, fridge_id: int, item_id: int) -> str:
        fridge = Fridge.by_id(fridge_id)
        item = Item.by_id(item_id)

        if item not in fridge:
            return {
                'message': f'Item ({item_id}) is not in fridge ({fridge_id})'
            }, 404

        data = request.json
        print(data.items())
        item.update(data)
        return item
