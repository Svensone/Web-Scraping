import scrapy

class PostsSpider(scrapy.Spider):

    name = "posts"

    start_urls = [
        'https://blog.scrapinghub.com/'
        # possible to go through sitemap without manually hardcode every url like below
        # 'https://blog.scrapinghub.com/page/1/',
        # 'https://blog.scrapinghub.com/page/2/',
    ]

    def parse(self, response):
     # step 2: loop through all posts
        for post in response.css('div.post-item'):
            yield {
                'title': post.css('.post-header h2 a::text')[0].get(),
                'date': post.css('.post-header a::text')[1].get(),
                'author': post.css('.post-header a::text')[2].get()
            }
        # step 1;
        # page = response.url.split("/")[-1] # only take the page numer
        # filename = 'posts-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        #step 3: add next page functionality 
        # get the Node with link for 'next page'
        # next_page = response.css('a.next-posts-link::attr(href)').get()
        # # check if next page available
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     # start from top (beginning of parse func.) again
        #     yield scrapy.Request(next_page, callback=self.parse)

        next_page = response.css('a.next-posts-link::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)