.. _HOWTO_JSONDATA:

JSONData - RFC7159 et al.
=========================
This howto focussed on applied code examples. 

.. toctree::
   :maxdepth: 2

   howto_class_jsondata

Branch Operations
-----------------
The branch operations provide for the operations of higher level
of structured data. 
These are also the technical base for the standards conformant
operations in accordance to RFC6902 and RFC6901,
see `JSONPatch - RFC6902 <howto_class_jsonpatch.html>`_
and
see `JSONPointer - RFC6901 <howto_class_jsonpointer.html>`_
.

Create Branch
^^^^^^^^^^^^^
Create a JSON document consisting of a new branch 
`JSONData <jsondata_jsondata_doc.html#init>`_.

.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   
   # JSON in-memory document
   D = JSONData(
           { 'a': { 'b': { 'c': 2, 'd': 3 } } }
       )
      
   # print structure
   print(D)

prints the result by *str*:

.. code-block:: json
   :linenos:

   {
       "a": {
           "b": {
               "c": 2,
               "d": 3
           }
       }
   }
    

or by *repr*:

.. code-block:: json
   :linenos:

   {'a': {'b': {'c': 2, 'd': 3}}}

Add Branch
^^^^^^^^^^
Object with Key
"""""""""""""""
Create a JSON document and add a branch,
see also :ref:`OP_IADD`

.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   D = JSONData({'a': {'b': {'c': 2, 'd': 3}}})
   source = {'lx': [{'v0': 100}, {'v1': 200}]}
   
   # JSON branch with array
   D.branch_add(source, D, 'e')
   
   print(D)
   # print(repr(D))


prints the result:

.. code-block:: json
   :linenos:

   {
       "a": {
           "b": {
               "c": 2,
               "d": 3
           }
       },
       "e": {
           "lx": [
               {
                   "v0": 100
               },
               {
                   "v1": 200
               }
           ]
       }
   }    

Object without Key
""""""""""""""""""
Create a JSON document and add a branch,
see also :ref:`OP_IADD`

.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   D = JSONData({'a': {'b': {'c': 2, 'd': 3}}})
   source = { 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
   
   # JSON branch with array
   D.branch_add(source, D)
   
   print(D)
   # print(repr(D))


prints the result:

.. code-block:: json
   :linenos:

   {
       "a": {
           "b": {
               "c": 2,
               "d": 3
           }
       },
       "e": {
           "lx": [
               {
                   "v0": 100
               },
               {
                   "v1": 200
               }
           ]
       }
   }    

Move
^^^^
Object Attribute
""""""""""""""""
Call with key
'''''''''''''
Move an attribute branch within a JSON document.


.. code-block:: python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
   
   target = JSONPointer('/a/b')
   source = JSONPointer('/a/b/c')
   
   D.branch_move(source, target, 'new')
   
   print(D)
   #print(repr(D))
 
prints the result:

.. code-block:: json
   :linenos:

   {
       "a": {
           "b": {
               "d": 3,
               "new": 2
           }
       },
       "e": {
           "lx": [
               {
                   "v0": 100
               },
               {
                   "v1": 200
               }
           ]
       }
   }

Call without key
''''''''''''''''
Move an attribute branch within a JSON document.


.. code-block:: python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
   
   target = JSONPointer('/a/b/new')
   source = JSONPointer('/a/b/c')
   
   D.branch_move(source, target)
   
   print(D)
   #print(repr(D))
 
prints the result:

.. code-block:: json
   :linenos:

   {
       "a": {
           "b": {
               "d": 3,
               "new": 2
           }
       },
       "e": {
           "lx": [
               {
                   "v0": 100
               },
               {
                   "v1": 200
               }
           ]
       }
   }

Array Element
"""""""""""""
Call with key
'''''''''''''
Move an array element within a JSON document.


.. code-block:: python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
   
   target = JSONPointer('/e/lx')
   source = JSONPointer('/e/lx/0')
   
   D.branch_move(source, target, '-')
   
   print(D)
   #print(repr(D))
 
prints the result:

.. code-block:: json
   :linenos:

   {
       "a": {
           "b": {
               "c": 2,
               "d": 3
           }
       },
       "e": {
           "lx": [
               {
                   "v1": 200
               },
               {
                   "v0": 100
               }
           ]
       }
   }

Call without key
''''''''''''''''
Move an array element within a JSON document.


.. code-block:: python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
   
   target = JSONPointer('/e/lx/-')
   source = JSONPointer('/e/lx/0')
   
   D.branch_move(source, target)
   
   print(D)
   #print(repr(D))
 
prints the result:

.. code-block:: json
   :linenos:

   {
       "a": {
           "b": {
               "c": 2,
               "d": 3
           }
       },
       "e": {
           "lx": [
               {
                   "v1": 200
               },
               {
                   "v0": 100
               }
           ]
       }
   }

Remove Branch
^^^^^^^^^^^^^
From Object
"""""""""""
Call with key
'''''''''''''
Remove a branch or item within a container by it's key,
convenient for loops.

.. code-block:: python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
   
   target = JSONPointer('/a/b')
   
   D.branch_remove(target, 'c')
   
   print(D)
   #print(repr(D))

prints the result:

.. code-block:: json
   :linenos:

   {
       "a": {
           "b": {
               "d": 3
           }
       },
       "e": {
           "lx": [
               {
                   "v0": 100
               },
               {
                   "v1": 200
               }
           ]
       }
   }

Call without key
''''''''''''''''
Remove a branch or item by it's path only.

.. code-block:: python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
   
   target = JSONPointer('/a/b/c')
   
   D.branch_remove(target)
   
   print(D)
   #print(repr(D))

prints the result:

.. code-block:: json
   :linenos:

   {
       "a": {
           "b": {
               "d": 3
           }
       },
       "e": {
           "lx": [
               {
                   "v0": 100
               },
               {
                   "v1": 200
               }
           ]
       }
   }

From Array
""""""""""
Call with key
'''''''''''''
Remove a branch or item within a container by it's key,
convenient for loops.

.. code-block:: python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
   
   target = JSONPointer('/e/lx')
   
   D.branch_remove(target, 1)
   
   print(D)
   #print(repr(D))

prints the result:

.. code-block:: json
   :linenos:

   {
       "a": {
           "b": {
               "c": 2,
               "d": 3
           }
       },
       "e": {
           "lx": [
               {
                   "v0": 100
               }
           ]
       }
   }

Call without key
''''''''''''''''
Remove a branch or item by it's path only.

.. code-block:: python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
   
   target = JSONPointer('/e/lx/1')
   
   D.branch_remove(target)
   
   print(D)
   #print(repr(D))

prints the result:

.. code-block:: json
   :linenos:

   {
       "a": {
           "b": {
               "c": 2,
               "d": 3
           }
       },
       "e": {
           "lx": [
               {
                   "v0": 100
               }
           ]
       }
   }

Similar calls with reverse index:

.. code-block:: python
   :linenos:

   target = JSONPointer('/e/lx/-1')
   target = JSONPointer('/e/lx/-2')

and special index rfc6901:

.. code-block:: python
   :linenos:

   target = JSONPointer('/e/lx/-')

Replace
^^^^^^^
Object Attribute
""""""""""""""""
Replace an attribute branch within a JSON document.


Replace a branch.

.. code-block:: python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
   
   
   # does not verify childnode, when 'parent=True' <=> 'new' does no longer exist
   targetnode = JSONPointer('/a/b').get_path_list()
   
   # new item
   sourcenode = {'alternate': 4711 }
   
   # replace old by new item
   ret = D.branch_replace(sourcenode, targetnode, 'c')
   assert ret == True
   
   # verify new item
   x = D('/a/b/c/alternate')  # see JSONData.__call__
   assert x == 4711
   
   print(D)

prints the result:

.. code-block:: json
   :linenos:

   {
       "a": {
           "b": {
               "c": {
                   "alternate": 4711
               },
               "d": 3
           }
       },
       "e": {
           "lx": [
               {
                   "v0": 100
               },
               {
                   "v1": 200
               }
           ]
       }
   }

Array Element
"""""""""""""
Move an array element within a JSON document.


.. code-block:: python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
   
   
   # does not verify childnode, when 'parent=True' <=> 'new' does no longer exist
   targetnode = JSONPointer('/e/lx/0').get_path_list()
   
   # new item
   sourcenode = {'alternate': 4711 }
   
   # replace old by new item
   ret = D.branch_replace(sourcenode, targetnode)
   assert ret == True
   
   # verify new item
   x = D('/e/lx/0/alternate')  # see JSONData.__call__
   assert x == 4711
   
   print(D)
 
prints the result:

.. code-block:: json
   :linenos:

   {
       "a": {
           "b": {
               "c": 2,
               "d": 3
           }
       },
       "e": {
           "lx": [
               {
                   "alternate": 4711
               },
               {
                   "v1": 200
               }
           ]
       }
   }

Branch Algebra
--------------

RFC7159 Examples
----------------
Create Objects
^^^^^^^^^^^^^^

.. seealso::

   See section "13. Examples" [RFC7159]_:
   
   .. code-block:: json
      :linenos:
   
      {
         "Image": {
            "Width": 800,
            "Height": 600,
            "Title": "View from 15th Floor",
            "Thumbnail": {
               "Url":
               "http://www.example.com/image/481989943",
               "Height": 125,
               "Width": 100
            },
            "Animated" : false,
            "IDs": [116, 943, 234, 38793]
         }
      }


The application with *JSONData* and *JSONPointer*, which e.g. sets the 
flag '/Image/Animated' to 'true' / *True*.

.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   D = JSONData(
           {
              "Image": {
                 "Width": 800,
                 "Height": 600,
                 "Title": "View from 15th Floor",
                 "Thumbnail": {
                    "Url": "http://www.example.com/image/481989943",
                    "Height": 125,
                    "Width": 100
                 },
                 "Animated" : False, # false,
                 "IDs": [116, 943, 234, 38793]
              }
           }
       )
   
   
   # does not verify childnode, when 'parent=True' <=> 'new' does no longer exist
   targetnode = JSONPointer('/Image/Animated')
   
   # new item
   sourcenode = True
   
   # replace old by new item
   ret = D.branch_replace(sourcenode, targetnode)
   assert ret == True
   
   # verify new item
   x = D('/Image/Animated')  # see JSONData.__call__
   assert x == True
   
   print(D)  # print uses JSON decoder, thus 'True' => 'true'

Results in:

.. code-block:: script
   :linenos:

   {
       "Image": {
           "Width": 800,
           "Height": 600,
           "Title": "View from 15th Floor",
           "Thumbnail": {
               "Url": "http://www.example.com/image/481989943",
               "Height": 125,
               "Width": 100
           },
           "Animated": true,
           "IDs": [
               116,
               943,
               234,
               38793
           ]
       }
   }

The JSON keyword 'true' is correctly transformed from the Python representation *True*
by the print method, same for the import/export parsers.

Create Arrays
^^^^^^^^^^^^^

.. seealso::

   See section "13. Examples" [RFC7159]_:
   
   .. code-block:: json
      :linenos:
   
      [
         {
            "precision": "zip",
            "Latitude": 37.7668,
            "Longitude": -122.3959,
            "Address": "",
            "City": "SAN FRANCISCO",
            "State": "CA",
            "Zip": "94107",
            "Country": "US"
         },
         {
            "precision": "zip",
            "Latitude": 37.371991,
            "Longitude": -122.026020,
            "Address": "",
            "City": "SUNNYVALE",
            "State": "CA",
            "Zip": "94085",
            "Country": "US"
         }
      ]

The application with *JSONData* and *JSONPointer*, which e.g. sets the 
flag '/Image/Animated' to 'true' / *True*.

.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   D = JSONData(
           [
              {
                 "precision": "zip",
                 "Latitude": 37.7668,
                 "Longitude": -122.3959,
                 "Address": "",
                 "City": "SAN FRANCISCO",
                 "State": "CA",
                 "Zip": "94107",
                 "Country": "US"
              },
              {
                 "precision": "zip",
                 "Latitude": 37.371991,
                 "Longitude": -122.026020,
                 "Address": "",
                 "City": "SUNNYVALE",
                 "State": "CA",
                 "Zip": "94085",
                 "Country": "US"
              }
           ]
       )
   
   # modify
   targetnode = JSONPointer('/0/Address')
   sourcenode = "office"
   ret = D.branch_replace(sourcenode, targetnode)
   assert ret == True
   
   targetnode = JSONPointer('/1/Address')
   sourcenode = "soho"
   ret = D.branch_replace(sourcenode, targetnode)
   assert ret == True
   
   # verify
   x = D('/0/Address')  # see JSONData.__call__
   assert x == "office"
   
   x = D('/1/Address')  # see JSONData.__call__
   assert x == "soho"
   
   print(D)  # print uses JSON decoder, thus 'True' => 'true'

Results in:

.. code-block:: script
   :linenos:

   [
       {
           "precision": "zip",
           "Latitude": 37.7668,
           "Longitude": -122.3959,
           "Address": "office",
           "City": "SAN FRANCISCO",
           "State": "CA",
           "Zip": "94107",
           "Country": "US"
       },
       {
           "precision": "zip",
           "Latitude": 37.371991,
           "Longitude": -122.02602,
           "Address": "soho",
           "City": "SUNNYVALE",
           "State": "CA",
           "Zip": "94085",
           "Country": "US"
       }
   ]

JSON Schema Validation
----------------------
JSONData()
^^^^^^^^^^
The schema validation is an optional part of the class *JSONData*.

The JSON data

.. code-block:: json
   :linenos:

   {
     "address":{
       "streetAddress": "21 2nd Street",
       "city":"New York",
       "houseNumber":12
     },
     "phoneNumber":
       [
       {
         "type":"home",
         "number":"212 555-1234"
       },
       {
         "type":"office",
         "number":"313 444-555"
       },
       {
         "type":"mobile",
         "number":"777 666-555"
       }
     ]
   }


is validated by the JSON schema

.. code-block:: json
   :linenos:

   {
      "$schema": "http://json-schema.org/draft-03/schema",
      "_comment": "This is a comment to be dropped by the initial scan:object(0)",
      "_doc": "This is a doc string to be inserted when the language supports it.:object(0)",
      "_doc": "Concatenated for the same instance.:object(0)",
      "type":"object",
      "required":false,
      "properties":{
         "address": {
            "_comment": "This is a comment(0):address",
            "type":"object",
            "required":true,
            "properties":{
               "city": {
                  "type":"string",
                  "required":true
               },
               "houseNumber": {
                  "type":"number",
                  "required":false
               },
               "streetAddress": {
                  "type":"string",
                  "required":true
               }
            }
         },
         "phoneNumber": {
            "_comment": "This is a comment(1):array",
            "type":"array",
            "required":false,
            "items":
            {
               "type":"object",
               "required":false,
               "properties":{
                  "number": {
                     "type":"string",
                     "required":false
                  },
                  "type": {
                     "type":"string",
                     "required":false
                  }
               }
            }
         }
      }
   }

The processing code is:

.. code-block:: Python
   :linenos:

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

JSONData.validate()
^^^^^^^^^^^^^^^^^^^

Conversions
-----------

*json* to *jsondata*
^^^^^^^^^^^^^^^^^^^^
The package *jsondata* relies on the standard package *json* or *ujson*,
therefore the conversion requires a call only.
The data is not actually converted, but just included by refrence into
a control, administration, and arithmetic branch operations object.
The data is still accessible native by the stored reference *JSONData.data*.

.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   jdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }
   
   jsondata = JSONData(jdata)
   
   print()
   print(jsondata)
   print()

Results in:

.. code-block:: script
   :linenos:

   {
       "a": {
           "b": {
               "c": 2,
               "d": 3
           }
       }
   }

Pointer from Node
^^^^^^^^^^^^^^^^^
The JSONPointer for a provided python reference to a node within a JSON data tree.

.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   jdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }
   
   targetnode = jdata['a']['b']['c']
   jsondata = JSONData(jdata)
   
   path_list = fetch_pointerpath(targetnode, jdata)
   path = JSONPointer(path_list[0])
   
   print()
   print(str(path_list) + ' -> ["' + str(path) + '"]')
   print()

Results in:

.. code-block:: script
   :linenos:

   [['a', 'b', 'c']] -> ["/a/b/c"]


Node from Pointer
^^^^^^^^^^^^^^^^^

The JSONPointer for a provided python reference to a node within a JSON data tree.

.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   jdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }
   
   targetpointer = '/a/b/c'
   
   jsonpointer = JSONPointer(targetpointer)
   jsondata = JSONData(jdata)
   
   targetnode = jsonpointer(jsondata)
   
   r = repr(jsonpointer)
   s = str(jsonpointer)
   
   print()
   print('"' + str(jsonpointer) + '" -> ' + str(targetnode))
   print()

Results in:

.. code-block:: script
   :linenos:

   "/a/b/c" -> 2

The same for a list with index '2'.

.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   jdata = { 'a': { 'b': { 'c': [1, 2, 3], 'd': 3 } } }
   
   targetpointer = '/a/b/c/2'
   
   jsonpointer = JSONPointer(targetpointer)
   jsondata = JSONData(jdata)
   
   targetnode = jsonpointer(jsondata)
   
   print()
   print('"' + str(jsonpointer) + '" -> ' + str(targetnode))
   print()


Results in:

.. code-block:: script
   :linenos:

   "/a/b/c/-" -> 3

The same for a list with special index '-' [RFC6901]_.

.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   jdata = { 'a': { 'b': { 'c': [1, 2, 3], 'd': 3 } } }
   
   targetpointer = '/a/b/c/-'
   
   jsonpointer = JSONPointer(targetpointer)
   jsondata = JSONData(jdata)
   
   targetnode = jsonpointer(jsondata)
   
   print()
   print('"' + str(jsonpointer) + '" -> ' + str(targetnode))
   print()


Results in:

.. code-block:: script
   :linenos:

   "/a/b/c/-" -> 3


Parent Node from Pointer
^^^^^^^^^^^^^^^^^^^^^^^^
The JSONPointer for the parent of a provided python pointer.

.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   jdata = { 'a': { 'b': { 'c': [1, 2, 3], 'd': 3 } } }
   
   targetpointer = '/a/b/c/2'
   
   jsonpointer = JSONPointer(targetpointer)
   jsondata = JSONData(jdata)
   
   parent, child = jsonpointer.get_node_and_child(jsondata)
   
   print()
   print('"' + str(jsonpointer) + '" -> parent-node = ' + str(parent) + ' child-node = ' + str(child))
   
   parent_pointer = fetch_pointerpath(parent, jsondata)[0]
   child_pointer = fetch_pointerpath(child, jsondata)[0]
   print('"' + str(jsonpointer)
         + '" -> parent-pointer = ' + str(JSONPointer(parent_pointer))
         + ' child-pointer = ' + str(JSONPointer(child_pointer)))
   print()

Results in:

.. code-block:: script
   :linenos:

   "/a/b/c/2" -> parent-node = [1, 2, 3] child-node = 3
   "/a/b/c/2" -> parent-pointer = /a/b/c child-pointer = /a/b/c/2

Parent Node for Node
^^^^^^^^^^^^^^^^^^^^
The parent node for a provided node.

.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   jdata = { 'a': { 'b': { 'c': [1, 2, 3], 'd': 3 } } }
   
   
   jsondata = JSONData(jdata)
   jsonnode = jsondata['a']['b']['c'][2]  #pylint: disable=unsubscriptable-object
   
   node_path = fetch_pointerpath(jsonnode, jsondata)[0]
   jsonpointer = JSONPointer(node_path)
   
   parent, child = jsonpointer.get_node_and_child(jsondata)
   
   
   print()
   print('jsondata = ' + str(jsondata))
   print('json-node = ' + str(jsonnode))
   print()
   print(' -> parent-json-node = ' + str(parent))
   
   parent_pointer = fetch_pointerpath(parent, jsondata)[0]
   child_pointer = fetch_pointerpath(child, jsondata)[0]
   print(' -> parent-pointer = ' + str(JSONPointer(parent_pointer)))
   print(' -> child-pointer = ' + str(JSONPointer(child_pointer)))
   print()

Results in:

.. code-block:: script
   :linenos:

   jsondata = {
       "a": {
           "b": {
               "c": [
                   1,
                   2,
                   3
               ],
               "d": 3
           }
       }
   }
   json-node = 3
   
    -> parent-json-node = [1, 2, 3]
    -> parent-pointer = /a/b/c
    -> child-pointer = /a/b/c/2


Comparison Operators
--------------------

.. _OP_EQ:

S == x
^^^^^^
.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   S = JSONData(
           { 'a': { 'b': { 'c': 2, 'd': 3 } } }
       )
     
   x = JSONData(
           { 'a': { 'b': { 'c': 2, 'd': 3 } } }
       )
   
   assert S == x
   assert S.data == x.data
   
   print(S == X)
   print(S.data == x.data)
   

.. _OP_NE:

S != x
^^^^^^
.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   S = JSONData(
           { 'a': { 'b': { 'c': 2, 'd': 3 } } }
       )
     
   x = JSONData(
           { 'a': { 'b': { 'c': 2, 'd': 4 } } }
       )
   
   assert S != x
   assert S.data != x.data
   
   print(S != x)
   print(S.data != x.data)

