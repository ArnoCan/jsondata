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
from jsondata  import MS_DRAFT4, V3K
# from jsondata.jsondata import JSONData
from filesysobjects.configdata import ConfigPath

if V3K:
    from io import StringIO
else:
    from StringIO import StringIO

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

        self.oout = sys.stdout
        sys.stdout = StringIO()
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)

        sys.stdout = self.oout

    def testCase000(self):

        with open(self.datafile) as data_file:
            self.jval = myjson.load(data_file)
        if self.jval == None:
            raise BaseException("Failed to load data:" + str(data_file))

        assert self.cdata == self.jval

    def testCase010(self):
        self.jval = []

        schemafile = self.cp.get_config_filepath('testdata.jsd')
        configdata = ConfigData(
            self.jval,
            schemafile=schemafile,
            datafile=self.datafile,
            validator=MS_DRAFT4,
            )
        assert self.jval == self.cdata
        assert configdata.data ==self.cdata

        res = configdata.dump_data(False, sort_keys=True)
        conf_out = u"""[{"phoneNumber": "212 555-1234"}, {"city": "New York"}, {"streetAddress": "21 2nd Street"}, {"houseNumber": 12}]"""

        self.assertEqual(conf_out, res)

        kargs = {'sourcefile': os.path.dirname(
            __file__) + os.sep + "testdata.jsd"}
        res = configdata.dump_schema(False, sort_keys=True, **kargs)
        print(res)
        sout = sys.stdout.getvalue()
        conf_out = """{"$schema": "http://json-schema.org/draft-03/schema", "items": {"city": {"required": true, "type": "string"}, "houseNumber": {"required": true, "type": "number"}, "phoneNumber": {"required": true, "type": "string"}, "streetAddress": {"required": true, "type": "string"}}, "required": true, "type": "array"}
"""

        import re
        self.assertEqual(re.sub(r'[ \t\n\r]', '', conf_out), re.sub(r'[ \t\n\r]', '', sout))


if __name__ == '__main__':
    unittest.main()
