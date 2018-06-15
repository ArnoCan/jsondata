# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import unittest
import os
import sys

from jsondata import V3K

if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
else:
    import json as myjson
import jsonschema

if V3K:
    unicode = str


from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF
from jsondata.jsonpatch import JSONPatch, JSONPatchItem
from filesysobjects.configdata import ConfigPath
from jsondata.jsonpointer import JSONPointer


class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
 
        _cp = ConfigPath(replace=os.path.dirname(__file__))
        self.datafile = _cp.get_config_filepath('datafile.json')
        self.schemafile = _cp.get_config_filepath('schema.jsd')
        self.configdata = ConfigData(
            {},
            datafile=self.datafile,
            schemafile=self.schemafile,
            validator=MS_OFF,
            )

        # load data
        with open(self.datafile) as data_file:
            self.jval = myjson.load(data_file)
        if self.jval == None:
            raise BaseException("Failed to load data:" + str(data_file))

        assert self.jval

    def testCase010(self):

        with open(self.schemafile) as schema_file:
            sval = myjson.load(schema_file)
        if sval == None:
            raise BaseException("Failed to load schema:" + str(schema_file))

    def testCase900(self):

        assert self.configdata.data["address"]["streetAddress"] == "21 2nd Street"
        assert self.configdata.data["address"]["city"] == "New York"
        assert self.configdata.data["address"]["houseNumber"] == 12

    def testCase901(self):

        assert self.configdata.data["phoneNumber"][0]["type"] == "home"
        assert self.configdata.data["phoneNumber"][0]["number"] == "212 555-1234"
        pass

    def testCase920(self):

        assert self.configdata.data["address"]["streetAddress"] == self.jval["address"]["streetAddress"]
        assert self.configdata.data["address"]["city"] == self.jval["address"]["city"]
        assert self.configdata.data["address"]["houseNumber"] == self.jval["address"]["houseNumber"]

    def testCase921(self):

        assert self.configdata.data["phoneNumber"][0]["type"] == self.jval["phoneNumber"][0]["type"]
        assert self.configdata.data["phoneNumber"][0]["number"] == self.jval["phoneNumber"][0]["number"]
        pass


#
#######################
#
if __name__ == '__main__':
    unittest.main()
