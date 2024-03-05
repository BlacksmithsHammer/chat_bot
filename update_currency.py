import json
import requests
import time

def updade_course():
    
    while True:
        with open("exchange rate.json", "w", encoding="utf-8") as file:
            data = json.loads(requests.get("https://www.cbr-xml-daily.ru/daily_json.js").text)
            json.dump(data, file)
        
        time.sleep(60)
        
if __name__ == "__main__":
    updade_course()