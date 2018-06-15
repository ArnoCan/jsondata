jsondata
========


The package *jsondata* provides the management of modular data structures based on JSON.
The provided features support standards for JSON patch RFC6902, and JSON pointer RFC6901,
and others.

The data is represented by an in-memory main data tree with
dynamically added and/or removed branches and values. The logical branches of data
structures provide for the ease of custom data sets and slightly modified repetitive structures.
The in-memory data could be serialized as JSON files for persistent storage and reuse.

The *jsondata* package provides a standards conform layer for the processing of JSON
based data with emphasis on in-memory performance and low resource consume.
The implementation integrates seamless into the standard interfaces and data structures
of Python.

The main interface classes are:

* **JSONData** - Core for RFC7159 based data structures. Provides modular data components.

* **JSONDataSerializer** - Core for RFC7159 based data persistence. Provides modular data serialization.

* **JSONPointer** - RFC6901 for addressing by pointer paths. Provides pointer arithmetics.

* **JSON Relative Pointer** - draft-handrews-relative-json-pointer/2018, contained in JSONPointer.

* **JSONPatch** - RFC6902 for modification by patch lists. Provides the assembly of modular patch entries and the serialization of resulting patch lists.

* **JSONDiff** - Diff utility for JSON data.

* **JSONSearch** - Search utility JSON patterns.

The syntax primitives of underlying layers are provided
by the imported packages '**json**' or the package ultra-json '**ujson**', and '**jsonschema**' in conformance to related ECMA and RFC
standards and proposals. Here ECMA-262, ECMA-404, RFC7159/RFC4627,
draft-zyp-json-schema-04, and others.

The architecture is based on the packages 'json' or 'ujson', and
'jsonschema' ::

                   +-------------------------+
    Applications   |    application-layer    |   see e.g. jsonlathe, restdrill
                   +-------------------------+
    .   .  .  .  .  . | .  .  . | .  .  .  .| .  .  .  .  .  .  .  .  .
                   + - - - - - - - - - - - - +    see package jsoncompute,
    Process JSON   |     JSON processing     |    jsondataunit,
                   + - - - - - - - - - - - - +    jsoncliopts
    .   .  .  .  .  . | .  .  . | .  .  .  .| .  .  .  .  .  .  .  .  .
                      |         V           |     
                      |  +--------------+   |      RFC8259/RFC7159/RFC4627
    Data Structures   |  |  jsondata    |   |      RFC6901/draft-handrews-relative-json-pointer
    Pointer           |  | jsonpointer  |   |      RFC6902
    Patch             |  |  jsonpatch   |   |      +draft-handrews-relative-json-pointer
                      |  |              |   |      +pointer arithmetics +extensions
    Tools             |  |  jsondif     |   |
                      |  | jsondatafind |   |
                      |  |              |   |  
    Command line      |  | jsondc cli   |   |
                      |  +--------------+   |      
                      |      |    |         |      
                      |      |    |         |
    .  .  .  .  .  .  | .  . | .  | .  .  . | .  .  .  .  .  .  .  .  .
                      +---+--+    +---+-----+
                          |           |
                          V           V
                   +------------+------------+    RFC8259/RFC7159/RFC4627
    JSON           |    json,   | jsonschema |    ECMA-262/ECMA-404
    Syntax         |    ujson   |            |    draft-zyp-json-schema-04
                   +------------+------------+


The supported platforms are:
 
* Linux, BSD, Unix, OS-X, Cygwin, and Windows7/Windows10
* Python2.7+, Python3.5+

**Online documentation**:

* https://jsondata.sourceforge.io/


**Runtime-Repository**:

* PyPI: https://pypi.org/project/jsondata/

  Install: *pip install jsondata*, see also 'Install'.

**Downloads**:

* bitbucket.org: https://bitbucket.org/acue/jsondata/downloads/
* github.com: https://github.com/ArnoCan/jsondata/
* pypi.org: https://pypi.python.org/pypi/jsondata/
* sourceforge.net: https://sourceforge.net/projects/jsondata/files/


Project Data
------------

* PROJECT: *jsondata*

* MISSION: Provide and extend JSONPointer and JSONPatch - RFC6901, RFC6902

* VERSION: 00.02

* RELEASE: 00.02.022

* STATUS: alpha

* AUTHOR: Arno-Can Uestuensoez

* COPYRIGHT: Copyright (C) 2010,2011,2015-2018 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez

* LICENSE: Artistic-License-2.0 + Forced-Fairplay-Constraints
  Refer to enclose documents:

  *  ArtisticLicense20.html - for base license: Artistic-License-2.0

  *  licenses-amendments.txt - for amendments: Forced-Fairplay-Constraints

Python support:

*  Python2.7, and Python3.5+

OS-Support:

* Linux: Fedora, CentOS, Debian, and Raspbian 

* BSD - OpenBSD, and FreeBSD

* OS-X: Snow Leopard

* Windows: Win7, Win10

* Cygwin

* UNIX: Solaris


**Current Release**

Rework of APIs - thus not backward compatible to former releases.
 
Major Changes:

* Restructured modules.

* Restructured call interfaces.

* Extended class JSONData.

* Added support for draft/2018 of Relative JSON Pointers. 

* Added combined support for Python2.7+ and Python3.5+.

* Enhanced documentation.

