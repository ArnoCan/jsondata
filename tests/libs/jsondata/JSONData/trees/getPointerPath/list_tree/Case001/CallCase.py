"""Append list element.
"""
from __future__ import absolute_import

import unittest
import os
import sys

# pre-set the base JSON libraries for 'jsondata' by PyUnit call
if 'ujson' in sys.argv:
    import ujson as myjson
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

    def testCase110(self):
        n3 = [[[[2], [[3]], [[4]]]]]
        n4 = [[[[3], [[4]], [[5]]]]]
        sl4 = [n3, n4, ]

        p0 = fetch_pointerpath(n4, sl4)
        resx = [[1]]
        assert p0 == resx
        pass


if __name__ == '__main__':
    unittest.main()
