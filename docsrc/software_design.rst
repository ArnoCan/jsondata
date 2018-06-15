Software Design - A Blueprint
*****************************

The integration of 'jsondata' into the JSON processing flow could be extended
by custom classes as required::

              +----------------------------------------------+
              |              application-layer               |    <= Application layer, e.g including 
              +-------------+-------------+--------------+   |       REST-Middleware
              | JSONCompute | jsoncliopts | jsondataunit |   |    <= JSON processing and test
              +-------------+-------------+--------------+   |       
              +--------------+-------------------------------+       
                     |       |         |
            .  .  .  |  .  . | .  .  . | .  .  .  . <= combined API  
                     |       V         |
                     | +-----------+   | 
    RFC6902          | | JSONPatch |   |            <= modify JSON data 
                     | +-----------+   | 
                     |     |     |     |
                     V     V     |     |
                +-------------+  |     | 
    RFC6901     | JSONPointer |  |     |            <= address JSON data
                +-------------+  |     |
                       |         |     | 
                       V         V     V
    RFC7159         +---------------------+
       +            |      JSONData       |         <= integrate JSON+JSONschema
    DRAFT4          +----------o----------+
                               |
                    +---------------------+
                    | JSONDataSerializer  |         <= provide persistency for
                    +---------------------+            JSONData

                *         *          *        *
            .  .| .  .  . | .  .  .  | .  .  .| .  .<= common access to JSON data
                V         V          V        V
             +----------------+-----------------+ 
    RFC7159  |     json       |   jsonschema    |  <= provide JSON data and JSONschema
       &&    |     ujson      |                 |      
    DRAFT4   +----------------+-----------------+

For referenced components refer to resources at 
`PyPI <index.html#resources>`_ .

Layered Subcomponents for Reuse
*******************************

The overall design is structured for component wise reuse.
Therefore a layered software stack is implemented, which starts above basic JSON data encoding and decoding
and adds on top various features:

* Manage branches of substructures - **jsondata.jsondata**
* Serialize JSON documents - **jsondata.jsondataserializer**
* Access pointer paths and values - **jsondata.jsonpointer**
* Modify data structures and values - **jsondata.jsonpatch**

With the external packages:

* Computing JSON based data - **jsoncompute.JSONCompute**
* Unit tests for the data content of JSON based data - **jsondataunit.JSONDataUnit**
* Commandline processing  - **jsoncliopts.JSONCLIOpts**

The JSON-DSL is moved into the package 'jsoncompute'.

Utilities for structure analysis and operations on JSON data structures, e.g. diff.

The syntax primitives of underlying layers are processed by the imported standard packages 'json' and 'jsonschema' 
in conformance to related standards.
Current supported compatible packages include: 'ujson'.

The examples from the standards with some extensions are included as Use-Cases in order to 
verify implementation details for the recommendations.
This serves also as a first introduction to JSON processing with the
package 'jsondata'.

This document provides the developer information for the API, Use-Cases, and the 
documentation of the PyUnit tests as examples and application patterns.

Unittest on JSON Data
=====================

The component 'jsondata' relies on unittest.TestCase class due to it's lower position within
the software stack.
In case of large amounts of JSON based data is to be verified consider using the packgae
'jsondataunit' `[online] <https://pypi.python.org/pypi/jsondataunit/>`_, which
is derived from this package 'jsondata.jsondataserializer'.::

     +---------------------+
     |    JSONDataUnit     |
     +----------+----------+
                |
     +----------+----------+
     | JSONDataSerializer  |
     +----------+----------+
                |
     +----------+----------+
     |       JSONData      |
     +---------------------+

Du to it's base class the class 'JSONDataUnit' provides the full scope of:

* Serialization and persistency for regression
* Logic and arithmetic operators for advanced tests

Commandline processing
======================

The component 'jsoncliopts' extends 'jsondata' for advanced commandline processing.
This enables for:

*  partial options which are removed before further processed, e.g.
   by 'getopts', or 'argparser'
*  standard internal representation of complex options with subpoptions

The sturture is due to common processing with additional persistency when reauired as follows:
::

     +---------------------+       +---------------------+
     |    JSONCLISubOpts   | <---> | JSONDataSerializer  |
     +----------+----------+       +----------+----------+
                |                             |
                +--------------+--------------+
                               |
                    +----------+----------+
                    |       JSONData      |
                    +---------------------+

Persistency may be required e.g. in case of test automation for load of regression data.

Du to it's base class the class 'JSONDataUnit' provides the full scope of:

* Logic and arithmetic operators for advanced tests

with optional:
 
* Serialization and persistency for regression

DSL for JSON Data - JSONCompute
===============================

Documents following soon.


