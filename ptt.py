import requests
from bs4 import BeautifulSoup

url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
cookies = {'over18': '1'}
resp = requests.get(url, cookies=cookies)
soup = BeautifulSoup(resp.text, 'html.parser')
arts = soup.find_all('div', class_='r-ent')

for art in arts:
    title_element = art.find('div', class_='title')
    link_element = art.find('div', class_='title').a
    author_element = art.find('div', class_='author')
    
    if title_element and link_element and author_element:
        title = title_element.getText().strip()
        link = 'https://www.ptt.cc' + link_element['href'].strip()
        author = author_element.getText().strip()
        
        print(f'title: {title}\nlink: {link}\nauthor: {author}\n')