HowTo JSONPointer - RFC6901
===========================

.. toctree::
   :maxdepth: 2

      howto_class_jsonpointer

Pointer Syntax
--------------


JSON String Representation
--------------------------

.. seealso::

   See RFC6901 section "5. JSON String Representation"

   .. code-block:: json
      :linenos:
   
      {
         "foo": ["bar", "baz"],
         "": 0,
         "a/b": 1,
         "c%d": 2,
         "e^f": 3,
         "g|h": 4,
         "i\\j": 5,
         "k\"l": 6,
         " ": 7,
         "m~n": 8
      }
   
   
   The following JSON strings evaluate to the accompanying values:
   
   .. code-block:: json
      :linenos:
   
      ""          // the whole document
      "/foo"      ["bar", "baz"]
      "/foo/0"    "bar"
      "/"         0
      "/a~1b"     1
      "/c%d"      2
      "/e^f"      3
      "/g|h"      4
      "/i\\j"     5
      "/k\"l"     6
      "/ "        7
      "/m~0n"     8

URI Fragment Identifier Representation
--------------------------------------

.. seealso::

   See RFC6901 section "6. URI Fragment Identifier Representation"

   .. code-block:: json
      :linenos:
   
      {
         "foo": ["bar", "baz"],
         "": 0,
         "a/b": 1,
         "c%d": 2,
         "e^f": 3,
         "g|h": 4,
         "i\\j": 5,
         "k\"l": 6,
         " ": 7,
         "m~n": 8
      }
   
   
   Given the same example document as above, the following URI fragment
   identifiers evaluate to the accompanying values:

   .. code-block:: json
      :linenos:

      #            // the whole document
      #/foo        ["bar", "baz"]
      #/foo/0      "bar"
      #/           0
      #/a~1b       1
      #/c%25d      2
      #/e%5Ef      3
      #/g%7Ch      4
      #/i%5Cj      5
      #/k%22l      6
      #/%20        7
      #/m~0n       8

Evaluate Nodes, Keys, and Values
--------------------------------

get_node_and_child
^^^^^^^^^^^^^^^^^^
Gets the parent node and the node of a given pointer.
The child is the value of the actual pointed node.
The data:

.. code-block:: json
   :linenos:
   
   # -*- coding:utf-8   -*-
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
      
   jsondata = JSONData(
       {
           "a": 10,
           "b": 11,
           "c": {
               "x": 20,
               "y": 21,
               "z": [
                   {"r": 30},
                   {"o": 31}
               ]
           }
       }
       )
   
   x0,x1  = JSONPointer("/c/z/0").get_node_and_child(jsondata)
   
evaluates to:

.. code-block:: json
   :linenos:
   
   x0 = [{'r': 30}, {'o': 31}]  # /c/z
   x1 = {'r': 30}               # /c/z/0


get_node_and_key
^^^^^^^^^^^^^^^^
Gets the parent node and the key of a given pointer.
The key is the last item of the path, pointing to
the node.
The data:

.. code-block:: json
   :linenos:
   
   # -*- coding:utf-8   -*-
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
      
   jsondata = JSONData(
       {
           "a": 10,
           "b": 11,
           "c": {
               "x": 20,
               "y": 21,
               "z": [
                   {"r": 30},
                   {"o": 31}
               ]
           }
       }
       )
   
   x0,x1  = JSONPointer("/c/z/0").get_node_and_key(jsondata)
   
evaluates to:

.. code-block:: json
   :linenos:
   
   x0 = [{'r': 30}, {'o': 31}]  # /c/z
   x1 = 0                       # 0

get_node_value
^^^^^^^^^^^^^^
Gets the value of the pointed node, which is basically the
same as the result of *get_node*.
The data:

.. code-block:: json
   :linenos:
   
   # -*- coding:utf-8   -*-
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
      
   jsondata = JSONData(
       {
           "a": 10,
           "b": 11,
           "c": {
               "x": 20,
               "y": 21,
               "z": [
                   {"r": 30},
                   {"o": 31}
               ]
           }
       }
       )
   
   x0,x1  = JSONPointer("/c/z/0").get_node_value(jsondata)
   
evaluates to:

.. code-block:: json
   :linenos:
   
   x = {'r': 30}   # /c/z/0

get_node_exist
^^^^^^^^^^^^^^
Gets the path splitted into it's existing component, and the
non-existent part of the path.
When the node exists, the latter is empty.
The data:

.. code-block:: json
   :linenos:
   
   # -*- coding:utf-8   -*-
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
      
   jsondata = JSONData(
       {
           "a": 10,
           "b": 11,
           "c": {
               "x": 20,
               "y": 21,
               "z": [
                   {"r": 30},
                   {"o": 31}
               ]
           }
       }
       )
   
   x0,x1  = JSONPointer("/c/z/0").get_node_value(jsondata)
   
evaluates to:

.. code-block:: json
   :linenos:
   
   x = [{'r': 30}, None]

While the call:

.. code-block:: json
   :linenos:
   
   x  = JSONPointer("/c/z/0/y").get_node_value(jsondata)

evaluates to:

.. code-block:: json
   :linenos:
   
   x = [{'r': 30}, ['y']]

Iterate Paths
-------------
Iterate Path Items
^^^^^^^^^^^^^^^^^^
The method *iter_path* iterates the path parts of the *JSONPointer* itself.

.. code-block:: json
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   jsondata = JSONData(
       {'a': {'b': [{'c': 2, 'd': 4, 'f': 3}]}}
       )
   
   jp = JSONPointer('/a/b/0/c')
     
   
   for jpi in jp.iter_path():
       print(jpi)

with the resulting display

.. code-block:: json
   :linenos:

   a
   b
   0
   c

The following example verifies the path items for presence
by using the data.

.. code-block:: json
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   jsondata = JSONData(
       {'a': {'b': [{'c': 2, 'd': 4, 'f': 3}]}}
       )
   
   jp = JSONPointer('/a/b/1/c')
     
   
   for jpi in jp.iter_path(jsondata):
       print(jpi)

Resulting for '*/a/b/1/c*' in the error

.. code-block:: json
   :linenos:

   jsondata.JSONPointerError: ERROR::Node(2):1 of /a/b/1/c:list index out of range

Iterate Sub Paths
^^^^^^^^^^^^^^^^^
The method *iter_path_subpaths* iterates the sub paths resulting from cumulated
the path items.

.. code-block:: json
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   jsondata = JSONData(
       {'a': {'b': [{'c': 2, 'd': 4, 'f': 3}]}}
       )
   
   jp = JSONPointer('/a/b/0/c')
   for jpi in jp.iter_path_subpaths(jsondata):
       print(jpi)

Resulting for '*/a/b/0/c*' in 

.. code-block:: json
   :linenos:

   ['a']
   ['a', 'b']
   ['a', 'b', 0]
   ['a', 'b', 0, 'c']

Iterate Path Nodes
^^^^^^^^^^^^^^^^^^
The method *iter_path_nodes* iterates the nodes resulting from the path items of
the *JSONPointer*.

.. code-block:: json
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   jsondata = JSONData(
       {'a': {'b': [{'c': 2, 'd': 4, 'f': 3}]}}
       )
   
   jp = JSONPointer('/a/b/0/c')

   for jpi in jp.iter_path_nodes(jsondata):
       print(jpi)

Resulting for '*/a/b/0/c*' in the display of the node contents
of the cumulated subpaths

.. code-block:: json
   :linenos:

   {'b': [{'c': 2, 'd': 4, 'f': 3}]}
   [{'c': 2, 'd': 4, 'f': 3}]
   {'c': 2, 'd': 4, 'f': 3}
   2

Iterate Path Data
^^^^^^^^^^^^^^^^^
The method *iter_path_subpathdata* iterates the complete data resulting from the path items of
the *JSONPointer*.

.. code-block:: json
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   jsondata = JSONData(
       {'a': {'b': [{'c': 2, 'd': 4, 'f': 3}]}}
       )
   
   jp = JSONPointer('/a/b/0/c')

   for jpi in jp.iter_path_subpathdata(jsondata):
       print(jpi)

Resulting for '*/a/b/0/c*' in the display of the node contents
of the cumulated subpaths consisting of the tuple

.. code-block:: json
   :linenos:

   (<path-item>, <sub-path>, <node>)

with the output

.. code-block:: json
   :linenos:

   ('a', ['a'], {'b': [{'c': 2, 'd': 4, 'f': 3}]})
   ('b', ['a', 'b'], [{'c': 2, 'd': 4, 'f': 3}])
   (0, ['a', 'b', 0], {'c': 2, 'd': 4, 'f': 3})
   ('c', ['a', 'b', 0, 'c'], 2)

