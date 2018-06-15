"""Import of branches by jsondata.jsondataserializer.branch_import().
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

from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_DRAFT4, B_ADD
from jsondata import JSONDataKeyError, JSONDataNodeTypeError


class CallUnits(unittest.TestCase):
    """Base branch import by branch_add.
    """

    @classmethod
    def setUpClass(cls):
        super(CallUnits, cls).setUpClass()

        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('datafile.json')
        schemafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('schema.jsd')

        _cp = ConfigPath(replace=os.path.dirname(__file__))
        
        cls.configdata = ConfigData(
            {},
            datafile=datafile,
            schemafile=schemafile,
            validator=MS_DRAFT4,
            )

        resx = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                'phoneNumber': [{'type': 'home', 'number': '212 555-1234'},
                                {'type': 'office', 'number': '313 444-555'},
                                {'type': 'mobile', 'number': '777 666-555'}]}

        assert cls.configdata.data == resx


    def testCase500(self):

        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch0.json')
        schema = {
            'phoneNumber': self.configdata.schema['properties']['phoneNumber']
        }

        kargs = {}
        kargs['schema'] = schema
        kargs['validator'] = MS_DRAFT4
        # kargs['mechanic'] = B_ADD

        target = self.configdata.data['phoneNumber']
        ret = self.configdata.json_import(datafile, target, '-', **kargs)
        assert ret == True

        # expected - after branch_add_only the same state as before
        conf_dat = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                    'phoneNumber': [{'type': 'home', 'number': '212 555-1234'},
                                    {'type': 'office', 'number': '313 444-555'},
                                    {'type': 'mobile', 'number': '777 666-555'},
                                    {'type': 'home', 'number': '111 222-333'}]}
        assert self.configdata.data == conf_dat

    def testCase501(self):

        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber': self.configdata.schema['properties']['phoneNumber']
        }
        kargs = {}
        kargs['schema'] = schema
        kargs['validator'] = MS_DRAFT4
        # kargs['mechanic'] = B_ADD

        target = self.configdata.data['phoneNumber']
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch1.json')
        ret = self.configdata.json_import(datafile, target, '-', **kargs)
        assert ret == True

        conf_dat = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                    'phoneNumber': [{'type': 'home', 'number': '212 555-1234'},
                                    {'type': 'office', 'number': '313 444-555'},
                                    {'type': 'mobile', 'number': '777 666-555'},
                                    {'type': 'home', 'number': '111 222-333'},
                                    {'type': 'home2', 'number': '222 222-333'}]}

        assert self.configdata.data == conf_dat

    def testCase502(self):

        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber': self.configdata.schema['properties']['phoneNumber']
        }

        kargs = {}
        kargs['schema'] = schema
        kargs['validator'] = MS_DRAFT4
        # kargs['mechanic'] = B_ADD

        target = self.configdata.data['phoneNumber']
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch2.json')
        ret = self.configdata.json_import(datafile, target, 0, **kargs)
        assert ret == True

        conf_dat = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                    'phoneNumber': [{'type': 'home2', 'number': '333 222-333'},
                                    {'type': 'office', 'number': '313 444-555'},
                                    {'type': 'mobile', 'number': '777 666-555'}, 
                                    {'type': 'home', 'number': '111 222-333'},
                                    {'type': 'home2', 'number': '222 222-333'}]}

        assert self.configdata.data == conf_dat

    def testCase510(self):

        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber': self.configdata.schema['properties']['phoneNumber']
        }

        kargs = {}
        kargs['schema'] = schema
        kargs['validator'] = MS_DRAFT4
        # kargs['mechanic'] = B_ADD

        target = self.configdata.data  # ['phoneNumber']
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch2.json')
        ret = self.configdata.json_import(
            datafile, target, 'phoneNumber', **kargs)
        assert ret == True

        conf_dat = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                    'phoneNumber': {'type': 'home2', 'number': '333 222-333'}}
        assert self.configdata.data == conf_dat

    def testCase511(self):

        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber': self.configdata.schema['properties']['phoneNumber']
        }

        kargs = {}
        kargs['schema'] = schema
        kargs['validator'] = MS_DRAFT4
        # kargs['mechanic'] = B_ADD

        target = self.configdata.data['phoneNumber']
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch2.json')
        ret = self.configdata.json_import(datafile, target, **kargs)
        assert ret == True

        conf_dat = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                    'phoneNumber': {'type': 'home2', 'number': '333 222-333'}}
        assert self.configdata.data == conf_dat


if __name__ == '__main__':
    unittest.main()
