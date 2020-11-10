import time
from bs4 import BeautifulSoup
import urllib.request

server = 'http://www.hitsz.edu.cn'
target = 'http://www.hitsz.edu.cn/article/id-'
catalog = ['116', '80', '74', '75', '77', '78', '79.html?subjectId=23', '79.html?subjectId=22',
           '79.html?subjectId=12', '79.html?subjectId=21', '79.html?subjectId=10',
           '79.html?subjectId=9', '79.html?subjectId=15', '81', '124'
           ]


def get_text(titles, page_urls):
    with open('result.txt', 'a', encoding='utf-8') as result_file:
        urls_len = len(page_urls)
        for i in range(urls_len):
            print("%d/%d" % (i, urls_len))
            url_e = page_urls[i]
            # text = titles[i] + '\n'
            text = titles[i]
            try:
                req = urllib.request.urlopen(url_e)
            except Exception as e:
                print("%s: %s" % (type(e), url_e))

            req = req.read()
            bs = BeautifulSoup(req, 'html.parser')
            div = bs.find('div', class_='edittext')
            # bs_p = BeautifulSoup(str(div), 'html.parser')
            # p = bs_p.find_all('p')
            # for each_p in p:
            #     text = text + each_p.text + ' '
            text += div.get_text()
            # text += '\n'
            # writefile = open('news.txt', 'a', encoding='utf-8')
            result_file.write(text)
            # writefile.close()


def crawler(port, first_url, current_url):
    page_urls = []
    titles = []
    while True:
        # print(current_url)
        try:
            req = urllib.request.urlopen(current_url)
        except Exception as e:
            print("%s: %s" % (type(e), current_url))
        content_page = req.read()
        title_o = []

        content_bs = BeautifulSoup(content_page, 'html.parser')
        a_next = content_bs.find('a', class_='next')

        if port in ['80', '74', '78', '81']:
            label = content_bs.find_all(
                ['div', 'li'],
                class_=['lecture_top',
                        'first image_none top_item', 'image_none top_item', 'image_none'
                        ]
            )
            for each_label in label:
                bs = BeautifulSoup(str(each_label), 'html.parser')
                title_o.append(bs.find('a'))
        else:
            title_o = content_bs.find_all('a', class_='title_o')

        for each_title in title_o:  # 将标题和url加入链表，并写入文档
            titles.append(''.join(each_title.text.split()))
            page_urls.append(server + each_title.get('href'))
            # f.write(str(num) + '\t\t' + ''.join(each_title.text.split()) + '\t\t' + server + each_title.get(
            #     'href') + '\n')
            # num += 1

        if a_next is None:
            return titles, page_urls
        else:
            next_url = first_url + a_next.get('href')
            current_url = next_url


def main():
    for port in catalog:
        first_url = target + port + '.html'
        # content_urls.append(current_url)
        current_url = first_url
        titles, page_urls = crawler(port, first_url, current_url)
        get_text(titles, page_urls)
        time.sleep(5)


if __name__ == '__main__':
    main()
