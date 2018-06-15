Install Python - CPython
========================

.. toctree::
   :maxdepth: 2

   howto_install-python

Linux
-----
Standard procedure,
see `Python.org <https://www.python.org/downloads/>`_,
`Python2 <https://docs.python.org/2/using/unix.html>`_,
and 
`Python3 <https://docs.python.org/3/using/unix.html>`_.

The package expects eventuall custom build Python interpreters
located at the path:

.. code-block:: script
   :linenos: 

      /opt/python/python-<version>

The runtime routinesexpand the version suffix in case of partial numbers to
the highest available completion.
This includes the Python convention.

For the available versions

.. code-block:: script
   :linenos: 

        [acue@lap001 syscalls]$ ls /opt/python/
        python-2.6.6  python-2.6.9   python-2.7.12  python-3.3.6  python-3.5.2  python-3.6.2
        python-2.6.8  python-2.7.11  python-2.7.13  python-3.4.6  python-3.5.3

the following examples apply:

.. code-block:: script
   :linenos: 

   python2        => python-2.7.13
   python2.7      => python-2.7.13
   python3        => python-3.6.2

   python-2       => python-2.7.13
   python-2.7     => python-2.7.13
   python-2.7.11  => python-2.7.11
   python-3.5     => python-3.5.3
   python-3       => python-3.6.2
   python-2.6     => python-2.6.9

 
Windows
-------
Standard procedure, with expected defaults:

+-----------+----------+-------------+
| Python    | Drive    | Path        |
+===========+==========+=============+
| Python2.7 | C: E: F: | \\Python2.7 |
+-----------+----------+-------------+
| Python3.5 | C: E: F: | \\Python3.5 |
+-----------+----------+-------------+
| Python3.6 | C: E: F: | \\Python3.6 |
+-----------+----------+-------------+

See `Python.org <https://www.python.org/downloads/>`_.

OS-X
----
Standard procedure with some "quirks".

* *homebrew*

  The "almost formally correct" use of *brew*,
  when it works proper - from the box.

  .. code-block:: script
     :linenos:

      brew install python

* Install with *installer*

  In case of difficulties, e.g. with the *git* error, 
  the on-board utilities approach may help.

  .. code-block:: script
     :linenos:

     installer -pkg python-3.5.3-macosx10.6.pkg -target /
     installer -pkg python-3.6.2-macosx10.6.pkg -target /

See `Python.org <https://www.python.org/downloads/>`_.

FreeBSD and OpenBSD
-------------------
See `Python2 <https://docs.python.org/2/using/unix.html>`_,
and 
`Python3 <https://docs.python.org/3/using/unix.html>`_.

Solaris
-------
a.s.a.p.

RaspberryPI - ARM
-----------------

Raspbian
^^^^^^^^
a.s.a.p.

FreeBSD
^^^^^^^
a.s.a.p.

Kali-Linux
^^^^^^^^^^
a.s.a.p.

OpenWRT
^^^^^^^
a.s.a.p.
