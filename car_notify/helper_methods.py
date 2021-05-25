import requests
from lxml import html
import math
import smtplib
from car_model import CarModel
from typing import List

def __get_number_of_results(url):
    r = requests.get(url+"1")
    tree = html.fromstring(r.text)
    num_of_results = tree.xpath(".//div[@class='brojrezultata']/span")[0]
    return int(num_of_results.text)

def get_number_of_pages(url):
    num_of_results = __get_number_of_results(url)
    return math.ceil(num_of_results/30)+1

def get_current_cars() -> List[CarModel]:
    current_cars: List[CarModel] = []
    with open("urls.txt", 'r') as file: 
        temp_list = file.read().splitlines()
    for elem in temp_list:
        url = elem.split(",")[0].strip()
        price = elem.split(",")[1].strip()
        current_cars.append(CarModel(url, price))
    return current_cars

def get_cars(url) -> List[CarModel]:
    r = requests.get(url)
    tree = html.fromstring(r.text)
    cars = tree.xpath(".//div[contains(@class,'imaHover')]")
    cars_list: List[CarModel] = []
    for car in cars:
        car_url: str = car.xpath(".//div[@class='naslov']/a")[0].attrib.get("href")
        price: str = car.xpath(".//div[@class='datum']/span[1]/text()[1]")[0].strip()
        cars_list.append(CarModel(car_url, price))
    return cars_list

def save_cars(current_cars: List[CarModel]):
    with open("urls.txt", 'w') as file: 
        file.write('\n'.join(f"{car.url}, {car.price}" for car in current_cars))

def send_yandex(user, pwd, recipient, subject, body):
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP_SSL("smtp.yandex.com", 465)
        server.ehlo()
        server.login(user, pwd)
        print("I fail!!!!!!!!!!!")
        server.sendmail(FROM, TO, message)
        server.close()
        print("Successfully sent the mail") 
    except Exception as e:
        print(f"Failed to send mail. Exception: {e}")

def send_gmail(user, pwd, recipient, subject, body):
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print("Successfully sent the mail") 
    except Exception as e:
        print(f"Failed to send mail. Exception: {e}")

def get_email_body(new_cars_to_mail, deleted_cars_to_mail, changed_cars_price_to_mail):
    new_urls_text = ""
    deleted_urls_text = ""
    changed_cars_price_text = ""
    if len(new_cars_to_mail) > 0:
        new_urls_text = "Nova auta:\n\n" + "\n".join(car.url for car in new_cars_to_mail) + "\n\n"
    if len(deleted_cars_to_mail) > 0:
        deleted_urls_text = "Izbrisana auta:\n\n" + "\n".join(car.url for car in deleted_cars_to_mail) + "\n\n"
    if len(changed_cars_price_to_mail) > 0:
        changed_cars_price_text = "Auta sa izmjenjenom cijenom:\n\n" + "\n".join(f"{car[0].url} | {car[0].price} -> {car[1]}" for car in changed_cars_price_to_mail)
    return f"{new_urls_text}{deleted_urls_text}{changed_cars_price_text}"