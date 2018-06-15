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

try:
    from jsondata.jsonpointer import JSONPointer
    from jsondata.jsondata import JSONData
except Exception as e:
    print("\n#\n#*** Set 'PYTHONPATH' (" + str(e) + ")\n#\n")

#
#######################
#


class CallUnits(unittest.TestCase):

    def testCase100(self):
        data = {'a': {'b': {'c': [2, 3, 4]}}}
        D = JSONData(data)
        p = JSONPointer('/a/b/c/1')
        n = p(D.data)

        assert n == 3
