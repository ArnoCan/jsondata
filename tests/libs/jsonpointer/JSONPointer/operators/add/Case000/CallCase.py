"""Basic operator tests for: __add__
"""
from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
else:
    import json as myjson
import jsonschema


from jsondata.jsonpointer import JSONPointer
from jsondata.jsonpatch import JSONPatch, JSONPatchItem
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF

# name of application, used for several filenames as MS_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME
#
#######################
#


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

        
        #
        # validate
        #

        self.jsonpatchlist = JSONPatch()
#         self.jsonpatchlist += JSONPatchItem(
#             "add", "/a100", "v100")
# 
#         self.jsonpatchlist += JSONPatchItem(
#             "copy", "/a200", "/a100")
# 
#         self.jsonpatchlist += JSONPatchItem(
#             "replace", "/a100", 99)

        self.jsonpatchlist += \
              JSONPatchItem("test", "/address/streetAddress", "21 2nd Street") \
            + JSONPatchItem("test", "/address/city", "New York") \
            + JSONPatchItem("test", "/address/houseNumber", 12) \
            + JSONPatchItem("test", "/phoneNumber/0/type", "home0") \
            + JSONPatchItem("test", "/phoneNumber/0/number", "000") \
            + JSONPatchItem("test", "/phoneNumber/1/type", "home1") \
            + JSONPatchItem("test", "/phoneNumber/1/number", "111") \
            + JSONPatchItem("test", "/phoneNumber/2/type", "office") \
            + JSONPatchItem("test", "/phoneNumber/2/number", "222") \
            + JSONPatchItem("test", "/phoneNumber/3/type", "holidays") \
            + JSONPatchItem("test", "/phoneNumber/3/number", "333") \
            + JSONPatchItem("test", "/customers/domestic/0/name", "customer0") \
            + JSONPatchItem("test", "/customers/domestic/0/industries", "construction") \
            + JSONPatchItem("test", "/customers/domestic/0/products/0/name", "excavator") \
            + JSONPatchItem("test", "/customers/domestic/0/products/0/quantities", 2) \
            + JSONPatchItem("test", "/customers/domestic/0/products/0/priority", 0) \
            + JSONPatchItem("test", "/customers/domestic/0/products/1/name", "shovel") \
            + JSONPatchItem("test", "/customers/domestic/0/products/1/quantities", 2000) \
            + JSONPatchItem("test", "/customers/domestic/0/products/1/priority", 3) \
            + JSONPatchItem("test", "/customers/domestic/1/name", "customer1") \
            + JSONPatchItem("test", "/customers/domestic/1/industries", "telecommunications") \
            + JSONPatchItem("test", "/customers/domestic/1/products/0/name", "phone") \
            + JSONPatchItem("test", "/customers/domestic/1/products/0/quantities", 20) \
            + JSONPatchItem("test", "/customers/domestic/1/products/0/priority", 0) \
            + JSONPatchItem("test", "/customers/domestic/1/products/1/name", "smartphone") \
            + JSONPatchItem("test", "/customers/domestic/1/products/1/quantities", 200) \
            + JSONPatchItem("test", "/customers/domestic/1/products/1/priority", 0) \
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
            + JSONPatchItem("test", "/customers/abroad/2/name", "customer0") \
            + JSONPatchItem("test", "/customers/abroad/2/industries", "food") \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/name", "juice") \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/quantities", 20000) \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/priority", 3) \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/name", "coffee") \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/quantities", 2000) \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/priority", 3) \
            + JSONPatchItem("test", "/customers/abroad/2/name", "customer1") \
            + JSONPatchItem("test", "/customers/abroad/2/industries", "construction") \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/name", "screwdriver") \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/quantities", 2) \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/priority", 6) \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/name", "screw") \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/quantities", 2000) \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/priority", 6) \
            + JSONPatchItem("test", "/customers/abroad/2/name", "customer2") \
            + JSONPatchItem("test", "/customers/abroad/2/industries", "informationtechnology") \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/name", "pc") \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/quantities", 2) \
            + JSONPatchItem("test", "/customers/abroad/2/products/0/priority", 6) \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/name", "informationtechnology") \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/quantities", 200) \
            + JSONPatchItem("test", "/customers/abroad/2/products/1/priority", 6)

        n, err = self.jsonpatchlist.apply(self.configdata)

#         print("4TEST:" + str(self.configdata))
#         print("4TEST:n   = " + str(n))
#         print("4TEST:err = " + str(JSONPatch(self.jsonpatchlist.getpatchitems(*err, idxlist=True))))

        ref = {"foo": "bar", "a100": "99", "a200": "v100"}
        assert n == 62
        assert err ==  [35, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 51, 44, 59]

        
        self.record_check()

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

    def testCase100(self):
        jsonptr = JSONPointer('/address/streetAddress')
        if not jsonptr:
            raise BaseException("Failed to create JSONPointer")

        jsonptrdata = jsonptr.get_node_value(self.configdata.data)
        jsx = str(jsonptrdata)
        assert jsx == self.configdata.data["address"]["streetAddress"]

        

if __name__ == '__main__':
    unittest.main()
