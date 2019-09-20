import scrapy
import pymongo
import re
from bson.json_util import dumps

#Commands
#scrapy shell 'https://www.basketball-reference.com/players/'

uri = "mongodb+srv://tempReader:tempPassword@cluster0-focx3.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client.NBA_Match_Ups

class GamelogSpider(scrapy.Spider):
    name = "gamelog" #Name of Crawler
    download_delay = 0.5
    currentseason = ""

    def start_requests(self):
        players = db.Players.find({},{'basketballreference_page':1, "_id": 0}) #Project only the url of basketball reference page
        listOfUrls = [] #Empty List
        for document in players: #For loop to go through the entire Cursor
            listOfUrls.append(document['basketballreference_page']) #Add the url to the list

        # List of Urls to go through
        urls = listOfUrls
        #urls = [#"https://www.basketball-reference.com/players/l/lillada01/gamelog/2013"]
         #   "https://www.basketball-reference.com/players/l/lillada01.html"]
        for url in urls:  # Run parse for each url in urls
            yield scrapy.Request(url=url, callback=self.parsePlayers)
    
    def parsePlayers(self,response):
        links = response.css('ul[class=""] a::attr(href)').getall()
        links = set(links)
        for i in links:
            if "gamelog" in i and "playoffs" not in i: #Only keep gamelogs from the set
                    yield scrapy.Request(url=response.urljoin(i), callback=self.parseGameLogs)

    def parseGameLogs(self,response):
        #Player
        h1 = response.xpath('//h1/text()').get()
        h1 = h1.split(' ')
        name = ' '.join(h1[:-3]) #Go Backward
        #Year/Season
        year = h1[-3]
        #Game Number played by player
        numGamesPlayed = len(response.xpath('//tr[contains(@id,"pgl")]').getall())
        gameResults = response.xpath('//tr[contains(@id,"pgl")]//td[contains(@data-stat,"game_result")]//text()').getall()
        #Tm, OP
        teams = response.xpath('//tr[contains(@id,"pgl")]//td[contains(@data-stat,"team_id")]//text()').getall()
        opps = response.xpath('//tr[contains(@id,"pgl")]//td[contains(@data-stat,"opp_id")]//text()').getall()
        #Minutes
        mp = response.xpath('//tr[contains(@id,"pgl")]//td[contains(@data-stat,"mp")]//text()').getall()
        #Field Goal %       
        fg_pct = response.xpath('//tr[contains(@id,"pgl")]//td[contains(@data-stat,"fg_pct")]//text()').getall()
        #Points
        pts = response.xpath('//tr[contains(@id,"pgl")]//td[contains(@data-stat,"pts")]//text()').getall()
        #For each Yield
        for i in range (numGamesPlayed):
            yield{
                "name" : name,
                "year" : year,
                "game" : i+1,
                "team" : teams[i],
                "opponent" : opps[i],
                "result" : gameResults[i],
                "points" : int(pts[i]),
                "minutes" : mp[i],
                "fg_pct" : float(fg_pct[i])
            }

