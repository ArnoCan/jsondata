'jsondata.jsondata' - Module
****************************
Core features for the processing of structured JSON based in-memory data.
This comprises the load of a master model from a JSON file - which could 
be initally empty, and the incremental addition and removal of branches
by loading additional JSON modules into the master model.
The resulting data could be saved for later reuse.
The implementation is based on the standard packages *json* [json]_,
*ujson* [ujson]_, and 'jsonschema' [jsonschema]_.

Additional modification of the data is supported the module `jsonpatch <jsondata_jsonpatch_doc.html>`_
analysis and comparison by the module `jsondatadiff <jsondata_jsondiff_doc.html>`_.

Module
======

.. automodule:: jsondata.jsondata

JSONData
========

This class provides for the handling of the in-memory data
by the main hooks 'data', and 'schema'. This includes generic 
methods for the advanced management of arbitrary 'branches'
in extension to RCF6902, and additional methods strictly 
compliant to RFC6902.

Attributes:
  **data**: The data tree of JSON based objects provided
      by the module 'json'.
  **schema**: The validator for 'data' provided by 
      the module 'jsonschema'.

Common call parameters provided by the methods of this class are:
  **targetnode** := *addressreference*
      The target node of called method. The 'targetnode' in general 
      represents the target of the called method. In most cases this
      has to be a reference to a container for the modification 
      and/or insertion of resulting elements. The methods require
      the change of contained items, which involves the application
      of a 'key' pointing to the hook in point of the reference
      to the modification.

  **key** := *key-value* 
      The hook-in point for references of modified entries within
      the targetnode container. The following values are supported:

  **sourcenode** := *addressreference*
      The in-memory node address of the source branch for the method,
      e.g. 'copy' or 'move' operation.

The address references supported in this class refer the resulting
in-memory representation of a pointer path. The target is a node 
within a Python data representation as provided by the package 
'**json**' and compatible packages, e.g. '**ujson**'. The supported input
syntax is one of the following interchangeable formats:

   .. parsed-literal::

      # The reference to a in-memory-node.
      addressreference := (
            nodereference
          | addressreference-source
      )

      nodereference:= (
            <in-memory>
          | ''
      )
   
      <in-memory> := "Memory representation of a JSON node, a 'dict'
                      or a 'list'. The in-memory Python node reference
                      has to be located within the document, due to 
                      performance reasons this is not verified by default.
   
                     The 'nodereference' could be converted from the
                     'addressreference-source' representation."
   
      '' := "Represents the whole document in accordance to RFC6901.
             Same as 'self.data'." 
   
      # The source of the syntax for the description of the reference
      # pointer path to a node. This is applicable on paths to be created.
      addressreference-source := (
          JSONPointer
      )
   
      JSONPointer:="A JSONPointer object in accordance to RFC6901.
                    for additional information on input formats refer
                    to the class documentation.
                    This class provides a fully qualified path pointer,
                    which could be converted into any of the required representations."

For hooks by 'key-value' within addressed containers:

   .. parsed-literal::
   
      key-value:=(None|<list-index>|<dict-key>) 
   
      None := "When the 'key' parameter is 'None', the action 
              optionally could be based on the keys of the 'sourcenode'.  
              The contents of the branch replace the node contents
              when the type of the branch matches the hook."
   
      <list-index>:=('-'|int)
   
      <dict-key>:="Valid for a 'dict' only, sets key/value pair, 
                   where present is replace, new is created."
   
      '-' := "Valid for a 'list' only, appends to present."
   
      int := "Valid for a 'list' only, replaces present when
              0 < #int < len(Node)."

In the parameter lists of methods used term 'pointer' is either 
an object of class 'JSONPointer', or a list of pointer path 
entries.

The JSON types 'object' and 'array' behave in Python slightly 
different in accordance to RFC6902. The main difference arise 
from the restrictions on applicable key values. Whereas the
ranges are limited logically by the actual container sizes, 
the object types provide free and unlimited keys. The limit 
is set by type restriction to unicode and 'non-nil' only 
for keys.  


.. autoclass:: JSONData

Attributes
----------

* *JSONData.data*

  JSON object data tree.
  The data tree of JSON based objects provided
  by the module *json*/*ujson*.

* *JSONData.schema*

  JSONschema object data tree.
  The validator for 'data' provided by 
  the module *jsonschema*.

Common Call Parameters
----------------------
Common call parameters provided by most methods of this class are:
  **targetnode** := *addressreference*

   The target node of the called method. The *targetnode* in general 
   represents the target of the called method. In most cases this
   has to be a reference to a container for the modification 
   and/or insertion of resulting elements. The methods require
   the change of contained items, which involves the application
   of a *key* pointing to the hook-in point of the reference
   for modification.

  **key** := *key-value* 

   The hook-in point for references of modified entries within
   the *targetnode* container.

  **sourcenode** := *addressreference*

   The in-memory node address of the source branch for the method,
   e.g. for the  *copy* and *move* operation.

The address references supported in this class refer the resulting
in-memory representation of a pointer path. The target is a node 
within a Python data representation as provided by the package 
'**json**' and compatible packages, e.g. '**ujson**'. The supported input
syntax is one of the following interchangeable formats:

  .. parsed-literal::

     # The reference to a in-memory-node.
     addressreference := (
          nodereference
        | addressreference-source
     )

     nodereference:= (
           <in-memory>
         | ''
     )
   
     <in-memory> := "Memory representation of a JSON node, a 'dict'
                     or a 'list'. The in-memory Python node reference
                     has to be located within the document, due to
                     performance reasons this is not verified by default.
   
                     The 'nodereference' could be converted from the
                     'addressreference-source' representation."
   
     '' := "Represents the whole document in accordance to RFC6901.
            Same as 'self.data'." 
   
     # The source of the syntax for the description of the reference
     # pointer path to a node. This is applicable on paths to be created.
     addressreference-source := (
         JSONPointer
     )
   
     JSONPointer:="A JSONPointer object in accordance to RFC6901.
                  for additional information on input formats refer
                  to the class documentation.
                  This class provides a fully qualified path pointer,
                  which could be converted into any of the required
                  representations."

For hooks by 'key-value' within addressed containers:

  .. parsed-literal::

     key-value:=(None|<list-index>|<dict-key>) 

     None := "When the 'key' parameter is 'None', the action 
             optionally could be based on the keys of the 'sourcenode'.  
             The contents of the branch replace the node contents
             when the type of the branch matches the hook."

     <list-index>:=('-'|int)

     <dict-key>:="Valid for a 'dict' only, sets key/value pair, 
                  where present is replace, new is created."

     '-' := "Valid for a 'list' only, appends to present."

     int := "Valid for a 'list' only, replaces present when
            0 < #int < len(Node)."

In the parameter lists of methods used term 'pointer' is either 
an object of class 'JSONPointer', or a list of pointer path 
entries.

The JSON types 'object' and 'array' behave in Python slightly 
different in accordance to RFC6902. The main difference arise 
from the restrictions on applicable key values. Whereas the
ranges are limited logically by the actual container sizes, 
the object types provide free and unlimited keys. The limit 
is set by type restriction to unicode and 'non-nil' only 
for keys.  

Methods
-------

__init__
^^^^^^^^
.. automethod:: JSONData.__init__

__repr__
^^^^^^^^
.. automethod:: JSONData.__repr__

__str__
^^^^^^^
.. automethod:: JSONData.__str__

branch_add
^^^^^^^^^^
.. automethod:: JSONData.branch_add

branch_copy
^^^^^^^^^^^
.. automethod:: JSONData.branch_copy

branch_create
^^^^^^^^^^^^^
.. automethod:: JSONData.branch_create

branch_move
^^^^^^^^^^^
.. automethod:: JSONData.branch_move

branch_remove
^^^^^^^^^^^^^
.. automethod:: JSONData.branch_remove

branch_replace
^^^^^^^^^^^^^^
.. automethod:: JSONData.branch_replace

branch_superpose
^^^^^^^^^^^^^^^^
.. automethod:: JSONData.branch_superpose

branch_test
^^^^^^^^^^^
.. automethod:: JSONData.branch_test

clear
^^^^^
.. automethod:: JSONData.clear

copy
^^^^
.. automethod:: JSONData.copy

deepcopy
^^^^^^^^
.. automethod:: JSONData.deepcopy

get
^^^
.. automethod:: JSONData.get

get_canonical_value
^^^^^^^^^^^^^^^^^^^
.. automethod:: JSONData.get_canonical_value

get_data
^^^^^^^^
.. automethod:: JSONData.get_data

get_schema
^^^^^^^^^^
.. automethod:: JSONData.get_schema


pop
^^^
.. automethod:: JSONData.pop

dump_data
^^^^^^^^^
.. automethod:: JSONData.dump_data

dump_schema
^^^^^^^^^^^
.. automethod:: JSONData.dump_schema

set_schema
^^^^^^^^^^
.. automethod:: JSONData.set_schema

setkargs
^^^^^^^^
.. automethod:: JSONData.setkargs

validate
^^^^^^^^
.. automethod:: JSONData.validate

Operators
---------

Comparison
^^^^^^^^^^
S==x
""""
.. automethod:: JSONData.__eq__

S!=x
""""
.. automethod:: JSONData.__ne__

Miscellaneous
^^^^^^^^^^^^^
S()
"""
.. automethod:: JSONData.__call__

Iterators
---------
The iterator is based on pre-set parameters for data processing.

S[k]
^^^^
.. automethod:: JSONData.__getitem__

__iter__
^^^^^^^^
.. automethod:: JSONData.__iter__

get_data_items
^^^^^^^^^^^^^^
.. automethod:: JSONData.get_data_items

Conxtext Manager
----------------
The context manager provides setting specific parameters for the data processing, 
which is reset to the state before after finishing.

__enter__
^^^^^^^^^
.. automethod:: JSONData.__enter__

__exit__
^^^^^^^^
.. automethod:: JSONData.__exit__

Miscellaneous Operators
-----------------------

__delitem__
^^^^^^^^^^^
.. automethod:: JSONData.__delitem__

__getitem__
^^^^^^^^^^^
.. automethod:: JSONData.__getitem__

__setitem__
^^^^^^^^^^^
.. automethod:: JSONData.__setitem__


Exceptions
==========
.. autoexception:: jsondata.JSONDataError
.. autoexception:: jsondata.JSONDataIndexError
.. autoexception:: jsondata.JSONDataKeyError
.. autoexception:: jsondata.JSONDataNodeTypeError
.. autoexception:: jsondata.JSONDataParameterError
.. autoexception:: jsondata.JSONDataPathError
.. autoexception:: jsondata.JSONDataSourceFileError
.. autoexception:: jsondata.JSONDataTargetFileError
.. autoexception:: jsondata.JSONDataValueError
            