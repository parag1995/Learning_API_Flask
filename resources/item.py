import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help="This field cannot be blank!"
    )
    
    parser.add_argument('store_id',
    type=float,
    required=True,
    help="Every item need a store id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'item not found'}, 404
        # item = next(filter(lambda x:x['name']==name,items),None)
        # for item in items:
        #     if item['name']==name:
        #         return item
        # return {'item':item},200 if item else 404

    def post(self, name):
        if ItemModel.find_by_name(name):
        #   if next(filter(lambda x:x['name']==name,items),None):
            return {'message' :"An item with name '{}' already exist".format(name)},400

        data = Item.parser.parse_args()
        # data = request.get_json()#(force=True) #force=True(not suggested)  it will check if json is not provided by client and header of request is not set to jason
        item =ItemModel(name,data['price'],data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting thr item"},500 #internal server error
        return item.json(),201

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message":"item deleted"}
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = 'DELETE FROM items WHERE name=?'
        # cursor.execute(query,(name,))
        # connection.commit()
        # connection.close()
        # return{"message" : "item deleted"}

    def put(self,name):
        data =Item.parser.parse_args()      #request.get_json()
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name,data['price'])
        # item = next(filter(lambda x: x['name']==name,items),None)
        if item is None:
            item = ItemModel(name,data['price'],data['store_id'])
        else:
            item.price = data['price']


        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items":[item.json() for item in ItemModel.query.all()]}

        # return {"items":list(map(lambda x:x.json(), ItemModel.query.all()))}



        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        #
        # query = 'SELECT * FROM items'
        # result= cursor.execute(query)
        # items=[]
        # for row in result:
        #     items.append({'name':row[0],'price':row[1]})
        #
        # # connection.commit()
        # connection.close()
        # return {'items':items}
