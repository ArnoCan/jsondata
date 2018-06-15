"""Add an existing entry again.
"""

from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
else:
    import json as myjson
import jsonschema


from filesysobjects.configdata import ConfigPath
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata import MS_OFF, MS_DRAFT4
from jsondata.jsonpointer import JSONPointer


class CallUnits(unittest.TestCase):

    def testCase000(self):
        self.maxDiff = None
        
        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('datafile.json')
        schemafile = _cp.get_config_filepath('schema.jsd')
        configdata = ConfigData(
            {},
            datafile=datafile,
            schemafile=schemafile,
            validator=MS_OFF,
            )

        resx = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                'phoneNumber': [{'type': 'home', 'number': '212 555-1234'},
                                {'type': 'office', 'number': '313 444-555'},
                                {'type': 'mobile', 'number': '777 666-555'}]}

        self.assertEqual(configdata.data, resx) 

        branchfile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch0.json')

        # partial schema for branch
        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber': configdata.schema['properties']['phoneNumber']
        }

        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('branch0.json')
        branchdata = ConfigData(
            {},
            schema=schema,
            datafile=datafile,
            validator=MS_DRAFT4,
            )

        target = configdata.data
        tconf = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                 'phoneNumber': [{'type': 'home', 'number': '212 555-1234'},
                                 {'type': 'office', 'number': '313 444-555'},
                                 {'type': 'mobile', 'number': '777 666-555'}]}
        
        self.assertEqual(target, tconf)

        configdata.branch_add(branchdata['phoneNumber'], target['phoneNumber'])
        configdata.branch_add(branchdata['phoneNumber'][0], target['phoneNumber'], '-')  #pylint: disable=unsubscriptable-object

        conf_dat = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                 'phoneNumber': [{'type': 'home', 'number': '212 555-1234'},
                                 {'type': 'office', 'number': '313 444-555'},
                                 {'type': 'mobile', 'number': '777 666-555'},
                                    {"type": "home", "number": "111 222-333"},
                                    {"type": "home", "number": "111 222-333"}]}

        self.assertEqual(configdata.data, conf_dat)

        target = configdata.data['phoneNumber']
        datafile = os.path.abspath(
            os.path.dirname(__file__)) + os.sep + str('branch2.json')

        ret = configdata.json_import(
            datafile, target, '-')

        self.assertTrue(ret)

        conf_dat = {
            "number": "333 222-333",
            "type": "home2"
        }


        target = configdata.data['phoneNumber']
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch2.json')
        ret = configdata.json_import(
            datafile, target,
            schema=schema,
            validator=MS_DRAFT4
            )

        self.assertTrue(ret)

        
        self.assertEqual(configdata.data, conf_dat)

if __name__ == '__main__':
    unittest.main()




