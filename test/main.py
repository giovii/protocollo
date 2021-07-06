import json
from pprint import pprint
to_find = "Premier League"
# Opening JSON file

"""
    data = json.load(json_file)
    first_elem = data[0]
    entities = first_elem['Premier League']["team"]
    pprint(entities)
    """
nametocheck='arsenal'
ntc ="Arsenal"
with open('../squadre.json') as json_file:
    data = json.load(json_file)
    for s in range(len(data)):
        home =0
        away =0
        if 'Premier League' in data[s]:
            team=data[s]['Premier League']["team"]
            if nametocheck in team:
                a=data[s]["Premier League"]["over"]["home"][0]
                home=list(a).count(ntc)
                a=data[s]["Premier League"]["over"]["away"][0]
                away=list(a).count(ntc)
                #print("home="+str(home)+" away="+str(away))
                a=data[s]["Premier League"]["over"]["score"][0]
                totgoalhome=0
                homegoalhome=0
                homegoalaway=0
                homeover=0
                totgoalaway=0
                awaygoalhome=0
                awaygoalaway=0
                awayover=0
                stopat=0
                for n in range(len(a)):
                     goals=list(a)[n].split("-")
                     if ntc in list(data[s]["Premier League"]["over"]["home"][0])[n]:
                         homegoalhome= homegoalhome + int(goals[0])
                         homegoalaway=homegoalaway+int(goals[1])
                         if int(goals[0])+int(goals[1])>2:
                             homeover=homeover+1
                     else:
                         awaygoalhome=awaygoalhome +int(goals[0])
                         awaygoalaway=awaygoalaway +int(goals[1])
                         if int(goals[0])+int(goals[1])>2:
                             awayover=awayover+1

                     stopat=stopat+1
                     if stopat==3:
                         break
                print("totale partite"+str(len(a)))
                print("totalover"+str(awayover+homeover))
        exit(0)


"""
                if nametocheck in home:
                    home = home +1
                else:
                    away = away +1

    for s in range(len(data)):
        if data[s]:#["P remier League"] == to_find:
            print(data[s])
            print("######################################")
    """
