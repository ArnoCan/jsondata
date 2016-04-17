# -*- coding: utf-8 -*-
"""Standards tests from RFC6902 for compliance of patch syntax.

"""
from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson
else:
    import json as myjson

try:
    from jsondata.JSONPointer import JSONPointer
    from jsondata.JSONCompute import JSONCompute
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"

#
#######################
#
class CallUnits(unittest.TestCase):
    name=os.path.curdir+__file__

    output=True
    output=False

    def testCase011(self):
        import jsondata.JSONPointer

        a = JSONPointer("/a/b/c")
        b = JSONPointer("/x/y")
        c = JSONPointer("/a/b/c/2/x/y/v")

         
        for i in range(0,4):
            # print a + i + b > c
            try:
                assert a + i + b > c
            except:
                if i == 2:
                    raise
                else:
                    pass



if __name__ == '__main__':
    unittest.main()