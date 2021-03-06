import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
import sys
from datetime import datetime
import os


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
    scriptDir = Path(os.path.realpath(__file__)).parent
    with open(scriptDir / 'user.name', 'r') as f:
        userName = f.readline()
    with open(scriptDir / 'user.pass', 'r') as f:
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


def get_stories():
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

    return article_urls


class Issue():
    def __init__(self, url):
        self.url = url


    def read(self):
        page = s.get(self.url)

        soup = BeautifulSoup(page.content, "html.parser")
        
        #title = soup.find_all('h1')[1].find('div').get_text()
        #pubDate = soup.find_all('div', class_='field field--name-name field--type-string field--label-hidden field__item')

        result =soup.find('div', class_='article-publication-date').get_text().strip()
        x = re.search(r'[a-zA-Z]+ [0-9]{4}', result)
        self.pubDate = x.group()

        result = result[x.end():].strip()
        self.title = x = re.search(r'[a-zA-Z0-9][a-zA-Z0-9 ]+[^\n]', result).group()

    def write(self, fn):
        with open(fn, 'w') as f:
            f.write('# ' + self.title + '  \n' + self.pubDate)


class Story():
    def __init__(self, url):
        self.url = url

    def read(self):
        page = s.get(self.url)

        soup = BeautifulSoup(page.content, "html.parser")

        # get article title
        self.title = soup.find('h1').get_text().strip()

        # get article author
        x = soup.find('div', class_='article-author').get_text()
        self.author = x[x.find('By:') + 4:x.find('|')].strip() + ' | ' + x[x.find('|') + 1:].strip()

        # subtitle
        self.subtitle = soup.find('div', class_='article-subtitle').get_text().strip()
        
        # parse article body
        body_raw = soup.find_all(class_='clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item')[2].find_all('p')
        self.body = ''
        for i, p in enumerate(body_raw):
            if i > 0:
                self.body += '  \n\n' + p.get_text().strip()
            else:
                self.body += p.get_text().strip()
    

    def write(self, outputFile):
        with open(outputFile, 'w') as f:
            f.write('# ' + self.title + '  \n' + self.author + '  \n' + self.subtitle + '  \n\n' + self.body)


def main():
    # options
    outDir = Path('/home/kdcadet/nc/aa/grapevine')
    if not outDir.exists():
        outDir = Path(os.path.realpath(__file__)).parent / 'output'

    # http session
    try:
        global s
        s = login()

        storyURLs = get_stories()

        # issueTitle, pubDate = read_issue(s, storyURLs[0])
        issue = Issue(storyURLs[0])
        issue.read()
        outDir = outDir / (datetime.strptime(issue.pubDate, '%B %Y').strftime('%Y%m') + '-' + issue.title.replace(' ', '_'))
        # if already exists, exit and don't continue
        if outDir.exists():
            print(f'The current issue is already at {outDir}.')
        else:
            outDir.mkdir(parents=True, exist_ok=True)
            issue.write(outDir / 'readme.md')

            for i, url in enumerate(storyURLs):
                story = Story(url)
                story.read()
                fn = str(i).zfill(2) + '-' + story.title.replace(' ', '_') + '.md'
                story.write(outDir / fn)

            print(f'Finished downloading the {issue.pubDate} issue to {outDir}')

    finally:
        print('Closing session.')
        s.close()


if __name__ == '__main__':
    main()
