"""Load and access data.
"""
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import unittest
import copy


if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
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


if __name__ == '__main__':
    unittest.main()
