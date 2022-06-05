import requests
from bs4 import BeautifulSoup
import re

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

def login():
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

    return s


def get_articles(s):
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

    return s, article_urls


def read_issue(s, url):
    page = s.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    
    #title = soup.find_all('h1')[1].find('div').get_text()
    #pubDate = soup.find_all('div', class_='field field--name-name field--type-string field--label-hidden field__item')

    result =soup.find('div', class_='article-publication-date').get_text().strip()
    x = re.search(r'[a-zA-Z]+ [0-9]{4}', result)
    pubDate = x.group()

    result = result[x.end():].strip()
    title = x = re.search(r'[a-zA-Z0-9][a-zA-Z0-9 ]+[^\n]', result).group()

    return title, pubDate


def read_article(s, url):
    page = s.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    # get article title
    title = soup.find('h1').get_text().strip()

    # get article author
    print(soup.find('div', class_='article-author'))

    # parse article body
    results = soup.find_all(class_='clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item')

    body_raw = results[2].find_all('p')
    body = ''
    for p in body_raw:
        body += '  \n\n' + str(p)[15:-18]


def main():
    s = login()

    s, articleURLs = get_articles(s)

    title, pubDate = read_issue(s, articleURLs[0])


    for article_url in articleURLs[0:2]:
        read_article(s, article_url)

    s.close()


if __name__ == '__main__':
    main()
