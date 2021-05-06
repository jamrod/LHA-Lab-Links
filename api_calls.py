import requests
import json

from secrets import USER, PASSWORD, SHOP

base_url = f"https://{USER}:{PASSWORD}@{SHOP}.myshopify.com/admin/api/2021-01/"

def get_collections():
    """Return all collections for store"""
    url = f"{base_url}custom_collections.json"
    response = requests.get(
        url
    )
    return response.json()

def get_collection_products(id):
    """Return all products for given collection"""
    url = f"{base_url}collections/{id}/products.json?limit=250"
    response = requests.get(
        url
    )
    return response.json()

def get_smart_collections():
    """Return smart collections for store"""
    url = f"{base_url}smart_collections.json"
    response = requests.get(
        url
    )
    return response.json()

def get_product(id):
    """Return product by id"""
    url = f"{base_url}products/{id}.json"
    response = requests.get(
        url
    )
    return response.json()
