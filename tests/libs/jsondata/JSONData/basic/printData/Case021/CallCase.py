"""Load and access data.
"""
from __future__ import absolute_import

import unittest
import os
import sys

from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF, MS_DRAFT4, V3K
from jsondata.jsondata import JSONData
from filesysobjects.configdata import ConfigPath

if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport @UnusedImport pylint: disable=import-error
else:
    import json as myjson  # @Reimport
import jsonschema

if V3K:
    from io import StringIO
else:
    from StringIO import StringIO



class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.maxDiff = None

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
        self.assertEqual(cdata, self.jval)

        schemafile = _cp.get_config_filepath('testdata.jsd')
        configdata = ConfigData(
            self.jval,
            schemafile=schemafile,
            datafile=datafile,
            validator=MS_DRAFT4,
            )
        self.assertEqual(self.jval, configdata.data)


#         oout = sys.stdout
#         sys.stdout = StringIO()

        source = open(os.path.dirname(__file__) +
                      os.sep + "testdata.json").read()
        source = myjson.loads(source)
        kargs = {'source': source}
        res = configdata.dump_data(False, sort_keys=True, **kargs)
        print(res)
        sout = sys.stdout.getvalue()
#         sys.stdout = oout
        conf_out = """[{"phoneNumber": "212 555-1234"}, {"city": "New York"}, {"streetAddress": "21 2nd Street"}, {"houseNumber": 12}]
"""
        self.assertEqual(conf_out, sout)


if __name__ == '__main__':
    unittest.main()
