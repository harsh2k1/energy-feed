import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksCrawlSpider(CrawlSpider):
    name = 'books_crawl'
    # allowed_domains = ['books.toscrape.com']
    start_urls = ['https://www.reuters.com/site-search/?query=renewable+energy&offset=0']

    le_book_details = LinkExtractor(restrict_css='div.media-story-card__body__3tRWy a')
    print(le_book_details)
    le_next = LinkExtractor(restrict_css='div.search-results__pagination__2h60k > button:nth-child(3) > span > svg')  # next_button
    # le_cats = LinkExtractor(restrict_css='.side_categories > ul > li > ul > li a')  # Categories

    rule_book_details = Rule(le_book_details, callback='parse_item')
    rule_next = Rule(le_next, follow=True)
    # rule_cats = Rule(le_cats, follow=True)

    rules = (
        rule_book_details,
        rule_next
        # rule_cats
    )

    def parse_item(self, response):
        yield {
            'Title': response.css('h1 ::text').get(),
            # 'Category': response.css('div.text__text__1FZLe.text__dark-grey__3Ml43.text__medium__1kbOh.text__small__1kGq2.article-header__author__3PcB3 ::text').get(),
            # 'Link': response.url
        }