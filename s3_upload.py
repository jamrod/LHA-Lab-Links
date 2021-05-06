import json
import boto3 
import botocore  


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