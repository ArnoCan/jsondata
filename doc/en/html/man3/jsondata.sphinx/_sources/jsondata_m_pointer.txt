'jsondata.JSONPointer' - Module
*******************************

.. automodule:: jsondata.JSONPointer

JSONPointer
===========

.. autoclass:: JSONPointer

Attributes
----------

**JSONPointer**:

* JSONPointer.ptr: JSONPointer data.

* JSONPointer.raw: Raw input string for JSONPointer.

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

get_node
^^^^^^^^

.. automethod:: JSONPointer.get_node

get_node_and_child
^^^^^^^^^^^^^^^^^^

.. automethod:: JSONPointer.get_node_and_child

get_node_exist
^^^^^^^^^^^^^^

.. automethod:: JSONPointer.get_node_exist

get_node_or_value
^^^^^^^^^^^^^^^^^

.. automethod:: JSONPointer.get_node_or_value

get_path_list
^^^^^^^^^^^^^

.. automethod:: JSONPointer.get_path_list

get_path_list_and_key
^^^^^^^^^^^^^^^^^^^^^

.. automethod:: JSONPointer.get_path_list_and_key

get_pointer
^^^^^^^^^^^

.. automethod:: JSONPointer.get_pointer

get_raw
^^^^^^^

.. automethod:: JSONPointer.get_raw

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

Exceptions
==========

* `jsondata.JSONPointerException [source] <_modules/jsondata/JSONPointer.html#JSONPointerException>`_

