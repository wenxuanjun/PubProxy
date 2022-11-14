from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import time
import os

ip, port, result = [], [], []
pages = int(input("请输入需要获取的页数："))

def run(key):
    host='http://' + ip[key] + ':' + port[key]
    proxy={'http': host,  'https': host}
    try:
        get = requests.get('http://account.microsoft.com', proxies=proxy, timeout=5)
        sec = get.elapsed.total_seconds()
    except:
        pass
    else:
        if get.status_code == 200:
            result.append({'ip': ip[key], 'port': port[key], 'time': sec})

def reduce(data):
    new, val = [], []
    for item in data:
        if item['ip'] not in val:
            new.append(item)
            val.append(item['ip'])
    return new

with tqdm(range(1, pages + 1)) as pbar:
    for page in pbar:
        pbar.set_description('Fetching page')
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
        src = requests.get('https://www.kuaidaili.com/free/intr/' + str(page), headers=headers).text
        html = BeautifulSoup(src, 'html5lib')
        for item in html.find('tbody').find_all('tr'):
            ip.append(item.find('td', attrs={'data-title':'IP'}).string)
            port.append(item.find('td', attrs={'data-title':'PORT'}).string)
        time.sleep(0.8)

os.system("clear")
with ThreadPoolExecutor(len(ip)) as pool:
    with tqdm(range(1,  len(ip) + 1)) as pbar:
        tasks = []
        for key in range(len(ip)):
            pbar.set_description('Testing proxies')
            task = pool.submit(run, key)
            task.add_done_callback(lambda p: pbar.update())
            tasks.append(task)
        wait(tasks, return_when=ALL_COMPLETED)
        pool.shutdown()

os.system("clear")
for item in sorted(reduce(result),  key=lambda val: val['time']):
    print(f"Ip: {item['ip']}  Port: {item['port']}  Time: {round(item['time']*1000,  2)}ms")
