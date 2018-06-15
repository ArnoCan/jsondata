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

        ref = {u'~1': 10, u'/': 9}
        assert ref == self.configdata

    def testCase001(self):

        #
        # assemble patches
        jsonpatchlist = JSONPatch()
        jsonpatchlist += JSONPatchItemRaw(
            """{"op": "test", "path": "/~01", "value": "10"}""",
            replace=True)
        ref = repr(jsonpatchlist)
        ref = [{u'op': u'test', u'path': u'/~1', u'value': u'10'}]
        assert ref == jsonpatchlist

        cnt, failed = jsonpatchlist.apply(self.configdata)  # apply all patches
        assert cnt == 1  # number of patch items
        assert failed == [0]  # list of failed patch items


#
#######################
#
if __name__ == '__main__':
    unittest.main()
