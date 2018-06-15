Install
=======

**Prerequisites and Resources**:

+--------------+--------------+---------------------------------------------------+-------------------------+
| prerequisite | reference    | description                                       | details                 |
+==============+==============+===================================================+=========================+
| Runtime      | Python       | CPython2.7+, CPython3.5+                          | [`install python`_]     |
+--------------+--------------+---------------------------------------------------+-------------------------+
|              | PyPy         | PyPy2, PyPy3                                      | [`install pypy`_]       |
+--------------+--------------+---------------------------------------------------+-------------------------+
|              | stackless    | stackless2, stackless3                            | [`install stackless`_]  |
+--------------+--------------+---------------------------------------------------+-------------------------+
|              | ironpython   | ironpython                                        | [`install ironpython`_] |
+--------------+--------------+---------------------------------------------------+-------------------------+
|              | OS           | Linux, Mac-OS/OS-X, BSD, UNIX, Cygwin, MS-Windows |                         |
+--------------+--------------+---------------------------------------------------+-------------------------+
|              | Devices      | RaspberryPI (2,3): Raspbian, FreeBSD, OpenWRT     |                         |
+--------------+--------------+---------------------------------------------------+-------------------------+
| SDK2         | Python       | CPython2.7+                                       |                         |
+--------------+--------------+---------------------------------------------------+-------------------------+
|              | bash         | bash-4.x                                          |                         |
+--------------+--------------+---------------------------------------------------+-------------------------+
|              | documents    | Sphinx >=1.4, Epydoc >=3 or Apydoc >=4            |                         |
+--------------+--------------+---------------------------------------------------+-------------------------+
|              | OS           | Linux, Mac-OS/OS-X, BSD, UNIX, Cygwin,            |                         |
+--------------+--------------+---------------------------------------------------+-------------------------+
| SDK2+3       | Python       | CPython2.7+, CPython3.5+                          |                         |
+--------------+--------------+---------------------------------------------------+-------------------------+
|              | bash         | bash-4.x                                          |                         |
+--------------+--------------+---------------------------------------------------+-------------------------+
|              | documents    | Sphinx >=1.4, Apydoc >=4                          |                         |
+--------------+--------------+---------------------------------------------------+-------------------------+
|              | OS           | Linux, Mac-OS/OS-X, BSD, UNIX, Cygwin,            |                         |
+--------------+--------------+---------------------------------------------------+-------------------------+
| Download     | PyPI         | https://pypi.python.org/pypi/jsondata             |                         |
+--------------+--------------+---------------------------------------------------+-------------------------+
|              | Sourceforge  | https://sourceforge.net/projects/jsondata/        |                         |
+--------------+--------------+---------------------------------------------------+-------------------------+
|              | github.com   | https://github.com/ArnoCan/jsondata/              |                         |
+--------------+--------------+---------------------------------------------------+-------------------------+
| Documents    | pythonhosted | https://pythonhosted.org/jsondata/                |                         |
+--------------+--------------+---------------------------------------------------+-------------------------+

.. _install: howto_install-python.html
.. _installpypy: howto_install-pypy.html
.. _installstackless: howto_install-stackless.html
.. _installironpython: howto_install-ironpython.html

.. _install python: howto_install-python.html
.. _install pypy: howto_install-pypy.html
.. _install stackless: howto_install-stackless.html
.. _install ironpython: howto_install-ironpython.html

**Install**:

+-------------+-------------------------------------------------------------------------+
| environment | description                                                             |
+=============+=========================================================================+
| Runtime     | Standard procedure online local install e.g. into virtual environment:  |
|             |                                                                         |
|             | * *pip install jsondata*                                                |
|             | * *python setup.py install*                                             |
+-------------+-------------------------------------------------------------------------+
|             | Standard procedure online local install into user home:                 |
|             |                                                                         |
|             | * *python setup.py install --user*                                      |
+-------------+-------------------------------------------------------------------------+
|             | Custom procedure offline by:                                            |
|             |                                                                         |
|             | * *python setup.py install --user --offline*                            |
+-------------+-------------------------------------------------------------------------+
|             | Copy archive distribution:                                              |
|             |                                                                         |
|             | * *python setup.py cpdist (tar.gz |tgz|zip)*                            |
+-------------+-------------------------------------------------------------------------+
| SDK         | Required for document creation, add '--sdk' option, checks build tools: |
|             |                                                                         |
|             | * *python setup.py install --sdk*                                       |
+-------------+-------------------------------------------------------------------------+
|             | Creation of documents, requires Sphinx including 'sphinx-apidoc',       |
|             | and Epydoc:                                                             |
|             |                                                                         |
|             | * *python setup.py build_doc install_project_doc install_doc*           |
+-------------+-------------------------------------------------------------------------+
|             | Create a document archive for copy distribution:                        |
|             |                                                                         |
|             | * *python setup.py docdist*                                             |
|             |                                                                         |
|             | Creates  *tar.gz* and *tgz* in *dist*                                   |
+-------------+-------------------------------------------------------------------------+

**Extensions**:

The following custom options are added to the standard options of *setup.py*.

+----------+-------------------------+------------------------------------------+
| call     | description             |                                          |
+==========+=========================+==========================================+
| setup.py | *build_sphinx*          | Builds sphinx-only documents.            |
+----------+-------------------------+------------------------------------------+
|          | *build_doc*             | Builds complete documentation.           |
+----------+-------------------------+------------------------------------------+
|          | *build_epydoc*          | Builds epydoc-only documents.            |
+----------+-------------------------+------------------------------------------+
|          | *build_apydoc*          | Builds apydoc-only documents.            |
+----------+-------------------------+------------------------------------------+
|          | *cpdist*                | Creates an archives for simple unpack:   |
|          |                         | tarball, zip                             |
+----------+-------------------------+------------------------------------------+
|          | *docdist*               | Creates documentation for simple unpack: |
|          |                         | tarball, zip                             |
+----------+-------------------------+------------------------------------------+
|          | *install_doc*           | Installs documentation.                  |
+----------+-------------------------+------------------------------------------+
|          | *tests*                 | Runs unittests from 'tests'.             |
+----------+-------------------------+------------------------------------------+
|          | *usecases*              | Runs unittests from 'UseCases'.          |
+----------+-------------------------+------------------------------------------+
|          | *--exit*                | Exits the *setup.py* before execution.   |
+----------+-------------------------+------------------------------------------+
|          | *--help-commands*       | Print includes extensions.               |
+----------+-------------------------+------------------------------------------+
|          | *--help-jsondata*       | Prints help for extensions.              |
+----------+-------------------------+------------------------------------------+
|          | *--no-install-requires* | Ignores install dependencies.            |
+----------+-------------------------+------------------------------------------+
|          | *--offline*             | Supress *PyPI* access, includes          |
|          |                         | *--no-install-requires*.                 |
+----------+-------------------------+------------------------------------------+
|          | *--sdk*                 | Installs SDK, including *sphinx*,        |
|          |                         | and *apydoc*.                            |
+----------+-------------------------+------------------------------------------+

For help on current available extensions to standard options call online help:: 

   python setup.py --help-jsondata

