# rcooper 05/19/18
import urllib
import requests
import util
from util import DIR_PATH

class TypeID:
    '''
        Class that loads the typeid list from online source.
        Provides options to cache local copy for fast debugging.
    '''
    def __init__(self, url='http://eve-files.com/chribba/typeid.txt', file=DIR_PATH + 'lib/pickled/typeid.p', from_cache=False, cache=True):
        self.url = url
        self.file = file

        if from_cache:
            self.data = self.__from_file()
        else:
            self.data = self.__get()

        if cache:
            self.__to_file()

    def __get(self):
        response = urllib.request.urlopen(self.url)
        if response.getcode() != 200:
            raise Exception("Recieved status code %d from %s" % (response.getcode(), self.url))

        data = {} # eve entity lookup table
        for i, line in enumerate(response):
            # skip lines 0 and 1
            if i in [0, 1]:
                continue
            # process into a dictionary
            else:
                line = line.decode("utf-8").split()
                # check valid line
                if len(line) < 2:
                    continue
                else:
                    data.update({line[0]: " ".join(line[1:])})

        return data

    def __to_file(self):
        util.save_to_file(self.data, self.file)

    def __from_file(self):
        return util.load_from_file(self.file)

    def get(self):
        return self.data
