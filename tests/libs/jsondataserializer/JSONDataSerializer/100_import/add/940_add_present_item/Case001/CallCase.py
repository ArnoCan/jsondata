"""Import of branches by jsondata.jsondataserializer.branch_import().
"""

from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport @UnusedImport pylint: disable=import-error
else:
    import json as myjson  # @Reimport @UnusedImport
import jsonschema


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

        # partial schema for branch
        schema = {
            'phoneNumber': self.configdata.schema['properties']['phoneNumber']}

        kargs = {}
        kargs['schema'] = schema
        kargs['validator'] = MS_DRAFT4
        kargs['mechanic'] = B_ADD

        target = self.configdata.data
        self.configdata.json_import(datafile, target, 'phoneNumber', **kargs)

        # Expected the nodes within the datafile to be removed.
        # No content is checked, just the complete tree is removed.
        # conf_dat = repr(self.configdata.data)
        conf_dat = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                    'phoneNumber': {'phoneNumber': [{'type': 'home', 'number': '111 222-333'}]}}
        assert self.configdata.data == conf_dat


#
#######################
#
if __name__ == '__main__':
    unittest.main()
