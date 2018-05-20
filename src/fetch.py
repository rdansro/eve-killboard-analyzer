import util
import os
from zkillboard import zKillboard
from typeid import TypeID
from killboarddb import KillboardDB
from util import DIR_PATH
from pprint import pprint
import collections


class Fetcher() :
    def __init__(self, clean=False, from_cache=True, timeout=1.5):
        self.kbdb = KillboardDB(clean=clean)
        self.kb = zKillboard(timeout_seconds=timeout)
        self.typeid = TypeID(from_cache=from_cache).get()


    def fetch(self, start_page=1, end_page=1000, verbose=False, save_page_to_file=False, save_path=DIR_PATH + 'lib/pickled/'):
        count = 0
        inserted = 0
        for i in range(start_page, end_page + 1):
            page = self.kb.get('page/%d/' % i)
            if len(page) == 0:
                if verbose: print('Found empty page... stopping fetch')
                break
            if save_page_to_file: util.save_to_file(page, save_path + '%d.p' % i)

            commit = 0
            for event in page:
                if self.kbdb.insert_kill(event):
                    commit += 1
                count += 1
            if verbose: print('Finished page %d | committed %d new killmails to db' % (i, commit))

if __name__ == '__main__':
    Fetcher(clean=False, from_cache=True, timeout=1.5).fetch(start_page=1000, end_page=1100, verbose=True)
