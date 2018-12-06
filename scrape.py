import requests

import scrapy
from scrapy.http.request import Request
from bs4 import BeautifulSoup


class GutenbergDESpider(scrapy.Spider):
    name = "books"

    def start_requests(self):
        MAX_NO_RESULT = 100
        no_result = 0

        i = getattr(self, 'start_id', 0)
        end_id = getattr(self, 'start_id', None)

        while True and (end_id is None or i <= end_id) and no_result < MAX_NO_RESULT:
            r = requests.get(
                f"http://gutenberg.spiegel.de/buch/{i}/1")
            book_after_redirect = r.url.split('/')[-2]
            if book_after_redirect == f'x-{i}':
                no_result += 1
            else:
                no_result = 0
                yield Request(r.url, self.parse)
            i += 1

    def parse(self, response):
        # http://gutenberg.spiegel.de/buch/uber-die-grundfrage-des-pessimismus-in-methodischer-hinsicht-12/1
        url_parts = response.url.split('/')

        chapter = int(url_parts[-1])

        soup = BeautifulSoup(response.css('div#gutenb').extract_first())
        text = soup.get_text().strip()

        meta = {}

        for tr in response.css('div#metadata tr'):
            tds = tr.css('td *::text').extract()
            if len(tds) == 2:
                meta[tds[0]] = tds[1]

        yield {
            'chapter': chapter,
            'text': text,
            'meta': meta,
        }

        links = response.css('a')

        for l in links:
            href = l.xpath('@href').extract_first()
            if href is None:
                continue
            link_parts = href.split('/')

            if len(link_parts) >= 2 and link_parts[-2] == url_parts[-2] and int(link_parts[-1]) == chapter + 1:
                yield response.follow(l, self.parse)


# just for debugging
if __name__ == "__main__":

    s = GutenbergDESpider()
    for x in s.start_requests():
        print(x)
