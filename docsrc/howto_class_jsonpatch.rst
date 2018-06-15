JSONPatch - RFC6902
===================

.. toctree::
   :maxdepth: 2

      howto_class_jsonpatch

Standards Operations
--------------------
Create,Add
^^^^^^^^^^
Simple
""""""
Create a JSON document
[`download <_static/examples/jsonpatch_howto_example_create_000.py>`_].

.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON in-memory document
   D = JSONData(
           { 'a': { 'b': { 'c': 2, 'd': 3 } } }
       )
     
   
   # the same as native Pyhton data
   rdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }
   
   # compare contained raw data by Python type
   assert D.data == rdata
   
   # compare data as JSONData object, see JSONData.__eq__
   assert D == rdata
   
   # print structure
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
       }
   }
    

Complex
^^^^^^^
Create a JSON document, add and create branches
[`download <_static/examples/jsonpatch_howto_example_create_001.py>`_].

.. code-block:: Python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   from jsondata.jsondata import JSONData
   from jsondata.jsonpointer import JSONPointer
   
   # JSON document
   jdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }
     
   # JSON branch with array
   arr = { 'e': { 'lx': [] } }
     
   # Branch elements for array
   ai0 = { 'v0': 100}
   ai1 = { 'v1': 200}
     
     
   # JSON branch with object
   obj = { 'f': { 'ox': {} } }
     
   # Branch elements for object
   l0 = { 'o0': 10}
   l1 = { 'o1': 20}
     
     
   # JSON in-memory document
   D = JSONData(jdata)
     
     
   # Add a branch with an array
   D.branch_add(JSONPointer('/a/b'),'e',arr['e'])
     
   # Add a items to the new array
   # Remark: for '-' refer to RFC6901 - array-index
   D.branch_add(JSONPointer('/a/b/e/lx'),'-',ai0)
   D.branch_add(JSONPointer('/a/b/e/lx'),'-',ai1)
     
     
   # Add a branch with an object
   D.branch_add(JSONPointer('/a/b'),'f',obj['f'])
     
   # Add an item to the new object, from an object
   D.branch_add(JSONPointer('/a/b/f/ox'),'v0',ai0['v0'])
     
   # Add an item to the new object
   ai1v1 = ai1['v1']
   D.branch_add(JSONPointer('/a/b/f/ox'),'v1',ai1v1)
   
   
   nodex = JSONPointer(['a','b'])(D.data)
   ret = D.branch_create(nodex, ['g','x'], {})
   
   ret['x0'] = 22
   ret['x1'] = 33
     
   ret = D.branch_create(nodex, ['g','x','xlst'], [])
   
   ret.append('first')
   ret.append('second')
   
   rdata = {'a': {'b': {'c': 2, 'e': {'lx': [{'v0': 100}, 
     {'v1': 200}]}, 
     'd': 3, u'g': {u'x': {'x0': 22, 'x1': 33, 
     u'xlst': ['first', 'second']}}, 
     'f': {'ox': {'v0': 100, 'v1': 200}}}}
   }
   assert D.data == rdata
   
   print(D)

prints the result:

.. code-block:: json
   :linenos:

   {
       "a": {
           "b": {
               "c": 2,
               "d": 3,
               "e": {
                   "lx": [
                       {
                           "v0": 100
                       },
                       {
                           "v1": 200
                       }
                   ]
               },
               "f": {
                   "ox": {
                       "v0": 100,
                       "v1": 200
                   }
               },
               "g": {
                   "x": {
                       "x0": 22,
                       "x1": 33,
                       "xlst": [
                           "first",
                           "second"
                       ]
                   }
               }
           }
       }
   }
    

Access values
^^^^^^^^^^^^^

Various access to values
[`download <_static/examples/jsonpatch_howto_example_access_001.py>`_].


.. code-block:: python
   :linenos:

   print D(['a', 'b', 'c'])
   
   print D(JSONPointer('/a/b/c'))
   
   print D('/a/b/c')
   
   n = JSONPointer('/a/b/c')(D.data,True)
   print n['c']
   
   n = JSONPointer('/a/b/c')(D.data,True)
   px = D.fetch_pointerpath(n, D.data)[0]
   px.append('c')
   print D(JSONPointer(px))

prints the result:

.. code-block:: json
   :linenos:

   2
   2
   2
   2
   2

Move
^^^^

Move a branch.

.. code-block:: python
   :linenos:

   target = JSONPointer('/a/b/new')
   source = JSONPointer('/a/b/c')
   
   print D(source)
   n = D('/a/b')
   n['c'] = 77
   
   targetnode = target(D.data,True)
   sourcenode = source(D.data,True)
   
   D.branch_move(targetnode, 'new', sourcenode, 'c')
   print D(target)
   
   # check new position
   assert D(target) == 77 
     
   # validate old position
   try:
     x = D('/a/b/c')
   except JSONPointerError as e:
     pass
   else:
     raise
 
prints the result:

.. code-block:: json
   :linenos:

   2
   77

Remove
^^^^^^

Remove a branch.

.. code-block:: python
   :linenos:

   # get a pointer
   target     = JSONPointer('/a/b/new')
   
   # get the parent node for the pointer
   targetnode = target(D.data,True)
   
   # verify existence
   x = D('/a/b/new')
   assert x == 77
   
   # remove item
   D.branch_remove(targetnode, 'new')
   
   # validate old position
   try:
     x = D('/a/b/new')
   except JSONPointerError as e:
     pass
   else:
     raise
   pass

Replace
^^^^^^^

Replace a branch.

.. code-block:: python
   :linenos:

   # does not verify childnode, when 'parent=True' <=> 'new' does no longer exist
   targetnode = JSONPointer('/a/b/new')(D.data,True)
   
   # new item
   sourcenode = {'alternate': 4711 }
   
   # replace old by new item
   ret = D.branch_replace(targetnode, 'f', sourcenode)
   assert ret == True
   
   # verify new item
   x = D('/a/b/f/alternate')
   assert x == 4711


Test
^^^^

Test value.

.. code-block:: python
   :linenos:

   # variant 0
   ret = D.branch_test(JSONPointer('/a/b/f/alternate').get_node_value(D.data), 4711)
   assert ret == True
   
   # variant 1
   ret = D.branch_test(JSONPointer('/a/b/f/alternate')(D.data), 4711)
   assert ret == True
   
   # variant 2
   p = JSONPointer('/a/b/f/alternate')
   ret = D.branch_test(p(D.data), 4711)
   assert ret == True

Copy
^^^^

Copy branch.

.. code-block:: python
   :linenos:

   # JSON branch with array
   arr = { 'cpy': { 'cx': [ 2, 3, 4, ] } }
   
   # Copy a branch with an array
   D.branch_copy(JSONPointer('/a/b'),'cpy',arr['cpy'])

Patch-Set Algebra
-----------------

RFC6902 Examples
----------------

Section 3
^^^^^^^^^

.. seealso::

   RFC6902 - section 3. Document Structure

   The following is an example JSON Patch document, transferred in an

   .. code-block:: JSON
      :linenos:

      HTTP PATCH request:
      PATCH /my/data HTTP/1.1
      Host: example.org
      Content-Length: 326
      Content-Type: application/json-patch+json
      If-Match: "abc123"
      [
         {"op": "test",    "path": "/a/b/c", "value": "foo"            },
         {"op": "remove",  "path": "/a/b/c"                            },
         {"op": "add",     "path": "/a/b/c", "value": [ "foo", "bar" ] },
         {"op": "replace", "path": "/a/b/c", "value": 42               },
         {"op": "move",    "from": "/a/b/c", "path": "/a/b/d"          },
         {"op": "copy",    "from": "/a/b/d", "path": "/a/b/e"          }
      ]



Section 4
^^^^^^^^^

.. seealso::

   RFC6902 - section 4. Operations

   Note that the ordering of members in JSON objects is not significant;
   therefore, the following operation objects are equivalent:

   .. code-block:: JSON
      :linenos:

      { "op": "add", "path": "/a/b/c", "value": "foo" }
      { "path": "/a/b/c", "op": "add", "value": "foo" }
      { "value": "foo", "path": "/a/b/c", "op": "add" }


Section 4.1
^^^^^^^^^^^

.. seealso::

   RFC6902 - section 4.1 add

   .. code-block:: JSON
      :linenos:

      { "op": "add", "path": "/a/b/c", "value": [ "foo", "bar" ] }

Section 4.2
^^^^^^^^^^^

.. seealso::

   RFC6902 - section 4.2 remove

   .. code-block:: JSON
      :linenos:

      { "op": "add", "path": "/a/b/c", "value": [ "foo", "bar" ] }

Section 4.3
^^^^^^^^^^^

.. seealso::

   RFC6902 - section 4.3 replace

   .. code-block:: JSON
      :linenos:

      { "op": "replace", "path": "/a/b/c", "value": 42 }

Section 4.4
^^^^^^^^^^^

.. seealso::

   RFC6902 - section 4.4 move

   .. code-block:: JSON
      :linenos:

      { "op": "move", "from": "/a/b/c", "path": "/a/b/d" }

Section 4.5
^^^^^^^^^^^

.. seealso::

   RFC6902 - section 4.5 copy

   .. code-block:: JSON
      :linenos:

      { "op": "copy", "from": "/a/b/c", "path": "/a/b/e" }

Section 4.6
^^^^^^^^^^^

.. seealso::

   RFC6902 - section 4.6 test

   .. code-block:: JSON
      :linenos:

      {"op": "test", "path": "/a/b/c", "value": "foo" }


Section 5
^^^^^^^^^

.. seealso::

   RFC6902 - section 5. Error Handling

   .. code-block:: JSON
      :linenos:

      [
         { "op": "replace", "path": "/a/b/c", "value": 42 },
         { "op": "test", "path": "/a/b/c", "value": "C" }
      ]



Appendix A.1.
^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.1 Adding an Object Member

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      { "foo": "bar"}

   A JSON Patch document:

   .. code-block:: JSON
      :linenos:

      [
         { "op": "add", "path": "/baz", "value": "qux" }
      ]

   The resulting JSON document:

   .. code-block:: JSON
      :linenos:

      {
         "baz": "qux",
         "foo": "bar"
      }

Appendix A.2.
^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.2 Adding an Array Element

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      { "foo": [ "bar", "baz" ] }

   A JSON Patch document:

   .. code-block:: JSON
      :linenos:

      [
         { "op": "add", "path": "/foo/1", "value": "qux" }
      ]

   The resulting JSON document:

   .. code-block:: JSON
      :linenos:

      { "foo": [ "bar", "qux", "baz" ] }


Appendix A.3.
^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.3 Removing an Object Member

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      {
         "baz": "qux",
         "foo": "bar"
      }

   A JSON Patch document:

   .. code-block:: JSON
      :linenos:

      [
         { "op": "remove", "path": "/baz" }
      ]

   The resulting JSON document:

   .. code-block:: JSON
      :linenos:

      { "foo": "bar" }

Appendix A.4.
^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.4 Removing an Object Member

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      { "foo": [ "bar", "qux", "baz" ] }

   A JSON Patch document:

   .. code-block:: JSON
      :linenos:

      [
         { "op": "remove", "path": "/foo/1" }
      ]

   The resulting JSON document:

   .. code-block:: JSON
      :linenos:

      { "foo": [ "bar", "baz" ] }

Appendix A.5.
^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.5 Replacing a Value

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      {
         "baz": "qux",
         "foo": "bar"
      }

   A JSON Patch document:

   .. code-block:: JSON
      :linenos:

      [
         { "op": "replace", "path": "/baz", "value": "boo" }
      ]

   The resulting JSON document:

   .. code-block:: JSON
      :linenos:

      {
         "baz": "boo",
         "foo": "bar"
      }

Appendix A.6.
^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.6 5 Replacing a Value

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      {
         "foo": {
            "bar": "baz",
            "waldo": "fred"
         },
         "qux": {
            "corge": "grault"
         }
      }

   A JSON Patch document:

   .. code-block:: JSON
      :linenos:

      [
         { "op": "move", "from": "/foo/waldo", "path": "/qux/thud" }
      ]

   The resulting JSON document:

   .. code-block:: JSON
      :linenos:

      {
         "foo": {
               "bar": "baz"
         },
         "qux": {
            "corge": "grault",
            "thud": "fred"
         }
      }

Appendix A.7.
^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.7 Moving an Array Element

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      { "foo": [ "all", "grass", "cows", "eat" ] }

   A JSON Patch document:

   .. code-block:: JSON
      :linenos:

      [
         { "op": "move", "from": "/foo/1", "path": "/foo/3" }
      ]

   The resulting JSON document:

   .. code-block:: JSON
      :linenos:

      { "foo": [ "all", "cows", "eat", "grass" ] }

Appendix A.8.
^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.8 Testing a Value: Success

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      {
         "baz": "qux",
         "foo": [ "a", 2, "c" ]
      }

   A JSON Patch document that will result in successful evaluation:

   .. code-block:: JSON
      :linenos:

      [
         { "op": "test", "path": "/baz", "value": "qux" },
         { "op": "test", "path": "/foo/1", "value": 2 }
      ]

Appendix A.9.
^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.9 Testing a Value: Error

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      { "baz": "qux" }

   A JSON Patch document that will result in successful evaluation:

   .. code-block:: JSON
      :linenos:

      [
         { "op": "test", "path": "/baz", "value": "bar" }
      ]

Appendix A.10.
^^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.10 Testing a Value: Error

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      { "foo": "bar" }

   A JSON Patch document:

   .. code-block:: JSON
      :linenos:

      [
         { "op": "add", "path": "/child", "value": { "grandchild": { } } }
      ]

   The resulting JSON document:

   .. code-block:: JSON
      :linenos:

      {
         "foo": "bar",
         "child": {
            "grandchild": {
            }
         }
      }

Appendix A.11.
^^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.11 0 Testing a Value: Error

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      { "foo": "bar" }

   A JSON Patch document:

   .. code-block:: JSON
      :linenos:

      [
         { "op": "add", "path": "/baz", "value": "qux", "xyz": 123 }
      ]

   The resulting JSON document:

   .. code-block:: JSON
      :linenos:

      {
         "foo": "bar",
         "baz": "qux"
      }

Appendix A.12.
^^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.12 Adding to a Nonexistent Target

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      { "foo": "bar" }

   A JSON Patch document:

   .. code-block:: JSON
      :linenos:

      [
         { "op": "add", "path": "/baz/bat", "value": "qux" }
      ]

   This JSON Patch document, applied to the target JSON document above,
   would result in an error (therefore, it would not be applied),
   because the "add" operation’s target location that references neither
   the root of the document, nor a member of an existing object, nor a
   member of an existing array.

Appendix A.13.
^^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.13 Invalid JSON Patch Document

   A JSON Patch document:

   .. code-block:: JSON
      :linenos:

      [
         { "op": "add", "path": "/baz", "value": "qux", "op": "remove" }
      ]

   This JSON Patch document cannot be treated as an "add" operation,
   because it contains a later "op":"remove" element. JSON requires
   that object member names be unique with a "SHOULD" requirement, and
   there is no standard error handling for duplicates.

Appendix A.14.
^^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.14  ̃ Escape Ordering

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      {
         "/": 9,
         " ̃1": 10
      }

   A JSON Patch document:

   .. code-block:: JSON
      :linenos:

      [
         {"op": "test", "path": "/ ̃01", "value": 10}
      ]

   The resulting JSON document:

   .. code-block:: JSON
      :linenos:

      {
         "/": 9,
         " ̃1": 10
      }

Appendix A.15.
^^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.15 Comparing Strings and Numbers

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      {
         "/": 9,
         " ̃1": 10
      }

   A JSON Patch document:

   .. code-block:: JSON
      :linenos:

      [
         {"op": "test", "path": "/ ̃01", "value": "10"}
      ]

   This results in an error, because the test fails. The document value
   is numeric, whereas the value being tested for is a string.

Appendix A.16.
^^^^^^^^^^^^^^

.. seealso::

   RFC6902 - section A.16 Adding an Array Value

   An example target JSON document:

   .. code-block:: JSON
      :linenos:

      { "foo": ["bar"] }

   A JSON Patch document:

   .. code-block:: JSON
      :linenos:

      [
         { "op": "add", "path": "/foo/-", "value": ["abc", "def"] }
      ]

   The resulting JSON document:

   .. code-block:: JSON
      :linenos:

      { "foo": ["bar", ["abc", "def"]] }

