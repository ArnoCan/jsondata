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

    def testCase900(self):

        # in mem
        assert self.configdata.data["address"]["streetAddress"] == "21 2nd Street"

    def testCase901(self):

        # by pointer
        jsonptr = JSONPointer('/address')
        if not jsonptr:
            raise BaseException("Failed to create JSONPointer")
        jsonptr += 'streetAddress'

        assert jsonptr == u'/address/streetAddress'

    def testCase902(self):

        # now in one line
        assert self.configdata.data["address"]["streetAddress"] == JSONPointer(
            '/address/streetAddress').get_node_value(self.configdata.data)



#
#######################
#
if __name__ == '__main__':
    unittest.main()
