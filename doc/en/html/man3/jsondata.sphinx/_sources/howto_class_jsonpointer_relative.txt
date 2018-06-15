Relative JSONPointer - draft-handrews-relative-json-pointer
===========================================================

.. toctree::
   :maxdepth: 2

      howto_class_jsonpointer_relative

Pointer Syntax
--------------

.. code-block:: python
   :linenos:

   jp = JSONPointerWithRel("0#")
   
   jdoc = {
      'a': {
         'b': {
            'c': {
               'd': [
                  3,
                  4
               ]
            }
         }
      }
   }
   
   idx0 = jp(jdoc['/a/b/c/d/1'])
   idx1 = jp(jdoc['/a/b/c/d'])
   idx2 = jp(jdoc['/a/b/c'])
   idx2 = jp(jdoc['/a/b'])
   idx3 = jp(jdoc['/a'])

   

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


