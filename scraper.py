import requests
from bs4 import BeautifulSoup

cookies = {
    'SSESS4cae9a55eb3358ae812f45d860b25d2f': 'bYVNfjhKylR1obHpnmylePX%2C58V%2C5dXBg57zkVCmaYdTexwF',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept': 'image/webp,*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Referer': 'https://www.aagrapevine.org/magazine',
    # 'Cookie': 'SSESS4cae9a55eb3358ae812f45d860b25d2f=bYVNfjhKylR1obHpnmylePX%2C58V%2C5dXBg57zkVCmaYdTexwF',
    'Sec-Fetch-Dest': 'image',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin',
    'Cache-Control': 'max-age=0',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

page = requests.get('https://www.aagrapevine.org/magazine', cookies=cookies, headers=headers)

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



article_page = requests.get(article_urls[0], cookies=cookies, headers=headers)

soup = BeautifulSoup(article_page.content, "html.parser")

results = soup.find_all(class_='clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item')

print(results[0])
