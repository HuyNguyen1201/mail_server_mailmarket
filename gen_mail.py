from email import message
from operator import index
import requests
import cloudscraper
import pickle
import os
from bs4 import BeautifulSoup

# init scraper list
scraper_list = []
for _, _, filenames in os.walk('./scrappers'):
    break
for name in filenames:
    with open('./scrappers/' + name, 'rb') as f:
        scraper = pickle.load(f)
        scraper_list.append(scraper)

index_scraper = 0


def get_scraper():
    return cloudscraper.create_scraper()
    global index_scraper, scraper_list
    index_scraper += 1
    if index_scraper >= len(scraper_list):
        index_scraper = 0
    return scraper_list[index_scraper]


def gen_mail():
    while True:
        try:
            scraper = get_scraper()
            response = scraper.post("https://web2.temp-mail.org/mailbox")
            data = response.json()
            if 'token' in data.keys():
                print(data['mailbox'], 'created succesfully')
                return data['mailbox'], data['token']
        except:
            pass
# def get_code(token):
#     scraper = get_scraper()
#     url = "https://web2.temp-mail.org/messages"
#     headers = {
#         'Authorization': token
#     }
#     response = scraper.get(url, headers=headers)
#     if len(response.json()['messages']) == 0:
#         return -1
#     else:
#         messages = []
#         for mess in response.json()['messages']:
#             id = mess['_id']
#             headers = {
#                 'Authorization': token
#             }
#             url = 'https://web2.temp-mail.org/messages/' + id
#             r = scraper.get(url, headers=headers)
#             temp = dict()
#             temp['from'] = r.json()['from']
#             temp['subject'] = r.json()['subject']
#             temp['receivedAt'] = r.json()['receivedAt']
#             temp['body'] = r.json()['bodyHtml']
#             messages.append(temp)
#         return messages


def get_code(token):
    scraper = get_scraper()
    url = "https://web2.temp-mail.org/messages"
    headers = {
        'Authorization': token
    }
    response = scraper.get(url, headers=headers)
    if len(response.json()['messages']) == 0:
        return -1
    else:
        for mess in response.json()['messages'][::-1]:
            id = mess['_id']
            headers = {
                'Authorization': token
            }
            url = 'https://web2.temp-mail.org/messages/' + id
            r = scraper.get(url, headers=headers)
            # get code in subject
            subject_list = r.json()['subject'].split(' ')
            for sub in subject_list:
                if sub.isnumeric() and len(sub) >= 3:
                    return sub
            soup = BeautifulSoup(r.json()['bodyHtml'], features="html.parser")
            text = soup.get_text()
            if 'confirmation code in the app:' in text:
                index = text.index('confirmation code in the app:') + 29
                code = text[index: index + 5]
                return code
            for t in text.replace('.', ' ').split(' '):
                if t.isnumeric() and len(t) > 4:
                    return t
    return -1


def read_mail(mail_dict, mail):
    value = mail_dict[mail]
    token = value[1]
    code = get_code(token)
    if code == -1:
        return 201, 'havent received any messages yet'
    if code == 0:
        return 201, 'message doesnt contain any code'
    if code != value[2]:
        value[3] += 1
        value[2] = code
    # if len(code) >3:
    #     del mail_dict[mail]
    return 200, code
