import scrapy


class JogostabuleiroSpider(scrapy.Spider):
    name = "jogostabuleiro"
    start_urls = ["https://boardgamegeek.com/browse/boardgame/page/1"]

    def parse(self, response):
        for jogo in response.css('#row_'):
            yield{
                'rank': jogo.css('.collection_rank a::attr(name)').get(),
                'nome': jogo.css('.primary::text').get(),
                'nota': jogo.css('#row_ .collection_bggrating:nth-child(5)::text').get().split()[0],
            }

        if response.url == "https://boardgamegeek.com/browse/boardgame/page/1":
            next_page_xpath = '//*[@id="maincontent"]/p/a[5]'
        else:
            next_page_xpath = '//*[@id="maincontent"]/p/a[7]'

        next_page = response.xpath(next_page_xpath).attrib['href']

        if next_page is not None: 
            yield response.follow(next_page, callback=self.parse)