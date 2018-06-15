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
from jsondata.jsondata import JSONData, C_REF, C_DEEP, C_SHALLOW

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

        cdata = {u'phoneNumber':
                 [
                     {u'type': u'office', u'number': u'313 123-456'},
                     {u'type': u'office', u'number': u'444 444-444'}
                 ],
                 u'address': {}
                 }
        assert cdata == jval

        # data
        self.kargs = {}
        self.kargs['data'] = jval
        self.kargs['nodefaultpath'] = True
        self.kargs['nosubdata'] = True
        self.kargs['pathlist'] = os.path.dirname(__file__)
        self.kargs['validator'] = MS_OFF

        self.pframe = {'address': cdata['address']}
        self.pframe_org = {'address': cdata['address']}
        self.poffice = {'phoneNumber': [cdata['phoneNumber'][0]]}
        self.poffice1 = {'phoneNumber': [cdata['phoneNumber'][1]]}

        self.addr = {
            u'address': {
                u'town': u'nowhere'
            }
        }

        pass

    def testCase010(self):
        """Copy by reference.
        """
        jval = JSONData(self.pframe, copydata=C_REF)
        jval.branch_add(self.poffice)
        j0 = jval["phoneNumber"]
        j1 = self.poffice["phoneNumber"]
        assert j0 == j1
        assert self.pframe != self.pframe_org
        assert self.pframe == jval()

        #copy.deepcopy(self.pframe_org, self.pframe)
        pass

    def testCase020(self):
        """Copy by de-reference up to the first level in case of containers.
        """
        jval = JSONData(self.pframe, copydata=C_SHALLOW)
        jval.branch_add(self.poffice)
        j0 = jval["phoneNumber"]
        j1 = self.poffice["phoneNumber"]
        assert j0 == j1
        assert self.pframe == self.pframe_org

        jval1_org = copy.deepcopy(jval)
        jval1 = copy.copy(jval)
        self.assertEqual(jval, jval1)
        self.assertEqual(jval1, jval1_org)
        self.assertEqual(jval, jval1_org)

        jval.branch_add(self.poffice1)
        jval.branch_add(self.addr)
        assert jval1['address'] == self.addr['address']

        #copy.deepcopy(self.pframe_org, self.pframe)
        pass

    def testCase030(self):
        """Copy by deep iteration in case of containers.
        """
        jval = JSONData(self.pframe, copydata=C_DEEP)
        jval.branch_add(self.poffice)
        j0 = jval["phoneNumber"]
        j1 = self.poffice["phoneNumber"]
        assert j0 == j1
        assert self.pframe == self.pframe_org

        #copy.deepcopy(self.pframe_org, self.pframe)
        pass


#
#######################
#

if __name__ == '__main__':
    unittest.main()
