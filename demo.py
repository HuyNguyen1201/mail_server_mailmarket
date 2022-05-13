import pickle
# read scrapper
with open(f'./scrappers/26.pickle','rb') as f:
    scraper = pickle.load(f)
response = scraper.post("https://web2.temp-mail.org/mailbox")
data = response.json()
token = data['token']
print(data)