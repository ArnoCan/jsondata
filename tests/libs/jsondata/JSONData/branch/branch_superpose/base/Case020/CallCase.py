from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import unittest

if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport  @UnusedImport pylint: disable=import-error
else:
    import json as myjson  # @Reimport
import jsonschema  # @UnusedImport


from jsondata  import MS_OFF
from jsondata.jsondata import JSONData, C_DEEP, C_REF, C_SHALLOW

_APPNAME = "jsondc"
appname = _APPNAME


class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        # data
        self.datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('testdata.json')
        if not os.path.isfile(self.datafile):
            raise BaseException("Missing JSON data:file=" + str(self.datafile))
        # load data
        with open(self.datafile) as data_file:
            jval = myjson.load(data_file)
        if jval == None:
            raise BaseException("Failed to load data:" + str(data_file))

        cdata = {u'phoneNumber': [
            {u'type': u'home', u'number': u'212 555-1234'}], u'address': {}}
        assert cdata == jval

        # data
        self.kargs = {}
        self.kargs['data'] = jval
        self.kargs['nodefaultpath'] = True
        self.kargs['nosubdata'] = True
        self.kargs['pathlist'] = os.path.dirname(__file__)
        self.kargs['validator'] = MS_OFF

        self.pframe = {
            'address': {}
        }

        self.pframe_org = {
            'address': {}
        }

        self.poffice = {
            "phoneNumber": [
                {
                    "type": "office",
                    "number": "313 123-456"
                }
            ]
        }
        
        self.jsondoc = self.pframe.copy()
        self.jsondoc.update(self.poffice)

    def testCase010(self):
        jval = JSONData(self.pframe)
        jval.branch_add(self.poffice)
        self.assertEqual(self.jsondoc, jval)
        
    def testCase020(self):
        jval = JSONData(self.pframe, copydata=C_REF)
        jval.branch_add(self.poffice)
        self.assertEqual(self.jsondoc, jval)

    def testCase030(self):
        jval = JSONData(self.pframe, copydata=C_DEEP)
        jval.branch_add(self.poffice)
        self.assertEqual(self.jsondoc, jval)

    def testCase040(self):
        jval = JSONData(self.pframe, copydata=C_SHALLOW)
        jval.branch_add(self.poffice)
        self.assertEqual(self.jsondoc, jval)

if __name__ == '__main__':
    unittest.main()
