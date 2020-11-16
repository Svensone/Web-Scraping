Notes 

https://www.youtube.com/watch?v=ALizgnSFTwQ&ab_channel=TraversyMedia

2020.11.16
scrapy shell "url"
response.css('h3::text)[3].get()    # .getall() also possible

css('.post-header a::text').get()   # only the link text of post-header
response.css('p::text').re(r's\w+') # all paragraph text with reg. expression s plus world

REg Exp r'(w\+) you (w\+)' # all the words with 'you' in the middle

XPath = language to get notes in XML documents
(css Selector uses Xpath, difficult but versitle)


