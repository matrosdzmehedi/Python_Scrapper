import scrapy
import itertools
import re
import csv


class MySpider(scrapy.Spider):

    name = 'imdbspider'

    def start_requests(self):
        urls = [
            'https://www.imdb.com/chart/top?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=7JC20WDSY71Z63PV55VV&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=moviemeter&ref_=chtmvm_ql_3'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.css('.titleColumn a::text').getall()
        year = response.css('.secondaryInfo::text').re(
            r'[0-9][0-9][0-9][0-9]')
        rating = response.css('td.ratingColumn strong::text').getall()

        file = open('movie-top250.csv', 'w', newline='')
        with file:
            header = ['Name', 'Year', 'Rating']
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()

            for (a, b, c) in itertools.zip_longest(title, year, rating):
                writer.writerow({'Name': a,
                                 'Year': b,
                                 'Rating': c})
