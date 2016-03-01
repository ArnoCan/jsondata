jsondata
========

This package contains library modules for the management of JSON based
in-memory data. The data representation is based on the modules 'json',
and 'jsonschema'.

The managed unit of this package is the branch of a tree. Thus this
package is in particular applicable for the dynamic configuration of
software components.

The features comprise the serialization, the addition and removal of
modular branch data, and the validation by JSONschema.

Examples are provided as PyUnit tests for Eclipse, a commandline interface
for the interactive test of JSON data and schema definitions is included.

The code provides for the '-O/-OO' options of python, therefore some debugging
is included by wrapping with the '__debug__' variable.

The documents are available as Sphinx based documents and in addition
resulting from Epydoc. The main priority was compatibility with the Google
style guide for pydoc, thus the html documents may not utilize the full scope
of presentation features.

setup.py
--------

The installer adds a few options to the standard setuptools options.

* build_sphinx: 
Creates documentation for runtime system by Sphinx, html only.
Calls 'callDocSphinx.sh'.

* build_epydoc: 
Creates documentation for runtime system by Epydoc, html only.
Calls 'callDocEpydoc.sh'.

* build_testsphinx:
Creates documentation for unit tests by Sphinx, html only.
Calls 'callTestSphinx.sh'.

* build_testepydoc:
Creates documentation for unit tests by Epydoc, html only.
Calls 'callTestEpydoc.sh'.

* test:
Runs PyUnit tests by discovery.

* --help-jsondata: 
Displays this help.

* --no-install-requires:
Suppresses installation dependency checks, requires 
appropriate PYTHONPATH.

* --offline: 
Sets online dependencies to offline, or ignores online dependencies.

* --exit:
Exit 'setup.py'.
