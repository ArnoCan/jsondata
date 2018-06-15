"""Load and access data.
"""
from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson
else:
    import json as myjson
import jsonschema


from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF, MS_DRAFT4
from jsondata.jsondata import JSONData
from filesysobjects.configdata import ConfigPath


class CallUnits(unittest.TestCase):

    def testCase000(self):

        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('testdata.json')

        with open(datafile) as data_file:
            self.jval = myjson.load(data_file)
        if self.jval == None:
            raise BaseException("Failed to load data:" + str(data_file))

        cdata = {u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}], u'address': {
            u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}
        assert cdata == self.jval

        schemafile = _cp.get_config_filepath('testdata.jsd')
        configdata = ConfigData(
            self.jval,
            schemafile=schemafile,
            datafile=datafile,
            validator=MS_OFF,
            )
        assert self.jval == configdata.data

        assert configdata.data["address"]["streetAddress"] == "21 2nd Street"
        assert configdata.data["address"]["city"] == "New York"
        assert configdata.data["address"]["houseNumber"] == 12

        assert configdata.data["phoneNumber"][0]["type"] == "home"
        assert configdata.data["phoneNumber"][0]["number"] == "212 555-1234"

        assert configdata.data["address"]["streetAddress"] == self.jval["address"]["streetAddress"]
        assert configdata.data["address"]["city"] == self.jval["address"]["city"]
        assert configdata.data["address"]["houseNumber"] == self.jval["address"]["houseNumber"]

        assert configdata.data["phoneNumber"][0]["type"] == self.jval["phoneNumber"][0]["type"]
        assert configdata.data["phoneNumber"][0]["number"] == self.jval["phoneNumber"][0]["number"]


if __name__ == '__main__':
    unittest.main()
