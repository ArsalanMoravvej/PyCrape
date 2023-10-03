import scrapy
from jobscraper.items import JobinjaItem
import re

class JobspiderSpider(scrapy.Spider):
    name = "jobspider"
    allowed_domains = ["jobinja.ir"]
    start_urls = ["https://jobinja.ir/jobs?&filters%5Bkeywords%5D%5B0%5D=golang"]

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
        job_item = JobinjaItem()

        spec = response.css('.c-infoBox__item')

        items = {}
        for thing in spec:
            items[thing.css(".c-infoBox__itemTitle::text").get()] = ", ".join([item.get().replace("\n","").strip() for item in thing.css(".tags .black::text")])

        try:
            company_url = response.css('.c-companyHeader__metaItem a ::text')[1].get()
        except:
            company_url = None

        job_item['job_id'] =               response.css('.c-sharingJobOnMobile__uniqueURL::text').get().strip().replace('https://jobinja.ir/', '')
        job_item['position'] =         response.css('.c-jobView__titleText h1 ::text').get()
        job_item['companyname_eng'] =  response.css('.c-companyHeader__name::text')[1].get().strip()
        job_item['companyname_per'] =  response.css('.c-companyHeader__name::text')[0].get().strip()
        job_item['industry'] =         response.css('.c-companyHeader__metaItem a ::text')[0].get()
        job_item['category'] =         items.get('دسته‌بندی شغلی')
        job_item['location'] =         items.get('موقعیت مکانی').replace(" ","").strip()
        job_item['job_type'] =         items.get('نوع همکاری')
        job_item['experience'] =       items.get('حداقل سابقه کار')
        job_item['salary'] =           items.get('حقوق')
        job_item['languages'] =        items.get('زبان‌های مورد نیاز')
        job_item['skills'] =           items.get('مهارت‌های مورد نیاز')
        job_item['gender'] =           items.get('جنسیت')
        job_item['military_status'] =  items.get('وضعیت نظام وظیفه')
        job_item['min_edu_degree'] =   items.get('حداقل مدرک تحصیلی')
        job_item['direct_url'] =       response.css('.c-sharingJobOnMobile__uniqueURL::text').get().strip()
        job_item['company_url'] =      company_url
        job_item['url'] =              response.url


        yield job_item