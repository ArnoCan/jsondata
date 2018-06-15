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

        ref = {u'qux': {u'corge': u'grault'}, u'foo': {u'bar': u'baz', u'waldo': u'fred'}}
        assert ref == self.configdata

    def testCase001(self):

        jsonpatchlist = JSONPatch()
        jsonpatchlist += JSONPatchItem("replace", "/baz", "boo")
        ref = repr(jsonpatchlist)
        ref = [{u'op': u'replace', u'path': u'/baz', u'value': u'boo'}]
        assert ref == jsonpatchlist

        jsonpatchlist.apply(self.configdata)
        ref = repr(self.configdata)
        ref = {u'qux': {u'corge': u'grault'}, u'foo': {u'bar': u'baz', u'waldo': u'fred'}, u'baz': u'boo'}
        assert ref == self.configdata


if __name__ == '__main__':
    unittest.main()
