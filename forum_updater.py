import time
import urllib

import bs4 as bs4
import requests

headers = {
    'authority': 'www.pathofexile.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'origin': 'https://www.pathofexile.com',
    'upgrade-insecure-requests': '1',
    'dnt': '1',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'referer': 'https://www.pathofexile.com/forum/edit-thread/2822110?history=1',
    'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,pl;q=0.5,sl;q=0.4',
    'cookie': '__cfduid=d4f8fd4272c7e2285694e6e615ab64cb71586376370; _ga=GA1.2.2084030156.1586505898; _gid=GA1.2.397570792.1586645386; stored_data=1; cf_clearance=f42d23711f26466c576dc10108f2223d0945ef0d-1586771863-0-150; POESESSID=8720d642a4621f9055fd918942e07959',
}


def update_forum(content,thread='2822110'):
    title='delerious bcuz corona'

    # headers["Cookie"]= f"POESESSID={ssid}"
    url =f'https://www.pathofexile.com/forum/edit-thread/{thread}?history=1'
    response = requests.get(url,headers=headers )
    time.sleep(1)
    soup = bs4.BeautifulSoup(response.content)
    hash = soup.find('input',{'name':'hash'})['value']
    data=dict(title=title,content=content,notify_owner='0',hash=hash,post_submit='submit')
    print(len(content))
    response = requests.post(url,headers=headers,data=urllib.parse.urlencode(data))
    print(response.status_code)
    print(url.replace('edit','view'))

    time.sleep(1)

    # response = requests.post(f'https://www.pathofexile.com/forum/view-thread/{thread}', headers=headers)
    # time.sleep(1)
    # assert content in response.text
if __name__ == '__main__':
    update_forum("nothing currently!")