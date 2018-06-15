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

# import 'jsondata'
from jsondata.jsondataserializer import JSONData


class CallUnits(unittest.TestCase):
    """Base branch_add.
    """

    def testCase000(self):
        """Load initial main/master data, and validate it with standard draft4.
        """
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}]}})
        source = {'v1': 200}
        
        D.branch_add(source, D['e']['lx'], 1)  #pylint: disable=unsubscriptable-object

        # print(repr(D))
        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}

        self.assertEqual(D, resx)        


if __name__ == '__main__':
    unittest.main()
