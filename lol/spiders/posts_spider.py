import json

import scrapy


class Nonloso(scrapy.Item):
    team = scrapy.Field()
    # pts = scrapy.Field()

class PostsSpider(scrapy.Spider):
    name = "posts"
    start_urls = ["https://www.soccerstats.com/latest.asp?league=italy"]
    """
                  "https://www.soccerstats.com/latest.asp?league=england",
                  "https://www.soccerstats.com/latest.asp?league=spain",
                  "https://www.soccerstats.com/latest.asp?league=france",
                  "https://www.soccerstats.com/latest.asp?league=germany"]

"""

    def parse(self, response):
        #for x in range(2,22):
           # a = response.xpath("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[5]/div[3]/table[3]/tr[2]/td[2]/a")
        a=[]
        links=[]
        for tr in response.xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[5]/div[3]/table[3]/tr[2]/td[2]'):
            a=tr.xpath("//a/@href").re("^(team\.asp\?league=[a-z]*&stats=.*)")
        for team in a:
           links="https://www.soccerstats.com/"+team
           yield scrapy.Request(links, callback=self.parse_attr)

    def parse_attr(self, response):
        "/html/body/div[1]/div/div/div[2]/div[2]/div[5]/div/div[2]/div[2]/div[1]/table[2]/tbody/tr[2]"
        temp_dict = {}
        for x in range(2,15):
            if x < 8:
                if x%2==0:
                    a=response.xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[5]/div/div[2]/div[2]/div[1]/table[2]/tr["+str(x)+"]/td[3]/b//text()").extract()
                    temp_dict.update({x:{'desc': a}})
                else:
                    a=response.xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[5]/div/div[2]/div[2]/div[1]/table[2]/tr["+str(x)+"]/td[2]/b//text()").extract()
                    temp_dict.update({x:{'desc': a}})

            else:
                if x%2==0:
                    a=response.xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[5]/div/div[2]/div[2]/div[1]/table[2]/tr["+str(x)+"]/td[2]/b//text()").extract()
                    temp_dict.update({x:{'desc': a}})

                else:
                    a=response.xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[5]/div/div[2]/div[2]/div[1]/table[2]/tr["+str(x)+"]/td[3]/b//text()").extract()
                    temp_dict.update({x:{'desc': a}})


       #link_text = tr.xpath('//a//text()').extract()
       #print(link_text)
        """
        n = Nonloso()
        n["team"] = tr.xpath('tr[2]/td[2]"//a/text()').extract()[0].strip()
        #n["pts"]
        print(n)
           
            a = response.xpath('/html/body/div/div/div[1]/div[2]/div[2]/div[5]/div[3]/table[3]/tr['+str(x)+']//text()').extract()
            print(a)
            punteggioClassifica = a[6]+a[32]
            goals=a[56]+a[68]+a[80]+a[92]+a[104]+a[116]
            g=[0,0,0,0,0,0]
            g[0]=int(goals[0])+int(goals[2] )
            g[1]=int(goals[3])+int(goals[5] )
            g[2]=int(goals[6])+int(goals[8] )
            g[3]=int(goals[9])+int(goals[11])
            g[4]=int(goals[12])+int(goals[14]   )
            g[5]=int(goals[15])+int(goals[17]    )

            #a= response.css('tr[height="29"]').getall()
            print(punteggioClassifica)
            print(g)

            #f = open("lol.html","a")
            #f.write(a)
    #        page = response.url.split
    #        page = response.url.split
    #        page = response.url.split
    """

    def parseGoal(self, response):
        for r in range(1,9):
            a = response.xpath("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[5]/div/div[1]/table[2]/tr/td[1]/table[2]/tr["+str(r)+"]//text()").extract()[2:8]
            print(a)
