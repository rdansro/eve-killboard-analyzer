# rcooper 05/19/18
import urllib
import requests
import util
import bz2
import csv
from util import DIR_PATH

class TypeID:
    '''
        Class that loads the typeid list from online source.
        Provides options to cache local copy for fast debugging.
    '''
    def __init__(self, url='https://www.fuzzwork.co.uk/dump/latest/invTypes.csv.bz2', file=DIR_PATH + 'lib/pickled/typeid.p', from_cache=False, cache=True):
        self.url = url
        self.file = file

        if from_cache:
            self.data = self.__from_file()
        else:
            self.data = self.__get()

        if cache:
            self.__to_file()

    def __get(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception("Recieved status code %d from %s" % (response.getcode(), self.url))

        # decompress and convert to csv iterable
        bz2_obj = bz2.decompress(response.content)
        reader = csv.DictReader(bz2_obj.decode('utf-8').split('\n'), delimiter=',')

        data = {} # eve entity lookup table
        for line in reader:
            data.update({line['typeID'] : line['typeName']})

        return data

    def __to_file(self):
        util.save_to_file(self.data, self.file)

    def __from_file(self):
        return util.load_from_file(self.file)

    def get(self):
        return self.data

if __name__ == '__main__':
    a = TypeID(from_cache=False)
