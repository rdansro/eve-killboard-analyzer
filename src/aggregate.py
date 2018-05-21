import numpy as np
import ship_classes
from killboarddb import KillboardDB
from typeid import TypeID
from pprint import pprint


class Aggregator():
    def __init__(self, solo=True, from_cache=True):
        self.kbdb = KillboardDB(clean=False)
        self.typeid = TypeID(from_cache=from_cache).get()

        if solo:
            self.killList = self.kbdb.get_solo_ship_kills()
        else:
            raise NotImplementedError
        self.killCounter = self.aggregate_kills()
        self.deathCounter = self.aggregate_deaths()

        # id = 670
        # print('Kills: ' + str(self.killCounter[id]['TOTAL']))
        # print('Deaths: ' + str(self.deathCounter[id]['TOTAL']))


    def aggregate_kills(self):
        # aggregate kills
        killCounter = {}
        for kill in self.killList:
            try:
                killCounter[kill[2]]
            except KeyError:
                killCounter.update({kill[2] : {'TOTAL' : 0}})

            try:
                killCounter[kill[2]]['TOTAL'] += 1
                killCounter[kill[2]][kill[1]] += 1
            except KeyError:
                killCounter[kill[2]].update({kill[1] : 1})

        return killCounter

    def aggregate_deaths(self):
        # aggregate deaths
        deathCounter = {}
        for kill in self.killList:
            try:
                deathCounter[kill[1]]
            except KeyError:
                deathCounter.update({kill[1] : {'TOTAL' : 0}})

            try:
                deathCounter[kill[1]]['TOTAL'] += 1
                deathCounter[kill[1]][kill[2]] += 1
            except KeyError:
                deathCounter[kill[1]].update({kill[2] : 1})
        return deathCounter

    def aggregate_wr(self, class1, class2):
        kdList = []

        # TODO: set this to any ship value
        if class1 == None:
            raise NotImplementedError


        for ship in class1:
            shipName = self.typeid[ship]

            # Aggregate kills by ship class
            kills = 0
            if class2 == None:
                try:
                    kills += self.killCounter[int(ship)]['TOTAL']
                except:
                    pass
            else:
                for ship2 in class2:
                    try:
                        kills += self.killCounter[int(ship)][int(ship2)]
                    except KeyError:
                        continue

            # Aggregate deaths by ship class
            deaths = 0
            if class2 == None:
                try:
                    deaths += self.deathCounter[int(ship)]['TOTAL']
                except:
                    pass
            else:
                for ship2 in class2:
                    try:
                        deaths += self.deathCounter[int(ship)][int(ship2)]
                    except KeyError:
                        continue

            if kills == 0 and deaths == 0:
                # kdList.append( (ship, shipName, kills, deaths, 0) )
                continue
            elif deaths == 0:
                kdList.append( (ship, shipName, kills, deaths, np.inf) )
            else:
                kdList.append( (ship, shipName, kills, deaths, kills / (kills + deaths)) )


        return sorted(kdList, key=lambda x: x[4], reverse=True)

if __name__ == '__main__':
    aggregate = Aggregator()


    class1 = ship_classes.FRIGATE
    class2 = ship_classes.FRIGATE
    # print('===== Frigate vs Frigate Win Rate =====')
    # kdList = aggregate.aggregate_wr(class1, class2)
    kdList = aggregate.aggregate_wr(class1, ['593'])
    # kdList = aggregate.aggregate_wr(ship_classes.FRIGATE_CLASS, None)

    for kill in kdList:
        print('Ship %s (%s) solo win rate = %lf (kills=%d, deaths=%d)' % (kill[0], kill[1], kill[4], kill[2], kill[3]))
