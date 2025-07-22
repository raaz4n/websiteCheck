# websiteCheck.py
# developed by raaz4n@github
''' smtplib and ssl will transmit delivery to a specified email. json and boto3 will be used in lambda_handler for AWS integration.
    requests and hashlib will get information from a URL and trip once a change occurs within the website. '''

import smtplib, ssl, json, boto3, requests, hashlib

s3 = boto3.client("s3", region_name="us-east-2")
def lambda_handler(event, context):
    bucket = "hash-data-save"
    key = "test"
    return {
        'statusCode': 200,
    }

# This function will get the hash of the URL. It will crash if the page isn't found.
def web_hash(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        raw_web_data = response.content
        h = hashlib.sha256()
        h.update(raw_web_data)
        hashHex = h.hexdigest()
        return hashHex
    except requests.exceptions.HTTPError:
        print("Error. Page not found.")
        return None
    

# This is the email that will be used to send emails with.
# You should probably use a throwaway email, as sensitive information will be accessed.
from_email = "from@email.com"

# This is the email that will receive the message that the website has been updated.
to_email = "to@email.com"

'''For my own usage, I will be using a throwaway gmail account that uses an app password.
   You may tweak this to your liking, but I don't want to use the actual email password.
   You can use environment variables if you'd like to. '''
KEY = "apppassword"

# This is the URL the user would like to check.
URL = "https://test.com"