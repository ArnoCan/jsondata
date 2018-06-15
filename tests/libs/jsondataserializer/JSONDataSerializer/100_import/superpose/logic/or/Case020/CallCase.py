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

# import 'jsondata'
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_DRAFT4, B_OR
# from jsondata import JSONDataKeyError, JSONDataNodeTypeError

# name of application, used for several filenames as MS_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME


class CallUnits(unittest.TestCase):
    """Base branch import by branch_add.
    """

    def setUp(self):
        """Load initial main/master data, and validate it with standard draft4.
        """
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


    def testCase502(self):
        """Import a branch into initial main/master data, and validate it with branch schema.

        Use insertion point:
          target = configdata.data['phoneNumber']

        for file:
          'branch2.json'
          #---
            {
              "type":"home2",
              "number":"333 222-333"
            }
          #---

        Apply '$schema' key for branch/subtree of master schema.
        """

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
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MS_DRAFT4
        kargs['mechanic'] = B_OR

        # target container
        target = self.configdata.data['phoneNumber']

        # do it...
        # REMARK: schemafile is here None, because we use an in memory schema,
        #         and do not export - for now
        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch1.json')
        ret = self.configdata.json_import(datafile, target, '-', **kargs)
        assert ret == True

        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch2.json')
        ret = self.configdata.json_import(datafile, target, 0, **kargs)
        assert ret == True

        # expected - after branch_add_only the same state as before
        # conf_dat = repr(self.configdata.data)
#         conf_dat = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
#                     'phoneNumber': [{'type': 'home2', 'number': '333 222-333'},
#                                     {'type': 'home', 'number': '212 555-1234'},
#                                     {'type': 'office', 'number': '313 444-555'},
#                                     {'type': 'mobile', 'number': '777 666-555'}, 
#                                     {'type': 'home2', 'number': '222 222-333'}]}
        conf_dat = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                    'phoneNumber': [
                        {'type': 'home2', 'number': '333 222-333'}, 
                        {'type': 'office', 'number': '313 444-555'}, 
                        {'type': 'mobile', 'number': '777 666-555'}, 
                        {'type': 'home2', 'number': '222 222-333'}]
                    }

        # print("4test:configdata.data:" + str(self.configdata.data))
        # print("4test:conf_dat:       " + str(conf_dat))

        self.assertEqual(self.configdata.data, conf_dat)


if __name__ == '__main__':
    unittest.main()
