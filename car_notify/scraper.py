import helper_methods
import os
from car_model import CarModel
from typing import List

url = "https://www.olx.ba/pretraga?kategorija=18&do=16000&godiste_min=2010&kilometra-a_max=200000&stranica="

def main():
    current_cars: List[CarModel] = helper_methods.get_current_cars()
    new_cars: List[CarModel] = []
    number_of_pages = helper_methods.get_number_of_pages(url)
    for i in range(number_of_pages):
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
        helper_methods.send_gmail(os.environ.get("SENDING_EMAIL"), os.environ.get("SENDING_EMAIL_PASSWORD"), [os.environ.get("RECEIVING_EMAIL")], "OLX update", email_body)
    
if __name__ == '__main__':
    main()
    
