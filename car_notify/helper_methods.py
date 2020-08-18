import requests
from lxml import html
import math
import smtplib

def __get_number_of_results(url):
    r = requests.get(url+"1")
    tree = html.fromstring(r.text)
    num_of_results = tree.xpath(".//div[@class='brojrezultata']/span")[0]
    return int(num_of_results.text)

def get_number_of_pages(url):
    num_of_results = __get_number_of_results(url)
    return math.ceil(num_of_results/30)+1

def get_cars_urls(url):
    r = requests.get(url)
    tree = html.fromstring(r.text)
    titles = tree.xpath(".//div[@class='naslov']/a")
    car_urls = []
    for title in titles:
        car_urls.append(title.attrib.get("href"))
    return car_urls

def send_email(user, pwd, recipient, subject, body):
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.office365.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print("Successfully sent the mail")
    except Exception as e:
        print(f"Failed to send mail. Exception: {e}")

def get_email_body(new_urls_to_mail, deleted_urls_to_mail):
    new_line = '\n'
    return f"Nova auta po pretrazi:{new_line}{new_line.join(new_urls_to_mail)}{new_line}{new_line}Izbrisana auta po pretrazi:{new_line}{new_line.join(deleted_urls_to_mail)}"