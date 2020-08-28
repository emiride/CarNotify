import requests
from lxml import html
import helper_methods
import smtplib
import os
from car_model import CarModel
from typing import List

url = "https://www.olx.ba/pretraga?kategorija=30&id=2&stanje=0&vrstapregleda=grid&sort_order=desc&kanton=9&grad%5B%5D=3879&grad%5B%5D=3812&grad%5B%5D=3969&grad%5B%5D=5896&grad%5B%5D=4048&grad%5B%5D=4126&stranica="

def main():
    current_cars: List[CarModel] = helper_methods.get_current_cars()
    new_cars: List[CarModel] = []
    for i in range(helper_methods.get_number_of_pages(url)):
        new_cars.extend(helper_methods.get_cars(url + str(i+1)))

    deleted_cars_to_mail = []
    new_cars_to_mail = []
    changed_cars_price_to_mail = []

    temp_list = current_cars.copy()
    for current_car in temp_list:
        for new_car in new_cars:
            if current_car == new_car:
                if current_car.price != new_car.price:
                    changed_cars_price_to_mail.append([current_car, new_car.price])
                    current_cars.remove(current_car)
                    current_cars.append(new_car)

    temp_list = current_cars.copy()
    for current_car in temp_list:
        if current_car not in new_cars:
            deleted_cars_to_mail.append(current_car)
            current_cars.remove(current_car)

    for new_car in new_cars:
        if new_car not in current_cars:
            new_cars_to_mail.append(new_car)
            current_cars.append(new_car)


    helper_methods.save_cars(current_cars)
    email_body = helper_methods.get_email_body(new_cars_to_mail, deleted_cars_to_mail, changed_cars_price_to_mail)
    if len(deleted_cars_to_mail) != 0 or len(new_cars_to_mail) != 0:
        helper_methods.send_gmail("emir.hodzex@gmail.com", "NajnovijaSifr@", ["emir.hodzich@gmail.com"], "OLX update", email_body)
    
if __name__ == '__main__':
    main()
    
