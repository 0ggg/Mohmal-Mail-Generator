import requests, time
from bs4 import BeautifulSoup
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',}
response = requests.get('https://www.mohmal.com/ar/create/random', headers=headers)
cookies = response.cookies
mail = response.text.split('value="')[1].split('"')[0]
cok = cookies["connect.sid"]
cookies = {"connect.sid": cok}
response = requests.get('https://www.mohmal.com/ar/inbox', cookies=cookies, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
email_div = soup.find('div', class_='email')
print(f"Email : {email_div.get('data-email')}")
seen_ids = set()
while True:
    time.sleep(3)
    response = requests.get('https://www.mohmal.com/ar/inbox', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    msg = soup.find_all('tr', attrs={'data-msg-id': True})
    if not msg:
        print("No Messages")
        continue
    for m in msg:
        msg_id = m.get('data-msg-id')
        if msg_id in seen_ids:
            continue
        seen_ids.add(msg_id)
        print(f"Id : {msg_id}")
        msg_headers = {**headers, 'referer': 'https://www.mohmal.com/ar/inbox', 'sec-fetch-site': 'same-origin'}
        msg_response = requests.get(f'https://www.mohmal.com/ar/message/{msg_id}', cookies=cookies, headers=msg_headers)
        print(msg_response.text)
        exit()