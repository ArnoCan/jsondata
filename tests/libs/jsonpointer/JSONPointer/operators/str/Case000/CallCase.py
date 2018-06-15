# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import unittest
import os
import sys

if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
else:
    import json as myjson
import jsonschema

from jsondata import V3K, JSONPointerError
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF
from jsondata.jsonpatch import JSONPatch, JSONPatchItem
from filesysobjects.configdata import ConfigPath
from jsondata.jsonpointer import JSONPointer

if V3K:
    unicode = str


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

    def testCase010(self):

        jp = JSONPointer('/streetAddress/address')
        assert str(jp) == '/streetAddress/address'

    def testCase020(self):

        jp = JSONPointer('0/streetAddress/address', startrel='/a/b')
        assert str(jp) == '/a/b/streetAddress/address'

    def testCase030(self):

        jp = JSONPointer('1/streetAddress/address', startrel='/a/b')
        assert str(jp) == '/a/streetAddress/address'

    def testCase040(self):

        jp = JSONPointer('2/streetAddress/address', startrel='/a/b')
        assert str(jp) == '/streetAddress/address'

    def testCase050(self):

        try:
            jp = JSONPointer('3/streetAddress/address', startrel='/a/b')
        except JSONPointerError:
            pass
        else:
            raise AssertionError("expected Exception for int-prefix overflow")

if __name__ == '__main__':
    unittest.main()
