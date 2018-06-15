"""Append list element.
"""
from __future__ import absolute_import

import unittest
import os
import sys

# pre-set the base JSON libraries for 'jsondata' by PyUnit call
if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
elif 'json' in sys.argv:
    import json as myjson
else:
    import json as myjson
import jsonschema

from jsondata.jsonpointer import JSONPointer, fetch_pointerpath

# name of application, used for several filenames as MS_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME

#
#######################
#


class CallUnits(unittest.TestCase):
    """Base branch_add.
    """

    def testCase100(self):

        n3 = [[[[2], [[3]], [[4]]]]]
        n4 = [[[[3], [[4]], [[5]]]]]
        n6 = [[[[n3, n4]]]]
        sl6 = [n3, n6, n4, ]

        a = n4[0][0][2]
        assert n4[0][0][2] == [[5]]

        p0 = fetch_pointerpath(n4[0][0][2], n4)
        resx = [[0, 0, 2]]
        assert p0 == resx

        p0 = fetch_pointerpath(n4[0][0][2], sl6)
        resx = [[1, 0, 0, 0, 1, 0, 0, 2]]
        assert p0 == resx


if __name__ == '__main__':
    unittest.main()
