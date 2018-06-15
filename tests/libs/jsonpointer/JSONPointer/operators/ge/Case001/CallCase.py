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
from jsondata.jsonpointer import JSONPointer


class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
 
        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('testdata.json')
        schemafile = _cp.get_config_filepath('testdata.jsd')
        self.configdata = ConfigData(
            {},
            datafile=datafile,
            schemafile=schemafile,
            validator=MS_OFF,
            )

    def testCase900(self):
        """Compare with an additional trailing '/'.
        """
        jp = JSONPointer('/address/streetAddress')
        assert jp >= '/address/streetAddress/'

    def testCase901(self):
        """Compare with an additional trailing '/'.
        """
        jp = JSONPointer('/address/streetAddress')
        assert jp >= '/address/streetAddress'



#
#######################
#
if __name__ == '__main__':
    unittest.main()
