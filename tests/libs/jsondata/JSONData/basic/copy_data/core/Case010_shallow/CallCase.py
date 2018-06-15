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

        self.pframe = {
            u'address': {}
        }

        self.pframe_org = {
            u'address': {}
        }

        self.poffice = {
            u'phoneNumber': [
                {
                    u'type': u'office',
                    u'number': u'313 123-456'
                }
            ]
        }

        self.poffice1 = {
            u"phoneNumber": [
                {
                    u'type': u'office',
                    u'number': u'444 444-444'
                }
            ]
        }
        self.addr = {
            u'address': {
                u'town': u'nowhere'
            }
        }

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


if __name__ == '__main__':
    unittest.main()
