"""Add an existing entry again.
"""

from __future__ import absolute_import

import unittest
import os
import sys

from filesysobjects.configdata import ConfigPath
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata import MS_OFF, MS_DRAFT4, V3K
from jsondata.jsonpointer import JSONPointer

if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
else:
    import json as myjson
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

    def testCase000(self):
        self.maxDiff = None

        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('testdata.json')
        schemafile = _cp.get_config_filepath('testdata.jsd')
        configdata = ConfigData(
            [],
            datafile=datafile,
            schemafile=schemafile,
            validator=MS_OFF,
            )

        oout = sys.stdout
        sys.stdout = StringIO()
        res = configdata.dump_schema(sort_keys=True)
        print(res)
        sout = sys.stdout.getvalue()
        sys.stdout = oout
        conf_out = u"""{
    "$schema": "http://json-schema.org/draft-03/schema",
    "items": {
        "city": {
            "required": true,
            "type": "string"
        },
        "houseNumber": {
            "required": true,
            "type": "number"
        },
        "phoneNumber": {
            "required": true,
            "type": "string"
        },
        "streetAddress": {
            "required": true,
            "type": "string"
        }
    },
    "required": true,
    "type": "array"
}
"""

#         print("4TEST:" + str(sout))
#         print("4TEST:" + str(conf_out))

#         resXHex  = ' '.join(hex(ord(x)) for x in sout)
#         resXChar = '    '.join(x for x in conf_out)
#         resHex   = ' '.join(hex(ord(x)) for x in sout)
#         resChar  = '    '.join(x for x in conf_out)
#         print("4TEST:arg     = " + str(arg))
#         print("4TEST:argEsc  = " + str(argEsc))
#         print("4TEST:resX    = " + str(resX))
#         print("4TEST:res     = " + str(res))
#         print()
#         print("4TEST:resXHex = " + str(resXHex))
#         print("4TEST:resHex  = " + str(resHex))
#         print("4TEST:resChar = " + str(resXChar))
#         print("4TEST:resChar = " + str(resChar))

        import re
        self.assertEqual(re.sub(r'[ \t\n\r]', '', conf_out), re.sub(r'[ \t\n\r]', '', sout))


if __name__ == '__main__':
    unittest.main()
