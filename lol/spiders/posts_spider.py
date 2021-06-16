
import scrapy
import re
from scrapy.shell import inspect_response
from ..items import LolItem
from scrapy.selector import Selector

def add_values_in_dict(sample_dict, key, list_of_values):
    """Append multiple values to a key in the given dictionary"""
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    return sample_dict

class Nonloso(scrapy.Item):
    team = scrapy.Field()
    # pts = scrapy.Field()
class PostsSpider(scrapy.Spider):
    name = "posts"
    start_urls = ["https://www.soccerstats.com/latest.asp?league=england",
                  "https://www.soccerstats.com/latest.asp?league=italy",
                  "https://www.soccerstats.com/latest.asp?league=spain",
                  "https://www.soccerstats.com/latest.asp?league=france",
                  "https://www.soccerstats.com/latest.asp?league=germany"]



    def parse(self, response):
        items = LolItem()
        #for x in range(2,22):
           # a = response.xpath("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[5]/div[3]/table[3]/tr[2]/td[2]/a")
        teams=[]
        links=[]
        for tr in response.xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[5]/div[3]/table[3]/tr[2]/td[2]'):
            teams=tr.xpath("//a/@href").re("^(team\.asp\?league=[a-z]*&stats=.*)")

        for team in teams:
            links="https://www.soccerstats.com/"+team
            #yield {'team': items["team"]}

            line = re.sub(r"team\.asp\?league\=[a-z]*\&[a-z]*\=\d+-", "", team)


            yield scrapy.Request(links, callback=self.parse_attr,meta={'team':line,'champ':"eng"})
            #items["team"] = links
           # items["name"] = a


            #print(temp_dict["desc"])
            #items["name"] = temp_dict


    def parse_attr(self, response):
        "/html/body/div[1]/div/div/div[2]/div[2]/div[5]/div/div[2]/div[2]/div[1]/table[2]/tbody/tr[2]"
        items = LolItem()
        temp_dict = []
        final_list = []
        for x in range(2,15):
            if x < 8:
                if x%2==0:
                    a=response.xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[5]/div/div[2]/div[2]/div[1]/table[2]/tr["+str(x)+"]/td[3]/b//text()").extract()
                    temp_dict.append(a)
                    #temp_dict.update({x:{'desc': a}})
                else:
                    a=response.xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[5]/div/div[2]/div[2]/div[1]/table[2]/tr["+str(x)+"]/td[2]/b//text()").extract()
                    temp_dict.append(a)

                    #temp_dict.update({x:{'desc': a}})

            else:
                if x%2==0:
                    a=response.xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[5]/div/div[2]/div[2]/div[1]/table[2]/tr["+str(x)+"]/td[2]/b//text()").extract()
                    temp_dict.append(a)

                    #temp_dict.update({x:{'desc': a}})

                else:
                    a=response.xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[5]/div/div[2]/div[2]/div[1]/table[2]/tr["+str(x)+"]/td[3]/b//text()").extract()
                    temp_dict.append(a)

                    #temp_dict.update({x:{'desc': a}})

        new_list = list(filter(None, temp_dict))
        even = []
        ods = []

        for i in range(len(new_list)):
            if (i%2)==0:
                even.append(new_list[i])
            else:
                ods.append(new_list[i])
        items["fatti"]=even
        items["subiti"]=ods
        items["champ"] =response.xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/table/tr/td[3]/font//text()").extract()[0]
        items["team"] = response.meta.get('team')

       # items["name"] = new_list
        sel = Selector(response)
        for x in range(3,40):
            tables= sel.xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[5]/div/div[1]/table[4]/tr[" + str(x) + "]")
            for table in tables:
                date = table.xpath('td[1]/font//text()').extract()
                date = [x.strip('\n') for x in date]
                date[:] = [x for x in date if x]
                home = table.xpath('td[2]//text()').extract()
                home = [x.strip('\n') for x in home]
                home[:] = [x for x in home if x]
                score = table.xpath('td[3]/a/font/b//text()').extract()
                score = [x.strip('\n') for x in score]
                score = [x.replace(' ', '') for x in score]
                score[:] = [x for x in score if x]
                away =  table.xpath('td[4]//text()').extract()
                away = [x.strip('\n') for x in away]
                away[:] = [x for x in away if x]
                items = add_values_in_dict(items, 'date', date)
                items = add_values_in_dict(items, 'home', home)
                items = add_values_in_dict(items, 'score', score)
                items = add_values_in_dict(items, 'away',away)
                """

                items['date'] = table.xpath('td[1]/font//text()').extract()
                items['home'] = table.xpath('td[2]//text()').extract()
                items['score'] = table.xpath('td[3]/a/font/b//text()').extract()
                items['away'] = table.xpath('td[4]//text()').extract()
                items[[x]]={}
                items[[x]]={"date":items["date"],"home":items["home"],"score":items["score"],"away":items["away"]}
                                """


        final_list.append(items)
        updated_list = []

        for item in final_list:

                sub_item = {}
                sub_item[items["champ"]] = {}
                #sub_item['champ']["champ"]=[]
                sub_item[items["champ"]]['team'] = [item['team']]
                sub_item[items["champ"]]['every15'] = {}
                sub_item[items["champ"]]['every15']["fatti"] =[item["fatti"]]
                sub_item[items["champ"]]['every15']["subiti"] =[item["subiti"]]
                sub_item[items["champ"]]['over']= {}
                sub_item[items["champ"]]['over']["date"] =[item["date"]]

                sub_item[items["champ"]]['over']["date"] =[item["date"]]
                sub_item[items["champ"]]['over']["home"] =[item["home"]]
                sub_item[items["champ"]]['over']["score"] =[item["score"]]
                sub_item[items["champ"]]['over']["away"] =[item["away"]]


                updated_list.append(sub_item)

        print("#############################################################")
        return updated_list


        #items["team"]["name"] = self.
        #yield {'name':items["name"] }
        #link_text = tr.xpath('//a//text()').extract()
        #print(link_text)
        #
"""
        n = Nonloso()
        n["team"] = response.xpath('tr[2]/td[2]"//a/text()').extract()[0].strip()
        #n["pts"]
        print(n)
        h = response.xpath('/html/body/div/div/div[1]/div[2]/div[2]/div[5]/div[3]/table[3]/tr['+str(x)+']//text()').extract()
        print(h)
        punteggioClassifica = h[6]+h[32]
        goals=h[56]+h[68]+h[80]+h[92]+h[104]+h[116]
        g=[0,0,0,0,0,0]
        g[0]=int(goals[0])+int(goals[2] )
        g[1]=int(goals[3])+int(goals[5] )
        g[2]=int(goals[6])+int(goals[8] )
        g[3]=int(goals[9])+int(goals[11])
        g[4]=int(goals[12])+int(goals[14]   )
        g[5]=int(goals[15])+int(goals[17]    )

        #a= response.css('tr[height="29"]').getall()
        print("#############################################################")
        print(punteggioClassifica)
        print(g)
        """

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
"""