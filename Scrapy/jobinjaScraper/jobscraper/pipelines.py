# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JobscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        position = adapter.get('position')
        adapter['position'] = position.replace("استخدام ","").strip()

        return item


import sqlite3

class SaveToDatabasePipeline:
    def __init__(self):
        #Making a connection
        self.conn = sqlite3.connect("/workspaces/133903613/for_deletion/jobinjaScraper/jobs.db")

        #Creating a cursur, to execute commands
        self.cur = self.conn.cursor()

        self.cur.execute("DROP TABLE IF EXISTS jobinja")

        #Creating table
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS jobinja (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id NUMERIC NOT NULL,
            position TEXT NOT NULL,
            companyname_eng TEXT NOT NULL,
            companyname_per TEXT NOT NULL,
            industry TEXT NOT NULL,
            category TEXT NOT NULL,
            location TEXT NOT NULL,
            job_type TEXT NOT NULL,
            experience TEXT,
            salary TEXT NOT NULL,
            languages TEXT,
            skills TEXT NOT NULL,
            gender TEXT NOT NULL,
            military_status TEXT,
            min_edu_degree TEXT,
            direct_url TEXT NOT NULL,
            company_url TEXT,
            url TEXT NOT NULL
        )
        """)

    def process_item(self, item, spider):

        #Insert statement
        self.cur.execute("""INSERT INTO jobinja (
                         job_id,
                         position,
                         companyname_eng,
                         companyname_per,
                         industry,
                         category,
                         location,
                         job_type,
                         experience,
                         salary,
                         languages,
                         skills,
                         gender,
                         military_status,
                         min_edu_degree,
                         direct_url,
                         company_url,
                         url
                         ) VALUES (
                         :job_id,
                         :position,
                         :companyname_eng,
                         :companyname_per,
                         :industry,
                         :category,
                         :location,
                         :job_type,
                         :experience,
                         :salary,
                         :languages,
                         :skills,
                         :gender,
                         :military_status,
                         :min_edu_degree,
                         :direct_url,
                         :company_url,
                         :url)""",
                         {
                             "job_id":          item["job_id"],
                             "position":        item["position"],
                             "companyname_eng": item["companyname_eng"],
                             "companyname_per": item["companyname_per"],
                             "industry":        item["industry"],
                             "category":        item["category"],
                             "location":        item["location"],
                             "job_type":        item["job_type"],
                             "experience":      item["experience"],
                             "salary":          item["salary"],
                             "languages":       item["languages"],
                             "skills":          item["skills"],
                             "gender":          item["gender"],
                             "military_status": item["military_status"],
                             "min_edu_degree":  item["min_edu_degree"],
                             "direct_url":      item["direct_url"],
                             "company_url":     item["company_url"],
                             "url":             item["url"],
                          })

        #Commiting insertion of data into database
        self.conn.commit()
        return item

    def close_spider(self, spider):
        #closing cursor and connection
        self.cur.close()
        self.conn.close()