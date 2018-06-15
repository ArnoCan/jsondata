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
from jsondata import M_FIRST, M_ALL
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
        c0 = [4]

        n3 = [[[1,    [[3]],  [c0]]]]
        n4 = [[[[3], [c0],    [c0]]]]

        sl6 = [n3, ]

        p0 = fetch_pointerpath(n4[0][0][2][0], sl6, M_ALL)
        resx = [
            [0, 0, 0, 2, 0],
        ]

        assert p0 == resx


if __name__ == '__main__':
    unittest.main()
