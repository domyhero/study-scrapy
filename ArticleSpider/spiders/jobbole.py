# -*- coding: utf-8 -*-
import scrapy
import re
import datetime

from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    # start_urls = ['http://blog.jobbole.com/112238/']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")

            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": parse.urljoin(response.url, image_url)}, callback=self.parse_detail)
        #提取下一页并交给scrapy下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        # xpath 选取字段
        title = response.xpath("//div[@class='entry-header']/h1/text()").extract_first()
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].replace('·', '').strip()
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()

        vote_post_up = int(response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0])

        bookmark_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract_first()
        if bookmark_nums:
            match_re = re.match(".*(\d+).*", bookmark_nums)
            if match_re:
                bookmark = int(match_re.group(1))

        comment_nums = response.xpath("//a[@href='#article-comment']/text()").extract_first()
        if comment_nums:
            match_re = re.match(".*(\d+).*", comment_nums)
            if match_re:
                comment = int(match_re.group(1))

        # css 选取字段
        article_item = JobBoleArticleItem()
        article_item['title'] = title
        article_item['create_date'] = create_date
        article_item['front_image_url'] = [response.meta['front_image_url']]
        article_item['url'] = response.url
        article_item['url_object_id'] = get_md5(response.url)
        yield article_item

