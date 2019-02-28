"""
BSParser


Author
José Lopes de Oliveira Jr. <bierminen.com>


Overview
BSParser is an Aclla submodule to parse BeerSmith's XML files.  This tool can
help users to build their own databases.

"""


import xml.etree.ElementTree as ET
import json


class Grain(object):
    """
    Retrive data from a bsmx file with grain information --usually Grain.bsmx.

    ARGS:
    - path (string): path to the bsmx file.

    """
    def __init__(self, path='/usr/share/BeerSmith2/Grain.bsmx'):
        self.root = ET.parse(path).getroot()

    def parse(self, tags):
        """
        ARGS:
        - tags (list): a list of tags you want to retrive --see README.md for a
            list of common tags.

        """
        return json.dumps({'grains': [dict((tag.tag,tag.text)
            for tag in el if tag.tag in tags)
            for el in self.root.iter('Grain')]})


if __name__ == '__main__':
    print(Grain().parse(['F_G_NAME', 'F_G_ORIGIN', 'F_G_COLOR', 'F_G_YIELD']))
