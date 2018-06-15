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
from jsondata  import MS_DRAFT4
from jsondata.jsonpatch import JSONPatch, JSONPatchItem
from filesysobjects.configdata import ConfigPath
from jsondata.jsonpointer import JSONPointer


class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('datafile.json')
        schemafile = _cp.get_config_filepath('schema.jsd')
        self.configdata = ConfigData(
            {},
            datafile=datafile,
            schemafile=schemafile,
            validator=MS_DRAFT4,
            )

    def testCase900(self):

        conf_dat = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 'phoneNumber': [{'type': 'home', 'number': '212 555-1234'}]}
        # print(repr(configdata.data))
        assert self.configdata.data == conf_dat

    def testCase007(self):

        conf_schema = {'$schema': 'http://json-schema.org/draft-03/schema', '_comment': 'This is a comment to be dropped by the initial scan:object(0)', '_doc': 'Concatenated for the same instance.:object(0)', 'type': 'object', 'required': False, 'properties': {'address': {'_comment': 'This is a comment(0):address', 'type': 'object', 'required': True, 'properties': {'city': {'type': 'string', 'required': True}, 'houseNumber': {'type': 'number', 'required': False}, 'streetAddress': {'type': 'string', 'required': True}}}, 'phoneNumber': {'_comment': 'This is a comment(1):array', 'type': 'array', 'required': False, 'items': {'type': 'object', 'required': False, 'properties': {'number': {'type': 'string', 'required': False}, 'type': {'type': 'string', 'required': False}}}}}}
        
        # print(repr(configdata.schema))
        assert self.configdata.schema == conf_schema


#
#######################
#
if __name__ == '__main__':
    unittest.main()
