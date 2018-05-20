import util
import os
from zkillboard import zKillboard
from typeid import TypeID
from killboarddb import KillboardDB
from util import DIR_PATH
from pprint import pprint
import collections

if __name__ == '__main__':
    kbdb = KillboardDB(clean=True)
    fetcher = zKillboard()
    typeid = TypeID(from_cache=True).get()
    killList = []

    # obj = util.load_from_file(DIR_PATH + "lib/pickled/test.p")
    # obj = fetcher.get("losses/solo/page/1/")
    # obj += fetcher.get("losses/solo/page/2/")

    # for i in range(1, 6):
    #     util.save_to_file(fetcher.get('losses/solo/page/%d/' % i), DIR_PATH + 'lib/pickled/%d.p' % i)

    for i in range(1, 6):
        killList += util.load_from_file(DIR_PATH + 'lib/pickled/%d.p' % i)


    ids = []

    for event in killList:
        kbdb.insert_kill(event)
        # ids.append(event['killmail_id'])
        # print(event['killmail_id'])
        # pprint(event)
        exit()


    print(ids)
    print(len(ids))
    print([item for item, count in collections.Counter(ids).items() if count > 1])
