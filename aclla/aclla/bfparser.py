"""
BFParser


Author
José Lopes de Oliveira Jr. <bierminen.com>


Overview
BFParser is an Aclla submodule to parse BeerSmith's XML files.  This tool can
help users to build their own databases.

"""


from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET
import re, json

from bs4 import BeautifulSoup


class Fermentable(object):
    """
    Parses the table of fermentables from Brewer's Friend into a usable format.

    """
    def __init__(self,
        url='http://www.brewersfriend.com/fermentables/?filter=All%20Fermentables'):
        html = urlopen(Request(url,
            headers={'User-Agent':'Browserminen'})).read()
        self.table = [list([col.get_text() for col in row.find_all('td')])
            for row in BeautifulSoup(html,
            'html.parser').find_all('table')[0].find_all('tr')[2:]]

    def parse(self):
        return json.dumps({'fermentables': [self.equaliser(line)
            for line in self.table]})

    def equaliser(self, list_):
        "Receives a list, returns a dictionary"
        d = {}
        try:
            d['fermentable'] = list_[0].strip()
            d['country'] = list_[1].strip()
            d['category'] = list_[2].strip()
            d['type'] = list_[3].strip()
            d['color'] = re.sub('[^0-9.]', '', list_[4])
            d['ppg'] = re.sub('[^0-9.]', '', list_[5])
        except IndexError:
            return None
        return d


if __name__ == '__main__':
    print(Fermentable().parse())
