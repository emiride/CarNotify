import requests
from lxml import html
import helper_methods
import smtplib
import os

url = "https://www.olx.ba/pretraga?kategorija=18&sort_order=desc&do=15100&godiste_min=2010&kilometra-a_max=131000&gorivo_select_benzin=Benzin&gorivo_select_plin=Plin&stranica="

def main():
    with open("urls.txt", 'r') as file: current_urls = file.read().splitlines()
    new_urls = []

    for i in range(helper_methods.get_number_of_pages(url)):
        new_urls.extend(helper_methods.get_cars_urls(url + str(i+1)))

    deleted_urls_to_mail = []
    new_urls_to_mail = []
    for value in current_urls:
        if value not in new_urls:
            current_urls.remove(value)
            deleted_urls_to_mail.append(value)

    for value in new_urls:
        if value not in current_urls:
            current_urls.append(value)
            new_urls_to_mail.append(value)

    with open("urls.txt", 'w') as file: file.write('\n'.join(current_urls))
    email_body = helper_methods.get_email_body(new_urls_to_mail, deleted_urls_to_mail)
    pwd = os.environ["OUTLOOK_PWD"]
    if len(deleted_urls_to_mail) != 0 or len(new_urls_to_mail) != 0:
        helper_methods.send_email("emir.hodzic@outlook.com", pwd, "emir.hodzich@gmail.com", "OLX update", email_body)
    
if __name__ == '__main__':
    main()
    
