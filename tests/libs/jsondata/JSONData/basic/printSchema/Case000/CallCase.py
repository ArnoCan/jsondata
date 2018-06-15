"""Load and access data.
"""
from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport @UnusedImport pylint: disable=import-error
else:
    import json as myjson  # @Reimport
import jsonschema  # @UnusedImport

from io import StringIO

from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF, MS_DRAFT4, V3K
from jsondata.jsondata import JSONData
from filesysobjects.configdata import ConfigPath

if V3K:
    from io import StringIO
else:
    from StringIO import StringIO

class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.oout = sys.stdout
        sys.stdout = StringIO()
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)

        sys.stdout = self.oout

    def testCase000(self):

        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('testdata.json')

        with open(datafile) as data_file:
            self.jval = myjson.load(data_file)
        if self.jval == None:
            raise BaseException("Failed to load data:" + str(data_file))

        cdata = [
            {"phoneNumber": "212 555-1234"},
            {"city": "New York"},
            {"streetAddress": "21 2nd Street"},
            {"houseNumber": 12}
        ]
        assert cdata == self.jval

        schemafile = _cp.get_config_filepath('testdata.jsd')
        configdata = ConfigData(
            [],
            schemafile=schemafile,
            datafile=datafile,
            validator=MS_DRAFT4,
            )
        assert self.jval == configdata.data

        res = configdata.dump_data(False, sort_keys=True)
        cdata = """[{"phoneNumber": "212 555-1234"}, {"city": "New York"}, {"streetAddress": "21 2nd Street"}, {"houseNumber": 12}]
"""
        import re
        self.assertEqual(re.sub(r'[ \t\n]', '', str(cdata)), re.sub(r'[ \t\n]', '', str(res)))

        res = configdata.dump_schema(sort_keys=True)
        print(res)
        sout = sys.stdout.getvalue()

        cdata = """{
    "$schema": "http://json-schema.org/draft-03/schema",
    "items":{
        "city": {
            "required":true,
            "type":"string"
        },
        "houseNumber": {
            "required":true,
            "type":"number"
        },
        "phoneNumber": {
            "required":true,
            "type":"string"
        },
        "streetAddress": {
            "required":true,
            "type":"string"
        }
    },
    "required": true,
    "type": "array"
}
"""

        import re
        x0 = re.sub(r'[ \t\n]', '', str(cdata))
        x1 = re.sub(r'[ \t\n]', '', str(sout))

        self.assertEqual(x0, x1)
        pass


if __name__ == '__main__':
    unittest.main()
