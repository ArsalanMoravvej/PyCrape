# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobinjaItem(scrapy.Item):
    job_id = scrapy.Field()
    position = scrapy.Field()
    companyname_eng = scrapy.Field()
    companyname_per = scrapy.Field()
    industry = scrapy.Field()
    category = scrapy.Field()
    location = scrapy.Field()
    job_type = scrapy.Field()
    experience = scrapy.Field()
    salary = scrapy.Field()
    languages = scrapy.Field()
    skills = scrapy.Field()
    gender = scrapy.Field()
    military_status = scrapy.Field()
    min_edu_degree = scrapy.Field()
    direct_url = scrapy.Field()
    company_url = scrapy.Field()
    url = scrapy.Field()