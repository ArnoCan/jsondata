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
        self.datafile = _cp.get_config_filepath('data.json')
        self.configdata = ConfigData(
            {},
            datafile=self.datafile,
            validator=MS_OFF,
            )

        ref = {u'foo': [u'bar', u'baz']}
        assert ref == self.configdata

        self.jsonpatchlist = JSONPatch()
        self.jsonpatchlist += JSONPatchItem("add", "/foo/1", "qux")
        ref = repr(self.jsonpatchlist)
        ref = [{u'op': u'add', u'path': u'/foo/1', u'value': u'qux'}]
        assert ref == self.jsonpatchlist

    def testCase002(self):
        global appname

        self.jsonpatchlist.apply(self.configdata)
        ref = {u'foo': [u'bar', u'qux', u'baz']}
        assert self.configdata.data
        assert ref == self.configdata.data


#
#######################
#
if __name__ == '__main__':
    unittest.main()
