import requests
from bs4 import BeautifulSoup
import re
import csv
import _thread
import time
User_Agent = 'Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11'
headers = {
    'User-Agent': User_Agent,
}
# ��ȡÿһҳ�����е�Ӱ��������
def get_new_movie(page):
    r = requests.get(url="https://www.ygdy8.com/html/gndy/dyzz/list_23_{}.html".format(page), headers=headers) 
    
    r.encoding = 'gb2312' #��Ϊ����վ�ı�����gb2312����������������Ҫ����һ�±��룬����ᱨ��
    html = r.text
    name_list = [] # ����װ��ȡ���ĵ�Ӱ����
    download_list = [] # ����װ��ȡ���ĵ�Ӱ��������
    bs = BeautifulSoup(html, "html.parser") # ��BeautifulSoup����html����
    b = bs.findAll(class_="co_content8")
    b = b[0].findAll(class_="ulink") # �˴��õ���ÿһҳ�еĵ�Ӱ�б�
    for i in range(0, len(b)):
        name = b[i].get_text() # ��ȡÿ����Ӱ������
        href = "https://www.ygdy8.com/"+b[i].get("href") # ��ȡÿ����Ӱ������ҳ���url
        print(b[i].get_text())
        r1 = requests.get(url=href,headers=headers) # ����ÿ����Ӱ������ҳ��
        r1.encoding = 'gb2312'
        html1 = r1.text
        bs1 = BeautifulSoup(html1, "html.parser")
        b1 = bs1.find("tbody").find_next("td").find_next("a")
        download_url = b1.get("href") # ��ȡ����������
        print(download_url)
        name_list.append(name)
        download_list.append(download_url)
    return name_list,download_list


def get_total_page(url):
    r = requests.get(url=url,headers=headers)
    r.encoding = 'gb2312'

    pattern = re.compile(r'(?<=ҳ/)\d+') # re����
    t = pattern.findall(r.text)

    return int(t[0])


def wirte_into_csv(name,down_url):
    f = open('���µ�Ӱ.csv', 'a+', encoding='utf-8') # a+��ʾ׷��
    csv_writer = csv.writer(f)
    csv_writer.writerow([name,down_url])
    f.close()

def run(start_page, end_page):
    for p in range(start_page, end_page):
        name_list, down_list = get_new_movie(p)
        for i in range(0, len(name_list)):
            wirte_into_csv(name_list[i],down_list[i])
        time.sleep(3)

if __name__ == '__main__':

    # get_new_movie()
    total_page = get_total_page("https://www.ygdy8.com/html/gndy/oumei/list_7_1.html")
    total_page = int(total_page/25+1)
    end = int(total_page/4)
    print(end)
    # �����ĸ��̣߳��������������
    try:
        _thread.start_new_thread(run, (1, end))
        _thread.start_new_thread(run, (end+1, end*2))
        _thread.start_new_thread(run, (end*2 + 1, end * 3))
        _thread.start_new_thread(run, (end*3 + 1, end * 4))
    except:
        print("Error: �޷������߳�")

    while(1):
        pass