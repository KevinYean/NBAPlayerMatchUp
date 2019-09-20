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
    name = "gamelog"
    download_delay = 0.5
    currentseason = ""

    def start_requests(self):
        pipeline = [ #MongoDB Pipeline
                {
                    '$project': {
                        'basketballreference_page': 1
                    }
                }
            ]
        players = db.GameLogs.aggregate(pipeline).next()

        urls = [  # List of Urls to go through
           "https://www.basketball-reference.com/players/l/lillada01.html"
        ]
        for url in urls:  # Run parse for each url in urls
            yield scrapy.Request(url=url, callback=self.parsePlayers)
    
    def parsePlayers(self,response):
        yield {
            "test" : response.url,
            "second Test" : db.list_collection_names()
        }