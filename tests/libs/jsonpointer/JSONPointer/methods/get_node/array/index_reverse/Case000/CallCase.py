# -*- coding: utf-8 -*-
"""Standards tests from RFC6902 for compliance of patch syntax.

"""
from __future__ import absolute_import

import unittest
import os
import sys
from jsondata import JSONPointerError


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
        p = JSONPointer('/a/b/c/-1')
        n = p(D.data)

        assert n == 4

    def testCase110(self):
        data = {'a': {'b': {'c': [2, 3, 4]}}}
        D = JSONData(data)
        p = JSONPointer('/a/b/c/-2')
        n = p(D.data)

        assert n == 3

    def testCase120(self):
        data = {'a': {'b': {'c': [2, 3, 4]}}}
        D = JSONData(data)
        p = JSONPointer('/a/b/c/-3')
        n = p(D.data)

        assert n == 2

    def testCase130(self):
        data = {'a': {'b': {'c': [2, 3, 4]}}}
        D = JSONData(data)
        p = JSONPointer('/a/b/c/-4')
        try:
            n = p(D.data)
        except JSONPointerError:
            return
        assert n == 2

    def testCase131(self):
        data = {'a': {'b': {'c': [2, 3, 4]}}}
        D = JSONData(data)
        p = JSONPointer('/a/b/c/4')

        try:
            n = p(D.data)
        except JSONPointerError:
            return
        assert n == 2

    def testCase140(self):
        data = {'a': {'b': {'c': [2, 3, 4]}}}
        D = JSONData(data)
        p = JSONPointer('/a/b/c/-0')
        n = p(D.data)

        assert n == 2

