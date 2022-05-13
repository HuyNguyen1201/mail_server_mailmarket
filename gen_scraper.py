import cloudscraper
import pickle


for i in range(400):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.post("https://web2.temp-mail.org/mailbox")
        data = response.json()
        if 'token' in data.keys():
            with open(f"./scrappers/{i}.pickle", 'wb') as f:
                pickle.dump(scraper,f)
    except:
        pass