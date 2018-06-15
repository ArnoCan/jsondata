# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import unittest
import os
import sys

from jsondata import V3K

if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
else:
    import json as myjson
import jsonschema

if V3K:
    unicode = str


from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF
from jsondata.jsonpatch import JSONPatch, JSONPatchItem
from filesysobjects.configdata import ConfigPath


class CallUnits(unittest.TestCase):

    def testCase004(self):

        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('data.json')
        schemafile = _cp.get_config_filepath('schema.jsd')
        configdata = ConfigData(
            {},
            datafile=datafile,
            schemafile=schemafile,
            validator=MS_OFF,
            )

        jsonpatchlist = None

        #
        # assemble
        #
        jsonpatchlist = JSONPatch()
        for i in range(0, 10):
            jsonpatchlist += JSONPatchItem(
                "add", "/a" + unicode(i), "v" + unicode(i))

        #
        # export
        #
        patch_file = os.path.dirname(__file__) + os.sep + 'exportimport.patch'
        ret = jsonpatchlist.patch_export(patch_file, pretty=True)  # @UnusedVariable

        #
        # re-import
        #
        implist = JSONPatch()
        retimp = implist.patch_import(patch_file)  # @UnusedVariable

        #
        # check
        #
        assert jsonpatchlist == implist


if __name__ == '__main__':
    unittest.main()
