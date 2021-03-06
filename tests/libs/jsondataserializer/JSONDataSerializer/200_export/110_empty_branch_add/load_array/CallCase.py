"""Import of new branches by jsondata.jsondataserializer.branch_import().
"""
from __future__ import absolute_import

import unittest
import os
import sys

# pre-set the base JSON libraries for 'jsondata' by PyUnit call
if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport @UnusedImport pylint: disable=import-error
elif 'json' in sys.argv:
    import json as myjson  # @Reimport @UnusedImport
else:
    import json as myjson  # @Reimport @UnusedImport
import jsonschema  # @UnusedImport

from filesysobjects.configdata import ConfigPath
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_DRAFT4


class CallUnits(unittest.TestCase):

    def setUp(self):

        unittest.TestCase.setUp(self)
        
        self.maxDiff = None

        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('datafile.json')
        schemafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('schema.jsd')

        _cp = ConfigPath(replace=os.path.dirname(__file__))
        
        self.configdata = ConfigData(
            {},
            datafile=datafile,
            schemafile=schemafile,
            validator=MS_DRAFT4,
            )

        resx = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                'phoneNumber': [{'type': 'home', 'number': '212 555-1234'},
                                {'type': 'office', 'number': '313 444-555'},
                                {'type': 'mobile', 'number': '777 666-555'}]}
        assert self.configdata.data == resx

    def testCase500(self):

        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber': self.configdata.schema['properties']['phoneNumber']
        }

        kargs = {}
        kargs['schema'] = schema
        kargs['validator'] = MS_DRAFT4
        target = self.configdata.data['phoneNumber']
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch1.json')
        ret = self.configdata.json_import(datafile, target, '-', **kargs)
        assert ret == True

        conf_dat = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                    'phoneNumber': [{'type': 'home', 'number': '212 555-1234'},
                                    {'type': 'office', 'number': '313 444-555'},
                                    {'type': 'mobile', 'number': '777 666-555'},
                                    {'type': 'home2', 'number': '222 222-333'}]}
        assert self.configdata.data == conf_dat


if __name__ == '__main__':
    unittest.main()
