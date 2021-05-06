import json
from api_calls import *
from secrets import COLLECTION, BUCKET
from s3_upload import update_file_on_s3

def log_collections():
    normal = get_collections()
    if "errors" in normal:
        print("Errors: ", normal.get("errors"))
        return
    smart = get_smart_collections()
    if "errors" in smart:
        print("Errors: ", smart.get("errors"))
        return
    data = normal.copy()
    data.update(smart)
    return json.dumps(data)

def create_course_links_file(col):
    data = get_collection_products(col)
    if "errors" in data:
        print("Errors: ", data.get("errors"))
        return False
    course_links = {}
    for course in data.get("products"):
        course_links[course["title"]] = str(course["handle"])
    return json.dumps(course_links) 
    
def get_and_upload_course_links(col, bucket, filename):
    json_data = create_course_links_file(col)
    if json_data:
        response = update_file_on_s3(bucket, filename, json_data)
        return json.dumps(response)
    return "No Data"

if __name__ == "__main__":
    # execute only if run as a script
    print(get_and_upload_course_links(COLLECTION, BUCKET, 'addresses.json'))