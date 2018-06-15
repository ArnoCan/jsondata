# -*- coding: utf-8 -*-
"""Extensions for standards tests from RFC6901.

This case covers in particular extensions to the standard contained
examples. 

For JSON notation of RFC6901::

  { "": { "": ["doubleempty0", "doubleempty1"] } }

Pointer access::

  ""       { "": { "": ["doubleempty0", "doubleempty1"] } }
  "/"            { "": ["doubleempty0", "doubleempty1"] }
  "//"                 ["doubleempty0", "doubleempty1"]
  "//0"                 "doubleempty0"
  "//1"                                 "doubleempty1"

"""
from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
else:
    import json as myjson
import jsonschema

from jsondata.jsonpointer import JSONPointer
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF
from jsondata.jsonpatch import JSONPatch, JSONPatchItem, JSONPatchItemRaw
from jsondata.jsonpointer import JSONPointer
from filesysobjects.configdata import ConfigPath


class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        _cp = ConfigPath(replace=os.path.dirname(__file__))
        self.datafile = _cp.get_config_filepath('rfc6901ext.json')
        self.configdata = ConfigData(
            {},
            datafile=self.datafile,
            validator=MS_OFF,
            )

    def testCase900(self):
        """JSONPointers: ""
        """
        jp = JSONPointer('')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = {u'': {u'': [u'doubleempty0', u'doubleempty1']}}

        assert jdata == jdoc

    def testCase901(self):
        """JSONPointers: "/"
        """
        jp = JSONPointer('/')
        jdata = jp(self.configdata.data)
        jdoc = {u'': [u'doubleempty0', u'doubleempty1']}

        assert jdata == jdoc

    def testCase902(self):
        """JSONPointers: "//"
        """
        jp = JSONPointer('//')
        jdata = jp(self.configdata.data)
        jdoc = [u'doubleempty0', u'doubleempty1']

        assert jdata == jdoc

    def testCase903(self):
        """JSONPointers: "///0"
        """
        jp = JSONPointer('///0')
        jdata = jp(self.configdata.data)
        jdoc = u'doubleempty0'

        assert jdata == jdoc

    def testCase904(self):
        """JSONPointers: "///1"
        """
        jp = JSONPointer('///1')
        jdata = jp(self.configdata.data)
        jdoc = u'doubleempty1'

        assert jdata == jdoc


#
#######################
#
if __name__ == '__main__':
    unittest.main()
