"""Import of new branches by jsondata.jsondataserializer.branch_import().
"""
from __future__ import absolute_import

import unittest
import os

from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_DRAFT4, MJ_RFC4627, MJ_RFC7159, JSONDataModeError


class CallUnits(unittest.TestCase):
    """Base branch import by branch_add.
    """
    
    def __init__(self, *args, **kargs):
        super(CallUnits, self).__init__(*args, **kargs)
        self.configdata = None

    def testCase500(self):
        unittest.TestCase.setUp(self)
        
        self.maxDiff = None

        self.configdata = ConfigData(None)

        resx = None
        assert self.configdata.data == resx

    def testCase510(self):
        unittest.TestCase.setUp(self)
        
        self.maxDiff = None

        self.configdata = ConfigData(None, mode=MJ_RFC7159)

        resx = None
        assert self.configdata.data == resx

    def testCase521(self):
        unittest.TestCase.setUp(self)
        
        self.maxDiff = None

        self.configdata = ConfigData([], mode=MJ_RFC4627)

        resx = []
        assert self.configdata.data == resx

    def testCase522(self):
        unittest.TestCase.setUp(self)
        
        self.maxDiff = None

        self.configdata = ConfigData({}, mode=MJ_RFC4627)

        resx = {}
        assert self.configdata.data == resx

    def testCase530(self):
        unittest.TestCase.setUp(self)
        
        self.maxDiff = None

        try:
            self.configdata = ConfigData(None, mode=MJ_RFC4627)
        except JSONDataModeError:
            pass
        else:
            raise AssertionError()

    def testCase531(self):
        unittest.TestCase.setUp(self)
        
        self.maxDiff = None

        try:
            self.configdata = ConfigData(11, mode=MJ_RFC4627)
        except JSONDataModeError:
            pass
        else:
            raise AssertionError()

    def testCase532(self):
        unittest.TestCase.setUp(self)
        
        self.maxDiff = None

        try:
            self.configdata = ConfigData(11.11, mode=MJ_RFC4627)
        except JSONDataModeError:
            pass
        else:
            raise AssertionError()

    def testCase533(self):
        unittest.TestCase.setUp(self)
        
        self.maxDiff = None

        try:
            self.configdata = ConfigData("abc", mode=MJ_RFC4627)
        except JSONDataModeError:
            pass
        else:
            raise AssertionError()


if __name__ == '__main__':
    unittest.main()
