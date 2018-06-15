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
        jp = JSONPointer('/address')
        jp = jp + 'streetAddress'
        # now in one line
        assert jp == '/address/streetAddress'

    def testCase901(self):
        jp = JSONPointer('/address') + 'streetAddress'
        # now in one line
        assert jp == '/address/streetAddress'

    def testCase902(self):
        assert self.configdata.data["phoneNumber"][0]["type"] == "home0"

        jp = JSONPointer('/phoneNumber') + 0 + 'type'
        assert jp == '/phoneNumber/0/type'

    def testCase903(self):
        assert self.configdata.data["phoneNumber"][0]["type"] == "home0"

        jp = JSONPointer('/phoneNumber') + 0
        jp = jp + 'type'
        assert jp == '/phoneNumber/0/type'

    def testCase904(self):
        assert self.configdata.data["phoneNumber"][0]["number"] == "000"
        jp = JSONPointer('/phoneNumber') + 0 + 'number'
        assert jp == '/phoneNumber/0/number'



#
#######################
#
if __name__ == '__main__':
    unittest.main()
