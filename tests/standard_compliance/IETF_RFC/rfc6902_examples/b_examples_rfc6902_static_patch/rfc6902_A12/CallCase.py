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

        ref = {u'foo': u'bar', u'baz': {}}
        assert ref == self.configdata

        #
        # assemble patches
        self.jsonpatchlist = JSONPatch()
        self.jsonpatchlist += JSONPatchItemRaw(
            """{ "op": "add", "path": "/baz/bat", "value": "qux" }""")
        ref = repr(self.jsonpatchlist)
        ref = [{u'op': u'add', u'path': u'/baz/bat', u'value': u'qux'}]
        assert ref == self.jsonpatchlist

    def testCase002(self):

        cnt, failed = self.jsonpatchlist.apply(self.configdata)
        ref = repr(self.configdata)
        ref = {u'foo': u'bar', u'baz': {u'bat': u'qux'}}
        assert cnt == 1  # number of patch items
        assert failed == []  # list of failed patch items
        assert ref == self.configdata  # the final result of cumulated patches


if __name__ == '__main__':
    unittest.main()
