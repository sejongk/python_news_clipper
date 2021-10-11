import os
import time
import traceback

import news
import mail


def news_to_html(news):
    news_html = '''
                    <tr>
                        <td rowspan="2" style="border-bottom: 1px solid #444444;padding: 10px;"><img src="{}"></td>
                        <td><h3>{}</h3>{}</td>
                    </tr>
                    <tr>
                        <td style="border-bottom: 1px solid #444444;padding: 10px;">
                            <p>{}</p>
                            <a href="{}">더 읽기</a>
                        </td>
                    </tr>
                '''.format(news['img'], news['title'], news['date'], news['summary'], news['link'])
    return news_html


def main():
    while True:
        try:
            news_list = news.get_news_list_with_category('internet')
            news_html = []
            for _news in news_list:
                news_html.append(news_to_html(_news))
            mail.send_mail(mail.create_mail_content(''.join(news_html)))
            sent_time = time.strftime('%Y-%m-%d,%H:%M:%S', time.localtime(time.time()))
            print("Daily news clippings are sent at {}.".format(sent_time), flush=True)
        except KeyboardInterrupt:
            break
        except Exception as e:
            traceback.print_exc()
        finally:
            time.sleep(int(os.environ['MAIL_INTERVAL_MIN']) * 60)


if __name__ == '__main__':
    main()