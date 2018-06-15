'jsondata.jsonpointer' - Module
*******************************

.. automodule:: jsondata.jsonpointer

Constants
=========

.. index::
  pair: pointer-notation; NOTATION_JSON
  pair: pointer-notation; NOTATION_HTTP_FRAGMENT

JSON Notation
-------------
Notation of the API - in/out, see :ref:`jsodnata.__init__ <COMMONCONSTSJSONNOTATION>` .

.. index::
  pair: node-types; VALID_NODE_TYPE

Node Types
----------
Valid node types represented by Python
types. ::

   VALID_NODE_TYPE = (
       dict,
       list,
       str,
       unicode,  # Python2, mapped in Python3 to str
       int,
       float,
       bool,
       None, )

.. index::
  pair: character-sets; CHARSET_UTF
  pair: character-sets; CHARSET_STR

Character Set
-------------
For Python3 these are identical to UTF-8.

* *CHARSET_UTF(0)* Unicode.
* *CHARSET_STR(1)* - Python string.


JSONPointer
===========

Represents exactly one JSONPointer in compliance with IETF and ECMA standards
[RFC6901]_, [RELPOINTER]_, and [ECMA404]_.
The JSONPointer is provided at the API as a utf(-8) string,
while the processed represenation is a list vector.

* self.raw:

  Raw input of the pointer string for the logical API.

* self:

  Split elements of the pointer path as a list of keys
  and idexes.

The class *JSONPointer* is derived from the *list* class and manages
the path elements as items::

   ptrlist := (<EMPTY>|plist)

   <EMPTY> := "empty list, represents the whole document relative to it's root"

   plist := pkey [, plist ]

   pkey := (''|int|keyname)

   '' := "the empty string is a valid key [RFC6901]_ and [RELPOINTER]_"
   int := "integer index of an array item, just digits"
   keyname := "the valid name of an object/property entry"

The empty quotation within a string has context specific semantics.

* pointer == '' == '""'

  The whole document.

* pointer == '/""' == '/'

  The top object node with an empty string as a key.

* pointer == '/any/path/""/and/more'

  Any node path entry with an empty string as a key.

The JSONPointer::

   "/address/0/streetName"

is represented as::

   ['address', 0, 'streetName' ]

The following special cases are handled: ::

   ""      <=> []                 # the whole document
   "/"     <=> ['']               # the top of current document, or sub-document
   "///"   <=> ['', '', '']       # a pointer path with empty keys
   "#"     <=> []                 # the whole document defined as URI fragment
   "#/"    <=> []                 # the top of current document referenced by a URI fragment
   "#///"  <=> ['', '', '']       # a fragment pointer path with empty keys

The relative pointer adds the syntax: ::

   "0<rfc6901-path>"              # document node relative to offset anchor
   "[1-9][0-9]*<rfc6901-path>"    # document node relative to offset anchor

   "0#"                           # the actual document node key/index of the offset anchor
   "[1-9][0-9]#"                  # the key/index at the resulting document node

The implemented interpretation of the following cases is similar to the common
handling of filesystem functions when a directory above the root directory
is selected. E.g. in case of Linux with ::

   [acue@somewhere dirXY]$ cd /
   [acue@somewhere /]$ pwd
   /
   [acue@somewhere /]$ cd ../../../../
   [acue@somewhere /]$ pwd
   /
   [acue@somewhere /]$

Due to the lack of definition within the current standards, the similar behavior is defined
for the *jsondata* package.
The offset-pointer defines the starting position
within the JSON document [RELPOINTER]_: ::

   rel-pointer = "0", offset-pointer=""      =>  ""  # the whole document
   rel-pointer = "4", offset-pointer=""      =>  ""  # still the whole document
   rel-pointer = "4", offset-pointer="/a/b"  =>  ""  # again the whole document

The JSON pointer is by definition in any case actually a relative pointer.

* rfc6901 - relative to the top of the document
* relative pointer - relative to an offset pointer within the document

The introduction of a relative pointer [RELPOINTER]_ keeps and reuses the
previous definitions and adds some syntax extensions:

* Notation for the reference of upper nodes within the hierarchy of the current
  JSON document.
* Addition of an offset pointer within the current JSON document as the anchor
  for the relative pointer.
* A notation for the get-request of the key or index of the containing element
  of the resulting node pointed to.

The methods and operators of *JSONPointer* implement the previous standards for
the pointer.
These handle by definition the pointer data itself, which is used
to address the data within a specific JSON document.
The methods of this class support in most cases multiple input formats of
the JSONPointer.

   'str':
      A string in accordance to RFC6901 or relative pointer/Draft-1/2018.

   'int':
      A numeric value in case of an array index.

   'JSONPointer':
      Another instance of the class.

   'list':
      Expects a path list containing the elements of a JSON pointer.

The JSONPointer class by itself is focused on the path pointer itself, though
the provided operations do not alter the content of the refrenced JSON document.
The pointer provides the hook into the JSON document.

.. autoclass:: JSONPointer

Attributes
----------

* *JSONPointer.isfragment*

  *True* for a URI fragment [RFC6901]_.
  Valid if *isrel* is *False*.

  This attribute is read-only.

* *JSONPointer.isrel*

  * *True* for a relative pointer [RELPOINTER]_

  * *False* for a standard JSON pointer or a JSON URI fragment [RFC6901]_.

  This attribute is read-only.

* *JSONPointer.isrelpathrequest*

  Valid only if *isrel* is *True*, defines the type of a relative pointer.

  * *True* when a relative pointer, e.g. ::

       "3/a/b/c"
       "3"

  * *False* for a key or index get-request, e.g. ::

       "3#"

  This attribute is read-only.

* *JSONPointer.raw*

  Raw input string for JSONPointer for internal use.

* *JSONPointer.start*

  The resulting start offset after processing of *JSONPointer.startrel*
  and the integer index of the relative JSONPointer.

  This is pre-processed in any case for each modification of the *startrel* attribute,
  independent of the value provided by the attribute *strict*.

  This attribute is read-only.

* *JSONPointer.startrel*

  The raw pointer offset to the sub node within the JSON document
  as the start node for the application of the
  relative pointer. Referenced as the "starting" node in [RELPOINTER]_.

  This attribute is read-only.

* *JSONPointer.strict*

  Controls two charcteristics of the behaviour of relative pointers:

  * Example document from [RELPOINTER]_: ::

      jsondata =    {
         "foo": ["bar", "baz"],
         "highly": {
            "nested": {
               "objects": true
            }
         }
      }

  * *integer prefix overflow*

    The integer prefix of a relative pointer may lead to a starting point
    exceeding the top of the document. For example ::

       startrel   = ""
       relpointer = "4/"

    The result is: ::

       strict=True:  raises an exception
       strict=False: results in the whole document

  * *JSONPointer.startrel*

    Controls the behavior of the *JSONPointer.startrel* offset.
    This is due to the circumstance, that the application of the integer
    prefix on a non-existent node could result in a valid node.
    When strict is *True* teh existens mandatory and is checked before
    the application of the integer prefix, when *False* the integer prefix
    is applied without verification of the *startrel*.


    The following relative pointers ::

       startrel    = "/foo/2"
       relpointer0 = "2/highly/nested/objects"
       relpointer1 = "4/highly/nested/objects"

    result in ::

       strict=True:  raises an exception
       strict=False: true

    The case *strict=False* covers here two variants,

    * *relpointer0*

      The relative start position defined by the integer index '2'
      is valid, while the *startrel* position is not.

    * *relpointer1*

      The relative start position defined by the integer index '4'
      lead to an document overflow and  is handled as defined
      by the previous rule.
      Thus the non-valid *startrel* position leads to a valid
      node when the integer prefix is applied, the whole document.

  This attribute is read-only.

Functions
---------

fetch_pointerpath
^^^^^^^^^^^^^^^^^
.. autofunction:: fetch_pointerpath


Methods
-------

__init__
^^^^^^^^

.. automethod:: JSONPointer.__init__

__repr__
^^^^^^^^

.. automethod:: JSONPointer.__repr__

__str__
^^^^^^^

.. automethod:: JSONPointer.__str__

check_node_or_value
^^^^^^^^^^^^^^^^^^^

.. automethod:: JSONPointer.check_node_or_value

copy_path_list
^^^^^^^^^^^^^^

.. automethod:: JSONPointer.copy_path_list

evaluate
^^^^^^^^

.. automethod:: JSONPointer.evaluate

get_node_and_child
^^^^^^^^^^^^^^^^^^

.. automethod:: JSONPointer.get_node_and_child

get_node_and_key
^^^^^^^^^^^^^^^^

.. automethod:: JSONPointer.get_node_and_key

get_node_exist
^^^^^^^^^^^^^^

.. automethod:: JSONPointer.get_node_exist

get_node_value
^^^^^^^^^^^^^^

.. automethod:: JSONPointer.get_node_value

get_path_list
^^^^^^^^^^^^^

.. automethod:: JSONPointer.get_path_list

get_path_list_and_key
^^^^^^^^^^^^^^^^^^^^^

.. automethod:: JSONPointer.get_path_list_and_key

get_pointer
^^^^^^^^^^^
.. automethod:: JSONPointer.get_pointer

get_pointer_and_key
^^^^^^^^^^^^^^^^^^^
.. automethod:: JSONPointer.get_pointer_and_key

get_pointer_str
^^^^^^^^^^^^^^^
.. automethod:: JSONPointer.get_pointer_str

get_raw
^^^^^^^
.. automethod:: JSONPointer.get_raw

get_relupidx
^^^^^^^^^^^^
.. automethod:: JSONPointer.get_relupidx

get_start
^^^^^^^^^
.. automethod:: JSONPointer.get_start

get_startrel
^^^^^^^^^^^^
.. automethod:: JSONPointer.get_startrel

isfragment
^^^^^^^^^^
.. automethod:: JSONPointer.isfragment

isrelpathrequest
^^^^^^^^^^^^^^^^
.. automethod:: JSONPointer.isrelpathrequest

isrel
^^^^^
.. automethod:: JSONPointer.isrel

isvalid_nodetype
^^^^^^^^^^^^^^^^
.. automethod:: JSONPointer.isvalid_nodetype

isvalrequest
^^^^^^^^^^^^
.. automethod:: JSONPointer.isvalrequest

Operators
---------

The syntax displayed for provided operators is::

  S: self
  x: parameter
  n: numerical parameter for shift operators.

Thus the position of the opreator and parameteres is defined as follows::

   z = S + x: LHS: __add__
   z = x + S: RHS: __radd__
   S += x:    LHS: __iadd__



'S+x'
^^^^^

.. automethod:: JSONPointer.__add__

'S(x)'
^^^^^^

.. automethod:: JSONPointer.__call__

'S==x'
^^^^^^

.. automethod:: JSONPointer.__eq__

'S>=x'
^^^^^^

.. automethod:: JSONPointer.__ge__

'S>x'
^^^^^

.. automethod:: JSONPointer.__gt__

'S+=x'
^^^^^^

.. automethod:: JSONPointer.__iadd__

'S<x'
^^^^^

.. automethod:: JSONPointer.__le__

'S<x'
^^^^^

.. automethod:: JSONPointer.__lt__

'S!=x'
^^^^^^

.. automethod:: JSONPointer.__ne__

'x+S'
^^^^^

.. automethod:: JSONPointer.__radd__

Iterators
---------

iter_path
^^^^^^^^^

.. automethod:: JSONPointer.iter_path

iter_path_nodes
^^^^^^^^^^^^^^^

.. automethod:: JSONPointer.iter_path_nodes

iter_path_subpathdata
^^^^^^^^^^^^^^^^^^^^^

.. automethod:: JSONPointer.iter_path_subpathdata

iter_path_subpaths
^^^^^^^^^^^^^^^^^^

.. automethod:: JSONPointer.iter_path_subpaths


Exceptions
==========
.. autoexception:: jsondata.JSONPointerError
.. autoexception:: jsondata.JSONPointerTypeError
.. autoexception:: jsondata.NotImplementedError
