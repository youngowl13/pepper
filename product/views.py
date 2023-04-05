from rest_framework.decorators import api_view
from rest_framework.response import Response

import openfoodfacts

from django.shortcuts import render
from django.core.cache import cache
from product.mongo import get_db_handle, get_collection_handle


@api_view(("GET",))
def list_view(request):
    db = get_db_handle("inddata")
    products = get_collection_handle(db, "products")
    page_number = int(request.GET["page"])
    search_query = {
        "price": {
            "$gt": int(request.GET["minPrice"]),
            "$lt": int(request.GET["maxPrice"]),
        }
    }
    if len(request.GET["search"]) > 0:
        search_query["product_name"] = {
            "$regex": request.GET["search"],
            "$options": "i",
        }
    if "brand" in request.GET:
        search_query["brands"] = {"$in": request.query_params.getlist("brand")}
    if "category" in request.GET:
        search_query["categories_tags"] = {
            "$in": request.query_params.getlist("category")
        }
    product_count = len(list(products.aggregate([{"$match": search_query}])))
    product_list = products.aggregate(
        [{"$match": search_query}, {"$skip": 9 * (page_number - 1)}, {"$limit": 9}]
    )
    json_docs = [
        {
            "id": doc["id"] if "id" in doc else "",
            "product_name": doc["product_name"] if "product_name" in doc else "",
            "brands": doc["brands"] if "brands" in doc else "",
            "categories_tags": doc["categories_tags"]
            if "categories_tags" in doc
            else "",
            "brands_tags": doc["brands_tags"] if "brands_tags" in doc else "",
            "quantity": doc["quantity"] if "quantity" in doc else "",
            "price": doc["price"] if "price" in doc else "",
        }
        for doc in product_list
    ]
    return Response(
        {"products": json_docs, "count": product_count}, content_type="application/json"
    )


@api_view(("GET",))
def detail_view(request, id):
    db = get_db_handle("inddata")
    products = get_collection_handle(db, "products")
    prod = products.find_one({"id": id})
    prod_doc = {
        "id": prod["id"] if "id" in prod else "",
        "product_name": prod["product_name"] if "product_name" in prod else "",
        "price": prod["price"] if "price" in prod else "",
    }
    return Response({"product": prod_doc}, content_type="application/json")


@api_view(("POST",))
def get_images(request):
    image_url = []
    for id in request.data["ids"]:
        if cache.get(id):
            image_url.append({"id": id, "image": cache.get(id)})
        else:
            response = openfoodfacts.products.get_product(id)
            if "image_front_url" in response["product"]:
                cache.set(id, response["product"]["image_front_url"], 7 * 24 * 3600)
                image_url.append({"id": id, "image": response["product"]["image_front_url"]})
            else:
                cache.set(id, "https://icon-library.com/images/no-image-icon/no-image-icon-0.jpg", 7 * 24 * 3600)
                image_url.append({"id": id, "image": "https://icon-library.com/images/no-image-icon/no-image-icon-0.jpg"})
    return Response({"response": image_url}, content_type="application/json")


@api_view(("GET",))
def get_brands(request):
    db = get_db_handle("inddata")
    products = get_collection_handle(db, "products")
    brand_list = products.distinct("brands")
    return Response({"response": brand_list}, content_type="application/json")


@api_view(("GET",))
def get_categories(request):
    db = get_db_handle("inddata")
    products = get_collection_handle(db, "products")
    category_list = products.distinct("categories_tags")
    return Response({"response": category_list}, content_type="application/json")
