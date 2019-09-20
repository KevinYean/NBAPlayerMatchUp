import scrapy
import re

#Commands
#scrapy shell "https://www.basketball-reference.com/teams/"

class GamelogSpider(scrapy.Spider):
    name = "team"
    download_delay = 0.5
    currentseason = ""

    def start_requests(self):
        urls = [  # List of Urls to go through
            "https://www.basketball-reference.com/teams/"
        ]
        for url in urls:  # Run parse for each url in urls
            yield scrapy.Request(url=url, callback=self.parseTeamIndex)

    def parseTeamIndex(self, response):
        teams = response.xpath('//tr[contains(@class,"full_table")]//a/@href').extract()
        for i in teams: #To-Do, Find a way to make it more efficient by simply going through it as opposed to all of it.
            x = response.urljoin(i)
            yield scrapy.Request(x, callback=self.parseTeam)
    
    def parseTeam(self,response):
        #Team Name
        teamName = response.xpath('//h1[contains(@itemprop,"name")]//span//text()').get()
         #Active Years
        years = response.xpath('//strong[contains(text(),"Seasons:")]/following::text()').get()
        years = years.split(';') #Split seasons and years
        seasonsActive = years[1].split() #Split on beginning and last seasons Team played
        firstYear = seasonsActive[0].split('-') #First Year
        lastYear = seasonsActive[2].split('-') #Last Year
        lastYear = lastYear[0][:2] + lastYear[1]

        ceiling = 2019 #Range
        floor = 2010 #Range

        #Url
        s = response.url.split("/")

        if (int(lastYear) >= ceiling):
            yield{
                "teamName" : teamName,
                "abbreviation" : s[-2]
            }