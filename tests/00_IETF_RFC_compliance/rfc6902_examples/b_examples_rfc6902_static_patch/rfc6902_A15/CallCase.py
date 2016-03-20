# -*- coding: utf-8 -*-
"""Standards tests from RFC6902 for compliance of patch syntax.

"""
from __future__ import absolute_import

import unittest
import os
import sys

import json,jsonschema
jval = None

try:
    from jsondata.JSONPointer import JSONPointer
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"
try:
    from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
    from jsondata.JSONDataSerializer import MODE_SCHEMA_OFF
    from jsondata.JSONPatch import JSONPatch,JSONPatchItem,JSONPatchItemRaw
    from jsondata.JSONPointer import JSONPointer
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"

# name of application, used for several filenames as MODE_SCHEMA_DRAFT4
_APPNAME = "jsondatacheck"
appname = _APPNAME
#
#######################
#
class CallUnits(unittest.TestCase):
    name=os.path.curdir+__file__

    output=True
    output=False

    def testCase000(self):
        """Create an object for data only - no schema.
        """
        global configdata
        global appname

        kargs = {}
        kargs['datafile'] = os.path.dirname(__file__)+os.sep+'data.json'
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kargs)

        ref = repr(configdata)
        ref = """{u'~1': 10, u'/': 9}"""
        assert ref == repr(configdata)

    def testCase001(self):
        """Assemble patch list, Comparing Strings and Numbers
        """
        global configdata
        global appname
        global jsonpatchlist

        #
        # assemble patches
        jsonpatchlist  = JSONPatch()
        jsonpatchlist += JSONPatchItemRaw("""{"op": "test", "path": "/~01", "value": "10"}""")
        ref=repr(jsonpatchlist)
        ref = """[{u'op': u'test', u'path': u'/~1', u'value': u'10'}]"""
        assert ref == repr(jsonpatchlist) # the complete patch list

    def testCase002(self):
        """Apply patch list, Comparing Strings and Numbers
        """
        global configdata
        global appname
        global jsonpatchlist

        cnt,failed = jsonpatchlist.apply(configdata) # apply all patches
        assert cnt == 1 # number of patch items
        assert failed == [0] # list of failed patch items

#
#######################
#
if __name__ == '__main__':
    unittest.main()