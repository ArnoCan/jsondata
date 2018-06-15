# -*- coding: utf-8 -*-
"""Extensions for standards tests from RFC6901.

This case covers in particular extensions to the standard contained
examples. 

For JSON notation of RFC6901::

  { "": { "": { "": ["tripleempty0", "tripleempty1"] } } }

Pointer access::

  ""       { "": { "": { "": ["tripleempty0", "tripleempty1"] } } }
  "/"            { "": { "": ["tripleempty0", "tripleempty1"] } }
  "//"                 { "": ["tripleempty0", "tripleempty1"] }
  "///"                      ["tripleempty0", "tripleempty1"]
  "///0"                      "tripleempty0"
  "///1"                                      "tripleempty1"

"""
from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson
else:
    import json as myjson
import jsonschema


jval = None

try:
    from jsondata.jsonpointer import JSONPointer
except Exception as e:
    print("\n#\n#*** Set 'PYTHONPATH' (" + str(e) + ")\n#\n")
try:
    from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
    from jsondata  import MS_OFF
except Exception as e:
    print("\n#\n#*** Set 'PYTHONPATH' (" + str(e) + ")\n#\n")

# name of application, used for several filenames as MS_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME
#
#######################
#


class CallUnits(unittest.TestCase):

    def testCase000(self):
        """Create an object for data only - no schema.
        """
        global configdata
        global appname

        kargs = {}
        kargs['datafile'] = os.path.dirname(
            __file__) + os.sep + 'rfc6901ext.json'
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MS_OFF
        configdata = ConfigData(appname, **kargs)

    def testCase900(self):
        """JSONPointers: ""
        """
        jp = JSONPointer('')
        jdata = jp.get_node_value(configdata.data)
        jdoc = {u'': {u'': {u'': [u'tripleempty0', u'tripleempty1']}}}
        resx = {u'': {u'': {u'': [u'tripleempty0', u'tripleempty1']}}}

        assert jdata == jdoc
        assert jdata == resx

    def testCase901(self):
        """JSONPointers: "/"
        """
        jp = JSONPointer('/')
        jdata = jp.get_node_value(configdata.data)
        jdoc =  {'': {'': {'': ['tripleempty0', 'tripleempty1']}}}
        resx =  {'': {'': ['tripleempty0', 'tripleempty1']}}

        assert jdata == jdoc['']
        assert jdata == resx

    def testCase902(self):
        """JSONPointers: "//"
        """
        jp = JSONPointer('//')
        jdata = jp.get_node_value(configdata.data)
        jdoc =  {'': {'': {'': ['tripleempty0', 'tripleempty1']}}}
        resx =  {'': ['tripleempty0', 'tripleempty1']}

        assert jdata == jdoc['']['']
        assert jdata == resx

    def testCase903(self):
        """JSONPointers: "///"
        """
        jp = JSONPointer('///')
        jdata = jp.get_node_value(configdata.data)
        jdoc =  {'': {'': {'': ['tripleempty0', 'tripleempty1']}}}
        resx =  ['tripleempty0', 'tripleempty1']

        assert jdata == jdoc['']['']['']
        assert jdata == resx

    def testCase904(self):
        """JSONPointers: "////0"
        """
        jp = JSONPointer('////0')
        jdata = jp.get_node_value(configdata.data)
        jdoc =  {'': {'': {'': ['tripleempty0', 'tripleempty1']}}}
        resx =  'tripleempty0'

        assert jdata == jdoc[''][''][''][0]
        assert jdata == resx

    def testCase905(self):
        """JSONPointers: "////1"
        """
        jp = JSONPointer('////1')
        jdata = jp.get_node_value(configdata.data)
        jdoc =  {'': {'': {'': ['tripleempty0', 'tripleempty1']}}}
        resx =  'tripleempty1'

        assert jdata == jdoc[''][''][''][1]
        assert jdata == resx


if __name__ == '__main__':
    unittest.main()
