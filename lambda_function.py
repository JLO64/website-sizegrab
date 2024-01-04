from website_sizegrab import calculate_website_size_data
import json

def lambda_handler(event, context):
    try: 
        return calculate_website_size_data(event["queryStringParameters"]["website-to-test"])
    except:
        return "error"