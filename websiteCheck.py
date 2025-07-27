# websiteCheck.py
# developed by raaz4n@github
# Description: This Python script will email te user once a website has been updated.
# This depends on how much of the website is written in JS, and if BeautifulSoup and requests
# can pick up the change.

''' smtplib and ssl will transmit delivery to a specified email. json and boto3 will be used in lambda_handler for AWS integration.
    requests, hashlib, and BeautifulSoup will get information from a URL and trip once a change occurs within the website. '''

import smtplib, ssl, json, boto3, requests, hashlib, os
from email.message import EmailMessage
from bs4 import BeautifulSoup

# This is the lambda handler that will be called when the AWS Lambda function is invoked.
# It will check the website for any updates and send an email if something has changed.
# It does this by comparing the current hash with the previous hash stored in an S3 bucket.
# For my own use, I schedule this to run every hour with AWS Lambda.
def lambda_handler(event, context):
    bucket = "hash-data-save"
    key = "test"
    newHash = web_hash(URL)

    s3 = boto3.client("s3", region_name="us-east-2")
    readS3 = s3.get_object(Key=key, Bucket=bucket)
    oldHash = readS3["Body"].read().decode("UTF-8")

    if oldHash != newHash:
        # Set up for the email subject & body.
            msg = EmailMessage()
            msg["Subject"] = "Website update"
            msg["From"] = from_email
            msg["To"] = to_email
            msg.set_content(message)

            send_mail(from_email, to_email, KEY, PORT, smtpMail, msg)
            s3.put_object(Bucket=bucket, Key=key, Body=(newHash).encode("UTF-8"))
    return{
        "statusCode": 200,
        "body": json.dumps("Website check completed successfully.")
    }

''' This function will get the raw HTML from the URL, and then hash it using SHA-256.
    It uses requests to get the content from the page, and then BeautifulSoup to get
    the text content. If the content is loaded with JS, the function won't work.
    In this case, using a library like Selenium or Playwright would be more appropriate. 
    If the page isn't found, it will return None and print an error message. '''
def web_hash(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        txt = soup.text
        encodedTxt = txt.encode()
        h = hashlib.sha256(encodedTxt)
        hashHex = h.hexdigest()
        return hashHex
    except requests.exceptions.HTTPError:
        print("Error. Page not found.")
        return None
    
# This function will send mail to the user.
def send_mail(fromMail, toMail, KEY, PORT, smtpMail, msg):
    serv = smtplib.SMTP(smtpMail, PORT)
    serv.starttls()
    serv.login(fromMail, KEY)
    serv.send_message(msg)
    serv.quit()

# This is the email that will be used to send emails with.
# You should probably use a throwaway email, as sensitive information will be accessed.
from_email = os.environ["FROM_EMAIL"]

# This is the email that will receive the message that the website has been updated.
to_email = os.environ["TO_EMAIL"]

# I will be using an environment variable to store the email key.
# This is the app password that will be used to authenticate the email.
KEY = os.environ["EMAILKEY"]

# This is the URL the user would like to check.
URL = os.environ["URL"]

# I will be using a gmail email, with the port being 587.
PORT = 587
smtpMail = "smtp.gmail.com"
message = f"{URL} has been updated!"