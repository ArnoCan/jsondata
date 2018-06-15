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
from jsondata  import MS_DRAFT4, B_ADD, \
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
        schemafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('schema.jsd')

        _cp = ConfigPath(replace=os.path.dirname(__file__))

        cls.configdata = ConfigData(
            {},
            datafile=datafile,
            schemafile=schemafile,
            validator=MS_DRAFT4,
            )

        resx = {'entry': []}
        assert cls.configdata.data == resx

        cls.schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            "type":"object",
            "required":True,
            "properties":{
                "entry": {
                    "required":True,
                    "type":"array",
                    "items":{
                        "number": {
                            "type":"string",
                            "required":True
                        },
                        "datatype": {
                            "type":"string",
                            "required":True
                        },
                        "region": {
                            "type":"string",
                            "required":True
                        }
                    }
                }
            }
        }

    def testCase500(self):
        kargs = {}
        kargs['schema'] = self.schema
        kargs['validator'] = MS_DRAFT4
        kargs['mechanic'] = B_ADD

        target = '/'
        key = ''
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch0.json')
        try:
            ret = self.configdata.json_import(datafile, target, key, **kargs)
        except JSONPointerError:
            pass


    def testCase501(self):
        kargs = {}
        kargs['schema'] = self.schema
        kargs['validator'] = MS_DRAFT4
        kargs['mechanic'] = B_ADD

        target = ''
        key = ''
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch0.json')
        ret = self.configdata.json_import(datafile, target, key, **kargs)
        assert ret == True

        conf_dat = {'entry': [{"number":"123-456"}]}
        self.assertEqual(self.configdata.data, conf_dat)

    def testCase502(self):

        kargs = {}
        target = JSONPointer('/entry')  # the whole document - RFC6901 pg.5
        key = '-'
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch1.json')

        kargs['schema'] = self.schema
        kargs['validator'] = MS_DRAFT4
        kargs['subpointer'] = "/entry/0"
        kargs['mechanic'] = B_ADD


        ret = self.configdata.json_import(datafile, target, key, **kargs)
        assert ret == True

        conf_dat = {'entry': [{"number":"123-456"},{"datatype":"home2"}]}
        self.assertEqual(self.configdata.data, conf_dat)

    def testCase510(self):

        # partial schema for branch, use here a subtree of main schema,
        # the entry:
        #    "$schema": "http://json-schema.org/draft-03/schema",
        # seems not to be required,
        #
        # but here just check it
        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            "type":"object",
            "required":True,
            "properties":{
                "region": {
                    "type":"string",
                    "required":True
                }
            }
        }

        # import settings
        kargs = {}
        kargs['schema'] = schema
        kargs['validator'] = MS_DRAFT4
        kargs['mechanic'] = B_ADD

        # target container
        # target = self.configdata.data['entry']
        target = self.configdata['entry']

        # do it...
        # REMARK: schemafile is here None, because we use an in memory schema,
        #         and do not export - for now
        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('branch2.json')
        ret = self.configdata.json_import(datafile, target, '-', **kargs)
        assert ret == True

        # expected - after branch_add failure
        # conf_dat = repr(configdata.data)
        conf_dat = {'entry': [{"number":"123-456"},{"datatype":"home2"},{"region":"north"}]}
        assert self.configdata.data == conf_dat

if __name__ == '__main__':
    unittest.main()
