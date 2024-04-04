import uuid
from flask import Flask, request
from db import items, stores
from flask_smorest import abort

app = Flask(__name__)


@app.get("/store")   # http://127.0.0.1:5000/store
def get_stores():
    return {"stores": list(stores.values())}


@app.get("/store/<string:store_id>")  # http://127.0.0.1:5000/store
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")


@app.post("/store")   # http://127.0.0.1:5000/store
def create_stores():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message="Bad request, ensure 'name' are included in JSON payload")

    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Store already exists.")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted"}
    except KeyError:
        abort(404, message="Store not found")


"""
When using "abort" it will be documented by flask, if not it will need to be documented manually
"""


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if(
        "price" not in item_data or
        "store_id" not in item_data or
        "name" not in item_data
    ):
        abort(400, message="Bad request, ensure 'price', 'store_id' and 'name' are included in JSON payload")

    for item in items.values():
        if(
            item_data["name"] == item["name"] and
            item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"item already exists.")

    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message="Bad request. Ensure 'price' and 'name' are included in the JSON payload")

    try:
        item = items[item_id]
        item |= item_data
    except KeyError:
        abort(404, message="Item not found")


@app.get("/item")   # http://127.0.0.1:5000/store
def get_all_items():
    return {"items": list(items.values())}



@app.get("/item/<string:item_id>")  # http://127.0.0.1:5000/store
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found")


@app.delete("/item/<string:item_id>")
def delete_items(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message="Item not found")



