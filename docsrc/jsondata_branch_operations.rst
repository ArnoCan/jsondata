Process branch data by 'JSONData'
*********************************

The class JSONData provides operations on data structures.
The class hierarchy is hereby reduced to a top-node representation
*JSONDATA* of *JSONDataSerializer*,
while the branches are allocated and processed as native Python
data elements.
Thus the perfomance impact of *JSONData* is kept minimal,
basically negligible.

Provided syntax elements are:

* **native access attributes**:

   The node addresses for the native access to 
   the JSON in-memory representation. The data format is compatible to the 
   packages 'json' and 'jsonschema', e.g. also to 'ujson'. Thus provides
   native Python access performance.

* **branch operations**:

   Handle complete sub structures as logical branches
   of a main JSON document. The interface is designed in accordance to RFC6902
   with extension for Python specifics.

* **tree utilities**:

   Generic tree functions for the provided in-memory
   representation by 'json' and 'jsonschema' are available
   as *jsondatadiff* [jsondatadiff]_ and *jsondatafind* [jsondatafind]_.

Syntax Elements
===============

The current release provides for branches the class 'JSONData'
with basic set operations for branches,

Data
----
Native JSON representation access attributes::

   attr := data, schema

This package supports in the current version the following data types:

+---------------+-----------+
| JSON          | Python    |
+===============+===========+
| object        | dict      |
+---------------+-----------+
| array         | list      |
+---------------+-----------+
| string        | unicode   |
+---------------+-----------+
| number (int)  | int, long |
+---------------+-----------+
| number (real) | float     |
+---------------+-----------+
| true          | True      |
+---------------+-----------+
| false         | False     |
+---------------+-----------+
| null          | None      |
+---------------+-----------+

It also understands ``NaN``, ``Infinity``, and
``-Infinity`` as their corresponding ``float`` 
values, which is outside the JSON spec.

The supported standard value types for Python 
of get_node_value() are mapped automatically 
as depicted in the following table. Additional
bindings may be implemented by sub-classing.

+-----------------------+----------------+
| JSONPointer(jsondata) | Python-valtype |
+=======================+================+
| object (dict)         | dict           |
+-----------------------+----------------+
| array  (list)         | list           |
+-----------------------+----------------+
| array  (tuple)        | list           |
+-----------------------+----------------+
| string                | unicode        |
+-----------------------+----------------+
| number (int)          | int            |
+-----------------------+----------------+
| number (long)         | long           |
+-----------------------+----------------+
| number (float)        | float          |
+-----------------------+----------------+
| *number (double)      | float          |
+-----------------------+----------------+
| number (octal)        | int            |
+-----------------------+----------------+
| number (hex)          | int            |
+-----------------------+----------------+
| number (binary)       | int            |
+-----------------------+----------------+
| number (complex)      | -- (custom)    |
+-----------------------+----------------+
| true                  | True           |
+-----------------------+----------------+
| false                 | False          |
+-----------------------+----------------+
| null                  | None           |
+-----------------------+----------------+

The mappings in detail are:

* object(dict) => dict:

  .. code-block:: json
     :linenos:

     {a:b} - native Python dictionary

* array(list) => list:

  .. code-block:: json
     :linenos:

     [a,b] - native Python list

* (*)array(tuple) => list:

  .. code-block:: json
     :linenos:

     (a,b) - native Python list

* string(str) => unicode"

  .. code-block:: json
     :linenos:

     "abc" - native Python unicode string UTF-8

* number(int) => int:

  .. code-block:: json
     :linenos:

     1234, −24, 0 - Integers (unlimited precision)

* number(long) => int:

  .. code-block:: json
     :linenos:

     1234, −24, 0 - Integers (unlimited precision)

* number(float) => float:

  .. code-block:: json
     :linenos:

     1.23, 3.14e-10, 4E210, 4.0e+210, 1., .1 - Floating-point 

  Normally implemented as C doubles in CPython.

* (*)number(double) => float:

  .. code-block:: json
     :linenos:

     1.23, 3.14e-10, 4E210, 4.0e+210, 1., .1 - Floating-point 

  Normally implemented as C doubles in CPython.

* number(octal) => int:

  .. code-block:: json
     :linenos:

     0o177 - Octal, hex, and binary literals for integers

* number(hex) => int:

  .. code-block:: json
     :linenos:

     0x9ff - Octal, hex, and binary literals for integers

* number(binary) => int:

  .. code-block:: json
     :linenos:

     0b1111 - Octal, hex, and binary literals for integers

* number(complex) => <not-supported>(requires custom):

  .. code-block:: json
     :linenos:

     3+4j, 3.0+4.0j, 3J - Complex numbers

* true(True) => boolean(True):

  .. code-block:: json
     :linenos:

     True - native Python boolean

* false(False) => boolean(False):

  .. code-block:: json
     :linenos:

     False - native Python boolean

* null(None) => None(None):

  .. code-block:: json
     :linenos:

     False - native Python None


The specification *RFC4627* [RFC4627]_ and the updated *RFC7159* [RFC7159]_ 
define different valid top-level nodes.

* RFC4627: top-level must be object or array
* RFC7159: any valid node type is permitted as top-level, including *null*
This behaviour is provided by the *jsondata* package by setting the *mode*
parameter appropriately.

|jsondataevaluation|
|jsondataevaluation_zoom|

.. |jsondataevaluation_zoom| image:: _static/zoom.png
   :alt: zoom 
   :target: _static/jsondata-evaluation.png
   :width: 16

.. |jsondataevaluation| image:: _static/jsondata-evaluation.png
   :width: 550

Administrative Operations
-------------------------
Branch operations(branch_<ops>), see RFC6902::

   ops := branch_add | branch_copy | branch_create | branch_div
          | branch_move | branch_remove | branch_replace
          | branch_superpose | branch_test


Comparison Operators
--------------------
Pointer comparison::

   ops := '==' | '!=' 

Logic Operators
---------------
The logic operators provide basic set operations.
The scope of the operations is the top level keys of the branch,
deep level operations are supported by the interfaces of type
*branch_\**.

Operators for the set calculation of branches ::

   ops := '&' | '|' | '^' #   
 
Behavior Operators
------------------
Value evaluation operators::

   ops := '[]' | '()'

Iterators
---------
Generic operations::

   ops := iter_ | fetch_pointerpath

Selection Operations
--------------------
Selection operations::

   ops := fetch_pointerpath 
          | get | get_data

Schema Support
--------------
Selection operations::

   ops := get_schema | set_schema | validate

    

