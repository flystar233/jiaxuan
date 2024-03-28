from bs4 import BeautifulSoup
import requests
import csv


pages =154
result = open('cipai.csv','a',newline='',encoding='utf-8')
writer = csv.writer(result)
writer.writerow(['词牌名', '韵律'])

for page in range(1,pages):
    url = f'http://longyusheng.org/cipai/cipai{page}.html'
    response = requests.get(url)
    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1', class_='PageTitle').text

    # 找到韵律
    rhythm = []
    for div in soup.find_all('div', class_='ci'):
        for blockquote in div.find_all('blockquote'):
            # 直接获取blockquote标签的所有文本
            line = blockquote.get_text(separator='', strip=True)
            line = line.replace('（韵）', '')
            rhythm.append(line)
    writer.writerow([title, ' '.join(rhythm)])



    