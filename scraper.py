import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Origin': 'https://www.aagrapevine.org',
    'Connection': 'keep-alive',
    'Referer': 'https://www.aagrapevine.org/user/login',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

with open('user.name', 'r') as f:
    userName = f.readline()
with open('user.pass', 'r') as f:
    userPass = f.readline()

data = {
    'name': userName,
    'pass': userPass,
    'form_build_id': 'form-3LnHtbxBJ2X1VWbuUQHTQ4qv2y3WEkBr4V0ywmhGmQ0',
    'form_id': 'user_login_form',
    'op': 'Log in',
}

s = requests.session()
response = s.post('https://www.aagrapevine.org/user/login', headers=headers, data=data)


page = s.get('https://www.aagrapevine.org/magazine')#, cookies=cookies, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all(class_='read-more')

article_urls = []
for i in results:
    article_url = str(i)
    i0 = article_url.find('<a href="')
    article_url = article_url[i0+9:]
    i1 = article_url.find('">Read<')
    article_url = article_url[:i1]
    article_urls.append(article_url)

#print(article_urls)

# find the issue date
result = soup.find(class_='field field--name-name field--type-string field--label-hidden field__item')



for article_url in article_urls:
    article_page = s.get(article_url)

    soup = BeautifulSoup(article_page.content, "html.parser")

    results = soup.find_all(class_='clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item')

    for element in results:
        element_results = element.find_all('p')
        print(len(element_results))
    print('_' * 50)
s.close()
