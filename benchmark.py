import time
from bs4 import BeautifulSoup, SoupStrainer

doc = b"<html>" + b"<div>hello world</div>" * 1000 + b"<div class='campreview' data-cam-preview-server-id-value='123'></div>" + b"</html>"

start = time.time()
for _ in range(100):
    soup = BeautifulSoup(doc, 'html.parser')
    params = soup.find(class_='campreview')
print("html.parser:", time.time() - start)

start = time.time()
for _ in range(100):
    soup = BeautifulSoup(doc, 'lxml')
    params = soup.find(class_='campreview')
print("lxml:", time.time() - start)

start = time.time()
strainer = SoupStrainer(class_='campreview')
for _ in range(100):
    soup = BeautifulSoup(doc, 'html.parser', parse_only=strainer)
    params = soup.find(class_='campreview')
print("html.parser with SoupStrainer:", time.time() - start)

start = time.time()
for _ in range(100):
    soup = BeautifulSoup(doc, 'lxml', parse_only=strainer)
    params = soup.find(class_='campreview')
print("lxml with SoupStrainer:", time.time() - start)
