import imp
from django.shortcuts import render
from product.mongo import get_db_handle, get_collection_handle
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import openfoodfacts
from bson import json_util


@api_view(('GET',))
def list_view(request):
    db, mongo_client = get_db_handle('inddata')
    products = get_collection_handle(db, 'products')
    product_list = products.find({})[0:9]
    json_docs = [{"id": doc["id"] if "id" in doc else "",
                  #   "allergens_tags": doc["allergens_tags"] if "allergens_tags" in doc else "",
                  #   "ingredients_analysis": doc["ingredients_analysis"] if "ingredients_analysis" in doc else "",
                  #   "ingredients_text_with_allergens_en": doc["ingredients_text_with_allergens_en"] if "ingredients_text_with_allergens_en" in doc else "",
                  "product_name": doc["product_name"] if "product_name" in doc else "",
                  #   "ingredients": doc["ingredients"] if "ingredients" in doc else "",
                  #   "generic_name": doc["generic_name"] if "generic_name" in doc else "",
                  "brands": doc["brands"] if "brands" in doc else "",
                  "categories_tags": doc["categories_tags"] if "categories_tags" in doc else "",
                  #   "categories": doc["categories"] if "categories" in doc else "",
                  #   "manufacturing_places": doc["manufacturing_places"] if "manufacturing_places" in doc else "",
                  #   "origins": doc["origins"] if "origins" in doc else "",
                  #   "ingredients_analysis_tags": doc["ingredients_analysis_tags"] if "ingredients_analysis_tags" in doc else "",
                  #   "ingredients_original_tags": doc["ingredients_original_tags"] if "ingredients_original_tags" in doc else "",
                  "brands_tags": doc["brands_tags"] if "brands_tags" in doc else "",
                  "quantity": doc["quantity"] if "quantity" in doc else "",
                  }
                 for doc in product_list]
    # for doc in json_docs:
    #     response = openfoodfacts.products.get_product(doc["id"])
    #     response = openfoodfacts.products.get_product('8902080013869')
    #     import pdb
    #     pdb.set_trace()
    #     doc['images'] = response["product"]["selected_images"]

    return Response({'products': json_docs}, content_type='application/json')


@api_view(('POST',))
def get_images(request):
    image_url = []
    for id in request.data['ids']:
        response = openfoodfacts.products.get_product(id)
        image_url.append({'id': id, 'image': response["product"]["image_front_url"]})
    return Response({'response': image_url}, content_type='application/json')
