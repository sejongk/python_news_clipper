import requests
from bs4 import BeautifulSoup


link_dict ={
        'security': 'https://news.naver.com/main/list.nhn?mode=LS2D&sid2=732&sid1=105&mid=shm&date=20210623&page=1',
        'it-general': 'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230',
        'internet': 'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=226'
    }

def get_news_summary_and_date(news_url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

    req = requests.get(news_url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')

    date = soup.find('span', {'class': 't11'}).text
    try:
        summary = soup.find('strong', {'class':'media_end_summary'}).get_text(separator=', ')
    except AttributeError:
        summary = "요약 없음"

    return summary, date

def get_news_list_with_category(category): 
    news_url = link_dict[category]
    news_list = []

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    req = requests.get(news_url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    
    table = soup.find('div', {'class':'list_body newsflash_body'})
    li_list = table.find_all('li')

    for li in li_list:
        try:
            news = {
                'title': li.find('img').get('alt'),
                'img': li.find('img').get('src'),
                'link': li.find('a').get('href')
            }
            news['summary'], news['date'] = get_news_summary_and_date(news['link'])
            news_list.append(news)
        except AttributeError:
            continue

    return news_list