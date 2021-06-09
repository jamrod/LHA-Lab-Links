import json
import boto3 
import botocore 
import os
import requests

USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']
SHOP = os.environ['SHOP']
COLLECTION = os.environ['COLLECTION']
BUCKET = os.environ['BUCKET']
CODEWORD = os.environ['CODEWORD']

def lambda_handler(event, context):
    # retrive course list from Shopify and update links for Thinkific in s3
    print("Received Event " + json.dumps(event))
    if CODEWORD in event:
        response = get_and_upload_course_links(COLLECTION, BUCKET, 'addresses.json')
        if response:
            print(response)
            return {
                'statusCode': 200,
                'body': json.dumps('Success!')
            }
        return {
            'statusCode': 500,
            'body': json.dumps('Errors occured, check the logs!')
        }
    print('Wrong Codeword')
    return {
        'statusCode': 401,
        'body': json.dumps('Wrong Codeword!')
    }

def get_collection_products(id):
    """Return all products for given collection from shopify admin API"""
    base_url = f"https://{USER}:{PASSWORD}@{SHOP}.myshopify.com/admin/api/2021-01/"
    url = f"{base_url}collections/{id}/products.json?limit=250"
    response = requests.get(
        url
    )
    return response.json()

def create_course_links_file(col):
    """calls get_collection_products on thinkific courses collection then returns a dictionary of course names with links to their respective product pages """
    data = get_collection_products(col)
    if "errors" in data:
        print("Errors: ", data.get("errors"))
        return False
    course_links = {}
    for course in data.get("products"):
        course_links[course["title"]] = str(course["handle"])
    return json.dumps(course_links)

def update_file_on_s3(bucket, filename, json_data):
    """upload json data to file on s3"""
    s3 = boto3.client('s3')

    try:
        response = s3.put_object(
            Body=(bytes(json_data.encode('UTF-8'))),
            Bucket=bucket,
            Key=filename
        )

    except botocore.exceptions.ClientError as error:
        print(error)
        response = "Client error occured"
    except botocore.exceptions.ParamValidationError as error:
        print(error)
        response = 'The parameters you provided are incorrect: {}'.format(error)

    return response
    
def get_and_upload_course_links(col, bucket, filename):
    json_data = create_course_links_file(col)
    if json_data:
        response = update_file_on_s3(bucket, filename, json_data)
        return json.dumps(response)
    return False