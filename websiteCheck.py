# websiteCheck.py
# developed by raaz4n@github
''' smtplib will transmit delivery to a specified email.
    requests and BeautifulSoup will get information from
    a URL and trip once a change occurs within the website.'''

import smtplib, requests
from bs4 import BeautifulSoup

