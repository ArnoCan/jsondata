# -*- coding: utf-8 -*-
"""Standards tests from RFC6902 for compliance of patch syntax.

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
        jdoc = {u'': {u'': {u'': [u'tripleempty0', u'tripleempty1']}}}
        # print "<"+repr(jdata)+">"
        # print "<"+jdoc+">"

        assert jdata == jdoc

    def testCase901(self):
        """JSONPointers: "/"
        """
        jp = JSONPointer('/')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = {u'': {u'': {u'': [u'tripleempty0', u'tripleempty1']}}}
        # print "<"+repr(jdata)+">"
        # print "<"+jdoc+">"

        assert jdata == jdoc

    def testCase902(self):
        """JSONPointers: "//"
        """
        jp = JSONPointer('//')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = {u'': [u'tripleempty0', u'tripleempty1']}
        # print "<"+repr(jdata)+">"
        # print "<"+jdoc+">"

        assert jdata == jdoc

    def testCase903(self):
        """JSONPointers: "///"
        """
        jp = JSONPointer('///')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = [u'tripleempty0', u'tripleempty1']
        # print "<"+repr(jdata)+">"
        # print "<"+jdoc+">"

        assert jdata == jdoc

    def testCase904(self):
        """JSONPointers: "////0"
        """
        jp = JSONPointer('////0')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = u'tripleempty0'
        # print "<"+repr(jdata)+">"
        # print "<"+jdoc+">"

        assert jdata == jdoc

    def testCase905(self):
        """JSONPointers: "////1"
        """
        jp = JSONPointer('////1')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = u'tripleempty1'
        # print "<"+repr(jdata)+">"
        # print "<"+jdoc+">"

        assert jdata == jdoc


#
#######################
#
if __name__ == '__main__':
    unittest.main()
