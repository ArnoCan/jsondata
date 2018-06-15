from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import unittest
import copy

if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport  @UnusedImport pylint: disable=import-error
else:
    import json as myjson  # @Reimport @UnusedImport
import jsonschema  # @UnusedImport

from jsondata.jsondata import JSONData


class CallUnits(unittest.TestCase):

    def testCase010(self):
        jval = JSONData({"a": 0, "b": 1,})
        jval.branch_add({"c": 2})
        assert jval == {"a": 0, "b": 1, "c": 2}


if __name__ == '__main__':
    unittest.main()
