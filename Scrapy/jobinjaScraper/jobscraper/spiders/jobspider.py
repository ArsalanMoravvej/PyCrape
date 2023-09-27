import scrapy
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

        spec = response.css('.c-infoBox__item')

        items = {}
        for thing in spec:
            items[thing.css(".c-infoBox__itemTitle::text").get()] = ", ".join([skill.get().replace("\n","").strip() for skill in thing.css (".tags .black::text")])

        try:
            company_url = response.css('.c-companyHeader__metaItem a ::text')[1].get()
        except:
            company_url = None

        yield {
            'id':               response.css('.c-sharingJobOnMobile__uniqueURL::text').get().strip().replace('https://jobinja.ir/', ''),
            'direct-url':       response.css('.c-sharingJobOnMobile__uniqueURL::text').get().strip(),
            'position':         response.css('.c-jobView__titleText h1 ::text').get().strip().replace("استخدام ",""),
            'companyname(eng)': response.css('.c-companyHeader__name::text')[1].get().strip(),
            'companyname(per)': response.css('.c-companyHeader__name::text')[0].get().strip(),
            'industry' :        response.css('.c-companyHeader__metaItem a ::text')[0].get(),
            'company_url':      company_url,
            'category':         items.get('دسته‌بندی شغلی'),
            'location':         items.get('موقعیت مکانی').replace(" ","").strip(),
            'type':             items.get('نوع همکاری'),
            'experience':       items.get('حداقل سابقه کار'),
            'salary':           items.get('حقوق'),
            'languages':        items.get('زبان‌های مورد نیاز'),
            'skills':           items.get('مهارت‌های مورد نیاز'),
            'gender':           items.get('جنسیت'),
            'military_status':  items.get('وضعیت نظام وظیفه'),
            'min_edu_degree':   items.get('حداقل مدرک تحصیلی'),
            'url': response.url,
        }