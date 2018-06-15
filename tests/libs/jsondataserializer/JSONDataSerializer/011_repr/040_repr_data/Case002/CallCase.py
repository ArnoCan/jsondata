from __future__ import absolute_import

import unittest
import os
import sys
from io import StringIO

from filesysobjects.configdata import ConfigPath
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF


class CallUnits(unittest.TestCase):

    def testCase000(self):
        self.maxDiff = None
        
        _cp = ConfigPath(replace=os.path.dirname(__file__))
        
        configdata = ConfigData(
            [],
            datafile=_cp.get_config_filepath('testdata.json'),
            schemafile=_cp.get_config_filepath('testdata.jsd'),
            validator=MS_OFF,
            )

        oout = sys.stdout
        sys.stdout = StringIO()
        configdata.dump_schema()
        sout = sys.stdout.getvalue()
        sys.stdout = oout

        srepr= repr(configdata.schema)
        # print(srepr)
        resx = {
            "$schema": "http://json-schema.org/draft-03/schema", 
            "required": True, 
            "type": "array",
            "items": {
                "city": {"required": True, "type": "string"}, 
                "streetAddress": {"required": True, "type": "string"}, 
                "houseNumber": {"required": True, "type": "number"}, 
                "phoneNumber": {"required": True, "type": "string"}
            }
        } 

        self.assertEqual(configdata.schema, resx)
#        self.assertEqual(str(configdata.schema), str(resx))


if __name__ == '__main__':
    unittest.main()
