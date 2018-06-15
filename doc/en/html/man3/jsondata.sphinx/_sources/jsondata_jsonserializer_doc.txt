'jsondata.jsondataserializer' - Module
**************************************
Core features for serialization of structured JSON based in-memory data.
This comprises the load of a model from a JSON file, and the 
incremental addition and removal of branches by loading additional
JSON modules.
The resulting data could be saved for later reuse, either as a complete
tree, or by modular parts as branches.
The implementation is based on the standard packages *json* and *jsonschema*.

This module uses either preloaded JSON data, or loads 
the data from  files. 

Additional modification of the data is supported the modules `jsondata <jsondata_jsondata_doc.html>`_
and `jsonpatch <jsondata_jsonpatch_doc.html>`_,
analysis and comparison by the module `jsondatadiff <jsondata_jsondiff_doc.html>`_.

Module
======
.. automodule:: jsondata.jsondataserializer

JSONDataSerializer
==================

.. autoclass:: JSONDataSerializer

Attributes
----------

* *JSONDataSerializer.data*

  In-memory JSON data, see *JSONData.data*.

* *JSONDataSerializer.schema*

  In-memory JSON schema, see *JSONData.schema*.


Methods
-------

__init__
^^^^^^^^

.. automethod:: JSONDataSerializer.__init__


json_export
^^^^^^^^^^^

.. automethod:: JSONDataSerializer.json_export

json_import
^^^^^^^^^^^

.. automethod:: JSONDataSerializer.json_import

dump_data
^^^^^^^^^

.. automethod:: JSONDataSerializer.dump_data

dump_schema
^^^^^^^^^^^

.. automethod:: JSONDataSerializer.dump_schema

set_schema
^^^^^^^^^^

.. automethod:: JSONDataSerializer.set_schema

Exceptions
==========

.. autoexception:: jsondata.JSONDataAmbiguityError
.. autoexception:: jsondata.JSONDataError
.. autoexception:: jsondata.JSONDataModeError
.. autoexception:: jsondata.JSONDataParameterError
.. autoexception:: jsondata.JSONDataSourceFileError
.. autoexception:: jsondata.JSONDataTargetFileError
.. autoexception:: jsondata.JSONDataValueError
