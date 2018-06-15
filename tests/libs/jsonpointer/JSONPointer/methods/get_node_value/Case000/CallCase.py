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
        datafile = _cp.get_config_filepath('testdata.json')
        schemafile = _cp.get_config_filepath('testdata.jsd')
        self.configdata = ConfigData(
            {},
            datafile=datafile,
            schemafile=schemafile,
            validator=MS_OFF,
            )

    def testCase000(self):

        # data
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('testdata.json')
        if not os.path.isfile(datafile):
            raise BaseException("Missing JSON data:file=" + str(datafile))
        # load data
        with open(datafile) as data_file:
            jval = myjson.load(data_file)
        if jval == None:
            raise BaseException("Failed to load data:" + str(data_file))

        jval = jval
        assert jval

    def testCase900(self):

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

    def testCase901(self):
        assert self.configdata.data["phoneNumber"][0]["type"] == "home0"
        assert self.configdata.data["phoneNumber"][0]["type"] == JSONPointer(
            '/phoneNumber/0/type').get_node_value(self.configdata.data)

    def testCase902(self):
        assert self.configdata.data["phoneNumber"][0]["number"] == "000"
        assert self.configdata.data["phoneNumber"][0]["number"] == JSONPointer(
            '/phoneNumber/0/number').get_node_value(self.configdata.data)

    def testCase910(self):
        assert self.configdata.data["phoneNumber"][0]["number"] == "000"
        assert self.configdata.data["phoneNumber"][0]["number"] == JSONPointer(
            '/phoneNumber/0/number').get_node_value(self.configdata.data)

#
#######################
#
if __name__ == '__main__':
    unittest.main()
