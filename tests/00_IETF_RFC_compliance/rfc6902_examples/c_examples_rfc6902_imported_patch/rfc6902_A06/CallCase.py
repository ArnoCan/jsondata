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
    from jsondata.JSONPatch import JSONPatch,JSONPatchItem
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
        ref = """{u'qux': {u'corge': u'grault'}, u'foo': {u'bar': u'baz', u'waldo': u'fred'}}"""
        assert ref == repr(configdata)

    def testCase001(self):
        global configdata
        global appname
        global jsonpatchlist

        jsonpatchlist = JSONPatch()
        patchfile = os.path.dirname(__file__)+os.sep+'patch.jsonp'
        jsonpatchlist.patch_import(patchfile)

        ref=repr(jsonpatchlist)
        ref = """[{u'op': u'move', u'path': u'/qux/thud', u'from': u'/foo/waldo'}]"""
        assert ref == repr(jsonpatchlist)

    def testCase002(self):
        global configdata
        global appname
        global jsonpatchlist

        jsonpatchlist.apply(configdata)
        ref=repr(configdata)
        ref = """{u'qux': {u'thud': u'fred', u'corge': u'grault'}, u'foo': {u'bar': u'baz'}}"""
        assert ref == repr(configdata)


#
#######################
#
if __name__ == '__main__':
    unittest.main()
