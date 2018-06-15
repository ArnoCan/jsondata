"""Load and access data.
"""
from __future__ import absolute_import

import os
import sys
import unittest
import copy


if 'ujson' in sys.argv:
    import ujson as myjson
else:
    import json as myjson
import jsonschema


jval = None

from jsondata.jsondataserializer import JSONDataSerializer as JSONDataLoader
from jsondata  import MS_OFF
from jsondata.jsondata import JSONData, C_DEEP

# name of application, used for several filenames as MS_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME
#
#######################
#


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

        self.poffice = {
            "phoneNumber": [
                {
                    "type": "office",
                    "number": "313 123-456"
                }
            ]
        }

        pass

    def testCase010(self):
        jval = JSONData(self.pframe, copydata=C_DEEP)
        jval.branch_add(self.poffice)
        jval1 = jval()
        assert jval["phoneNumber"] == self.poffice["phoneNumber"]
        assert jval == jval1
        pass

    def testCase011(self):
        jval = JSONData(self.pframe, copydata=C_DEEP)
        jval.branch_add(self.poffice)
        jval1 = JSONData(jval)()
        assert jval["phoneNumber"] == self.poffice["phoneNumber"]
        assert jval == jval1
        pass

#
#######################
#


if __name__ == '__main__':
    unittest.main()
