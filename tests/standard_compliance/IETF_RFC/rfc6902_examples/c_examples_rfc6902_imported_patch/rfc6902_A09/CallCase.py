# -*- coding: utf-8 -*-
"""Standards tests from RFC6902 for compliance of patch syntax.

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

        ref = {u'baz': u'qux'}
        assert ref == self.configdata

    def testCase001(self):

        jsonpatchlist = JSONPatch()
        patchfile = os.path.dirname(__file__) + os.sep + 'patch.jsonp'
        jsonpatchlist.patch_import(patchfile)

        ref = [{u'op': u'test', u'path': u'/baz', u'value': u'bar'}]
        assert ref == jsonpatchlist  # the complete patch list

        cnt, failed = jsonpatchlist.apply(self.configdata)  # apply all patches
        ref = self.configdata
        ref = {u'baz': u'qux'}
        assert cnt == 1  # number of patch items
        assert failed == [0]  # list of failed patch items
        assert ref == self.configdata  # the final result of cumulated patches


if __name__ == '__main__':
    unittest.main()
