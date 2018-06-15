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
        self.datafile = _cp.get_config_filepath('testdata.json')
        self.schemafile = _cp.get_config_filepath('testdata.jsd')
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

    def testCase899(self):
        # in mem
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

    def testCase900(self):
        jp = JSONPointer('/streetAddress')
        jp = '/address' + jp
        jp = JSONPointer(jp)

        # now in one line
        assert self.configdata.data["address"]["streetAddress"] == jp.get_node_value(
            self.configdata.data)

    def testCase901(self):
        jp = '/address' + JSONPointer('/streetAddress')
        jp = JSONPointer(jp)

        # now in one line
        assert self.configdata.data["address"]["streetAddress"] == jp.get_node_value(
            self.configdata.data)

    def testCase902(self):
        jp = JSONPointer('/address' + JSONPointer('/streetAddress'))

        # now in one line
        assert self.configdata.data["address"]["streetAddress"] == jp.get_node_value(
            self.configdata.data)

    def testCase903(self):
        assert self.configdata.data["phoneNumber"][0]["type"] == "home0"

        jp = '/phoneNumber' + JSONPointer('/0') + '/type'
        assert self.configdata.data["phoneNumber"][0]["type"] == JSONPointer(
            jp).get_node_value(self.configdata.data)

    def testCase904(self):
        assert self.configdata.data["phoneNumber"][0]["type"] == "home0"

        jp = JSONPointer('/phoneNumber/' + str(0) + JSONPointer('/type'))
        assert self.configdata.data["phoneNumber"][0]["type"] == jp.get_node_value(
            self.configdata.data)

    def testCase905(self):
        assert self.configdata.data["phoneNumber"][0]["type"] == "home0"

        jp = 0 + JSONPointer('/type')
        jp = '/phoneNumber' + jp
        assert self.configdata.data["phoneNumber"][0]["type"] == JSONPointer(
            jp).get_node_value(self.configdata.data)


#
#######################
#
if __name__ == '__main__':
    unittest.main()
