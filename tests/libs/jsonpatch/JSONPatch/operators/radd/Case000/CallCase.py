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

    def record_load(self, datafname, schemafname):
        # data
        if not os.path.isfile(datafname):
            raise BaseException("Missing JSON data:file=" + str(datafname))

        # load data
        with open(datafname) as data_file:
            self.jval = myjson.load(data_file)
        if self.jval == None:
            raise BaseException("Failed to load data:" + str(data_file))

        assert self.jval

 
        self.configdata = ConfigData(
            {},
            datafile=datafname,
            schemafile=schemafname,
            validator=MS_OFF,
            )

        return True

    def setUp(self):
        """Load a data file.
        """
        
        unittest.TestCase.setUp(self)

        # data
        self.datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('testdata.client.00.json')
        if not os.path.isfile(self.datafile):
            raise BaseException("Missing JSON data:file=" + str(self.datafile))

        self.datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('testdata.client.01.json')
        if not os.path.isfile(self.datafile):
            raise BaseException("Missing JSON data:file=" + str(self.datafile))

        # schema
        self.schemafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('testdata.jsd')
        if not os.path.isfile(self.datafile):
            raise BaseException("Missing JSON schema:file=" + str(self.datafile))

        #
        # load
        #
        self.record_load(self.datafile, self.schemafile)



    def record_check(self):

        #
        # validate content
        #
        assert self.configdata.data["address"]["streetAddress"] == "21 2nd Street"

        # by pointer
        jsonptr = JSONPointer('/address/streetAddress')
        if not jsonptr:
            raise BaseException("Failed to create JSONPointer")
        jsonptrdata = jsonptr.get_node_value(self.configdata.data)
        jsx = str(jsonptrdata)
        assert jsx == self.configdata.data["address"]["streetAddress"]

        # now in one line
        assert self.configdata.data["address"]["streetAddress"] == JSONPointer(
            '/address/streetAddress').get_node_value(self.configdata.data)

        return True

    def testCase100(self):

        self.jsonpatchlist = JSONPatch()

        self.jsonpatchlist = \
            JSONPatchItem("test", "/address/streetAddress", "21 2nd Street") \
            + self.jsonpatchlist
        resx = [
          {"op": "test", "path": "/address/streetAddress", "value": "21 2nd Street"},
        ]

        assert resx == self.jsonpatchlist 
        pass

    def testCase110(self):

        self.jsonpatchlist = JSONPatch()

        self.jsonpatchlist = \
              JSONPatchItem("test", "/address/streetAddress", "21 2nd Street") \
            + JSONPatchItem("test", "/address/city", "New York") \
            + JSONPatchItem("test", "/address/houseNumber", 12) \
            + self.jsonpatchlist 

        resx = [
          {"op": "test", "path": "/address/streetAddress", "value": "21 2nd Street"},
          {"op": "test", "path": "/address/city", "value": "New York"},
          {"op": "test", "path": "/address/houseNumber", "value": 12}
        ]
 
        assert resx == self.jsonpatchlist 
        pass

    def testCase120(self):

        self.jsonpatchlist = JSONPatch()

        self.jsonpatchlist = \
            JSONPatchItem("test", "/address/houseNumber", 12) \
            +  self.jsonpatchlist

        self.jsonpatchlist = \
            JSONPatchItem("test", "/address/city", "New York") \
            +  self.jsonpatchlist

        self.jsonpatchlist = \
            JSONPatchItem("test", "/address/streetAddress", "21 2nd Street") \
            +  self.jsonpatchlist

        resx = [
          {"op": "test", "path": "/address/streetAddress", "value": "21 2nd Street"},
          {"op": "test", "path": "/address/city", "value": "New York"},
          {"op": "test", "path": "/address/houseNumber", "value": 12}
        ]
        assert resx == self.jsonpatchlist 
        pass

    def testCase200(self):
        self.jsonpatchlist = JSONPatch()

        self.jsonpatchlist = \
              JSONPatchItem("test", "/address/streetAddress", "21 2nd Street") \
            + JSONPatchItem("test", "/address/city", "New York") \
            + JSONPatchItem("test", "/address/houseNumber", 12) \
            \
            + JSONPatchItem("test", "/phoneNumber/0/type", "home0") \
            + JSONPatchItem("test", "/phoneNumber/0/number", "000") \
            + JSONPatchItem("test", "/phoneNumber/1/type", "home1") \
            + JSONPatchItem("test", "/phoneNumber/1/number", "111") \
            + JSONPatchItem("test", "/phoneNumber/2/type", "office") \
            + JSONPatchItem("test", "/phoneNumber/2/number", "222") \
            + JSONPatchItem("test", "/phoneNumber/3/type", "holidays") \
            + JSONPatchItem("test", "/phoneNumber/3/number", "333") \
            \
            + JSONPatchItem("test", "/customers/domestic/0/name", "customer0") \
            + JSONPatchItem("test", "/customers/domestic/0/industries", "construction") \
            + JSONPatchItem("test", "/customers/domestic/0/products/0/name", "excavator") \
            + JSONPatchItem("test", "/customers/domestic/0/products/0/quantities", 2) \
            + JSONPatchItem("test", "/customers/domestic/0/products/0/priority", 0) \
            + JSONPatchItem("test", "/customers/domestic/0/products/1/name", "shovel") \
            + JSONPatchItem("test", "/customers/domestic/0/products/1/quantities", 2000) \
            + JSONPatchItem("test", "/customers/domestic/0/products/1/priority", 3) \
            \
            + JSONPatchItem("test", "/customers/domestic/1/name", "customer1") \
            + JSONPatchItem("test", "/customers/domestic/1/industries", "telecommunications") \
            + JSONPatchItem("test", "/customers/domestic/1/products/0/name", "phone") \
            + JSONPatchItem("test", "/customers/domestic/1/products/0/quantities", 20) \
            + JSONPatchItem("test", "/customers/domestic/1/products/0/priority", 0) \
            + JSONPatchItem("test", "/customers/domestic/1/products/1/name", "smartphone") \
            + JSONPatchItem("test", "/customers/domestic/1/products/1/quantities", 200) \
            + JSONPatchItem("test", "/customers/domestic/1/products/1/priority", 0) \
            \
            + JSONPatchItem("test", "/customers/domestic/2/name", "customer2") \
            + JSONPatchItem("test", "/customers/domestic/2/industries", "informationtechnology") \
            + JSONPatchItem("test", "/customers/domestic/2/products/0/name", "desktoppc") \
            + JSONPatchItem("test", "/customers/domestic/2/products/0/quantities", 200) \
            + JSONPatchItem("test", "/customers/domestic/2/products/0/priority", 0) \
            + JSONPatchItem("test", "/customers/domestic/2/products/1/name", "keyboard") \
            + JSONPatchItem("test", "/customers/domestic/2/products/1/quantities", 2000) \
            + JSONPatchItem("test", "/customers/domestic/2/products/1/priority", 0) \
            + JSONPatchItem("test", "/customers/domestic/2/products/1/name", "mouse") \
            + JSONPatchItem("test", "/customers/domestic/2/products/1/quantities", 2000) \
            + JSONPatchItem("test", "/customers/domestic/2/products/1/priority", 0) \
            \
            + JSONPatchItem("test", "/customers/abroad/2/name", "customer0") \
            + JSONPatchItem("test", "/customers/abroad/2/industries", "food") \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/name", "juice") \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/quantities", 20000) \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/priority", 3) \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/name", "coffee") \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/quantities", 2000) \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/priority", 3) \
            \
            + JSONPatchItem("test", "/customers/abroad/2/name", "customer1") \
            + JSONPatchItem("test", "/customers/abroad/2/industries", "construction") \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/name", "screwdriver") \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/quantities", 2) \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/priority", 6) \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/name", "screw") \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/quantities", 2000) \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/priority", 6) \
            \
            + JSONPatchItem("test", "/customers/abroad/2/name", "customer2") \
            + JSONPatchItem("test", "/customers/abroad/2/industries", "informationtechnology") \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/name", "pc") \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/quantities", 2) \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/priority", 6) \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/name", "informationtechnology") \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/quantities", 200) \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/priority", 6) \
            + self.jsonpatchlist

        resx = [
          {"op": "test", "path": "/address/streetAddress", "value": "21 2nd Street"},
          {"op": "test", "path": "/address/city", "value": "New York"},
          {"op": "test", "path": "/address/houseNumber", "value": 12},
          {"op": "test", "path": "/phoneNumber/0/type", "value": "home0"},
          {"op": "test", "path": "/phoneNumber/0/number", "value": "000"},
          {"op": "test", "path": "/phoneNumber/1/type", "value": "home1"},
          {"op": "test", "path": "/phoneNumber/1/number", "value": "111"},
          {"op": "test", "path": "/phoneNumber/2/type", "value": "office"},
          {"op": "test", "path": "/phoneNumber/2/number", "value": "222"},
          {"op": "test", "path": "/phoneNumber/3/type", "value": "holidays"},
          {"op": "test", "path": "/phoneNumber/3/number", "value": "333"},
          {"op": "test", "path": "/customers/domestic/0/name", "value": "customer0"},
          {"op": "test", "path": "/customers/domestic/0/industries", "value": "construction"},
          {"op": "test", "path": "/customers/domestic/0/products/0/name", "value": "excavator"},
          {"op": "test", "path": "/customers/domestic/0/products/0/quantities", "value": 2},
          {"op": "test", "path": "/customers/domestic/0/products/0/priority", "value": 0},
          {"op": "test", "path": "/customers/domestic/0/products/1/name", "value": "shovel"},
          {"op": "test", "path": "/customers/domestic/0/products/1/quantities", "value": 2000},
          {"op": "test", "path": "/customers/domestic/0/products/1/priority", "value": 3},
          {"op": "test", "path": "/customers/domestic/1/name", "value": "customer1"},
          {"op": "test", "path": "/customers/domestic/1/industries", "value": "telecommunications"},
          {"op": "test", "path": "/customers/domestic/1/products/0/name", "value": "phone"},
          {"op": "test", "path": "/customers/domestic/1/products/0/quantities", "value": 20},
          {"op": "test", "path": "/customers/domestic/1/products/0/priority", "value": 0},
          {"op": "test", "path": "/customers/domestic/1/products/1/name", "value": "smartphone"},
          {"op": "test", "path": "/customers/domestic/1/products/1/quantities", "value": 200},
          {"op": "test", "path": "/customers/domestic/1/products/1/priority", "value": 0},
          {"op": "test", "path": "/customers/domestic/2/name", "value": "customer2"},
          {"op": "test", "path": "/customers/domestic/2/industries", "value": "informationtechnology"},
          {"op": "test", "path": "/customers/domestic/2/products/0/name", "value": "desktoppc"},
          {"op": "test", "path": "/customers/domestic/2/products/0/quantities", "value": 200},
          {"op": "test", "path": "/customers/domestic/2/products/0/priority", "value": 0},
          {"op": "test", "path": "/customers/domestic/2/products/1/name", "value": "keyboard"},
          {"op": "test", "path": "/customers/domestic/2/products/1/quantities", "value": 2000},
          {"op": "test", "path": "/customers/domestic/2/products/1/priority", "value": 0},
          {"op": "test", "path": "/customers/domestic/2/products/1/name", "value": "mouse"},
          {"op": "test", "path": "/customers/domestic/2/products/1/quantities", "value": 2000},
          {"op": "test", "path": "/customers/domestic/2/products/1/priority", "value": 0},
          {"op": "test", "path": "/customers/abroad/2/name", "value": "customer0"},
          {"op": "test", "path": "/customers/abroad/2/industries", "value": "food"},
          {"op": "test", "path": "/customers/abroad/2/products/0/name", "value": "juice"},
          {"op": "test", "path": "/customers/abroad/2/products/0/quantities", "value": 20000},
          {"op": "test", "path": "/customers/abroad/2/products/0/priority", "value": 3},
          {"op": "test", "path": "/customers/abroad/2/products/1/name", "value": "coffee"},
          {"op": "test", "path": "/customers/abroad/2/products/1/quantities", "value": 2000},
          {"op": "test", "path": "/customers/abroad/2/products/1/priority", "value": 3},
          {"op": "test", "path": "/customers/abroad/2/name", "value": "customer1"},
          {"op": "test", "path": "/customers/abroad/2/industries", "value": "construction"},
          {"op": "test", "path": "/customers/abroad/2/products/0/name", "value": "screwdriver"},
          {"op": "test", "path": "/customers/abroad/2/products/0/quantities", "value": 2},
          {"op": "test", "path": "/customers/abroad/2/products/0/priority", "value": 6},
          {"op": "test", "path": "/customers/abroad/2/products/1/name", "value": "screw"},
          {"op": "test", "path": "/customers/abroad/2/products/1/quantities", "value": 2000},
          {"op": "test", "path": "/customers/abroad/2/products/1/priority", "value": 6},
          {"op": "test", "path": "/customers/abroad/2/name", "value": "customer2"},
          {"op": "test", "path": "/customers/abroad/2/industries", "value": "informationtechnology"},
          {"op": "test", "path": "/customers/abroad/2/products/0/name", "value": "pc"},
          {"op": "test", "path": "/customers/abroad/2/products/0/quantities", "value": 2},
          {"op": "test", "path": "/customers/abroad/2/products/0/priority", "value": 6},
          {"op": "test", "path": "/customers/abroad/2/products/1/name", "value": "informationtechnology"},
          {"op": "test", "path": "/customers/abroad/2/products/1/quantities", "value": 200},
          {"op": "test", "path": "/customers/abroad/2/products/1/priority", "value": 6}
        ]

        # print("4TEST:\n" + str(self.jsonpatchlist))
        
        assert resx == self.jsonpatchlist 
        pass

        

if __name__ == '__main__':
    unittest.main()
