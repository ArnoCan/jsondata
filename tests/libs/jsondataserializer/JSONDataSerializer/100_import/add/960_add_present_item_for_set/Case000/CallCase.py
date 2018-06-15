"""Import of branches by jsondata.jsondataserializer.branch_import().
"""
from __future__ import absolute_import

import unittest
import os
import sys

#
if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport @UnusedImport pylint: disable=import-error
else:
    import json as myjson  # @Reimport @UnusedImport
import jsonschema  # @UnusedImport

from filesysobjects.configdata import ConfigPath

from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_DRAFT4, B_ADD

# name of application, used for several filenames as MS_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME
#
#######################
#


class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

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

    def testCase100(self):

        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch0.json')

        # partial schema for branch, use here a subtree of main schema,
        # the entry:
        #    "$schema": "http://json-schema.org/draft-03/schema",
        # seems not to be required, else it has to be included
        schema = {
            'phoneNumber': self.configdata.schema['properties']['phoneNumber']}

        # import settings
        kargs = {}
        kargs['schema'] = schema
        kargs['validator'] = MS_DRAFT4
        kargs['mechanic'] = B_ADD

        # target container
        target = self.configdata.data

        # do it...
        # REMARK: schemafile is here None, because we use an in memory schema,
        #         and do not export - for now
        self.configdata.json_import(datafile, target, **kargs)

        # expected - after branch_replace-set
        conf_dat = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                    'phoneNumber': [{'type': 'home', 'number': '111 222-333'}]}

        assert self.configdata.data == conf_dat

    def testCase200(self):

        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch0.json')

        # partial schema for branch, use here a subtree of main schema,
        # the entry:
        #    "$schema": "http://json-schema.org/draft-03/schema",
        # seems not to be required,
        #
        # but here just check it
        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber': self.configdata.schema['properties']['phoneNumber']
        }

        # import settings
        kargs = {}
        kargs['schema'] = schema
        kargs['validator'] = MS_DRAFT4
        kargs['mechanic'] = B_ADD

        # target container
        target = self.configdata.data

        # do it...
        # REMARK: schemafile is here None, because we use an in memory schema,
        #         and do not export - for now
        self.configdata.json_import(datafile, target, **kargs)

        # expected - after branch_replace-set
        conf_dat = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                    'phoneNumber': [{'type': 'home', 'number': '111 222-333'}]}
        assert self.configdata.data == conf_dat


if __name__ == '__main__':
    unittest.main()
