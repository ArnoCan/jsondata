# -*- coding:utf-8   -*-

from __future__ import absolute_import
from __future__ import print_function

import unittest
import os
import sys

import json
import jsonschema

# import 'jsondata'
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_DRAFT4
from jsondata import JSONDataKeyError, JSONDataNodeTypeError

# name of application, used for several filenames as MS_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME


datafile = os.path.abspath(os.path.dirname(__file__)) \
    + os.sep + str('datafile.json')
schemafile = os.path.abspath(os.path.dirname(__file__)) \
    + os.sep + str('schema.jsd')

kargs = {}
kargs['datafile'] = datafile
kargs['schemafile'] = schemafile
kargs['nodefaultpath'] = True
kargs['nosubdata'] = True
kargs['pathlist'] = os.path.dirname(__file__)
kargs['validator'] = MS_DRAFT4

configdata = ConfigData(appname, **kargs)

resx = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
        'phoneNumber': [{'type': 'home', 'number': '212 555-1234'},
                        {'type': 'office', 'number': '313 444-555'},
                        {'type': 'mobile', 'number': '777 666-555'}]}

assert configdata.data == resx
pass
