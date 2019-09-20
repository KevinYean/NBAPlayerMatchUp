import scrapy
import re

#response.css('td[data-stat="player"]').getall() //Teams
#response.css('td[data-stat="player"] a::attr(href)').getall()
#response.xpath('//tr //a[contains(@href,"playoffs")]').get()


class QuotesSpider(scrapy.Spider):
    name = "player"
    DOWNLOAD_DELAY = 0.5
    currentseason = ""

    def start_requests(self):
        urls = [  # List of Urls to go through
            "https://www.basketball-reference.com/leagues/NBA_2019.html"
            #"https://www.basketball-reference.com/players/l/lillada01.html"
        ]
        for url in urls:  # Run parse for each url in urls
            yield scrapy.Request(url=url, callback=self.parseLeague)

    def parseLeague(self, response):
        #League Specific
        teams_page = response.css(
            'th[data-stat="team_name"] a::attr(href)').getall()
        nbaSeason = response.css(
            'h1 span::text').get()
        currentseason = str(nbaSeason)
        if teams_page is not None:
            for i in teams_page:
                x = response.urljoin(i)
                yield scrapy.Request(x, callback=self.parseTeam)
    
    def parseTeam(self,response):
        #Team Specific
        next_page = response.css(
            'td[data-stat="player"] a::attr(href)').getall()
        nbaTeam = response.css(
            'h1 span::text').getall()
        if next_page is not None:
            for i in next_page:
                x = response.urljoin(i)
                yield scrapy.Request(x, callback=self.parsePlayer)

    def parsePlayer(self, response):
        #Player's Name
        playerName = response.xpath("//h1//text()").get()
        mp_per_g = response.css('td[data-stat="mp_per_g"]::text').getall() #To do make more efficient
        if (float(mp_per_g[-1]) >= 10.0):
            yield {
                "player" : playerName,
                "career_mp_per_g" : float(mp_per_g[-1]),
                "basketballreference_page" : response.url
            }
