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

        id = 670                       

        print('Kills: ' + str(self.killCounter[id]['TOTAL']))
        print('Deaths: ' + str(self.deathCounter[id]['TOTAL']))

        print('Ship %d (%s) solo win rate = %lf' % (id, self.typeid[str(id)], self.killCounter[id]['TOTAL'] / (self.killCounter[id]['TOTAL'] + self.deathCounter[id]['TOTAL'])))


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

if __name__ == '__main__':
    Aggregator()
