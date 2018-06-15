"""Import of new branches by jsondata.jsondataserializer.branch_import().
"""
from __future__ import absolute_import

import unittest
import os
import sys

# pre-set the base JSON libraries for 'jsondata' by PyUnit call
if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
elif 'json' in sys.argv:
    import json as myjson
else:
    import json as myjson
import jsonschema

from filesysobjects.configdata import ConfigPath
from jsondata.jsondata import JSONData

# import 'jsondata'
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF, \
    JSONDataKeyError, JSONDataNodeTypeError, \
    JSONPointerError

from jsondata.jsonpointer import JSONPointer

class CallUnits(unittest.TestCase):
    """Base branch import by branch_add.
    """

    @classmethod
    def setUpClass(cls):

        cls.maxDiff = None

        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('datafile.json')

        _cp = ConfigPath(replace=os.path.dirname(__file__))

        cls.configdata = ConfigData(
            {},
            datafile=datafile,
            validator=MS_OFF,
            )

        resx = {'entry': []}
        assert cls.configdata.data == resx


    def testCase010(self):
        kargs = {}
        target = ''
        key = None
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch0.json')

        ret = self.configdata.json_import(datafile, target, key, **kargs)

        resx = {u'entry': [{u'number': u'123-456'}]}
        
        self.assertEqual(self.configdata.data, resx)

    def testCase020(self):
        kargs = {}
        target = ''
        key = None
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch1.json')

        ret = self.configdata.json_import(datafile, target, key, **kargs)

        resx = {'entry': [{'number': '123-456', 'datatype': 'home2'}]}
        
        self.assertEqual(self.configdata.data, resx)

    def testCase030(self):
        kargs = {}
        target = ''
        key = None
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch2.json')

        ret = self.configdata.json_import(datafile, target, key, **kargs)

        resx = {'entry': [{'number': '123-456', 'datatype': 'home2'}], 'region': 'north'}
        
        self.assertEqual(self.configdata.data, resx)


if __name__ == '__main__':
    unittest.main()
