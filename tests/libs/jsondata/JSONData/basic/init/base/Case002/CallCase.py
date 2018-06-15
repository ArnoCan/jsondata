"""Load and validate JSON data from files.
Access to in-memory storage of schema for validation.
Read entries.
"""
from __future__ import absolute_import
from __future__ import print_function

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
else:
    import json as myjson
import jsonschema

from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_DRAFT4
from filesysobjects.configdata import ConfigPath


class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.maxDiff = None

        self.cp = ConfigPath(replace=os.path.dirname(__file__))
        self.datafile = self.cp.get_config_filepath('testdata.json')

        self.cdata = [
            {u'phoneNumber': u'212 555-1234'},
            {u'city': u'New York'},
            {u'streetAddress': u'21 2nd Street'},
            {u'houseNumber': 12}
        ]

    def testCase000(self):

        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('testdata.json')
        schemafile = _cp.get_config_filepath('testdata.jsd')
        configdata = ConfigData(
            [],
            schemafile=schemafile,
            datafile=datafile,
            validator=MS_DRAFT4,
            )
        self.assertEqual(str(configdata.data), str(self.cdata))

        conf_schema = {u'items': {u'city': {u'required': True, u'type': u'string'}, u'streetAddress': {u'required': True, u'type': u'string'}, u'houseNumber': {u'required': True, u'type': u'number'}, u'phoneNumber': {u'required': True, u'type': u'string'}}, u'$schema': u'http://json-schema.org/draft-03/schema', u'required': True, u'type': u'array'}

        self.assertEqual(configdata.schema, conf_schema)


if __name__ == '__main__':
    unittest.main()
