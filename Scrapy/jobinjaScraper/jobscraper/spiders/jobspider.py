import scrapy
import re

# https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B%5D=data
class JobspiderSpider(scrapy.Spider):
    name = "jobspider"
    allowed_domains = ["jobinja.ir"]
    start_urls = ["https://jobinja.ir/jobs?&filters%5Bkeywords%5D%5B0%5D=data"]

    def parse(self, response):
        jobs = response.css('li.o-listView__item')

        for job in jobs:
            href = job.css('h2 a').attrib['href']
            job_url = re.search(r'.+jobs/.+/', href).group(0)
            yield response.follow(job_url, callback=self.parse_job)


        if response.css('.paginator-next-text'):
            next_page = response.css('.paginator li a')[-1].attrib['href']
            yield response.follow(next_page, callback= self.parse)

    def parse_job(self, response):
        #"""companyname = pers: response.css('.c-companyHeader__name::text')[0].get().strip()
        # companyname = eng: response.css('.c-companyHeader__name::text')[1].get().strip()
        # industry = response.css('.c-companyHeader__metaItem a ::text')[0].get()
        # company_url: response.css('.c-companyHeader__metaItem a ::text')[1].get()
        # """
