from bs4 import BeautifulSoup
import requests
import re
import csv

pages = 154
result = open('cipai.csv', 'a', newline='', encoding='utf-8')
writer = csv.writer(result)
writer.writerow(['词牌名', '韵律'])

for page in range(1, pages):
    print(f"正在处理第{page}页...")
    url = f'http://longyusheng.org/cipai/cipai{page}.html'
    response = requests.get(url)
    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1', class_='PageTitle').text

    for item in soup.find_all(class_="ItemTitle"):
        if "定格" in item.get_text() or  "格一" in item.get_text():
            next_block = item.find_next_sibling()
            while next_block and (next_block.name == "br" or (next_block.string and next_block.string.strip() == "")):
                next_block = next_block.find_next_sibling()
            if next_block:
                content = next_block.get_text(separator=" ", strip=True)
                content = re.sub(r"（韵）", "", content)
                content_one_line = re.sub(r"\s+", "", content)
                writer.writerow([title, content_one_line])  # 直接写入一行内容

result.close()