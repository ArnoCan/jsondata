"""Import of new branches by jsondata.jsondataserializer.branch_import().
"""
from __future__ import absolute_import

import unittest
import os

from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_DRAFT4


class CallUnits(unittest.TestCase):
    """Base branch import by branch_add.
    """
    
    def __init__(self, *args, **kargs):
        super(CallUnits, self).__init__(*args, **kargs)
        self.configdata = None

    def testCase500(self):
        unittest.TestCase.setUp(self)
        
        self.maxDiff = None


        self.configdata = ConfigData(
            [],
            schemafile=os.path.abspath(os.path.dirname(
                    __file__)) + os.sep + str('schema.jsd'),
            validator=MS_DRAFT4,
            )

        resx = []
        assert self.configdata.data == resx


if __name__ == '__main__':
    unittest.main()
